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
            "content": "请用一句话介绍 RUNOOB 菜鸟教程。"
        }
    ],
    thinking={"type": "disabled"}
)

print("AI 回复：")
print(response.choices[0].message.content)

if response.usage:
    print("输入 Token：", response.usage.prompt_tokens)
    print("输出 Token：", response.usage.completion_tokens)
    print("总 Token：", response.usage.total_tokens)
