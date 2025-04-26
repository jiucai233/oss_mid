from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def convert_to_notion_date(date_str, time_str=None):
    """
    将日期转换为 Notion API 可接受的格式（默认韩国时区 +09:00）。
    :param date_str: 输入日期字符串，例如 "2025-04-27 00:00"
    :param time_str: 可选的时间字符串，例如 "23:59:00"
    :return: 转换后的日期字符串，例如 "2025-04-30T23:59:00+09:00"
    """
    try:
        # 解析输入日期字符串
        input_format = "%Y-%m-%d %H:%M"
        date_obj = datetime.strptime(date_str, input_format)

        # 如果提供了时间字符串，更新时间
        if time_str:
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
            date_obj = datetime.combine(date_obj.date(), time_obj)

        # 默认将日期加 3 天，并设置时间为 23:59:00
        date_obj += timedelta(days=3)
        final_time = datetime.combine(date_obj.date(), datetime.strptime("23:59:00", "%H:%M:%S").time())

        # 转换为 ISO 8601 格式，添加时区偏移 +09:00
        return final_time.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    except Exception as e:
        print(f"Error in convert_to_notion_date: {e}")
        return None


def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取类型
    type_element = soup.find('title')
    type = type_element.text.strip() if type_element else "N/A"
    
    # 提取标题
    title_element = soup.find('h2')
    title = title_element.text.strip() if title_element else "N/A"

    # 提取内容
    content_element = soup.find('div', {'id': 'intro'})
    content = content_element.get_text(separator="\n").strip() if content_element else "N/A"
    
    # 提取 <a> 标签中的 href 链接
    a_tag = soup.find('a', href=True, title=["과제","Assignment"])
    if a_tag:
        href_link = a_tag['href']
        content = f"Link: {href_link}\n{content}"

    # 提取截止日期
    due_date_element = soup.find('td', string=["Due date", "종료 일시"])
    due_date = due_date_element.find_next_sibling('td').text.strip() if due_date_element else "N/A"
    if due_date:
        due_date = convert_to_notion_date(due_date)

    # 提取文件下载链接
    file_links = []
    file_elements = soup.find_all('a', href=True)
    for file_element in file_elements:
        if "forcedownload=1" in file_element['href']:
            file_links.append(file_element['href'])
    
    if file_links:
        for file_link in file_links:
            content += f"\nFile Link: {file_link}"
        
    return {
        "Type": type,
        "Title": title,
        "Content": content,
        "Date": due_date,
    }

if __name__ == "__main__":
    # 示例：读取 HTML 文件并提取信息
    file_paths = [
        "d:\\python\\oss\\midterm\\oss_mid\\calendar_1.html",
        "d:\\python\\oss\\midterm\\oss_mid\\calendar_2.html",
        "d:\\python\\oss\\midterm\\oss_mid\\calendar_3.html"
    ]

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            info = extract_info(html_content)
            print(info)