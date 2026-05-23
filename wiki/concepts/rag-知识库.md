---
title: RAG 知识库
type: concept
tags: [concept, rag, knowledge-base]
created: 2026-05-01
updated: 2026-05-01
---

# RAG 知识库

检索增强生成（Retrieval-Augmented Generation）是将外部知识检索与大模型生成结合的技术架构。

## 核心概念

- [[wiki/sources/高级-RAG-技术学习笔记.md|高级 RAG 技术]]
- [[wiki/sources/使用-Embedding-技术打造本地知识库助手.md|Embedding 知识库]]
- [[wiki/sources/基于结构化数据的文档问答.md|结构化数据问答]]

## 技术要点

1. **向量检索**：将文本转为向量，实现语义匹配
2. **块优化**：分块策略、 overlaps、层次索引
3. **Reranking**：相关性重排序
4. **多路召回**：关键词 + 向量 + 混合搜索

## 相关论文

- [[wiki/sources/2005.11401-rag.md|RAG 论文]]

## 工具生态

- Chroma、Weaviate、Pinecone
- LangChain RAG 模块
- LlamaIndex