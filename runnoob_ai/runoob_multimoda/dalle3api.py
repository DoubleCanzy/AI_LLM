# ============================================
# 文件：runoob_dalle3_demo.py
# 功能：使用 DALL·E 3 API 生成图片
# ============================================

import requests
import os
from datetime import datetime

# 配置 API 密钥（请替换为你的真实密钥）
OPENAI_API_KEY = "sk-your-api-key-here"
DALLE3_API_URL = "https://api.openai.com/v1/images/generations"


def generate_image_with_dalle3(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid",
    save_dir: str = "runoob_generated_images"
) -> dict:
    """
    使用 DALL·E 3 API 生成图片

    参数说明：
        prompt: 文字描述，越详细越好
        size: 图片尺寸
              可选：1024x1024、1024x1792（竖版）、1792x1024（横版）
        quality: 图片质量
                 可选：standard（标准）、hd（高清，更贵）
        style: 风格
               可选：vivid（生动，更有艺术感）、natural（自然，更真实）
        save_dir: 图片保存目录

    返回：
        包含图片 URL 和保存路径的字典
    """
    # 步骤 1：准备请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # 步骤 2：准备请求体
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,  # DALL·E 3 每次只能生成 1 张
        "size": size,
        "quality": quality,
        "style": style
    }

    # 步骤 3：发送请求
    print(f"正在生成图片，提示词：{prompt[:50]}...")
    response = requests.post(DALLE3_API_URL, headers=headers, json=payload)

    # 步骤 4：处理响应
    if response.status_code == 200:
        result = response.json()
        image_url = result["data"][0]["url"]
        revised_prompt = result["data"][0].get("revised_prompt", prompt)

        print(f"DALL·E 3 自动优化后的提示词：{revised_prompt}")

        # 步骤 5：下载并保存图片
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 用时间戳生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"runoob_dalle3_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)

        # 下载图片
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(image_response.content)
            print(f"图片已保存到：{filepath}")

        return {
            "image_url": image_url,
            "filepath": filepath,
            "revised_prompt": revised_prompt
        }
    else:
        error_msg = f"请求失败：{response.status_code} - {response.text}"
        print(error_msg)
        return {"error": error_msg}


def generate_runoob_logo_demo():
    """演示：生成 RUNOOB 风格的 Logo"""
    prompt = """
    A cute and friendly robot mascot for RUNOOB tutorial website.
    Blue and green color scheme, modern flat design, white background.
    The robot looks helpful and intelligent, with big friendly eyes.
    Simple, clean, suitable for a tech education brand.
    """
    # 中文提示词也可以，DALL·E 3 支持多语言
    prompt = """
    为 RUNOOB 教程网站设计一个可爱友好的机器人吉祥物。
    蓝绿色调，现代扁平化设计，白色背景。
    机器人看起来乐于助人且聪明，有大大的友好眼睛。
    简洁干净，适合科技教育品牌。
    """
    return generate_image_with_dalle3(
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        style="vivid"
    )


def generate_book_cover_demo():
    """演示：生成书籍封面"""
    prompt = """
    Book cover design for "AI Tutorial for Beginners".
    Modern minimalist style, deep blue and purple gradient background.
    The title text is elegant and readable.
    Subtle tech elements: floating geometric shapes, faint circuit patterns.
    Professional, trustworthy, suitable for a programming book.
    """
    return generate_image_with_dalle3(
        prompt=prompt,
        size="1024x1792",  # 竖版
        quality="hd",
        style="natural"
    )


def generate_banner_demo():
    """演示：生成横幅广告图"""
    prompt = """
    Web banner design for a coding tutorial website (RUNOOB).
    16:9 wide format. Modern gradient background from teal to blue.
    Clean layout with space for text.
    Abstract tech elements: floating code snippets, subtle grid lines.
    Professional and inviting.
    """
    return generate_image_with_dalle3(
        prompt=prompt,
        size="1792x1024",  # 横版
        quality="standard",
        style="vivid"
    )


# ============================================
# 主程序：演示不同的生成任务
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("RUNOOB DALL·E 3 图片生成演示")
    print("="*60)

    # 任务 1：生成 Logo
    print("\n[任务 1] 生成 Logo ...")
    result1 = generate_runoob_logo_demo()

    # 任务 2：生成书籍封面
    print("\n[任务 2] 生成书籍封面 ...")
    result2 = generate_book_cover_demo()

    # 任务 3：生成横幅
    print("\n[任务 3] 生成横幅 ...")
    result3 = generate_banner_demo()

    print("\n" + "="*60)
    print("所有任务完成！查看 runoob_generated_images 目录")
    print("="*60)