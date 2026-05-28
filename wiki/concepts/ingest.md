---
title: ingest（摄入）
type: concept
tags: [操作, 知识管理]
sources: [llm-wiki-核心思想.md]
created: 2026-04-28
updated: 2026-04-28
---

# ingest（摄入）

ingest 是 [[wiki/concepts/llm-wiki]] 系统的关键操作之一，指将新素材纳入知识库的过程。

## 流程
1. 将文件放入 raw/ 目录
2. AI 读取文件内容
3. 在 wiki/sources/ 创建摘要页
4. 识别概念和实体，创建或更新对应页面
5. 更新索引和交叉引用

## 作用
- 扩展知识库内容
- 建立新概念与现有知识的联系
- 维护知识体系的一致性

## References
- [[wiki/concepts/llm-wiki]]
- [[wiki/concepts/query]]
- [[wiki/concepts/lint]]