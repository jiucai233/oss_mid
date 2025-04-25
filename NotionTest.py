import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()  # 加载 .env 文件
api_key = os.getenv("NotionAPIKey")  # 获取值
database_id = "1a55db4ddc1781deb8b7dbf983774e00"

headers = {
    "Authorization": f"Bearer {api_key}",  # 添加 Bearer 前缀
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 使用正确的查询端点
response = requests.post(
    f'https://api.notion.com/v1/databases/{database_id}/query',
    headers=headers
)

data = response.json()

database_meta = requests.get(
    f"https://api.notion.com/v1/databases/{database_id}",
    headers=headers
).json()

# 获取数据库所有内容
database_content = requests.post(
    f"https://api.notion.com/v1/databases/{database_id}/query",
    headers=headers,
    json={"page_size": 10}  # 最多100条/次
).json()

# 合并结果
full_data = {
    "database_metadata": database_meta,
    "database_content": database_content
}

# 保存为JSON文件
with open("notion_db_raw.json", "w", encoding="utf-8") as f:
    json.dump(full_data, f, indent=2, ensure_ascii=False)

print("原始JSON已保存为 notion_db_raw.json")