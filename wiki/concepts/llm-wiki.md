---
title: LLM Wiki
type: concept
tags: [wiki, 知识管理, 方法论]
sources: [llm-wiki-核心思想.md, llm-wiki.md]
created: 2026-04-28
updated: 2026-04-29
---

# LLM Wiki

LLM Wiki 是一种基于编译增强生成（CAG）的知识管理系统，由 Karpathy 方法论提出。

## 核心理念
区别于传统的 [[wiki/concepts/rag]]（检索增强生成），LLM Wiki 采用 [[wiki/concepts/cag]]（编译增强生成）方法：
- RAG：考试时翻书找答案，每次都是临时的
- LLM Wiki：先把书读薄，内化成自己的知识体系，再回答问题

## 架构
采用三层结构：
1. **Raw（源材料）**：原始文档，只读，不可变
2. **Wiki（已编译知识）**：结构化、带链接的 Markdown 文件集合
3. **Schema（规则）**：配置文件（如 [[AGENTS]]），定义 AI 的工作方式

## 操作
- [[wiki/concepts/ingest]]：摄入新素材
- [[wiki/concepts/query]]：查询知识库
- [[wiki/concepts/lint]]：健康检查

## 优势
知识被提前编译和链接，所有交叉引用、矛盾标注、摘要综合都已经完成，AI 回答时不需要每次都在混乱的碎片里检索拼凑。

## 历史渊源
LLM Wiki 在精神上与 [[wiki/entities/vannevar-bush]] 的 Memex（1945）概念相关——一个私人的、精心策划的知识存储，文档之间有联想路径。Bush 的愿景更接近这个，而不是网络变成的样子：私人的、积极策划的，文档之间的连接与文档本身一样有价值。他无法解决的部分是谁来做维护工作。LLM 处理这一点。

## 推荐工具
- [[wiki/entities/obsidian]]：作为 wiki 的 Obsidian Vault，提供图形视图和双向链接
- [[wiki/entities/marp]]：基于 markdown 的幻灯片格式，用于演示
- [[wiki/entities/dataview]]：在页面 frontmatter 上运行查询的 Obsidian 插件
- [[wiki/entities/qmd]]：本地 markdown 文件搜索引擎，具有混合 BM25/向量搜索

## References
- [[wiki/concepts/cag]]
- [[wiki/concepts/rag]]
- [[wiki/concepts/ingest]]
- [[wiki/concepts/query]]
- [[wiki/concepts/lint]]
- [[wiki/entities/vannevar-bush]]
- [[wiki/entities/obsidian]]
- [[wiki/entities/marp]]
- [[wiki/entities/dataview]]