import json
import os
import requests
from learnus_calendar import get_links

def link_to_html(cookies_list):
    """
    Reads cookies from cookies.json and retrieves HTML content from LearnUS links.
    If cookies are invalid or expired, raises an error.
    """
    links = None  # Initialize links as None
    html_list = []  # List to store HTML content

    try:
  
        # --- Link Extraction ---
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
        print("Attempting to get links using cookies.")
        links = get_links(cookies_dict)

        if not links:
            raise ValueError("Failed to extract links. Cookies might be invalid or expired.")

        print("Links extracted successfully!")

        # --- HTML Content Retrieval ---
        print("\nReading calendar HTML files...")
        for link in links:
            try:
                print(f"Reading calendar from: {link}")
                html_content = requests.get(link, cookies=cookies_dict).text
                html_list.append(html_content)  # Append HTML content to the list
            except Exception as read_e:
                print(f"Error processing calendar from {link}: {read_e}")

        print("\nFinished reading calendars.")
        return html_list if html_list else None  # Return the list if not empty, else None

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  # Re-raise the exception for the caller to handle

if __name__ == "__main__":
    try:
        htmls = link_to_html()
        if htmls:
            for i, html in enumerate(htmls, start=1):
                with open(f'calendar_{i}.html', 'w', encoding='utf-8') as f:
                    f.write(html)
            print(f"Saved {len(htmls)} calendar HTML files.")
        else:
            print("No HTML files were retrieved.")
    except Exception as e:
        print(f"Failed to retrieve HTML content: {e}")

