---
title: "Agent Skills（官方文档）"
type: source
tags: [agent, skills, claude, anthropic, context]
sources: [Agent Skills.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
Agent Skills 是模块化能力，扩展 Claude 的功能。每个 Skill 将指令、元数据和可选资源（脚本、模板）打包，Claude 在相关时自动使用。

### 为什么使用 Skills
- **专业化 Claude**：为特定领域任务定制能力
- **减少重复**：创建一次，自动使用
- **组合能力**：组合 Skills 构建复杂工作流

### 渐进式披露架构
基于文件系统的架构实现渐进式披露：Claude 分阶段按需加载信息，而非预先消耗上下文。

- **Level 1: Metadata**：始终加载（启动时），每个 Skill 约 100 tokens，包含 YAML frontmatter 中的 name 和 description
- **Level 2: Instructions**：触发时加载，SKILL.md 主体，最多 5k tokens
- **Level 3+: Resources**：按需加载，effectively unlimited，通过 bash 执行脚本，代码从不进入上下文

### 可用预构建 Skills
- PowerPoint (pptx)：创建演示文稿、编辑幻灯片
- Excel (xlsx)：创建电子表格、分析数据、生成报告
- Word (docx)：创建文档、编辑内容
- PDF (pdf)：生成格式化的 PDF 文档和报告

### 安全考虑
强烈建议仅使用来自可信来源的 Skills（自己创建或来自 Anthropic）。恶意 Skill 可能导致数据泄露、未授权系统访问等安全风险。使用前需彻底审计。

## References
- [[concepts/agent-skills]]
- [[entities/anthropic]]
- [[sources/agent-skills-overview]]