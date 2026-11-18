# 文件路径：/Users/runoob/lmstudio_openai.py
# LM Studio 兼容 OpenAI API 格式

from openai import OpenAI

# 连接到 LM Studio 本地服务器
# 注意：需要先在 LM Studio 中开启服务器
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # LM Studio 用这个占位就行
)


def ask_local_model(prompt: str, system_prompt: str = "你是一个有用的助手。") -> str:
    """
    通过 OpenAI 兼容接口调用 LM Studio 本地模型
    """
    response = client.chat.completions.create(
        model="local-model",  # 这个字段会被 LM Studio 忽略
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# 测试
if __name__ == "__main__":
    question = "介绍一下 RUNOOB 教程的特色"
    answer = ask_local_model(
        prompt=question,
        system_prompt="你是 Runoob 的专属客服，专业回答关于编程学习的问题。"
    )
    print(f"问：{question}")
    print(f"答：{answer}")