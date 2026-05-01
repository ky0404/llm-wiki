---
title: "Effective context engineering for AI agents（Anthropic 官方）"
type: source
tags: [context-engineering, anthropic, agents, compaction, memory]
sources: [Effective context engineering for AI agents.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
Anthropic 官方发布的 AI 智能体有效上下文工程指南。

### 上下文工程 vs 提示工程
- **提示工程**：编写和组织 LLM 指令以获得最佳结果
- **上下文工程**：在 LLM 推理期间管理和维护最佳 token 集（信息）

随着智能体在多轮推理和更长时间范围内运行，我们需要管理整个上下文状态的策略。

### 有效上下文的解剖
好的上下文工程意味着找到**最小可能的高信号 token 集**，最大化期望结果的可能性。

- **System prompts**：使用简单直接的语言，在"正确的高度"呈现想法。平衡脆弱的 if-else 硬编码提示和过于模糊的指导。
- **Tools**：工具应返回 token 高效的信息并鼓励高效行为。避免过于庞大的工具集。提供清晰、无歧义的参数描述。
- **Examples**：few-shot 提示是最佳实践，但不要塞入大量边界情况。精选多样化、典型的示例。

### 上下文检索与智能体搜索
"just-in-time"策略：维护轻量级标识符（文件路径、存储查询等），运行时动态加载数据。允许智能体按需探索上下文，渐进式披露相关上下文。

混合策略：对于不太动态的内容（如法律或财务工作）可能更好。

### 长时任务的上下文工程
- **Compaction（压缩）**：当对话接近上下文窗口限制时，总结内容并用摘要重新初始化新上下文窗口
- **Structured Note-taking（结构化笔记）**：智能体定期写笔记持久化到上下文窗口外的内存
- **Sub-agent Architectures（子智能体架构）**：专门的子智能体处理专注任务，干净利落的上下文窗口，主智能体协调高级计划

### 核心原则
"找到最小的高信号 token 集，最大化期望结果的可能性"

## References
- [[concepts/上下文工程]]
- [[entities/anthropic]]
- [[sources/context-engineering]]
- [[sources/浅谈上下文工程]]