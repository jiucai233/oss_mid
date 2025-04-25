import json
import requests
import os
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from learnus_calendar import get_links
from learnus_getcookie import get_cookies  

while True:
    try:
        # Check if cookies.json exists
        if os.path.exists('cookies.json'):
            with open('cookies.json', 'r') as file:
                cookies_list = json.load(file)

        else:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cookies_list = get_cookies(username, password)  # Replace with your username and password

        # Convert cookies list to a dictionary
        cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
        links = get_links(cookies)
        if links:
            print("Links extracted successfully!")
            # Print the extracted links
            for link in links:
                print(link)
            break
        else:
            print("Failed to extract links, please check the cookies.")
            print("Re-enter your username and password.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cookies = get_cookies(username, password)

    except UnexpectedAlertPresentException as e:
        # Handle unexpected alert
        alert = Alert(driver=e.driver)  # Get the alert object
        alert_text = alert.text  # Extract the alert text
        print(f"Login failed: {alert_text}")
        alert.accept()  # Dismiss the alert
        print("Please try again.")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

i = 0
for link in links:
    i += 1
    calendar_html = requests.get(link, cookies=cookies).text
    with open(f'calendar{i}.html', 'w', encoding='utf-8') as file:
        file.write(calendar_html)

