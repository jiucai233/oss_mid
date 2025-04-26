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
- **NotionTest.py**: Tests integration with Notion (work-in-progress).

## Installation
Clone the repository and install the required packages:

```bash
git clone https://github.com/jiucai233/oss_mid.git
cd oss_mid
pip install -r requirement.txt
```
### Claude installation
Open Claude->Settings->Developer->Edit Config

{
    "mcpServers": {
        "learnus_calendar_html": {
          "command": "python",
            "args": ["Path_to_learnus_server.py"]
        }
    }
}

## License
This project is licensed under the terms described in the LICENCE file.