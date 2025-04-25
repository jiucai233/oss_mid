from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html

# --- FastMCP Implementation ---
mcp = FastMCP("LearnUsProcessor")

@mcp.tool()
def learnus_calendar_html() -> list:
    """
    Retrieves a list of HTML content from LearnUS links.
    """
    try:
        html_list = link_to_html()
        if html_list is None:
            raise ValueError("Failed to retrieve HTML content or no links available.")
        return html_list
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in learnus_calendar_html: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
