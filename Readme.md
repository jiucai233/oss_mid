# OSS_MID

## Overview
**OSS_MID** is a collection of Python tools designed to interact with the LearnUs platform.  
It includes modules for retrieving cookies, parsing calendars, converting HTML to JSON, and running a basic server to manage LearnUs data.

This project was developed for an **Open Source Software (OSS)** course midterm assignment.

## Features
- **learnus_getcookie.py**: Automates login and cookie retrieval from LearnUs.
- **learnus_calendar.py**: Parses and extracts calendar event data.
- **learunus_html.py**: Processes HTML content from LearnUs for easier data extraction.
- **learnus_server.py**: A simple server to serve LearnUs data.
- **html_tojson.py**: Converts LearnUs HTML structures into JSON format.
- **NotionConnection.py**: Integration with Notion.

## Installation
Clone the repository and install the required packages:

```bash
git clone https://github.com/jiucai233/oss_mid.git
cd oss_mid
pip install -r requirement.txt
```
### Claude installation
Open Claude->Settings->Developer->Edit Config

```json
{
    "mcpServers": {
        "learnus_calendar_html": {
          "command": "python",
            "args": ["Path_to_learnus_server.py"]
        }
    }
}
```
### Notion Connection (additional)
This project uses Notion as a database. To use it, you need to create a Notion integration and add its credentials to the `.env` file. (create a `.env` file in the root directory of the project)

```.env
NotionAPIKey = your_notion_api_key
```
We would recommend you to name your API key as `NotionAPIKey`, since it is used in the `NotionConnection.py` file.

Second, you need to create a Notion database and add the database ID to the `NotionConnection` file. Then add a connection in the database page
https://www.notion.com/help/add-and-manage-connections-with-the-api

Finally, connect the database to the notion calendar.

## Usage
When Claude installation is complete, you can provide your id and pw to Claude and it will automatically login and retrieve cookies. Then you can ask it to get your mission.

## License
This project is licensed under the terms described in the LICENCE file.