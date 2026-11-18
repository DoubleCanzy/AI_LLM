# ============================================
# 文件：runoob_whisper_demo.py
# 功能：使用 Whisper API 转写语音
# ============================================

import requests
import os

# 配置 API 密钥
OPENAI_API_KEY = "sk-your-api-key-here"
WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"


def transcribe_audio_with_whisper(
    audio_path: str,
    language: str = "zh",  # zh=中文, en=英文, 留空则自动识别
    prompt: str = "",     # 可选：提供一些术语提示，提高准确率
    temperature: float = 0.0
) -> dict:
    """
    使用 Whisper API 转写音频文件

    参数说明：
        audio_path: 音频文件路径（支持 mp3、wav、m4a 等）
        language: 语言代码（可选，不指定则自动识别）
                  常见代码：zh（中文）、en（英文）、ja（日文）
        prompt: 提示词（可选，把可能出现的专业词、人名写在这里）
        temperature: 采样温度（0.0 最确定，1.0 更多样）

    返回：
        包含转写文本的字典
    """
    # 步骤 1：检查文件是否存在
    if not os.path.exists(audio_path):
        return {"error": f"文件不存在：{audio_path}"}

    # 步骤 2：准备请求头
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # 步骤 3：准备请求体（注意：音频要用 multipart/form-data 格式）
    files = {
        "file": open(audio_path, "rb")
    }
    data = {
        "model": "whisper-1",
        "temperature": temperature
    }
    if language:
        data["language"] = language
    if prompt:
        data["prompt"] = prompt

    # 步骤 4：发送请求
    print(f"正在转写音频：{audio_path} ...")
    response = requests.post(WHISPER_API_URL, headers=headers, files=files, data=data)

    # 步骤 5：关闭文件
    files["file"].close()

    # 步骤 6：处理响应
    if response.status_code == 200:
        result = response.json()
        text = result["text"]
        print(f"转写完成，共 {len(text)} 字")
        return {
            "text": text,
            "language": language
        }
    else:
        error_msg = f"请求失败：{response.status_code} - {response.text}"
        print(error_msg)
        return {"error": error_msg}


def transcribe_with_timestamps(audio_path: str) -> dict:
    """
    带时间戳的转写（使用 verbose_json 格式）
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    files = {"file": open(audio_path, "rb")}
    data = {
        "model": "whisper-1",
        "response_format": "verbose_json",  # 返回详细信息，包括时间戳
        "timestamp_granularities": ["segment", "word"]  # 支持段级和词级时间戳
    }

    response = requests.post(WHISPER_API_URL, headers=headers, files=files, data=data)
    files["file"].close()

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": response.text}


def translate_audio_to_english(audio_path: str) -> dict:
    """
    将任意语言的音频翻译成英文文本
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    files = {"file": open(audio_path, "rb")}
    data = {
        "model": "whisper-1",
        "task": "translate"  # 特别指定：翻译任务
    }

    response = requests.post("https://api.openai.com/v1/audio/translations",
                            headers=headers, files=files, data=data)
    files["file"].close()

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


def runoob_meeting_minutes_demo(audio_path: str) -> str:
    """
    实战：生成会议纪要
    步骤 1：用 Whisper 转写录音
    步骤 2：用 GPT-4o 整理成纪要
    """
    # 先转写
    print("第一步：转写会议录音...")
    transcribe_result = transcribe_audio_with_whisper(
        audio_path,
        language="zh",
        prompt="这是一次 RUNOOB 技术团队的会议，讨论产品开发、进度、技术方案等"
    )

    if "error" in transcribe_result:
        return transcribe_result["error"]

    transcript = transcribe_result["text"]

    # 再整理（这里简化了，实际项目中可以调用 GPT-4o API）
    print("第二步：整理会议纪要...")
    # 这里为了演示，直接返回转写文本
    # 实际项目中，你可以把 transcript 发给 GPT-4o，让它整理
    return transcript


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    # 准备一个测试音频文件
    test_audio = "runoob_test_audio.mp3"

    if not os.path.exists(test_audio):
        print(f"提示：请准备一个音频文件，命名为 {test_audio}")
        print("或者用手机录一段语音，保存为 mp3 格式")
    else:
        # 任务 1：简单转写
        print("\n" + "="*50)
        print("任务 1：简单转写")
        print("="*50)
        result1 = transcribe_audio_with_whisper(test_audio, language="zh")
        if "text" in result1:
            print("转写结果：")
            print(result1["text"])

        # 任务 2：带时间戳的转写
        print("\n" + "="*50)
        print("任务 2：带时间戳的转写")
        print("="*50)
        result2 = transcribe_with_timestamps(test_audio)
        if "segments" in result2:
            print("段落信息：")
            for seg in result2["segments"][:3]:  # 只打印前 3 段
                start = round(seg["start"], 2)
                end = round(seg["end"], 2)
                text = seg["text"]
                print(f"[{start}-{end}] {text}")

        print("\n" + "="*50)
        print("RUNOOB Whisper 演示完成！")
        print("="*50)