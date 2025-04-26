import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # 加载 .env 文件
api_key = os.getenv("NotionAPIKey")  # 获取值
database_id = "1e05db4ddc178020b907fea9c4cc6c40"

headers = {
    "Authorization": f"Bearer {api_key}",  # 添加 Bearer 前缀
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_database_properties():
    """获取数据库的属性"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["properties"]
    else:
        print(f"获取数据库属性失败，状态码：{response.status_code}, 错误信息：{response.text}")
        return None

def create_notion_page(data, properties):
    """将数据插入到 Notion 数据库中"""
    create_url = "https://api.notion.com/v1/pages"

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {}
    }

    for prop_name, prop_schema in properties.items():
        if prop_schema["type"] == "title":
            new_page_data["properties"][prop_name] = {
                "title": [
                    {
                        "text": {
                            "content": data.get("Title", "")  # 假设 "Title" 对应 title 属性
                        }
                    }
                ]
            }
        elif prop_schema["type"] == "rich_text":
            new_page_data["properties"][prop_name] = {
                "rich_text": [
                    {
                        "text": {
                            "content": data.get("Content", "")  # 假设 "Content" 对应 rich_text 属性
                        }
                    }
                ]
            }
        elif prop_schema["type"] == "select":
            new_page_data["properties"][prop_name] = {
                "select": {
                    "name": data.get("Type", "")  # 假设 "Type" 对应 select 属性
                }
            }
        elif prop_schema["type"] == "date":
            # 处理日期类型，假设你有一个 `Date` 字段在 `data` 中
            new_page_data["properties"][prop_name] = {
                "date": {
                    "start": data.get("Date", "")  # 假设 "Date" 对应日期属性，格式为 "YYYY-MM-DD"
                }
            }
        else:
            print(f"不支持的属性类型：{prop_schema['type']}")

    response = requests.post(create_url, headers=headers, json=new_page_data)

    if response.status_code == 200:
        print("页面创建成功")
    else:
        print(f"页面创建失败，状态码：{response.status_code}, 错误信息：{response.text}")


# 提供的 JSON 数据
json_data = {
  "data": [
    {
      "Type": "과제",
      "Title": "중간고사 대체 과제",
      "Content": "Link: https://ys.learnus.org/mod/assign/view.php?id=4003830\n중간고사 대체 과제는 \n과제 가이드라인 https://hongbuzz.notion.site/1cfaf259fd05808d99bdc81cec8cb1cd?pvs=4\n에 맞춰서 \n개인별로 지정한 https://ys.learnus.org/mod/ubboard/view.php?id=4002760 (세부 주제 변경은 필요에 따라서 개별 수정가능하다 )\n과제 주제를 해결한다. \n제출형태 \n1. 파일 첨부 : 보고서 (양식은 가이드라인 참조) mid_term_nlp_학번_이름.pdf \n2. 직접 작성 : github repo url ( 공개 리포 추천, 만약 비공개의 경우 hongsw 아이디를 Collabolator로 추가 필수 )\n8주차는 중간고사 제출을 대체하고,(수업없음)\n9주차에 발표를 제출한 보고서를 바탕으로 진행합니다. \n평가방법 \n항목\n배점\n평가 포인트\n1. \n기획의 타당성과 시나리오 충실도\n25점\n문제 정의와 모델 선택이 합리적인가? 불필요한 기능 없이 목표를 잘 구현했는가?\n2. \n탐색과 실험 과정의 충실성\n25점\n다양한 시도, 실패/재도전, 데이터 처리/모델 적용 흐름이 명확하게 기록되었는가? (커밋, 노트북 포함)\n3. \n실험 결과 분석 및 성찰\n20점\n결과를 단순 나열하지 않고 비교·해석하며 인사이트를 도출했는가? 한계나 개선점에 대한 고민이 있는가?\n4. \n문서화 및 공유 구조 완성도\n15점\nGitHub + Colab 구조의 명확성, 커밋 메시지, 재현 가능성, 보고서 정돈 상태 등\n5. \n발표 내용과 표현력\n15점\n보고서를 기반으로 실험 내용을 정확히 설명하고, 질문에 논리적으로 대응했는가?",
      "Date": "2025-04-30T23:59:00+09:00"
    },
    {
      "Type": "과제",
      "Title": "중강고사 대체 과제",
      "Content": "Link: https://ys.learnus.org/mod/assign/view.php?id=4003848\n중간고사 대체 과제는 \n과제 가이드라인 https://hongbuzz.notion.site/2025_OSS_-1d1af259fd0580a3b7c6ddedcef71c52?pvs=4\n에 맞춰서 \n개인 및 팀별로 지정한 https://ys.learnus.org/mod/ubboard/view.php?id=4003541 (세부 주제 변경은 필요에 따라서 개별 개선 및 수정가능하다 )\n과제 주제를 해결한다. \n제출형태 \n1. 파일 첨부 : 보고서 (양식은 가이드라인 참조) mid_term_nlp_학번_이름_팀번호.pdf \n2. 직접 작성 : github repo url ( 공개 리포 추천, 만약 비공개의 경우 hongsw 아이디를 Collabolator로 추가 필수 )\n8주차는 중간고사 제출을 대체하고,(수업없음)\n9주차에 발표를 제출한 보고서를 바탕으로 진행합니다. \n평가방법 \n항목\n배점\n평가 포인트\n1. \n아이디어 기획의 실현 가능성과 실용성\n25점\n작업 문제를 잘 정의했는가? CLI/API/전문지식 기반으로 자동화 필요성이 있는가? 기능 범위는 적절한가?\n2. \n구현 및 협업 과정의 충실도\n25점\n역할 분담이 명확했고, 각 역할을 성실히 수행했는가? MCP 서버의 도구와 리소스가 정상 동작하며 커밋 기록이 정돈되었는가?\n3. \n기술 적용 및 문서화 완성도\n20점\nFastMCP/Node.js SDK/Docker 등 기술 스택 사용이 명확하며, schema/README.md 에 사용법 등 문서가 OpenSource 프로젝트의 요구사항(소개, 설치방법, 사용방법, 라이선스 명시)을 충실한가?\n4. \n실행 가능성과 재현성\n15점\n다른 사용자가 그대로 따라 실행 가능한가? 도구 실행 예시, 시연 흐름이 명확히 정리되었는가?\n5. \n발표 내용과 협업 설명력\n15점\n기능 설명이 명확하며 팀워크와 역할 수행 과정이 잘 전달되었는가? 질문에 실용적, 기술적으로 응답했는가?",
      "Date": "2025-04-30T23:59:00+09:00"
    },
    {
      "Type": "2025_10_AIC2110.01_00_U_H1 : 7주차 강의 #1",
      "Title": "N/A",
      "Content": "N/A",
      "Date": "N/A"
    },
    {
      "Type": "2025_10_AIC2110.01_00_U_H1 : 7주차 강의 #2",
      "Title": "N/A",
      "Content": "N/A",
      "Date": "N/A"
    },
    {
      "Type": "과제",
      "Title": "Assignment 1",
      "Content": "Link: https://ys.learnus.org/mod/assign/view.php?id=3989760\n과제 제출 마감\n\n\n\n\n04/28 (월) 자정\n\n\n이후에는 과제 제출 받지 않음\n\n\n\n\n과제 제출 형식\n\n\n\n\n보고서 형태로 작성해서 단일 PDF 파일로 제출\n\n\n구체적인 보고서 형식은 따로 없으며 자유롭게 구성\n\n\n영어/한국어 중 원하는 언어로 작성\n\n\n최대 파일 크기 5MB: 스크린샷 등으로 파일 크기가 너무 커지지 않도록 확인\n\n\n\n\n과제 진행 관련\n\n\n\n\n과제 명세 파일 자세히 읽을 것\n\n\nJupyter notebook 사용 관련: 첨부된 튜토리얼 파일 참고\nPython 프로그래밍 관련 ChatGPT, Claude, YATA 등 활용 가능\n \nassignment_1.pdf\n \n \nassignment_1.zip\n \n \nTutorial for Jupyter Notebook.pdf\nFile Link: https://ys.learnus.org/pluginfile.php/5878170/mod_assign/introattachment/0/assignment_1.pdf?forcedownload=1\nFile Link: https://ys.learnus.org/pluginfile.php/5878170/assignsubmission_file/submission_files/13486314/assignment_1.pdf?forcedownload=1",
      "Date": "2025-04-30T23:59:00+09:00"
    },
    {
      "Type": "과제",
      "Title": "'개인정보 보호와 활용’에 대하여 각각 두 가치에 대한 입론과 반론",
      "Content": "Link: https://ys.learnus.org/mod/assign/view.php?id=3955469\n자료 만드는 것은 아무것으로 해도 상관없습니다.\n4월 30일 저녁까지 제출하시고 \n같은 내용이라도 채점을 위해서 \n각 멤버는 자기 조에서 만든 동일한 자료를 각각 learnus로 제출해 주시기 바랍니다.\n제출 내용에 대해서는 자료 발표는 하지 않고 \n자료를 기반으로 하는 토론 배틀을 실시할 예정입니다.\n자료가 잘 만들어져 있어야 배틀에서 이깁니다.\n과제 조구성 및 조장은 첨부합니다.\n \n과제 조 구성.xlsx\nFile Link: https://ys.learnus.org/pluginfile.php/5841756/mod_assign/introattachment/0/%EA%B3%BC%EC%A0%9C%20%EC%A1%B0%20%EA%B5%AC%EC%84%B1.xlsx?forcedownload=1",
      "Date": "2025-04-30T23:59:00+09:00"
    }
  ]
}

# 获取数据库属性
properties = get_database_properties()

# 遍历 JSON 数据并创建 Notion 页面
if properties:
    for item in json_data["data"]:
        create_notion_page(item, properties)

print("所有页面创建完成")