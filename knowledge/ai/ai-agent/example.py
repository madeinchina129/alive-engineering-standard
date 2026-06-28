```python
# AI Agent 实现示例（ReAct 模式）
from typing import List, Dict, Any
from pydantic import BaseModel
from openai import OpenAI
import json

class Tool:
    """Agent 可用工具的定义"""
    name: str
    description: str
    parameters: Dict
    function: callable

class Agent:
    def __init__(self, tools: List[Tool], max_steps: int = 10):
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps
        self.memory = []

    async def run(self, goal: str) -> Dict:
        """执行 ReAct 循环"""
        system_prompt = """你是一个智能代理。你的目标是：{goal}

可用工具：{tool_descriptions}

请使用 ReAct 模式工作：
1. Thought: 分析当前状态和下一步行动
2. Action: 调用工具（格式：TOOL_CALL: tool_name | params_json）
3. Observation: 工具返回的结果
4. ...重复直到任务完成...
5. Final Answer: 输出最终结果

每次输出只包含一个 Thought 或 Action。
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": goal}
        ]

        for step in range(self.max_steps):
            # 推理
            response = await llm.chat(messages)
            content = response.choices[0].message.content
            self.memory.append({"step": step, "reasoning": content})

            # 检查是否最终答案
            if content.startswith("Final Answer:"):
                return {
                    "success": True,
                    "answer": content[13:].strip(),
                    "steps": step + 1,
                    "memory": self.memory
                }

            # 执行工具调用
            if "TOOL_CALL:" in content:
                tool_call = content.split("TOOL_CALL:")[1].strip()
                tool_name, params_str = tool_call.split("|", 1)
                params = json.loads(params_str.strip())

                if tool_name not in self.tools:
                    raise ValueError(f"Unknown tool: {tool_name}")

                # 参数校验
                # 高危操作检查
                if tool_name in ["delete", "update", "payment"]:
                    # 需用户确认
                    confirmed = await self.confirm_action(tool_name, params)
                    if not confirmed:
                        messages.append({"role": "user", "content": "用户取消了操作"})
                        continue

                result = await self.tools[tool_name].function(**params)
                messages.append({"role": "user", "content": f"Observation: {json.dumps(result, ensure_ascii=False)}"})

        # 超过最大步数
        return {"success": False, "error": "超过最大执行步数", "memory": self.memory}
```