---
title: Context Engineering 上下文工程
type: concept
tags: [concept, context, engineering]
created: 2026-05-01
updated: 2026-05-01
---

# Context Engineering 上下文工程

在智能体的每个步骤中填充恰好合适的信息到上下文窗口的科学与艺术。

## 核心概念

- [[wiki/sources/context-engineering.md|Context Engineering]]
- [[wiki/sources/effective-context-engineering-ai-agents.md|Effective Context Engineering]]
- [[wiki/sources/浅谈上下文工程.md|浅谈上下文工程]]

## 四大策略

1. **Write（写入）**：在每一步写入相关信息到上下文
2. **Select（选择）**：选择最相关的上下文信息
3. **Compress（压缩）**：压缩冗长信息，保持关键内容
4. **Isolate（隔离）**：隔离不同任务/会话的上下文

## 与 Agent 的关系

- 上下文工程是 Agent 可靠性的关键
- 长时任务需要状态管理与压缩
- LangGraph 设计支持所有这些策略

## 相关资源

- [[wiki/sources/llm-wiki-核心思想.md|LLM Wiki 核心理念]]
- [[wiki/sources/llm-wiki.md|LLM Wiki]]