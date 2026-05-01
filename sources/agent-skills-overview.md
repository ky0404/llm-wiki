---
title: "Agent Skills Overview"
type: source
tags: [agent, skills, open-standard, anthropic]
sources: [Agent Skills Overview.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
Agent Skills 是一个轻量级、开放格式的规范，用于为 AI 智能体扩展专业能力和工作流。

### 什么是 Agent Skills
一个技能（Skill）是一个文件夹，包含 `SKILL.md` 文件。该文件包含元数据（`name` 和 `description` 至少需要）以及告诉智能体如何执行特定任务的指令。技能还可以捆绑脚本、参考资料、模板和其他资源。

### 为什么使用 Agent Skills
智能体日益强大，但往往缺乏完成实际工作所需的上下文。技能通过将程序性知识和特定于公司、团队和用户的上下文打包成可移植的版本控制文件夹来解决这个问题，智能体按需加载。这赋予智能体：
- **领域专业知识**：将专业知识捕获为可重用指令和资源
- **可重复的工作流**：将多步骤任务转换为一致、可审计的流程
- **跨产品复用**：构建一次即可在任何支持技能的智能体上使用

### 工作原理
智能体通过**渐进式披露**分三个阶段加载技能：
1. **Discovery（发现）**：启动时，智能体仅加载每个可用技能的名称和描述，足以知道何时可能相关
2. **Activation（激活）**：当任务匹配技能的描述时，智能体将完整的 `SKILL.md` 指令读入上下文
3. **Execution（执行）**：智能体按照指令执行，可选择执行捆绑的代码或按需加载引用的文件

由于完整指令仅在任务需要时加载，智能体可以保留许多技能而仅占用很小的上下文空间。

### 开放开发
Agent Skills 格式最初由 Anthropic 开发，作为开放标准发布，已被越来越多的智能体产品采用。该标准欢迎来自更广泛生态系统的贡献。

## References
- [[concepts/agent-skills]]
- [[entities/anthropic]]
- [[sources/equipping-agents-for-the-real-world-with-agent-skills]]