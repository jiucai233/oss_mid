from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html
from html_tojson import extract_info
import os
from learnus_getcookie import get_cookies as login_to_cookies
import json
from dotenv import load_dotenv
from NotionConnection import Notion_upload
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

@mcp.tool()
def Notion_upload_mcp(resource: dict) -> dict:
    """
    Stores the extracted data into Notion.
    :param resource: A dictionary containing 'data' to be stored in Notion.
    """
    try:
        # basic validation of the resource
        calendar_datas = resource.get("calendar_datas")
        api_key = os.getenv("NotionAPIKey")  
        database_id = os.getenv("NotionDatabaseID")          
        if not database_id:
            return {"error": "database ID are required."}
        
        if not api_key:
            if bool(load_dotenv()):
                api_key = os.getenv("NotionAPIKey")
            else:
                return {"error": "API key is required."}

        if not calendar_datas:
            return {"error": "Calendar data is required."}

        Notion_upload(calendar_datas)
        Result = Notion_upload_mcp(calendar_datas, api_key, database_id)
        if not Result:
            return {"error": "Failed to store data in Notion. Please check your API key and database ID."}
        return {"message": "Data stored in Notion successfully."}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in store_to_notion: {e}")
        return {"error": str(e)}
    

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
