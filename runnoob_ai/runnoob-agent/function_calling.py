# ============================================
# 一个简化版的 Agent 工具调用演示
# 不需要真实的 API Key，用模拟数据演示
# ============================================

import json
import random
from typing import Dict, Any, List, Optional


class SimpleAgent:
    """一个简单的 Agent 演示类"""

    def __init__(self):
        # 注册可用的工具
        self.tools = self._define_tools()
        # 对话历史（记忆）
        self.messages: List[Dict] = []

    def _define_tools(self) -> List[Dict]:
        """定义所有可用的工具"""
        return [
            {
                "name": "web_search",
                "description": "搜索互联网获取最新信息",
                "parameters": {
                    "query": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["query"],
            },
            {
                "name": "calculate",
                "description": "执行数学计算",
                "parameters": {
                    "expression": {"type": "string", "description": "数学表达式"},
                },
                "required": ["expression"],
            },
            {
                "name": "get_weather",
                "description": "查询天气",
                "parameters": {
                    "city": {"type": "string", "description": "城市名"},
                    "date": {"type": "string", "description": "日期"},
                },
                "required": ["city", "date"],
            },
        ]

    def _call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """（模拟）调用工具并返回结果"""
        print(f"  [工具调用] {tool_name}({parameters})")

        if tool_name == "web_search":
            query = parameters["query"]
            # 模拟搜索结果
            results = {
                "runoob": "菜鸟教程（runoob）是一个编程学习网站，提供大量编程教程和实例。",
                "2024年6月18日北京天气": "北京 2024-06-18：晴天，25°C，湿度 45%。",
                "上海人口": "上海 2024 年常住人口约 2489 万。",
            }
            return results.get(query, f"搜索结果：未找到'{query}'的精确信息，这是一个模拟结果。")

        elif tool_name == "calculate":
            expr = parameters["expression"]
            try:
                # 注意：生产环境不要用 eval，这里只是演示
                result = eval(expr, {"__builtins__": None}, {
                    "sqrt": lambda x: x**0.5,
                    "pow": pow,
                })
                return f"计算结果：{expr} = {result}"
            except Exception as e:
                return f"计算错误：{e}"

        elif tool_name == "get_weather":
            city = parameters["city"]
            date = parameters["date"]
            # 模拟天气数据
            weathers = ["晴天", "多云", "小雨", "阴天"]
            temp = random.randint(15, 35)
            return f"{city} {date}：{random.choice(weathers)}，{temp}°C"

        else:
            return f"未知工具：{tool_name}"

    def _decide_action(self, user_input: str) -> Dict[str, Any]:
        """
        （模拟）LLM 决策过程
        实际项目中这里会调用真实的 LLM API
        """
        # 这里用简单的规则模拟，真实场景应该用 LLM
        if "搜索" in user_input or "查一下" in user_input or "什么是" in user_input:
            # 提取搜索词（简单模拟）
            query = user_input.replace("搜索", "").replace("查一下", "").replace("什么是", "").strip()
            if not query:
                query = "runoob"
            return {
                "action": "call_tool",
                "tool": "web_search",
                "parameters": {"query": query},
            }
        elif "计算" in user_input or "等于" in user_input:
            # 提取表达式（简单模拟）
            return {
                "action": "call_tool",
                "tool": "calculate",
                "parameters": {"expression": "25 * 4 + 10"},  # 示例固定值
            }
        elif "天气" in user_input:
            return {
                "action": "call_tool",
                "tool": "get_weather",
                "parameters": {"city": "北京", "date": "2024-06-18"},
            }
        else:
            return {
                "action": "respond",
                "content": "好的，我来帮你处理这个问题。" + user_input,
            }

    def run(self, user_input: str) -> str:
        """运行 Agent 处理用户输入"""
        print(f"[用户输入] {user_input}")
        self.messages.append({"role": "user", "content": user_input})

        # 第一步：决定做什么
        decision = self._decide_action(user_input)

        if decision["action"] == "call_tool":
            # 第二步：调用工具
            tool_result = self._call_tool(decision["tool"], decision["parameters"])
            self.messages.append({"role": "tool", "content": tool_result})

            # 第三步：基于工具结果生成最终回答
            # （这里简单拼接，实际应该让 LLM 生成）
            final_response = f"根据我的查询：{tool_result}\n\n希望这个信息对你有帮助！"
            self.messages.append({"role": "assistant", "content": final_response})
            return final_response

        else:
            # 直接回答
            self.messages.append({"role": "assistant", "content": decision["content"]})
            return decision["content"]


# ============================================
# 测试这个 Agent
# ============================================

agent = SimpleAgent()

print("=" * 60)
response1 = agent.run("搜索一下 runoob 是什么")
print(f"[Agent 回复]\n{response1}")

print("\n" + "=" * 60)
response2 = agent.run("帮我查 2024-06-18 北京的天气")
print(f"[Agent 回复]\n{response2}")

print("\n" + "=" * 60)
response3 = agent.run("计算一下 25 * 4 + 10 等于多少")
print(f"[Agent 回复]\n{response3}")