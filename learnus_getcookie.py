from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

def get_cookies(username, password):
    driver = webdriver.Chrome()  # Initialize the WebDriver

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
            return cookies, driver  # Return cookies and driver
        else:
            print("Login failed! Please check your username and password.")
            return None, driver  # Return driver even if login fails

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, driver  # Return driver in case of an error

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    get_cookies(username, password)