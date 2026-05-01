---
title: "你不知道的 Agent：原理、架构与工程实践"
type: source
tags: [agent, architecture, engineering, llm]
sources: [你不知道的 Agent：原理、架构与工程实践.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
本文深入探讨了 Agent 的核心原理、架构设计及工程实践。
- **Agent 基本原理**：大模型作为“大脑”，结合感知、规划和行动模块。通过 ReAct（Reasoning + Acting）模式，将推理与行动相结合。
- **架构设计**：
  - **单 Agent 架构**：适用于简单任务，但面临上下文限制和复杂任务处理能力不足的问题。
  - **多 Agent 架构**：通过角色分工、协作与竞争，处理更复杂的任务。包括 Planner-Executor、Peer-to-Peer 等模式。
- **工程实践**：
  - **工具调用 (Function Calling)**：使 Agent 能够与外部系统交互，执行搜索、计算、API 调用等。
  - **记忆机制**：短期记忆（对话历史）与长期记忆（向量数据库检索）的结合。
  - **规划能力**：任务分解、子目标设定与动态调整。
- **挑战与展望**：幻觉问题、工具调用的准确性、长程任务的稳定性以及多 Agent 协作的效率。

## References
- [[concepts/agent]]
- [[concepts/function-calling]]
- [[concepts/rag]]
- [[sources/工程技术-在智能体优先的世界中利用-codex]]
- [[sources/浅谈上下文工程]]
