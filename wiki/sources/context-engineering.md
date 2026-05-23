---
title: Context Engineering
type: source
tags: [context-engineering, langchain, agents]
sources: [Context Engineering.md]
created: 2026-05-01
updated: 2026-05-01
---

# Context Engineering

## 核心要点

1. **四大策略**：Write（写入）、Select（选择）、Compress（压缩）、Isolate（隔离）
2. **目标**：在智能体的每个步骤中填充恰好合适的信息到上下文窗口
3. **LangGraph 支持**：LangGraph 设计支持所有这些策略

## 策略详解

- **Write**：在每一步写入相关信息到上下文
- **Select**：选择最相关的上下文信息
- **Compress**：压缩冗长信息，保持关键内容
- **Isolate**：隔离不同任务/会话的上下文

## References

- [LangChain Blog: Context Engineering for Agents](https://www.langchain.com/blog/context-engineering-for-agents)
- [[skills/context-engineer]]