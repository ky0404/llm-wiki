---
title: awesome-ai-agents 资源清单
type: note
tags: [resource, ai-agent, awesome]
created: 2026-05-27
updated: 2026-05-27
---

# awesome-ai-agents 资源清单

> 来源: https://github.com/e2b-dev/awesome-ai-agents
> Stars: 28k | Forks: 2.9k

## 简介

AI 自主智能体 (Autonomous Agents) 精选列表，由 e2b-dev 维护。

## 核心主题

- python, agent, ai
- openai, gpt, gpt-4
- autogpt, babyagi, gpt-engineer
- autonomous-agents

## 适用场景

- 了解 AI Agent 生态
- 寻找开源 Agent 项目
- 学习 Agent 设计模式

## 相关链接

- [GitHub 仓库](https://github.com/e2b-dev/awesome-ai-agents)
- [e2b.dev docs](https://e2b.dev/docs)

## 学习笔记

### 一、核心框架（推荐学习）

| 框架 | 语言 | 特点 | 推荐度 |
|------|------|------|--------|
| **CrewAI** | Python | 多Agent编排，基于LangChain，角色扮演 | ⭐⭐⭐⭐⭐ |
| **AutoGen** | Python | 微软开源，多Agent对话框架 | ⭐⭐⭐⭐⭐ |
| **LangChain** | Python | Agent底层框架，生态丰富 | ⭐⭐⭐⭐ |
| **LangGraph** | Python | LangChain升级版，状态机编排 | ⭐⭐⭐⭐ |

### 二、经典项目系列

#### BabyAGI 系列（学习Agent基础）
- **BabyAGI** (~300行) - 任务驱动的自主Agent原型
- **BabyBeeAGI** - 复杂任务管理
- **BabyDeerAGI** - 并行任务，GPT-3.5可用
- **BabyElfAGI** - 支持自定义技能

#### Coding Agent
- **Aider** - 命令行代码编辑工具
- **Devika** - 开源AI软件工程师（对标Devin）
- **Devon** - Devin开源替代
- **ChatDev** - 多Agent软件公司模拟

### 三、学习路径建议

```
1. 入门：LangChain 基础（Tools、Agent、Memory）
2. 进阶：CrewAI（多Agent协作、角色定义）
3. 深入：AutoGen（多Agent对话、工具集成）
4. 实战：基于BabyAGI定制自己的Agent
```

### 四、Python 项目快速启动

```python
# CrewAI 最小示例
from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="研究AI最新进展")
task = Task(description="调研2024年AI Agent发展", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

### 五、关键概念

- **ReAct** - 推理+行动模式
- **Tool Use** - Agent调用外部工具
- **Memory** - 短期/长期记忆
- **Multi-agent** - 多Agent协作
- **SOP** - 标准操作流程

## 相关资源

- [awesome-sdks-for-ai-agents](https://github.com/e2b-dev/awesome-sdks-for-ai-agents)
- [E2B Code Interpreter](https://e2b.dev/docs)