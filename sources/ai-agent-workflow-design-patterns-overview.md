---
title: "AI Agent Workflow Design Patterns — An Overview"
type: source
tags: [agent, workflow, design-patterns, react, planning]
sources: [AI Agent Workflow Design Patterns — An Overview.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
本文系统梳理了 AI Agent 工作流设计模式，分为两大类别：**Reflection-focused（反思驱动）** 和 **Planning-focused（规划驱动）**。

### Reflection-focused（反思驱动）
- **Basic Reflection**：生成器与反思器之间的反馈循环，学生完成作业，老师提供反馈，学生根据反馈修订，循环直到满意。
- **Reflexion**：在基础反思上引入强化学习，通过语言反馈而非环境奖励来改进下一步行为。
- **Tree search (LATS)**：结合 TOT（Tree of Thoughts）与强化学习的反思。
- **Self-Discover**：在任务内部进行推理，反思任务本身的组成部分。

### Planning-focused（规划驱动）
- **Plan & Solve**：先计划再执行，Plan → Task list → RePlan，适合需要全局思考的任务。
- **LLM Compiler**：生成任务的有向无环图（DAG），自动并行执行依赖已满足的任务，显著提升效率（论文宣称3.6倍）。
- **REWOO**：Plan（包含依赖）→ Action（依赖前一步输出），解决变量传递问题，提高 Token 效率。
- **Storm**：搜索大纲 → 搜索大纲中每个主题 → 汇总为长文，适合 Wikipedia 风格的写作任务。

### 核心模式详解
- **ReAct Pattern**：核心是 Thought → Action → Observation 的交错循环。不同于 CoT 仅依赖内部知识，ReAct 将推理与外部世界反馈结合，有效减少幻觉。与纯 CoT 的区别在于每步都与现实环境核对。
- **Plan and Solve Pattern**：先规划后执行，Planner 生成多步骤计划，Replanner 根据当前进度调整计划。牺牲 ReAct 的实时适应性，换取更高执行效率。

## References
- [[concepts/react]]
- [[concepts/agent]]
- [[sources/ai-agent-主流设计模式]]