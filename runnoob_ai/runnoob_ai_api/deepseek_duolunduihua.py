import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

messages = [
    {
        "role": "system",
        "content": "你是一个 Python 入门教学助手。"
    }
]

def chat(question):
    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        thinking={"type": "disabled"}
    )

    answer = response.choices[0].message.content or ""

    messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer


print("第一轮：")
print(chat("什么是 Python？"))

print("\n第二轮：")
print(chat("它适合开发哪些项目？"))