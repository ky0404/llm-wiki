---
title: LLM Wiki 核心理念
type: source
tags: [方法论, wiki, karpathy]
sources: [llm-wiki-核心思想.md]
created: 2026-04-29
updated: 2026-04-29
---

# LLM Wiki 核心理念

## 核心区别：RAG vs CAG

不是 RAG（检索增强生成），而是 **CAG（编译增强生成）**。
- RAG 是考试时翻书找答案，每次都是临时的
- LLM Wiki 是先把书读薄，内化成自己的知识体系，再回答问题

## 三层架构

1. **Raw（源材料）**：原始文档，只读，不可变
2. **Wiki（已编译知识）**：结构化、带链接的 Markdown 文件
3. **Schema（规则）**：配置文件（如 AGENTS.md）

## 关键操作

- **Ingest（摄入）**：读取源文件，写出 Wiki 摘要，更新索引
- **Query（查询）**：读 index.md，定位具体 Wiki 页，综合回答
- **Lint（健康检查）**：检查矛盾、过时信息、孤立页面

## 优势

知识被提前编译和链接，交叉引用、矛盾标注、摘要综合都已完成。知识是**生长**出来的，不是**临场拼凑**的。

## References


- [[entities/andrej-karpathy]]