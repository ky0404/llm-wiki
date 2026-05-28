---
title: "AI Agent 主流的设计模式（ReAct, Reflection, LATS）"
type: source
tags: [agent, design-patterns, react, reflection, lats, planning]
sources: [AI Agent 主流的设计模式（ReAct,Reflection,LATS）其实没有很复杂。.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
本文以通俗易懂的方式介绍了 AI Agent 的主流设计模式。

### 规划类模式
- **ReAct (Reasoning and Acting)**：思想-行动-观察（Thought-Action-Observation）交错循环，核心是将推理与外部世界紧密结合，显著提升答案准确性。与 CoT 的本质区别在于将每步与现实反馈核对，有效减少幻觉。缺点是每次工具调用都需要 LLM 推理，速度慢且 Token 消耗高。
- **Plan & Execute**：将工作流分为"规划"和"执行"两个独立阶段。规划阶段由强大的 LLM 生成详细多步骤计划，执行阶段由轻量级模型逐个完成步骤。牺牲灵活性换取更高效率。
- **REWOO (Reasoning Without Observation)**：Plan & Execute 的高效变体，Planner 一次性生成包含变量占位符的完整计划，Worker 根据计划执行，Solver 汇总结果。引入变量避免重复调用 LLM 进行数据传递。
- **LLM Compiler**：生成任务的有向无环图（DAG），自动并行执行所有依赖已满足的任务，实现最大并发执行。

### 反思类模式
- **Basic Reflection**：任务完成后显式要求 LLM 对输出进行"反思"和"批判"，利用元认知能力进行自我纠正。
- **Reflexion**：将"语言反馈"作为强化学习的替代品，通过跨试验的试错学习不断改进。利用"评估器"判断行动轨迹成败，"反思器"生成文本化反思作为"动态记忆"存储。
- **LATS (Language Agent Tree Search)**：集大成者，将 LLM 与蒙特卡洛树搜索（MCTS）结合，同时探索多条路径并进行深度决策。结合 ReAct 的行动能力、Reflexion 的反思反馈和树状搜索的规划优势。

### 总结
- **效率优化路线**：ReAct → Plan & Execute / REWOO → LLM Compiler（核心优化 Token 消耗和执行速度）
- **反思增强路线**：ReAct → Basic Reflection → Reflexion → LATS（核心减少幻觉和探索更优路径）
- 设计模式的核心：**获取真实环境反馈以监督和避免模型幻觉**

## References
- [[wiki/concepts/agent-智能体]]
- [[wiki/concepts/agent-智能体]]
- [[wiki/sources/ai-agent-workflow-design-patterns-overview]]