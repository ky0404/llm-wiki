---
title: Python AI Agent 学习路径
type: guide
tags: [python, ai-agent, learning-path]
created: 2026-05-27
updated: 2026-05-27
prerequisites:
  - Python 基础
  - 面向对象编程
---

# Python AI Agent 学习路径

> 专为AI/大模型应用开发设计的Python学习路径

## 阶段一：Python 基础夯实

### 1.1 核心语法
- [x] 变量与数据类型
- [x] 条件语句与循环
- [x] 函数定义与参数
- [ ] 装饰器 @decorator
- [ ] 上下文管理器 with

### 1.2 面向对象
- [ ] 类与对象
- [ ] 继承与多态
- [ ] 魔术方法 __init__/__str__/__
- [ ] 抽象基类 ABC

### 1.3 异步编程（重要！）
- [ ] asyncio 基础
- [ ] async/await 语法
- [ ] 并发任务管理

**推荐资源**：
- `raw/Python-100-Days/` 目录
- [Python 官方文档](https://docs.python.org/3/)

---

## 阶段二：AI/大模型入门

### 2.1 API 调用
- [ ] OpenAI API (GPT-4/GPT-3.5)
- [ ] Anthropic API (Claude)
- [ ] 环境变量管理 .env

### 2.2 LangChain 基础
- [ ] LLM Chain
- [ ] Prompt Template
- [ ] Output Parser
- [ ] Chat Model

**推荐资源**：
- `wiki/sources/langchain-*.md`
- [LangChain 官方文档](https://python.langchain.com/)

---

## 阶段三：AI Agent 开发

### 3.1 Agent 核心概念
- [ ] ReAct 模式
- [ ] Tool Use (函数调用)
- [ ] Memory (短期/长期记忆)
- [ ] Planning (任务规划)

### 3.2 框架学习路径

```python
# 推荐学习顺序

# 阶段3.2.1: LangChain Agents
from langchain.agents import load_agent

# 阶段3.2.2: CrewAI (多Agent协作)
from crewai import Agent, Task, Crew

# 阶段3.2.3: AutoGen (微软多Agent框架)
from autogen import ConversableAgent
```

### 3.3 实战项目
- [ ] 个人助手 Agent
- [ ] RAG 问答系统
- [ ] 多Agent协作系统

**推荐资源**：
- `wiki/my-learning-path/theory/awesome-ai-agents.md`
- [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)

---

## 阶段四：项目实战

### 4.1 自主项目
- [ ] `wiki/my-learning-path/practice/code-graph-agent/` - 代码图谱Agent
- [ ] `wiki/my-learning-path/practice/open-source-doc-agent/` - 开源文档Agent

### 4.2 面试准备
- [ ] 手写 Agent 核心逻辑
- [ ] ReAct 模式实现
- [ ] Memory 管理方案

---

## 核心技能清单

| 技能 | 优先级 | 掌握程度 |
|------|--------|----------|
| Python 异步编程 | ⭐⭐⭐⭐⭐ | [ ] |
| LangChain | ⭐⭐⭐⭐⭐ | [ ] |
| CrewAI | ⭐⭐⭐⭐ | [ ] |
| AutoGen | ⭐⭐⭐⭐ | [ ] |
| FastAPI | ⭐⭐⭐⭐ | [ ] |
| RAG (检索增强生成) | ⭐⭐⭐⭐⭐ | [ ] |

---

## 每日学习任务

```
Day 1-7:   Python 异步 + LangChain 基础
Day 8-14:  LangChain Agent + Tool Use
Day 15-21: CrewAI 多Agent协作
Day 22-28: AutoGen 深度定制
Day 29-35: RAG 实战项目
Day 36-42: 面试准备 + 项目复盘
```

---

## 学习资源汇总

### 在线教程
- [LangChain Academy](https://academy.langchain.com/)
- [DeepLearning.AI AI Agent Course](https://www.deeplearning.ai/)

### 书籍
- 《Python编程：从入门到实践》
- 《利用Python进行数据分析》

### 实践平台
- [Replit](https://replit.com/) - 在线运行Python
- [Colab](https://colab.research.google.com/) - 免费GPU