---
title: Dataview
type: entity
tags: [tool, plugin, obsidian, query]
sources: [llm-wiki.md]
created: 2026-04-29
updated: 2026-04-29
---

# Dataview

## 描述
Dataview 是一个 Obsidian 插件，允许用户在 Markdown 文件的 YAML frontmatter 上运行查询，生成动态表格、列表和视图。

## 属性
- **类型**：Obsidian 插件
- **功能**：数据查询和可视化
- **查询语言**：类似 SQL 的查询语法
- **数据源**：Markdown 文件的 frontmatter

## 在 LLM Wiki 系统中的作用
### 数据查询
- **动态视图**：根据 frontmatter 元数据生成表格和列表
- **过滤排序**：按标签、日期、类型等过滤和排序页面
- **聚合统计**：计算页面数量、标签分布等统计信息

### 与 LLM 集成
如果 [[wiki/concepts/llm]] 为 wiki 页面添加 YAML frontmatter（如标签、日期、源计数），Dataview 可以：
1. **自动分类**：按类型、标签等组织页面
2. **时间线视图**：按创建/更新时间显示页面
3. **关系图谱**：显示页面间的连接关系
4. **统计报表**：生成知识库的统计信息

## 示例查询
```dataview
TABLE title, type, tags, created
FROM "wiki/concepts"
WHERE contains(type, "concept")
SORT created DESC
```

## 优势
1. **自动化**：减少手动维护目录的工作
2. **动态性**：内容更新时视图自动更新
3. **灵活性**：支持复杂的查询和过滤
4. **可视化**：以表格、列表、日历等形式展示数据

## 使用场景
1. **目录生成**：自动生成按类别组织的页面列表
2. **进度跟踪**：显示最近更新或创建的页面
3. **标签管理**：查看标签使用情况和分布
4. **知识图谱**：可视化页面间的关系

## 与 LLM Wiki 的集成
在 [[wiki/concepts/llm-wiki]] 架构中：
1. **元数据标准化**：LLM 为每个页面添加一致的 frontmatter
2. **自动查询**：Dataview 根据元数据生成动态视图
3. **实时更新**：当 LLM 更新页面时，Dataview 视图自动更新
4. **洞察发现**：通过查询发现知识库中的模式和关系

## References
- [[wiki/entities/obsidian]] - Dataview 的运行平台
- [[wiki/concepts/llm-wiki]] - 应用 Dataview 的知识管理系统
- [[wiki/concepts/wikilinks]] - frontmatter 查询的链接基础