---
title: Obsidian
type: entity
tags: [tool, note-taking, knowledge-management, markdown]
sources: [llm-wiki.md]
created: 2026-04-29
updated: 2026-04-29
---

# Obsidian

## 描述
Obsidian 是一款基于 Markdown 的知识管理和笔记应用，使用本地文件存储，支持双向链接、图形视图和丰富的插件生态系统。在 [[wiki/concepts/llm-wiki]] 系统中，Obsidian 被用作"IDE"，而 LLM 是"程序员"。

## 属性
- **类型**：知识管理工具、笔记应用
- **存储方式**：本地 Markdown 文件
- **核心特性**：双向链接、图形视图、插件系统
- **在 LLM Wiki 中的角色**：Wiki 的查看和浏览界面

## 在 LLM Wiki 系统中的作用
### 作为 IDE
- **比喻**：Obsidian 是 IDE，LLM 是程序员，wiki 是代码库
- **工作流程**：LLM 根据对话进行编辑，用户在 Obsidian 中实时浏览结果

### 关键功能
1. **图形视图**：查看 wiki 形状的最佳方式，显示页面连接关系、枢纽页面和孤立页面
2. **双向链接**：支持 [[wiki/concepts/wikilinks]] 格式，实现页面间的交叉引用
3. **本地存储**：所有文件存储在本地，便于版本控制（git）
4. **插件生态**：丰富的插件支持扩展功能

## 推荐插件
### Marp
- **功能**：基于 Markdown 的幻灯片格式
- **用途**：直接从 wiki 内容生成演示文稿
- **Obsidian 集成**：有专门的 Obsidian 插件

### Dataview
- **功能**：在页面 frontmatter 上运行查询
- **用途**：如果 LLM 为 wiki 页面添加 YAML frontmatter（标签、日期、源计数），Dataview 可以生成动态表格和列表

## 实用技巧
### Obsidian Web Clipper
- **功能**：浏览器扩展，将网页文章转换为 Markdown
- **用途**：快速将源材料获取到原始集合中

### 图像处理
1. **设置附件文件夹**：在 Obsidian 设置 → 文件和链接中，设置"附件文件夹路径"为固定目录（如 `raw/assets/`）
2. **下载热键**：在设置 → 热键中，搜索"Download"找到"为当前文件下载附件"并绑定热键（如 Ctrl+Shift+D）
3. **工作流程**：剪辑文章后，按热键将所有图像下载到本地磁盘

### 图像处理注意事项
- **LLM 限制**：LLM 无法原生一次性读取带有内联图像的 markdown
- **解决方法**：让 LLM 先读取文本，然后单独查看部分或所有引用的图像以获得额外上下文

## 优势
1. **本地优先**：所有数据存储在本地，隐私和安全有保障
2. **互操作性**：使用标准 Markdown 文件，易于与其他工具集成
3. **可视化**：图形视图提供 wiki 结构的直观展示
4. **可扩展性**：丰富的插件生态系统
5. **版本控制友好**：纯文本文件便于 git 管理

## 与 LLM Wiki 的集成
在 [[wiki/concepts/llm-wiki]] 架构中：
1. **原始源** → 存储在 `raw/` 目录中
2. **Wiki** → 存储在 `wiki/` 目录中，Obsidian 作为查看器
3. **模式** → 存储在 `wiki/AGENTS.md` 中，指导 LLM 操作

## References
- [[wiki/concepts/llm-wiki]] - 使用 Obsidian 作为 IDE
- [[wiki/entities/marp]] - 推荐的幻灯片插件
- [[wiki/entities/dataview]] - 推荐的数据查询插件
- [[wiki/concepts/wikilinks]] - Obsidian 支持的双向链接格式