import json
import requests
import os
from learnus_calendar import get_links
from learnus_getcookie import get_cookies  

while True:
    # Check if cookies.json exists
    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r') as file:
            cookies_list = json.load(file)

        # Convert cookies list to a dictionary
        cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        cookies = get_cookies(username, password)  # Replace with your username and password


    links = get_links(cookies)
    if links:
        print("Links extracted successfully!")
        # Print the extracted links
        for link in links:
            print(link)
        break
    else:
        print("Failed to extract links, please check the cookies.")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        cookies = get_cookies(username, password)

for link in links:
    calendar_html = requests.get(link, cookies=cookies).text
    print(calendar_html)
