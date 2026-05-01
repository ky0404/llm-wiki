---
title: 高级 RAG 技术学习笔记
type: source
tags: [rag, llamaindex, knowledge-base]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

本文深入探讨高级 RAG（检索增强生成）技术，包括朴素 RAG、高级 RAG 和模块化 RAG 三种范式演变，以及开发 RAG 系统面临的 12 个痛点与解决方案。文章结合 LangChain 和 LlamaIndex 框架进行实战演示，涵盖索引优化、查询优化、查询转换、重排序、上下文压缩等核心技巧。

## 核心要点

- RAG 本质是搜索 + LLM 提示，通过外部数据库获取知识弥补大模型信息差
- 高级 RAG 引入预检索和后检索过程，提升检索质量
- 12 个 RAG 痛点包括：缺失内容、排名遗漏、格式错误、安全性等
- LlamaIndex 将 RAG 分为加载、索引、存储、查询、评估五个阶段
- 查询转换技术包括查询重写、查询扩展、多查询等方法

## 关键数据

- 向量数据库初创公司：Chroma、Weaviate、Pinecone
- 7 个失败点 + 5 个扩展痛点 = 12 个 RAG 痛点

## References

- [[concepts/检索增强生成]]
- [[concepts/transformer]]
- [[concepts/参数高效微调]]