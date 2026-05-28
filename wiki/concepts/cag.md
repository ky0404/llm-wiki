---
title: CAG（编译增强生成）
type: concept
tags: [方法论, 知识管理, llm]
sources: [llm-wiki-核心思想.md]
created: 2026-04-28
updated: 2026-04-28
---

# CAG（编译增强生成）

CAG（Compilation-Augmented Generation，编译增强生成）是 [[wiki/concepts/llm-wiki]] 采用的知识管理方法。

## 定义
与 [[wiki/concepts/rag]] 相对的 AI 知识处理方法：
- RAG：检索增强生成，每次查询时实时检索文档片段
- CAG：编译增强生成，提前将知识编译成结构化、链接的 wiki 系统

## 工作方式
1. **编译阶段**：AI 读取原始素材，创建结构化知识页面
2. **链接阶段**：建立概念间的交叉引用和关联
3. **查询阶段**：基于已编译的知识体系回答问题

## 优势
- 知识被提前整理和内化
- 减少每次查询的计算开销
- 知识体系自然生长，形成有机联系
- 避免临场拼凑导致的碎片化回答

## References
- [[wiki/concepts/llm-wiki]]
- [[wiki/concepts/rag]]