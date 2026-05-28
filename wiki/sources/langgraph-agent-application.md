---
title: 基于 LangGraph 创建智能体应用
type: source
tags: [langgraph, agent, langchain]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

本文介绍 LangGraph 库，用于构建复杂的多智能体系统。LangGraph 通过状态图（State Graph）提供对应用程序流程和状态的精细控制，支持循环和分支、持久性、人机协同、流输出等核心特性。与传统 AgentExecutor 相比，LangGraph 更灵活，可实现复杂的循环工作流。

## 核心要点

- LangGraph 核心概念：图（Graph）、节点（Nodes）、边（Edges）、状态（State）
- 支持循环和条件语句，可实现复杂的迭代推理流程
- 持久性：自动保存每一步执行状态，支持暂停恢复、时间旅行
- 人机协同：允许在行动执行前中断，允许人工介入批准或编辑
- 与 LangChain、LangSmith 无缝集成，但不强依赖

## 关键特性

- 节点可以是任意 Python 函数，不一定非要是大模型调用
- 边可以是固定的或带条件的，条件边需要路由函数
- 规约函数（Reducers）定义状态如何更新，如 `add_messages`
- 消息传递机制源自 Google Pregel 和 Apache Beam

## References

- [[wiki/entities/langchain]]
- [[wiki/concepts/agent-智能体]]
- [[wiki/concepts/agent-智能体]]