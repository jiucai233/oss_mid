from mcp.server.fastmcp import FastMCP
from learunus_html import link_to_html

# --- FastMCP Implementation ---
mcp = FastMCP("LearnUsProcessor")

@mcp.tool()
def learnus_calendar_html() -> list:
    """
    Retrieves a list of HTML content from LearnUS links.
    """
    html_list = link_to_html()
    if html_list is None:
        raise ValueError("Failed to retrieve HTML content or no links available.")
    return html_list

if __name__ == "__main__":
    mcp.run()
