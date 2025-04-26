from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

def get_cookies(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    # Use webdriver-manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://ys.learnus.org/login/method/sso.php")
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)

        if driver.current_url == "https://ys.learnus.org/"or driver.current_url =="https://ys.learnus.org/?lang=ko" or driver.current_url == "https://ys.learnus.org/index.php?lang=en":
            print("Login successful!")
            cookies = driver.get_cookies()
            with open("cookies.json", "w") as cookie_file:
                json.dump(cookies, cookie_file)
            return cookies
        else:
            print("Login failed!")
            return None
    finally:
        driver.quit()

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    get_cookies(username, password)