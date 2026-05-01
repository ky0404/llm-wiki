---
title: lint（健康检查）
type: concept
tags: [操作, 维护, 质量]
sources: [llm-wiki-核心思想.md]
created: 2026-04-28
updated: 2026-04-28
---

# lint（健康检查）

lint 是 [[concepts/llm-wiki]] 系统的关键操作之一，指对知识库进行健康检查和维护。

## 检查内容
1. **孤立页面**：没有被其他页面引用的页面
2. **断裂的 wikilinks**：引用了不存在的页面
3. **缺少 frontmatter**：不符合格式规范的页面
4. **未处理的 raw 文件**：raw/ 中未被处理的文件

## 作用
- 维护知识库的结构完整性
- 发现并修复问题
- 确保知识体系的一致性和可用性

## References
- [[concepts/llm-wiki]]
- [[ingest]]
- [[query]]