---
title: query（查询）
type: concept
tags: [操作, 知识管理]
sources: [llm-wiki-核心思想.md]
created: 2026-04-28
updated: 2026-04-28
---

# query（查询）

query 是 [[wiki/concepts/llm-wiki]] 系统的关键操作之一，指从知识库中检索和回答问题。

## 流程
1. 用户提出问题
2. AI 读取 wiki/index.md 定位相关页面
3. AI 读取相关页面内容
4. 基于已编译的知识体系综合回答
5. 明确引用来源页面

## 特点
- 基于已编译的知识结构
- 避免临场拼凑
- 保证回答的一致性和准确性

## References
- [[wiki/concepts/llm-wiki]]
- [[wiki/concepts/ingest]]
- [[wiki/concepts/lint]]