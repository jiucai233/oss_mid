from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html
from html_tojson import extract_info

# --- FastMCP Implementation ---
mcp = FastMCP("LearnUsProcessor")

@mcp.tool()
def learnus_calendar_html() -> list:
    """
    Retrieves a list of HTML content from LearnUS links and extracts information.
    """
    try:
        html_list = link_to_html()
        if html_list is None:
            raise ValueError("Failed to retrieve HTML content or no links available.")
        
        # 提取每个 HTML 的信息
        extracted_data = [extract_info(html) for html in html_list]
        return {"data": extracted_data}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in learnus_calendar_html: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
