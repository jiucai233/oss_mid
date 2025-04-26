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
        file_paths = [
            "d:\\python\\oss\\midterm\\oss_mid\\calendar_1.html",
            "d:\\python\\oss\\midterm\\oss_mid\\calendar_2.html",
            "d:\\python\\oss\\midterm\\oss_mid\\calendar_3.html"
        ]
        html_list = []
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                html_list.append(html_content)
            
        extracted_data = [extract_info(html) for html in html_list]
        return {"data": extracted_data}
    except Exception as e:
        # Log the error and return it as a response
        print(f"Error in learnus_calendar_html: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting LearnUsProcessor MCP server...")
    mcp.run()
