# MCP-LearnUS

## Overview
**MCP-LearnUS** is a MCP tool designed to make Claude to interact with the LearnUs platform.  
This project was developed for an **Open Source Software (OSS)** course midterm assignment by 申英君(SHEN YINGJUN) and 辛奎霖(SHIN GYULIM).

## Features
- **learnus_getcookie**: Automates login and cookie retrieval from LearnUs.
- **learnus_server**: A simple server to serve LearnUs data.
- **NotionUpload**: Integration with Notion.

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
NotionDatabaseID = your_notion_database_id
```
We would recommend you to keep the variable name, since it is used in the other file.

Second, you need to add a connection in the database page(Notion Web page)

__reference:__
https://www.notion.com/help/add-and-manage-connections-with-the-api

Finally, connect the database to the notion calendar.

## Usage
When Claude installation is complete, you can provide your id and pw to Claude and it will automatically login and retrieve cookies. Then you can ask it to get your mission.

## License
This project is licensed under the terms described in the LICENCE file.