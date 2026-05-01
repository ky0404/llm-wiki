---
title: Andrej Karpathy
type: entity
tags: [person, researcher, ai, llm]
sources: [CLAUDE.md, README.zh.md]
created: 2026-04-29
updated: 2026-04-29
---

# Andrej Karpathy

## 描述
Andrej Karpathy 是 AI 研究员和工程师，以其在深度学习、计算机视觉和大型语言模型方面的工作而闻名。他是 OpenAI 的前研究总监，也是斯坦福大学 CS231n 课程的讲师。

## 属性
- **领域**：人工智能、深度学习、LLM
- **贡献**：提出了关于 LLM 编码陷阱的重要观察，启发了 [[sources/CLAUDE]] 的创建
- **关键洞察**："LLM 非常擅长循环执行直到达成特定目标……不要告诉它该做什么，给它成功标准，然后看着它完成。"

## 与 LLM Wiki 的关系
Karpathy 的方法论对 [[concepts/llm-wiki]] 系统有重要影响，特别是在以下方面：
1. **目标驱动执行**：将指令转化为可验证的成功标准
2. **编译增强生成（CAG）**：与传统的 [[concepts/rag]] 方法形成对比
3. **LLM 行为指南**：他的观察直接导致了 [[sources/CLAUDE]] 的制定

## References
- [[sources/CLAUDE]] - 基于他的观察
- [[concepts/llm-wiki]] - 受其方法论影响
- [[concepts/目标驱动编程]] - 相关概念