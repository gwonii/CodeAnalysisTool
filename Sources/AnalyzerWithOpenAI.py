import os
import tiktoken
from openai import OpenAI

GPT_MODEL = "gpt-4-turbo"

client = OpenAI(
    api_key="",
)

def count_tokens(text):
    try:
        return len(tokenizer.encode(text))
    except Exception as e:
        print(f"에러: {e}")
        return 0

def analyze_code(requirement, code):
    messages = [
        {
            "role": "system",
            "content": "개발 용어를 제외한 나머지는 한글로 대답해줘"
        },
        {
            "role": "assistant",
            "content": f"{code}"
        },
        {
            "role": "user", 
            "content": f"{requirement}"
        }
    ]

    completion = client.chat.completions.create(
        messages=messages,
        model=GPT_MODEL
    )

    return completion.choices[0].message.content.strip()

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
    contents = ""
    parts_analysis = {}
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

            contents += f"\n{content}\n"

    print(f"{count_tokens}")
    # analysis = analyze_code(requirement, contents)
    # parts_analysis[1] = analysis
                
    # write_markdown_report(report_file_path, file_relative_path, parts_analysis)

folder_path = "/Users/nhn/Documents/OpenSoruces/KarrotListKit/Sources/KarrotListKit"
file_ext = ".swift"
requirement = """
내 요청은 아래의 4가지야
1. 주어진 코드들을 기반으로 모든 class와 struct 를 표로 작성해줘
2. 중요한 class 또는 struct 를 순서대로 표기해줘. 가장 우선적으로 확인해야 하는 것들이 중요한 것이야
3. 존재하는 모든 class와 struct 의 상세 내용과 관계를 알기 위하여 mermaid 문법에 맞춰 class diagram 을 만들어줘
4. extension 항목들에 대해서 내가 쉽게 볼 수 있도록 잘 정리된 표로 작성해줘
"""
process_large_files(folder_path, file_ext, requirement, "KarrotListKit_ClassDiagram4.md")
