from anthropic import Anthropic

# 自动读取 ANTHROPIC_API_KEY
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": "请用三句话介绍 Python。"
        }
    ]
)

for block in response.content:
    if block.type == "text":
        print(block.text)