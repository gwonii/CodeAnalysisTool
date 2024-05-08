import os
import tiktoken
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"
TOKEN_LIMIT_RATIO = 0.8
TOKEN_LIMIT = 4096
TOKEN_THRESHOLD = int(TOKEN_LIMIT * TOKEN_LIMIT_RATIO)

tokenizer = tiktoken.get_encoding("p50k_base")
client = OpenAI(
    api_key="sk-proj-qfUepXimxE6IuYuedANVT3BlbkFJtw9Bi1Us4EdTtpDTq591",
)

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
    messages = [
        # {
        #     "role": "system",
        #     "content": "You are a helpful assistant."
        # },
        {
            "role": "system",
            "content": "한글로 대답해줘"
        }
    ]

    if requirement:
        messages.append({
            "role": "user", 
            "content": f"{requirement}: \n```\n{code}\n```"
        })
    else:
        messages.append({
            "role": "user", 
            "content": f"Here is some code for analysis, don't need to answer: \n```\n{code}\n```"
        })

    print(f"--> request messages: {messages}")
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

            # parts += split_into_parts(content)
            contents += f"\n{content}\n"
            
            # for i, part in enumerate(parts, start=1):
            #     print(f"parts count: {parts.count} / current count: {i}")
            #     if i == parts.count:
            #         print("last")
            #         analysis = analyze_code(requirement, part)
            #     else:
            #         print("not last")
            #         analysis = analyze_code("", part)

            #     if analysis:
            #         parts_analysis[str(i)] = analysis
                
            # write_markdown_report(report_file_path, file_relative_path, parts_analysis)
    
    # for i, part in enumerate(parts, start=1):
    #     print(f"parts count: {len(parts)} / current count: {i}")
        # if i == len(parts):
            # print("last")
            
        # else:
            # print("not last")
        # analysis = analyze_code("", part)

        # if analysis:
    analysis = analyze_code(requirement, contents)
    parts_analysis[1] = analysis
                
    # analysis = analyze_code(f"이전 {len(parts)} 개의 제공된 코드들을 기반으로 / {requirement}", "")
    write_markdown_report(report_file_path, file_relative_path, parts_analysis)

folder_path = "/Users/nhn/Documents/OpenSoruces/KarrotListKit/Sources/KarrotListKit"
# folder_path = "/Users/nhn/Documents/Gaein/CodeAnalysisTool/Sources/SwiftDummies"
file_ext = ".swift"
requirement = "protocol 별로 property, method 표로 정리해주고 핵심 로직 분석해줘, 그리고 간단한 사용법 및 응용할 수 있는 방법들도 정리해줘"
# requirement = "protocol, class, struct 로 분리해서 표로 정리해봐"
process_large_files(folder_path, file_ext, requirement, "Report2.md")