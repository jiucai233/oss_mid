from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html
from html_tojson import extract_info
import os
from learnus_getcookie import get_cookies as login_to_cookies
import json

# --- FastMCP Implementation ---
mcp = FastMCP("LearnUsProcessor")

@mcp.tool()
def login_get_cookies(resource: dict) -> dict:
    """
    Logs into LearnUS and retrieves cookies.
    :param resource: A dictionary containing 'username' and 'password'.
    """
    username = resource.get("username")
    password = resource.get("password")
    if not username or not password:
        return {"error": "Username and password are required."}
    try:
        cookies = login_to_cookies(username, password)
        if not cookies:
            return {"error": "Failed to retrieve cookies. Please check your credentials."}
        # Save cookies to a file
        with open("cookies.json", "w") as cookie_file:
            json.dump(cookies, cookie_file)
        return {"cookies": cookies, "message": "Cookies retrieved and saved successfully."}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in get_cookies: {e}")
        return {"error": str(e)}

@mcp.tool()
def learnus_calendar_html(resource: dict) -> dict:
    """
    Retrieves a list of HTML content from LearnUS links and extracts information.
    :param resource: A dictionary containing 'cookies_list' or uses cookies from 'cookies.json'.
    """
    try:
        # Check if cookies are provided in the resource
        cookies_list = resource.get("cookies_list")
        if not cookies_list:
            # If no cookies provided, try to load from cookies.json
            if os.path.exists("cookies.json"):
                with open("cookies.json", "r") as cookie_file:
                    cookies_list = json.load(cookie_file)
                print("Loaded cookies from cookies.json.")
            else:
                raise ValueError("No cookies provided and cookies.json not found. Please log in first.")

        # Fetch HTML content using the cookies
        html_list = link_to_html(cookies_list)
        if not html_list:
            raise ValueError("No HTML content retrieved. Please check your cookies or links.")

        # Extract information from the HTML content
        extracted_data = [extract_info(html) for html in html_list]
        return {"data": extracted_data, "message": "HTML content retrieved and parsed successfully."}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in learnus_calendar_html: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
