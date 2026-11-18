# ============================================
# 实战：自动信息收集 Agent
# ============================================

import json
import time
from typing import Dict, Any, List


class ResearchAgent:
    """
    一个简单的研究型 Agent：
    给定一个主题，自动搜索相关信息，整理成报告
    """

    def __init__(self, max_steps: int = 5):
        self.max_steps = max_steps
        self.memory: List[Dict] = []  # 记忆
        self.known_facts: List[str] = []  # 收集到的事实
        self.queries_used: List[str] = []  # 用过的搜索词

    def _search_web(self, query: str) -> str:
        """（模拟）网络搜索"""
        print(f"   搜索：{query}")
        time.sleep(0.5)  # 模拟延迟

        # 模拟知识库
        knowledge_base = {
            "人工智能": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
            "机器学习": "机器学习是人工智能的一个子集，它使计算机能够从数据中学习，而无需明确编程。",
            "深度学习": "深度学习是机器学习的一个子集，基于多层神经网络，特别擅长处理图像、文本等非结构化数据。",
            "大语言模型": "大语言模型（LLM）是一种基于 Transformer 架构的 AI 模型，经过海量文本训练，能够理解和生成人类语言。",
            "Agent": "AI Agent 是一种能自主感知环境、做出决策并采取行动的系统，通常由 LLM、工具、记忆、规划四部分组成。",
            "Transformer": "Transformer 是 Google 2017 年提出的一种神经网络架构，是现代 LLM 的基础，核心是注意力机制。",
            "runoob": "菜鸟教程（runoob）创建于 2013 年，是一个专注于编程教程的网站，提供多种编程语言的学习资源。",
        }

        # 查找最相关的知识
        for key, value in knowledge_base.items():
            if key in query:
                return value

        return f"关于'{query}'的搜索结果：这是一个非常有趣的主题，涉及多个技术领域。（模拟结果）"

    def _think(self, step: int, user_topic: str) -> Dict[str, Any]:
        """
        思考下一步做什么
        （真实项目中这里应该调用 LLM）
        """
        # 简单的启发式规则模拟思考过程
        if step == 1:
            # 第一步：先搜索主题本身
            return {
                "thought": f"我需要先了解'{user_topic}'的基本定义和背景。",
                "action": "search",
                "query": user_topic,
            }

        elif step == 2:
            # 第二步：搜索相关技术
            return {
                "thought": "基本定义有了，现在我需要搜索相关的技术和概念。",
                "action": "search",
                "query": f"{user_topic} 相关技术",
            }

        elif step < self.max_steps:
            # 中间步骤：继续深入
            return {
                "thought": "让我再搜索一些更多维度的信息，让报告更丰富。",
                "action": "search",
                "query": f"{user_topic} 应用场景",
            }

        else:
            # 最后一步：整理报告
            return {
                "thought": "我已经收集了足够的信息，现在可以整理最终报告了。",
                "action": "finish",
            }

    def _observe(self, action_result: str):
        """观察结果，记录到记忆"""
        self.known_facts.append(action_result)
        self.memory.append({
            "role": "observation",
            "content": action_result,
        })

    def _generate_report(self, topic: str) -> str:
        """基于收集到的信息生成报告"""
        report = f"# {topic} 研究报告\n\n"
        report += f"> 本报告由 runoob-researcher 自动生成\n\n"
        report += "---\n\n"
        report += "## 核心要点\n\n"

        for i, fact in enumerate(self.known_facts, 1):
            report += f"{i}. {fact}\n\n"

        report += "---\n\n"
        report += "## 总结\n\n"
        report += f"以上就是关于'{topic}'的主要信息整理。"
        report += "如需更深入的研究，可以进一步搜索相关学术论文或技术文档。\n"

        return report

    def run(self, topic: str) -> str:
        """运行研究 Agent"""
        print(f" runoob-researcher 启动！")
        print(f" 研究主题：{topic}")
        print("-" * 50)

        for step in range(1, self.max_steps + 1):
            print(f"\n 第 {step} 步 / 共 {self.max_steps} 步")

            # 1. 思考
            decision = self._think(step, topic)
            print(f"   思考：{decision['thought']}")

            if decision["action"] == "finish":
                print("   收集完成，开始整理报告...")
                break

            # 2. 行动
            if decision["action"] == "search":
                result = self._search_web(decision["query"])
                print(f"   结果：{result[:60]}...")

                # 3. 观察
                self._observe(result)

        # 生成最终报告
        print("\n" + "-" * 50)
        print(" 生成研究报告...")
        final_report = self._generate_report(topic)
        return final_report


# ============================================
# 试试看效果
# ============================================

agent = ResearchAgent(max_steps=4)
report = agent.run("Agent 智能体")

print("\n" + "=" * 50)
print(report)
print("=" * 50)