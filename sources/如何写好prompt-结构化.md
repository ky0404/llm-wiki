---
title: "如何写好 Prompt：结构化"
type: source
tags: [prompt-engineering, structure, best-practices]
sources: [如何写好Prompt 结构化.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
本文介绍了结构化 Prompt 的设计理念和常用模块。
- **什么是结构化**：对信息进行组织，使其遵循特定的模式和规则，从而方便有效理解信息。
- **结构化 Prompt 的常用模块**：
  - **Role（角色）**：指定角色让模型聚焦在对应领域进行信息输出。
  - **Profile**：作者、版本、描述等元数据。
  - **Goals**：一句话描述 Prompt 目标，聚焦 Attention。
  - **Constrains（限制条件）**：帮助模型进行剪枝，减少不必要分支的计算。
  - **Skills（技能项）**：强化对应领域的信息权重。
  - **Workflow（工作流）**：重点，指定模型按什么方式进行对话和输出。
  - **Initialization（初始化）**：冷启动时的对白，强调需注意的重点。
- **示例**：文章提供了一个“知识探索专家”的完整结构化 Prompt 示例，包含角色定义、目标、限制条件、技能和工作流。工作流按“它从哪里来？”、“它是什么？”、“它到哪里去？”三个框架展开，并通过分隔符、序号、缩进等进行排版美化。

## References
- [[concepts/提示词工程]]
- [[sources/elements-of-a-prompt]]
