import os
import requests
import tiktoken

# GPT-3.5-turbo API 설정
API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "apy_key"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

GPT_MODEL = "gpt-3.5-turbo"
TOKEN_LIMIT_RATIO = 0.8
TOKEN_LIMIT = 4096
TOKEN_THRESHOLD = int(TOKEN_LIMIT * TOKEN_LIMIT_RATIO)

tokenizer = tiktoken.get_encoding("p50k_base")

def count_tokens(text):
    try:
        return len(tokenizer.encode(text))
    except Exception as e:
        print(f"에러: {e}")
        return 0

def split_into_parts(content):
    lines = content.split('\n')
    parts = []
    part = ""
    for line in lines:
        if count_tokens(part + line) > TOKEN_THRESHOLD:
            parts.append(part)
            part = line + '\n'
        else:
            part += line + '\n'
    parts.append(part)
    return parts

def analyze_code(requirement, code):
    payload = {
        "model": GPT_MODEL,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": f"{requirement}: \n```\n{code}\n```"
            }
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"API 요청 실패: HTTP 상태 코드 {response.status_code}")
        print(f"응답 내용: {response.text}")
        return None

    try:
        response_data = response.json()
    except ValueError:
        print("응답이 JSON 형식이 아닙니다.")
        return None

    return response_data['choices'][0]['message']['content'].strip()

current_folder = os.path.dirname(os.path.abspath(__file__))

def write_markdown_report(file_path, file_relative_path, parts_analysis, mode='a'):
    with open(file_path, mode, encoding='utf-8') as md_file:
        for part_number, analysis in parts_analysis.items():
            if len(parts_analysis) == 1:
                md_file.write(f"### {file_relative_path}\n")
            else:
                md_file.write(f"### {file_relative_path} - part {part_number}\n")
            md_file.write(f"\n{analysis}\n\n")

def process_large_files(directory, file_ext, requirement, output):
    report_file_path = os.path.join(current_folder, output)
    if os.path.exists(report_file_path):
        os.remove(report_file_path)

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if not file_name.endswith(file_ext):
                continue

            print("* " + file_name)

            file_path = os.path.join(root, file_name)
            file_relative_path = os.path.relpath(file_path, start=directory)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_content:
                content = file_content.read()

            parts = split_into_parts(content)
            parts_analysis = {}
            for i, part in enumerate(parts, start=1):
                analysis = analyze_code(requirement, part)
                if analysis:
                    parts_analysis[str(i)] = analysis

            write_markdown_report(report_file_path, file_relative_path, parts_analysis)

folder_path = "/Users/gwonii/Documents/iOS/OpenSource/DifferenceKit/Sources"
file_ext = ".swift"
requirement = "protocol 별로 property, method 표로 정리해주고 핵심 로직 분석해줘, 그리고 간단한 사용법 및 응용할 수 있는 방법들도 정리해줘"
print("completed")
# process_large_files(folder_path, file_ext, requirement, "DifferenceKit.md")
