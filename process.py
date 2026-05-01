from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read input
with open("inbox.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip().split("\n")

def parse_line(line):
    parts = line.split("|")
    data = {}
    for part in parts:
        if ":" in part:
            k, v = part.split(":", 1)
            data[k.strip()] = v.strip()
    return data

def agent(task):
    prompt = f"""
Task: {task.get('task','')}
Topic: {task.get('topic','')}
Style: {task.get('style','')}
Length: {task.get('length','')}

Follow instructions exactly and respond clearly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise structured automation engine."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

outputs = []

for line in raw:
    if not line.strip():
        continue
    task_data = parse_line(line)
    result = agent(task_data)
    outputs.append(result)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("outputs.txt", "a", encoding="utf-8") as f:
    f.write("\n\n====================\n")
    f.write(f"BATCH RUN: {timestamp}\n\n")

    for o in outputs:
        f.write(o)
        f.write("\n--------------------\n")

print("Automation run complete.")