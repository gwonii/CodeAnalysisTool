# OpenAI Assistant API를 사용하여 코드를 분석하는 코드입니다.

import os
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"

client = OpenAI(
    api_key="",
)

def register_assistant(requirement, file_ext, output):
    targetFiles = []
    directory = "Files/"
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if not file_name.endswith(file_ext):
                continue

            print("* " + file_name)

            file_path = os.path.join(root, file_name)
            file = client.files.create(
                file=open(file_path, "rb"),
                purpose='assistants'
            )
            targetFiles.append(file)

    assistant = client.beta.assistants.create(
        name="Analyze Open Source",
        description="This is an assistant that analyzes open source code.",
        model="gpt-3.5-turbo",
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
            "file_ids": list(map(lambda x: x.id, targetFiles))
            }
        }
    )

    thread = client.beta.threads.create() 
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=requirement
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=""
    )
    
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )

def write_markdown_report(file_path, file_relative_path, parts_analysis, mode='a'):
    with open(file_path, mode, encoding='utf-8') as md_file:
        for part_number, analysis in parts_analysis.items():
            if len(parts_analysis) == 1:
                md_file.write(f"### {file_relative_path}\n")
            else:
                md_file.write(f"### {file_relative_path} - part {part_number}\n")
            md_file.write(f"\n{analysis}\n\n")

file_ext = ".swift"
requirement = "요청사항"

register_assistant(requirement, file_ext, "Report.md")
