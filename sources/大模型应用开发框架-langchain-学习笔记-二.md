---
title: "大模型应用开发框架 LangChain 学习笔记（二）"
type: source
tags: [langchain, agent, function-calling, framework]
sources: [大模型应用开发框架 LangChain 学习笔记（二）.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
本文是 LangChain 学习笔记的第二部分，重点介绍了 Agent 的概念、类型及实现。
- **OpenAI 插件与 Function Calling**：
  - ChatGPT Plugins 使模型能够访问互联网和执行任务。
  - Function Calling 通过 API 实现类似插件的交互能力，模型返回函数名称和参数，由应用侧执行后回传结果。支持多轮调用和参数自动补全。
- **LangChain Agent 核心概念**：
  - **Tools**：希望被 Agent 执行的函数，需清晰描述功能。
  - **Agent**：理解用户问题并从工具集中选择合适工具。
  - **Agent Executor**：本质上是 Chain，递归调用 Agent 获取下一步动作并执行，直到问题解决。
- **Agent 类型**：
  - **Zero-shot ReAct Agent**：基于 ReAct（Reasoning + Acting）范式，结合推理与行动。输出格式包含 Thought、Action、Action Input 和 Observation。
  - **Conversational ReAct Agent**：为 Agent 增加记忆功能，通过 `{chat_history}` 占位符引入历史会话。
  - **ReAct DocStore Agent**：标准 ReAct 实现，必须包含 Search 和 Lookup 两个工具。
  - **Self-Ask Agent**：使用搜索引擎作为唯一工具，通过 Follow up / Intermediate Answer 格式进行多步搜索。
  - **OpenAI Functions Agent**：基于 OpenAI Function Calling，比 ReAct 更可靠。OpenAI Multi Functions Agent 支持一次返回多个工具调用，实现并行执行。
  - **Plan and execute Agent**：提前制定完整执行计划，拆解为子任务后逐步执行，适合需要保持长期目标的复杂任务。

## References
- [[entities/langchain]]
- [[concepts/function-calling]]
- [[concepts/agent]]
- [[concepts/react]]
