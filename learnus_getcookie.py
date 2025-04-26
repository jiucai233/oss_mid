from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
import os

def get_cookies(username, password):
    """
    Logs into LearnUS and retrieves cookies.
    :param username: LearnUS username
    :param password: LearnUS password
    :return: Cookies as a list of dictionaries or None if login fails.
    """
    if os.path.exists("cookies.json"):
        with open("cookies.json", "r") as cookie_file:
            cookies = json.load(cookie_file)
            print("Cookies loaded from cookies.json.")
            return cookies

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Open the login page
        driver.get("https://ys.learnus.org/login/method/sso.php")

        # Enter username
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)

        # Enter password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(3)

        # Check if login was successful
        if driver.current_url == "https://ys.learnus.org/":
            print("Login successful!")

            # Get cookies after login
            cookies = driver.get_cookies()
            print("Cookies:", cookies)

            # Save cookies to a JSON file
            with open("cookies.json", "w") as cookie_file:
                json.dump(cookies, cookie_file)
            print("Cookies saved to cookies.json.")
            return cookies
        else:
            print("Login failed! Please check your username and password.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    get_cookies(username, password)