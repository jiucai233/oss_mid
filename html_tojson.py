from bs4 import BeautifulSoup

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
    
    # 提取截止日期
    due_date_element = soup.find('td', string=["Due date", "종료 일시"])
    due_date = due_date_element.find_next_sibling('td').text.strip() if due_date_element else "N/A"

    # 提取文件下载链接
    file_links = []
    file_elements = soup.find_all('a', href=True)
    for file_element in file_elements:
        if "forcedownload=1" in file_element['href']:
            file_links.append(file_element['href'])

    return {
        "Type": type,
        "Title": title,
        "Content": content,
        "Due Date": due_date,
        "File Links": file_links
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
            print(f"File: {file_path}")
            print(f"Type: {info['Type']}")
            print(f"Title: {info['Title']}")
            print(f"Content: {info['Content']}")
            print(f"Due Date: {info['Due Date']}")
            print(f"File Links: {', '.join(info['File Links']) if info['File Links'] else 'None'}")
            print("-" * 50)