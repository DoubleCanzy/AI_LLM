from openai import OpenAI

# 自动读取 OPENAI_API_KEY 环境变量
client = OpenAI()

response = client.responses.create(
    model="gpt-6-astra",
    input="请用一句话介绍 RUNOOB 菜鸟教程。"
)

print("AI 回复：")
print(response.output_text)