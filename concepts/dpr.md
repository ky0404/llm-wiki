---
title: DPR
type: concept
tags: [检索, 密集检索]
sources: [2005.11401v4.md]
created: 2026-04-29
updated: 2026-04-29
---

# Dense Passage Retrieval (DPR)

## 定义

使用密集向量表示的检索方法，基于双编码器架构。

## 架构

- **Query Encoder**：BERT 将查询编码为密集向量
- **Document Encoder**：BERT 将文档编码为密集向量
- 相似度：内积 `d(z)·q(x)`

## 与稀疏检索对比

| 方法 | 语义理解 | 实现复杂度 |
| --- | --- | --- |
| BM25 | 无 | 低 |
| DPR | 有 | 中 |

## References

- [[entities/facebook-ai-research]]
- [[synthesis/dpr-industrial-adoption]] - DPR 工业应用与落地实践