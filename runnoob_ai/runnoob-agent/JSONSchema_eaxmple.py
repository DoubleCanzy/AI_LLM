# 这是一个典型的工具定义（用 Python 字典表示，最终会转成 JSON）
tool_definition = {
    "type": "function",
    "function": {
        "name": "get_weather",  # 函数名
        "description": "查询指定城市指定日期的天气",  # 函数用途描述，LLM 会看这个
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，比如'北京'、'上海'、'深圳'",
                },
                "date": {
                    "type": "string",
                    "description": "日期，格式为 YYYY-MM-DD，比如'2024-06-18'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位，摄氏度或华氏度，默认摄氏度",
                },
            },
            "required": ["city", "date"],  # 必填参数
        },
    },
}

# 另一个工具：搜索
search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "在互联网上搜索最新信息，适合查新闻、实时数据、未知知识",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词或问题",
                },
                "num_results": {
                    "type": "integer",
                    "description": "返回多少条结果，默认 5",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
}

# 另一个工具：计算器
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "执行数学计算，支持加减乘除、幂运算等",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式，比如'25 * 4 + 10'、'sqrt(16)'",
                },
            },
            "required": ["expression"],
        },
    },
}

print(f"已定义 {len([tool_definition, search_tool, calculator_tool])} 个工具：get_weather, web_search, calculate")
# 输出：已定义 3 个工具：get_weather, web_search, calculate