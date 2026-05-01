---
title: "Equipping agents for the real world with Agent Skills"
type: source
tags: [agent, skills, anthropic, context-engineering]
sources: [Equipping agents for the real world with Agent Skills.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
Anthropic 提出了 **Agent Skills** 的概念，这是一种将领域专业知识打包成可组合、可移植资源的方式，使通用智能体能够转变为 specialized agents。
- **Skills 的本质**：包含指令、脚本和资源的文件夹，智能体可以动态发现并加载它们以更好地执行特定任务。核心文件是 `SKILL.md`，以 YAML frontmatter 开始，包含 `name` 和 `description`。
- **渐进式披露 (Progressive Disclosure)**：这是 Skills 的核心设计原则。
  - 第一级：启动时预加载每个已安装技能的 `name` 和 `description` 到系统提示中。
  - 第二级：当 Claude 认为某个技能与当前任务相关时，读取完整的 `SKILL.md`。
  - 第三级及以后：技能可以捆绑额外的文件（如 `reference.md`、`forms.md`），仅在需要时按需加载。
- **Skills 与上下文窗口**：技能不需要将所有内容读入上下文窗口，因此技能可以捆绑的上下文量实际上是无限的。
- **Skills 与代码执行**：技能可以包含供 Claude 执行的代码作为工具。某些操作（如排序列表）用代码执行比用 token 生成更高效且更具确定性。
- **开发与评估指南**：
  - 从评估开始，识别智能体能力的差距。
  - 当 `SKILL.md` 变得臃肿时，将内容拆分到单独的文件中。
  - 从 Claude 的角度思考，监控其实际使用情况并迭代。
  - 与 Claude 一起迭代，让其将成功方法和常见错误捕获到可重用的上下文中。
- **安全考虑**：仅安装来自可信源的技能。安装来自不太可信源的技能时，使用前需彻底审计。

## References
- [[concepts/上下文工程]]
- [[entities/anthropic]]
- [[concepts/agent-skills]]
- [[sources/工程技术-在智能体优先的世界中利用-codex]]
