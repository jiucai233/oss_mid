from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html
from html_tojson import extract_info
import os
# --- FastMCP Implementation ---
mcp = FastMCP("LearnUsProcessor")

@mcp.tool()


def learnus_calendar_html(resource: dict) -> list:
    """
    Retrieves a list of HTML content from LearnUS links and extracts information.
    """
    try:
        username = resource.get("username")
        password = resource.get("password")

        if not username or not password:
            html_list = link_to_html(username, password)
            if not html_list:
                raise ValueError("No HTML content found. Please check your credentials. Or try to login again.")   
        html_list = link_to_html(username, password)
        cookies_path = os.path.join(os.getcwd(), 'cookies.json')
        extracted_data = [extract_info(html) for html in html_list]
        return {"data": extracted_data, "cookies": cookies_path}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in learnus_calendar_html: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
