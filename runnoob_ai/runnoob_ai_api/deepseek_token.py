import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "user",
            "content": "请解释什么是 Python 列表。"
        }
    ],
    thinking={"type": "disabled"}
)

print(response.choices[0].message.content)

usage = response.usage

if usage:
    print("输入 Token：", usage.prompt_tokens)
    print("输出 Token：", usage.completion_tokens)
    print("总 Token：", usage.total_tokens)