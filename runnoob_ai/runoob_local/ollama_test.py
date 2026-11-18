# 文件路径：/Users/runoob/ollama_test.py
# 用 Python 调用 Ollama API

import requests
import json

# Ollama API 地址
OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt: str, model: str = "llama3") -> str:
    """
    向 Ollama 发送请求，获取模型回复

    Args:
        prompt: 用户输入的提示词
        model: 使用的模型名称，默认为 llama3

    Returns:
        模型的回复文本
    """
    # 构造请求数据
    payload = {
        "model": model,      # 使用的模型
        "prompt": prompt,    # 用户输入
        "stream": False      # 不使用流式输出，一次性返回
    }

    try:
        # 发送 POST 请求
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()  # 检查请求是否成功

        # 解析返回的 JSON
        result = response.json()
        return result.get("response", "")

    except requests.exceptions.ConnectionError:
        return "错误：无法连接到 Ollama 服务，请确认 Ollama 已启动"
    except requests.exceptions.RequestException as e:
        return f"请求错误：{str(e)}"


# 测试一下
if __name__ == "__main__":
    # 测试问题 1
    question1 = "请用一句话介绍 RUNOOB 教程"
    answer1 = ask_ollama(question1)
    print(f"问：{question1}")
    print(f"答：{answer1}")
    print("-" * 50)

    # 测试问题 2
    question2 = "写一个 Python 函数，计算斐波那契数列"
    answer2 = ask_ollama(question2)
    print(f"问：{question2}")
    print(f"答：{answer2}")