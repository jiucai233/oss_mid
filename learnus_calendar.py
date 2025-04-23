import re
import requests
import json
from bs4 import BeautifulSoup

# Load cookies from a JSON file
with open('cookies.json', 'r') as file:
    cookies_list = json.load(file)

# Convert cookies list to a dictionary
cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}

# URL of the website
url = "https://ys.learnus.org/calendar/view.php?view=upcoming"

# Send a GET request with cookies
response = requests.get(url, cookies=cookies)

# Check if the request was successful
if response.status_code == 200:
    print("HTML content fetched successfully!")
    # Write the HTML content to a file
    html_content = response.text
else:
    print(f"Failed to fetch HTML. Status code: {response.status_code}")


# 使用正则表达式提取注释中的 <a> 标签
pattern = r'<!--\s*<a href="(.*?)">.*?</a>\s*-->'
links = re.findall(pattern, html_content)

# 打印所有链接
for link in links:
    print("link", link)