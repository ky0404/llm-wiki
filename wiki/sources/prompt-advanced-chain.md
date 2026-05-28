---
title: Prompt 进阶 — 提示链
type: source
tags: [prompt, prompt-engineering, chain]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

本文探讨提示链（Prompt Chain）技术，将复杂任务拆解为多个子任务，通过链式调用逐步完成。每个子任务有独立的 Prompt，最终结果由多个 Prompt 协同产出。这种方法比单次调用更稳定，更易于调试和优化。

## 核心要点

- 提示链思想：将复杂任务拆解为简单子任务，分步执行
- 子任务独立性：每个子任务有明确的目标和输入输出
- 链式调用：前一个子任务的输出作为下一个子任务的输入
- 优势：降低单次 Prompt 复杂度，提高可维护性和可调试性

## 应用场景

- 长文本生成：分段生成后拼接
- 多步骤推理：分解为多个推理步骤
- 信息提取：先提取实体，再进行关系推理

## References

- [[wiki/concepts/prompt-提示工程]]
- [[wiki/concepts/prompt-提示工程]]
- [[wiki/entities/langchain]]