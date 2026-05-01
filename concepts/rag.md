---
title: RAG（检索增强生成）
type: concept
tags: [方法论, 知识管理, llm]
sources: [llm-wiki-核心思想.md]
created: 2026-04-28
updated: 2026-04-28
---

# RAG（检索增强生成）

RAG（Retrieval-Augmented Generation，检索增强生成）是传统的 AI 知识处理方法。

## 定义
一种 AI 知识处理方法，每次查询时：
1. 从文档库中检索相关片段
2. 将检索到的内容与查询一起提供给 LLM
3. LLM 基于检索到的内容生成回答

## 核心要点
在 RAG 的检索阶段，BERT 等预训练语言模型作为稠密检索编码器（如 DPR），通过将查询和文档映射到同一向量空间，实现语义级别的精准匹配，是其检索质量的关键保障。

## 特点
- **临时性**：每次查询都是独立的检索过程
- **实时性**：基于最新文档内容
- **碎片化**：每次只检索部分相关片段

## 与 CAG 对比
与 [[concepts/cag]] 相比：
- RAG：考试时翻书找答案，每次都是临时的
- CAG：先把书读薄，内化成自己的知识体系，再回答问题

## References
- [[concepts/cag]]
- [[concepts/llm-wiki]]