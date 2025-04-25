import re
import requests
import json
from bs4 import BeautifulSoup

def get_links(cookies):
    # URL of the website
    url = "https://ys.learnus.org/calendar/view.php?view=upcoming"

    # Send a GET request with cookies
    response = requests.get(url, cookies=cookies)

    # Check if the request was successful
    if response.status_code == 200:
        print("HTML content fetched successfully!")
        # Write the HTML content to a file
        html_content = response.text
            # 使用正则表达式提取注释中的 <a> 标签
        pattern = r'<!--\s*<a href="(.*?)">.*?</a>\s*-->'
        links = re.findall(pattern, html_content)

        return links
    else:
        print(f"Failed to fetch HTML. Status code: {response.status_code}")
        return None


