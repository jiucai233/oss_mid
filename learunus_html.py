import json
import os
import time
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from learnus_calendar import get_links
from learnus_getcookie import get_cookies
import requests

def link_to_html():
    # Initialize driver as None outside the loop
    driver = None
    links = None  # Initialize links as None
    html_list = []  # List to store HTML content

    MAX_RETRIES = 4
    retry_count = 0

    while retry_count <= MAX_RETRIES:
        try:
            cookies_list = None  # Initialize cookies_list for this attempt

            # --- Cookie Acquisition ---
            if os.path.exists('cookies.json'):
                print(f"Attempt {retry_count + 1}/{MAX_RETRIES + 1}: Found cookies.json, attempting to use saved cookies.")
                try:
                    with open('cookies.json', 'r') as file:
                        cookies_list = json.load(file)
                    # Basic validation: Check if it's a list and not empty
                    if not isinstance(cookies_list, list) or not cookies_list:
                        print("Invalid format in cookies.json. Deleting and requesting login.")
                        os.remove('cookies.json')
                        cookies_list = None  # Reset cookies_list
                    else:
                        print("Loaded cookies from file.")

                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"Error reading cookies.json: {e}. Requesting login.")
                    if os.path.exists('cookies.json'):
                        os.remove('cookies.json')  # Remove corrupted file
                    cookies_list = None  # Reset cookies_list

            if cookies_list is None:  # Need to login if no valid cookies loaded
                if driver:  # Quit any previous driver instance before creating a new one
                    driver.quit()
                    driver = None
                print(f"Attempt {retry_count + 1}/{MAX_RETRIES + 1}: cookies.json not found or invalid. Requesting login.")
                username = "2022106103"  # Replace with your username
                password = "Xinpig.123"  # Replace with your password
                cookies_list, driver = get_cookies(username, password)  # driver is assigned (or re-assigned) here

            # --- Link Extraction ---
            if cookies_list:
                cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
                print("Attempting to get links using cookies.")
                links = get_links(cookies_dict)

                if links:
                    print("Links extracted successfully!")
                    break  # Exit the while loop successfully
                else:
                    print("Failed to extract links. Cookies might be invalid or expired.")
                    if os.path.exists('cookies.json'):
                        os.remove('cookies.json')
            else:
                print("Failed to obtain cookies from login attempt.")

        except UnexpectedAlertPresentException:
            print("Caught an unexpected alert during login attempt.")
            if driver:
                try:
                    alert = Alert(driver)
                    alert_text = alert.text
                    print(f"Login failed due to alert: {alert_text}")
                    alert.accept()
                except Exception as alert_e:
                    print(f"Error handling alert: {alert_e}")
                finally:
                    driver.quit()
                    driver = None
            if os.path.exists('cookies.json'):
                os.remove('cookies.json')

        except (NoSuchElementException, TimeoutException) as selenium_error:
            print(f"A Selenium error occurred during login: {selenium_error}")
            if driver:
                driver.quit()
                driver = None
            if os.path.exists('cookies.json'):
                os.remove('cookies.json')

        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            if driver:
                driver.quit()
                driver = None
            retry_count = MAX_RETRIES + 1
            break

        retry_count += 1
        if retry_count <= MAX_RETRIES:
            print(f"Retrying ({retry_count}/{MAX_RETRIES})...")
            time.sleep(2)
        else:
            print("Maximum retry attempts reached. Exiting.")

    if driver:
        driver.quit()
        driver = None

    if links:
        print("\nReading calendar HTML files...")
        try:
            with open('cookies.json', 'r') as file:
                cookies_list_final = json.load(file)
            cookies_final = {cookie['name']: cookie['value'] for cookie in cookies_list_final}

            for link in links:
                try:
                    print(f"Reading calendar from: {link}")
                    # Simulate reading HTML content (replace with actual reading logic if needed)
                    html_content = requests.get(link, cookies=cookies_final).text
                    html_list.append(html_content)  # Append HTML content to the list
                except Exception as read_e:
                    print(f"Error processing calendar from {link}: {read_e}")
            print("\nFinished reading calendars.")
            return html_list if html_list else None  # Return the list if not empty, else None

        except FileNotFoundError:
            print("\nError: cookies.json not found when trying to read calendars.")
        except Exception as final_err:
            print(f"\nAn error occurred during calendar reading phase: {final_err}")

    return None  # Return None if no links or errors occurred

if __name__ == "__main__":
    htmls = link_to_html()
    i = 0
    for html in htmls:
        i += 1
        with open(f'calendar_{i}.html', 'w', encoding='utf-8') as f:
            f.write(html)

