import json
import requests
import os
import time
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from learnus_calendar import get_links
from learnus_getcookie import get_cookies

# Initialize driver as None outside the loop
driver = None
links = None # Initialize links as None

MAX_RETRIES = 4
retry_count = 0

while retry_count <= MAX_RETRIES:
    try:
        cookies_list = None # Initialize cookies_list for this attempt

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
                    cookies_list = None # Reset cookies_list
                else:
                     # Assume cookies are valid for now, get_links will verify
                     print("Loaded cookies from file.")

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cookies.json: {e}. Requesting login.")
                if os.path.exists('cookies.json'):
                    os.remove('cookies.json') # Remove corrupted file
                cookies_list = None # Reset cookies_list

        if cookies_list is None: # Need to login if no valid cookies loaded
             if driver: # Quit any previous driver instance before creating a new one
                 driver.quit()
                 driver = None
             print(f"Attempt {retry_count + 1}/{MAX_RETRIES + 1}: cookies.json not found or invalid. Requesting login.")
             username = input("Enter your username: ")
             password = input("Enter your password: ")
             # get_cookies should handle its own exceptions and return driver
             cookies_list, driver = get_cookies(username, password) # driver is assigned (or re-assigned) here

        # --- Link Extraction ---
        if cookies_list:
            # Convert cookies list to a dictionary for requests
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
            print("Attempting to get links using cookies.")
            links = get_links(cookies_dict) # Assuming get_links only needs cookies dict

            if links:
                print("Links extracted successfully!")
                # Print the extracted links
                for link in links:
                    print(link)
                # If successful, break the loop
                break # Exit the while loop successfully
            else:
                print("Failed to extract links. Cookies might be invalid or expired.")
                # Remove the potentially invalid cookies file to force re-login next time
                if os.path.exists('cookies.json'):
                    print("Deleting cookies.json.")
                    os.remove('cookies.json')
                # Fall through to increment retry_count and potentially retry
        else:
             # This happens if get_cookies failed (returned None for cookies_list)
             print("Failed to obtain cookies from login attempt.")
             # Fall through to increment retry_count and potentially retry

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
                # Quit the driver after handling the alert or if handling failed
                print("Quitting WebDriver after alert.")
                driver.quit()
                driver = None # Reset driver after quitting
        else:
            print("Driver was not initialized when UnexpectedAlertPresentException occurred.")
        # Remove cookies.json if it exists, as the login failed
        if os.path.exists('cookies.json'):
            print("Deleting cookies.json due to login failure.")
            os.remove('cookies.json')
        # Fall through to increment retry_count and potentially retry

    except (NoSuchElementException, TimeoutException) as selenium_error:
         print(f"A Selenium error occurred during login: {selenium_error}")
         if driver:
             print("Quitting WebDriver due to Selenium error.")
             driver.quit()
             driver = None
         if os.path.exists('cookies.json'):
             print("Deleting cookies.json due to login error.")
             os.remove('cookies.json')
         # Fall through to increment retry_count and potentially retry

    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {e}")
        # Clean up driver if it exists
        if driver:
            print("Quitting WebDriver due to unexpected error.")
            driver.quit()
            driver = None
        retry_count = MAX_RETRIES + 1 # Prevent further retries on unexpected errors
        break # Exit the loop

    # --- Retry Logic ---
    retry_count += 1
    if retry_count <= MAX_RETRIES:
        print(f"Retrying ({retry_count}/{MAX_RETRIES})...")
        time.sleep(2) # Wait a bit before retrying
    else:
        print("Maximum retry attempts reached. Exiting.")


# --- Final Driver Cleanup ---
# Clean up the driver if it's still active after the loop
if driver:
    print("Quitting WebDriver after loop completion.")
    driver.quit()
    driver = None


# --- Calendar Download ---
# Proceed only if links were successfully extracted in the loop
if links:
    print("\nDownloading calendar HTML files...")
    # Need cookies dict again. Reload from file as it should be valid now.
    try:
        with open('cookies.json', 'r') as file:
             cookies_list_final = json.load(file)
        cookies_final = {cookie['name']: cookie['value'] for cookie in cookies_list_final}

        i = 0
        for link in links:
            i += 1
            try:
                print(f"Downloading calendar from: {link}")
                calendar_html = requests.get(link, cookies=cookies_final, timeout=10).text # Added timeout
                filename = f'calendar{i}.html'
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(calendar_html)
                print(f"Saved {filename}")
            except requests.exceptions.RequestException as req_err:
                 print(f"Error downloading calendar from {link}: {req_err}")
            except Exception as download_e:
                print(f"Error processing or saving calendar from {link}: {download_e}")
        print("\nFinished downloading calendars.")

    except FileNotFoundError:
         print("\nError: cookies.json not found when trying to download calendars. This shouldn't happen if links were extracted.")
    except Exception as final_err:
         print(f"\nAn error occurred during calendar download phase: {final_err}")

elif retry_count > MAX_RETRIES:
     print("\nCould not retrieve links after maximum retries.")
else:
     # This case might happen if an unexpected error broke the loop early
     print("\nCould not retrieve links due to an earlier error.")
