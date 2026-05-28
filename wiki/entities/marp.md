---
title: Marp
type: entity
tags: [tool, presentation, markdown]
sources: [llm-wiki.md]
created: 2026-04-29
updated: 2026-04-29
---

# Marp

## 描述
Marp（Markdown Presentation Ecosystem）是一个基于 Markdown 的幻灯片制作工具，允许用户使用 Markdown 语法创建演示文稿。

## 属性
- **类型**：演示文稿工具
- **格式**：基于 Markdown
- **集成**：有 Obsidian 插件支持
- **用途**：直接从 wiki 内容生成演示文稿

## 在 LLM Wiki 系统中的作用
### 演示生成
- **内容复用**：可以直接从 wiki 页面生成幻灯片
- **格式统一**：使用相同的 Markdown 语法
- **自动化**：LLM 可以自动从知识库生成演示文稿

### Obsidian 集成
- **插件支持**：Obsidian 有专门的 Marp 插件
- **工作流程**：在 Obsidian 中编辑，用 Marp 渲染
- **实时预览**：编辑时实时查看幻灯片效果

## 优势
1. **简单性**：使用熟悉的 Markdown 语法
2. **一致性**：与 wiki 使用相同的格式
3. **自动化**：可以脚本化生成演示文稿
4. **版本控制**：幻灯片作为 Markdown 文件，可以用 git 管理

## 使用场景
1. **知识分享**：从 wiki 内容生成培训材料
2. **报告生成**：自动生成项目进度报告
3. **会议演示**：快速创建会议演示文稿
4. **教育材料**：从学习笔记生成教学幻灯片

## 与 LLM Wiki 的集成
在 [[wiki/concepts/llm-wiki]] 工作流中：
1. **内容来源**：从 wiki 页面提取关键信息
2. **幻灯片生成**：使用 Marp 格式组织内容
3. **样式定制**：应用主题和布局
4. **输出格式**：生成 PDF、HTML 或直接演示

## References
- [[wiki/entities/obsidian]] - Marp 的集成平台
- [[wiki/concepts/llm-wiki]] - 内容来源系统
- [[wiki/concepts/wikilinks]] - Markdown 链接基础