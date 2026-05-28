---
title: 聊聊 Deep Search 和 Deep Research
type: source
tags: [deep-search, deep-research, rag, ai-search]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

本文探讨 AI 搜索技术的发展，从朴素 RAG 到高级 RAG、Agentic RAG 再到 Deep Search。文章分析了传统 RAG 在复杂问题上的局限性，介绍了 Graph RAG、Agentic RAG 的核心思想，以及各大厂商的 AI+搜索产品布局。

## 核心要点

- AI + 搜索：朴素 RAG，直接调用搜索引擎接口获取结果
- 朴素 RAG 核心问题：检索精确性、多跳推理、全局性理解
- Graph RAG：引入知识图谱，提升复杂问题的回答质量
- Agentic RAG：引入智能体的任务规划、工具使用、反思重试机制

## Agentic RAG 核心能力

- 动态检索：根据生成内容中间结果决定是否二次检索
- 任务分解：将复杂问题拆解为子任务
- 工具调用：不仅检索，还可调用外部工具获取实时信息
- 反思与修正：自我评估结果，发现不足时重新检索
- 多轮交互：主动追问用户以澄清需求

## 常用搜索服务

Bing Web Search、Google Programmable Search、Serper、SerpAPI、Brave Search、Exa API、Tavily、博查搜索 API

## References

- [[wiki/concepts/检索增强生成]]
- 知识图谱
- [[wiki/concepts/agent-智能体]]
- deepseek
- kimi