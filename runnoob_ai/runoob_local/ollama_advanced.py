# 文件路径：/Users/runoob/ollama_advanced.py
# 使用 Ollama Python 库

# 先安装：pip install ollama

import ollama


def chat_with_runoob():
    """
    使用 Ollama Python 库进行多轮对话
    """
    # 消息历史
    messages = [
        {
            "role": "system",
            "content": "你是一个友好的编程助手，名叫 RunoobBot。你的回答要简洁、实用，多用代码示例。"
        }
    ]

    print("RunoobBot 已启动！输入 'quit' 退出。")
    print("-" * 50)

    while True:
        # 获取用户输入
        user_input = input("你：")

        if user_input.lower() in ["quit", "exit", "退出"]:
            print("再见！")
            break

        # 添加用户消息到历史
        messages.append({
            "role": "user",
            "content": user_input
        })

        # 调用模型
        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        # 获取回复
        assistant_message = response["message"]["content"]
        print(f"RunoobBot：{assistant_message}")
        print("-" * 50)

        # 添加助手回复到历史
        messages.append({
            "role": "assistant",
            "content": assistant_message
        })


if __name__ == "__main__":
    chat_with_runoob()