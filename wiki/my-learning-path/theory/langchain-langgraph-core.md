---
title: LangChain/LangGraph 核心知识点完整指南
type: theory
tags: [langchain, langgraph, ai-agent, framework, interview]
created: 2026-05-28
updated: 2026-05-28
---

> 本笔记整理自 LangChain 官方文档 (2025最新版)，结合你的项目经验，帮助你面试和工作中熟练运用 LangChain/LangGraph。

---

## 一、框架定位：三者关系辨析

| 层级 | 框架 | 定位 | 适用场景 |
|------|------|------|----------|
| **Deep Agents** | Deep Agents SDK | 开箱即用的 Agent | 需要快速上线，不需要太多定制 |
| **LangChain** | `create_agent` | 高度可配置的 Agent 框架 | 有定制需求，需要灵活组装 Model/Tools/Prompt |
| **LangGraph** | StateGraph | 底层编排框架 | 复杂工作流、状态机、多 Agent 协作 |

**核心公式：** `Agent = Model + Harness`

- **Harness（马具）**：模型周围的everything：prompt、tools、middleware
- **LangChain** 提供 `create_agent` 作为 Harness，用户只需关注 Model、Tools、System Prompt
- **LangGraph** 是 Harness 的底层实现，提供持久化、流式、人机交互等能力

**面试话术：** 
> "LangChain 是高层 Agent 框架，封装了常用的 Agent 模式；LangGraph 是底层状态机引擎，专注工作流编排。我的心理陪伴系统就是用 LangGraph 实现的 4 节点状态机（risk_detect → rag_retrieve → llm_generate → safety_check），生产环境运行 1840 条请求零故障。"

---

## 二、LangChain 核心 API

### 2.1 create_agent（推荐）

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-5.4",           # 模型标识符
    tools=[get_weather, search],       # 工具列表
    system_prompt="You are a helpful assistant"
)
```

**四大核心组件：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `model` | 模型标识符，格式 `"provider:model"` | `"openai:gpt-5.4"`, `"ollama:devstral-2"` |
| `tools` | 工具列表，支持函数/LangChain Tool | `@tool` 装饰器或 `Tool` 类 |
| `system_prompt` | 系统提示词 | 字符串或 `SystemMessage` |
| `response_format` | 结构化输出 | Pydantic 模型类 |

**支持的模型提供商：**
- OpenAI, Anthropic, Google (Gemini)
- Ollama (本地模型)
- OpenRouter, Fireworks, Baseten
- Azure OpenAI, AWS Bedrock, HuggingFace

### 2.2 工具定义（Tools）

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"
```

**工具类型：**
1. **Python 函数** → 自动转换为 Tool
2. **LangChain Tool 对象** → 手动定义
3. **Tool Dict** → 字典格式

### 2.3 调用 Agent

```python
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

# 带持久化的调用
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    checkpointer=InMemorySaver(),  # 开启对话历史
)

config = {"configurable": {"thread_id": str(uuid7())}}

# 首次对话
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config
)

# 后续对话（复用 thread_id，自动携带历史）
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config
)
```

**关键概念：**
- `thread_id`：会话ID，相同 ID 自动持久化对话历史
- `checkpointer`：持久化存储，支持内存（InMemorySaver）或数据库（PostgresSaver）
- `context`：每次调用的运行时上下文（用户ID、API Key等）

```python
from dataclasses import dataclass

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "hi"}]},
    config=config,
    context=Context(user_id="user-123")
)
```

### 2.4 流式输出（Streaming）

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Search AI news"}]},
    stream_mode="values"
):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
```

---

## 三、Middleware（中间件）系统

`create_agent` 的强大之处在于 **Middleware** 机制。每个 Middleware 负责一个关注点，自由组合。

### 3.1 Middleware 生态

| 类别 | Middleware | 功能 |
|------|------------|------|
| **执行环境** | `FilesystemMiddleware` | 虚拟文件系统 |
| **上下文管理** | `SummarizationMiddleware` | 历史摘要，防止上下文溢出 |
| | `MemoryMiddleware` | 长期记忆，加载持久化指令 |
| | `SkillsMiddleware` | 按需加载领域知识 |
| **规划与委托** | `TodoListMiddleware` | 任务清单 |
| | `SubAgentMiddleware` | 子 Agent 委托 |
| **容错** | `ModelRetryMiddleware` | 模型重试 |
| | `ToolRetryMiddleware` | 工具重试 |
| **Guardrails** | `PIIMiddleware` | PII 检测与脱敏 |
| **人机交互** | `HumanInTheLoopMiddleware` | 审批拦截 |

### 3.2 使用示例

```python
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware

agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(max_retries=2),
    ],
)
```

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[write_file],
    middleware=[
        HumanInTheLoopMiddleware(interrupt_on={"write_file": True})
    ],
)
```

**面试话术：**
> "我在项目中实现了类似 Middleware 的四级危机干预 SOP，通过关键词+LLM双重检测，在 Agent 输出前拦截高风险内容并强制插入心理援助热线，这本质上就是自定义的 Guardrails Middleware。"

---

## 四、LangGraph 底层架构

### 4.1 核心概念

LangGraph 是 **低层次编排框架**，专注：
- **持久化（Persistence）**：失败后可恢复，从断点继续
- **人机交互（Human-in-the-loop）**：任意节点可暂停等待审批
- **流式输出（Streaming）**：实时返回中间结果
- **记忆（Memory）**：短期工作记忆 + 长期会话记忆

### 4.1.1 Multi-Agent Supervisor 模式（新增）

> 官方库：[langgraph-supervisor-py](https://github.com/langchain-ai/langgraph-supervisor-py) (1.6k stars)

Supervisor 模式是**层级多智能体架构**，由一个中央 Supervisor 协调多个专业 Agent：

```
┌─────────────────────────────────────────┐
│           Supervisor                    │
│  (决策：调用哪个 Agent)                  │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌──────────┐
│Math   │ │Research│ │ Writing  │
│Expert │ │ Expert │ │  Agent   │
└───────┘ └───────┘ └──────────┘
```

**核心组件：**

| 组件 | 说明 |
|------|------|
| Supervisor | 中央协调 Agent，负责任务分发 |
| Worker Agents | 专业 Agent，各自负责特定领域 |
| Handoff Tools | Agent 间传递任务的工具 |

**快速示例：**

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

# 创建专业 Agent
math_agent = create_react_agent(
    model=model,
    tools=[add, multiply],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[web_search],
    name="research_expert",
    prompt="You are a world class researcher with access to web search."
)

# 创建 Supervisor 工作流
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt="You are a team supervisor managing research and math experts."
)

app = workflow.compile()
result = app.invoke({"messages": [{"role": "user", "content": "..."}]})
```

**消息历史管理模式：**

```python
# 完整历史（默认）
workflow = create_supervisor(agents, output_mode="full_history")

# 仅最后一条消息（节省 token）
workflow = create_supervisor(agents, output_mode="last_message")
```

**多层级 Supervisor：**

```python
# 二级 Supervisor
research_team = create_supervisor(
    [research_agent, math_agent],
    model=model,
    supervisor_name="research_supervisor"
).compile(name="research_team")

writing_team = create_supervisor(
    [writing_agent, publishing_agent],
    model=model,
    supervisor_name="writing_supervisor"
).compile(name="writing_team")

top_supervisor = create_supervisor(
    [research_team, writing_team],
    model=model,
    supervisor_name="top_level_supervisor"
)
```

**面试话术：**
> "我了解 langgraph-supervisor-py 的层级多智能体架构。Supervisor 模式适合任务可明确分组的场景，比如你的产品助手需要同时调用客服、推荐、风控多个 Agent。对于更复杂的场景，还可以组合 Supervisor 形成多层级架构。"

### 4.2 最小示例

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node("mock_llm", mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```

### 4.3 你的项目实战（YuanXinYeYu）

你的项目就是典型的 LangGraph 状态机应用：

```python
# 你的项目架构
graph = StateGraph(AgentState)

# 四节点线性流程
graph.add_node("risk_detect", risk_detection_node)
graph.add_node("rag_retrieve", rag_retrieval_node)
graph.add_node("llm_generate", llm_generation_node)
graph.add_node("safety_check", safety_check_node)

graph.add_edge(START, "risk_detect")
graph.add_edge("risk_detect", "rag_retrieve")
graph.add_edge("rag_retrieve", "llm_generate")
graph.add_edge("llm_generate", "safety_check")
graph.add_edge("safety_check", END)

graph = graph.compile()
```

**生产数据（1840条请求）：**
- 成功率：100%
- P50 延迟：4.75s
- 错误率：0%
- 双链路灰度验证（LangGraph vs 传统函数式）

### 4.4 State 与 Nodes

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    messages: list
    risk_level: str
    retrieved_docs: list
    final_response: str

def risk_node(state: AgentState) -> AgentState:
    # 检测风险级别
    risk = detect_risk(state["messages"][-1].content)
    return {"risk_level": risk}

def rag_node(state: AgentState) -> AgentState:
    # RAG 检索
    docs = retrieve(state["messages"][-1].content)
    return {"retrieved_docs": docs}

graph = StateGraph(AgentState)
graph.add_node("risk", risk_node)
graph.add_node("rag", rag_node)
graph.add_edge(START, "risk")
graph.add_edge("risk", "rag")
graph.add_edge("rag", END)
```

---

## 五、LangSmith 可观测性

### 5.1 核心功能

- **Tracing**：追踪每个 Agent 步骤
- **Evaluation**：评估输出质量
- **Prompts**：管理提示词版本
- **Deployment**：部署 Agent 到生产

### 5.2 快速集成

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"
```

### 5.3 你的项目实践

你的项目已经深度集成 Langfuse（类似 LangSmith）：

```python
# Langfuse 追踪统计（1840条请求）
Trace Breakdown:
├─ risk_detect spans: 1840 (100% coverage)
├─ rag_retrieve spans: 1840 (100% coverage)
│   ├─ route=vector: 60.3%
│   ├─ route=graph: 27.0%
│   └─ route=hybrid: 12.7%
├─ llm_generate spans: 1840 (100% coverage)
└─ safety_check spans: 1840 (100% coverage)
```

**面试话术：**
> "我在心理陪伴系统中实现了全链路可观测性，使用 Langfuse 追踪每个节点（risk_detect/rag_retrieve/llm_generate/safety_check），1840条请求全部可追溯，延迟 P50 4.75s，错误率 0%，这让我能快速定位问题并持续优化。"

---

## 六、面试高频问题汇总

### Q1: LangChain vs LangGraph 区别？

| 维度 | LangChain | LangGraph |
|------|-----------|-----------|
| 层级 | 高层抽象 | 底层引擎 |
| 适用 | 快速开发标准 Agent | 复杂工作流、状态机 |
| 持久化 | 需要手动配置 | 内置支持 |
| 控制力 | 中 | 高 |

**话术：** "我理解 LangChain 是封装好的 Agent 框架，适合快速开发；LangGraph 是底层状态机，适合需要精细控制复杂流程的场景。我的心理陪伴系统需要四级危机干预这种确定性流程，所以选用了 LangGraph。"

### Q2: Agent 的核心组成部分？

1. **Model**：大语言模型
2. **Tools**：Agent 可调用的外部能力
3. **Prompt**：指导模型行为的指令
4. **Harness**：环绕模型的框架（LangChain/LangGraph）
5. **Middleware**：可插拔的扩展机制

### Q3: 如何保证 Agent 可靠性？

1. **持久化**：LangGraph Checkpoint，失败后可恢复
2. **容错**：Middleware 重试机制
3. **Guardrails**：输出审核，内容过滤
4. **人机交互**：关键操作审批
5. **可观测性**：LangSmith 全链路追踪

### Q4: RAG 如何提升 Agent 能力？

RAG 是 Agent 的 **外部知识工具**，不是大脑。提升 Agent 能力的方式：

1. **多轮记忆**：`MemoryMiddleware` 或自定义 ConversationBuffer
2. **工具扩展**：增加更多 Tools
3. **推理链**：ReAct 模式，引入反思机制
4. **状态机**：LangGraph 条件分支，处理复杂流程

**话术：** "关于是否需要微调，我的观点：RAG 解决知识召回问题，微调改变说话风格。对于大学生心理陪伴场景，我们的 RAG 精准度已经达到 82%，危机识别准确率 98.2%，目前不需要微调。核心提升点在 Agent 推理能力和多轮对话一致性。"

### Q5: 你的项目为什么选 LangGraph？

1. **确定性流程**：四级危机干预需要精确控制
2. **可观测性**：每个节点都可追踪
3. **故障降级**：节点失败自动切换到旧链路
4. **生产验证**：1840条请求零故障

### Q6: 多智能体系统有哪些架构模式？

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **Supervisor** | 中央 Supervisor 协调多个 Worker | 任务可明确分组 |
| **Swarm** | Agent 间自由协作，去中心化 | 需要灵活协商 |
| **Plan-Execute** | 先规划再执行，Plan 指导整个流程 | 复杂任务需要全局视角 |
| **ReAct** | 推理+行动循环，边想边做 | 需要工具调用的任务 |

**话术：** "我了解 Supervisor 模式适合任务明确分组的场景，比如你的系统需要同时调用客服、推荐、风控多个 Agent。对于更动态的协作场景，可以用 Swarm 模式。我的心理陪伴系统因为需要精确的四级危机干预流程，选用 LangGraph 状态机更合适。"

### Q7: 如何设计 Agent 之间的通信？

1. **Tool-based Handoff**：通过调用工具转移控制权（Supervisor 模式）
2. **Shared State**：多个 Agent 读写共享状态
3. **Message Passing**：通过消息队列传递信息
4. **Graph Edge**：在 LangGraph 中通过边定义流向

**面试话术：** "在实际项目中，我倾向于用 Tool-based Handoff，因为这种方式的控制流清晰，便于追踪和调试。LangGraph 的 Supervisor 模式已经封装好了这套机制，使用起来很方便。"

### Q8: RAG 如何与 Agent 深度结合？

**核心理念：RAG 是 Agent 的"外部知识工具"，不是大脑。**

```python
# 你的项目架构：RAG 作为 Tool 嵌入 Agent 循环
@tool
def retrieve_knowledge(query: str) -> str:
    """检索心理陪伴知识库"""
    docs = hybrid_retrieval(query)  # Vector + Graph + BM25
    return format_docs(docs)

# Agent = Model + Tools(RAG)
agent = create_agent(
    model="openai:gpt-4o",
    tools=[retrieve_knowledge],
    system_prompt="你是心理陪伴助手，先检索知识库再回答"
)
```

**面试话术：** "在我的心理陪伴系统中，RAG 不是独立的模块，而是 Agent 的核心 Tool。用户的每条消息都会触发混合检索（向量60.3%+图谱27%+BM25 12.7%），召回的相关文档作为上下文送给 LLM 生成回答。这种设计的优势是：1）知识库可独立更新，不用重训模型；2）82%的精准度已经满足生产需求；3）危机识别模块可以优先干预，不需要等待 LLM 生成。"

---

## 六、Agent 设计模式全解析

### 6.1 ReAct (Reasoning and Acting)

**核心：Thought → Action → Observation 循环**

```
用户问题 → Think(分析) → Act(调用工具) → Observe(获取结果) → Think(分析结果) → ...
```

**原理：** 将推理与外部世界反馈紧密结合，每次工具调用都是一次"强化学习"。

```python
# LangGraph 实现 ReAct 模式
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class ReActState(TypedDict):
    messages: list
    reasoning: str
    action_result: str
    step: int

def reason_node(state: ReActState) -> ReActState:
    """Think: 分析问题，决定下一步行动"""
    last_msg = state["messages"][-1].content
    # LLM 决定要做什么
    reasoning = llm_reasoning(last_msg, state.get("action_result", ""))
    return {"reasoning": reasoning, "step": state["step"] + 1}

def action_node(state: ReActState) -> ReActState:
    """Act: 执行工具调用"""
    # 解析 reasoning 中的工具调用
    tool_name, tool_args = parse_tool_call(state["reasoning"])
    result = execute_tool(tool_name, tool_args)
    return {"action_result": result}

def observe_node(state: ReActState) -> ReActState:
    """Observe: 将结果加入上下文，检测是否完成"""
    # 判断任务是否完成
    is_done = check_completion(state["reasoning"], state["action_result"])
    return {"messages": state["messages"] + [AIMessage(content=state["action_result"])]}

graph = StateGraph(ReActState)
graph.add_node("reason", reason_node)
graph.add_node("action", action_node)
graph.add_node("observe", observe_node)
graph.add_edge(START, "reason")
graph.add_edge("reason", "action")
graph.add_edge("action", "observe")
# 条件边：完成则结束，否则回到 reason
graph.add_conditional_edges("observe", should_continue, {"continue": "reason", "end": END})
```

**优点：** 灵活、可实时调整、适合需要外部验证的任务
**缺点：** Token 消耗大、执行慢、可能陷入局部最优

**适用场景：** 需要查资料、调用 API、代码执行等需要外部反馈的任务

---

### 6.2 Plan & Execute

**核心：先规划，再执行（两阶段分离）**

```
用户问题 → Plan(一次性生成完整计划) → Execute(按计划执行) → 返回结果
```

**原理：** 将"智慧"(规划)与"体力"(执行)解耦，减少 LLM 调用次数。

```python
# Plan & Execute 模式
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List

class PlanExecuteState(TypedDict):
    messages: list
    plan: List[str]        # 计划步骤列表
    current_step: int      # 当前执行到第几步
    results: dict          # 各步骤执行结果

def planning_node(state: PlanExecuteState) -> PlanExecuteState:
    """Plan: 一次性生成完整计划"""
    user_query = state["messages"][-1].content
    plan = llm_generate_plan(user_query)  # 返回 ["步骤1", "步骤2", "步骤3"]
    return {"plan": plan, "current_step": 0, "results": {}}

def executing_node(state: PlanExecuteState) -> PlanExecuteState:
    """Execute: 执行当前步骤"""
    step = state["current_step"]
    plan = state["plan"]
    if step >= len(plan):
        return {"current_step": step + 1}
    
    # 执行当前步骤（可用小模型）
    result = execute_step(plan[step], state["results"])
    new_results = state["results"].copy()
    new_results[step] = result
    return {"results": new_results}

def should_continue(state: PlanExecuteState) -> str:
    """判断是否继续执行"""
    if state["current_step"] + 1 >= len(state["plan"]):
        return "end"
    return "continue"

graph = StateGraph(PlanExecuteState)
graph.add_node("planning", planning_node)
graph.add_node("executing", executing_node)
graph.add_edge(START, "planning")
graph.add_edge("planning", "executing")
graph.add_conditional_edges("executing", should_continue, {"continue": "executing", "end": END})
```

**优点：** 减少 LLM 调用次数、执行效率高、成本低
**缺点：** 计划静态，无法应对突发状况、容错性差

**适用场景：** 流程固定的多步骤任务（报告生成、数据处理）

---

### 6.3 ReWOO (Reasoning Without Observation)

**核心：计划中包含变量，一次性规划整个任务链**

```
Plan: ["步骤1 #E1=Tool1", "步骤2 #E2=Tool2(#E1)", "步骤3 #E3=Tool3(#E2)"]
Execute: 并行/串行执行，返回最终结果
```

```python
# ReWOO 模式：带变量的计划
def plan_with_variables(state: PlanExecuteState) -> PlanExecuteState:
    """生成带变量的计划"""
    user_query = state["messages"][-1].content
    # 计划中包含变量占位符：#E1, #E2 表示前序步骤的输出
    plan_with_vars = llm_generate_var_plan(user_query)
    # 例如: ["search(#QUERY)", "extract(#E1)", "summarize(#E2)"]
    return {"plan": plan_with_vars}

def execute_chain(state: PlanExecuteState) -> PlanExecuteState:
    """按依赖顺序执行"""
    results = {}
    for step in state["plan"]:
        # 解析变量引用，执行工具
        var_name, tool_call = parse_var_step(step, results)
        results[var_name] = execute_tool(**tool_call)
    return {"results": results}
```

**优点：** 变量传递高效、减少 Token 消耗
**缺点：** 仍是串行执行、无法并行利用独立任务

---

### 6.4 Reflexion (强化反思)

**核心：自我评估 + 动态记忆，从失败中学习**

```
生成结果 → 反思(评估) → 如失败则记录经验 → 重新生成 → ...
```

```python
# Reflexion 模式
class ReflexionState(TypedDict):
    messages: list
    memory: list           # 反思记忆：过去的成功/失败经验
    attempts: int          # 尝试次数

def generate_node(state: ReflexionState) -> ReflexionState:
    """生成初始回答"""
    context = build_context(state["messages"], state["memory"])
    response = llm_generate(context)
    return {"messages": state["messages"] + [AIMessage(content=response)]}

def reflect_node(state: ReflexionState) -> ReflexionState:
    """反思：评估回答质量"""
    last_response = state["messages"][-1].content
    evaluation = llm_evaluate(last_response)  # 返回: {"success": bool, "feedback": str}
    
    if evaluation["success"]:
        return {"attempts": state["attempts"] + 1}
    
    # 失败：生成反思文本，加入记忆
    reflection = f"尝试{state['attempts']}失败原因: {evaluation['feedback']}"
    new_memory = state["memory"] + [reflection]
    return {"memory": new_memory, "attempts": state["attempts"] + 1}

def should_retry(state: ReflexionState) -> str:
    """判断是否重试"""
    if state["attempts"] >= 3:
        return "end"
    last_response = state["messages"][-1].content
    if llm_evaluate(last_response)["success"]:
        return "end"
    return "retry"

graph = StateGraph(ReflexionState)
graph.add_node("generate", generate_node)
graph.add_node("reflect", reflect_node)
graph.add_edge(START, "generate")
graph.add_edge("generate", "reflect")
graph.add_conditional_edges("reflect", should_retry, {"retry": "generate", "end": END})
```

**优点：** 无需微调、通过文本反馈实现学习、可追踪
**缺点：** 依赖 LLM 自我评估能力、记忆容量有限

**适用场景：** 需要迭代优化的任务（代码生成、文本创作）

---

### 6.5 你的项目：ReAct + 条件分支

你的心理陪伴系统本质是 **ReAct + 条件分支** 的混合模式：

```python
# 你的项目架构：ReAct 循环 + 条件分支
class CrisisAgentState(TypedDict):
    messages: list
    risk_level: str        # normal / warning / urgent / crisis
    retrieved_docs: list
    final_response: str

# 节点1: 风险检测（类似 ReAct 的 Think + Act）
def risk_detection(state: CrisisAgentState) -> CrisisAgentState:
    user_msg = state["messages"][-1].content
    # 双重检测：关键词 + LLM 判断
    risk = detect_risk(user_msg)
    return {"risk_level": risk}

# 节点2: RAG 检索（类似 ReAct 的 Action）
def rag_retrieval(state: CrisisAgentState) -> CrisisAgentState:
    if state["risk_level"] == "crisis":
        return {"retrieved_docs": []}  # 危机模式不检索
    docs = hybrid_retrieval(state["messages"][-1].content)
    return {"retrieved_docs": docs}

# 节点3: LLM 生成（类似 ReAct 的 Observation 后再次 Think）
def llm_generation(state: CrisisAgentState) -> CrisisAgentState:
    if state["risk_level"] == "crisis":
        response = generate_crisis_response()
    else:
        response = generate_with_docs(state["retrieved_docs"])
    return {"final_response": response}

# 节点4: 安全审核
def safety_check(state: CrisisAgentState) -> CrisisAgentState:
    if contains_sensitive(state["final_response"]):
        state["final_response"] = insert_helpline(state["final_response"])
    return state

# 条件边：不同风险级别走不同流程
graph.add_conditional_edges(
    "risk_detection",
    lambda s: "urgent_flow" if s["risk_level"] in ["urgent", "crisis"] else "normal_flow"
)
```

**面试话术：** "我的系统结合了 ReAct 和状态机模式。ReAct 的核心是 Thought-Act-Observation 循环，我的系统将这个思想具象化为四级危机干预流程：risk_detect（判断）→ rag_retrieve（行动）→ llm_generate（生成）→ safety_check（审核）。不同风险级别走不同分支，危机级别直接触发热线介入，这比单纯的 ReAct 更加可控和可解释。"

---

### 6.6 设计模式对比总结

| 模式 | 核心思想 | 优点 | 缺点 | 适用场景 |
|------|----------|------|------|----------|
| **ReAct** | 边想边做，循环反馈 | 灵活、可实时调整 | Token消耗大 | 需要查资料、调用API |
| **Plan-Execute** | 先规划再执行 | 效率高、成本低 | 灵活性差 | 固定流程多步骤任务 |
| **ReWOO** | 计划带变量 | 变量传递高效 | 仍是串行 | 链式工具调用 |
| **Reflexion** | 自我反思+记忆 | 无需微调、可学习 | 依赖评估能力 | 代码生成、文本创作 |
| **LATS** | 树搜索+反思 | 综合最优 | 成本极高 | 复杂决策 |

**面试话术：** "我理解这些设计模式的核心权衡：ReAct 最灵活但成本高；Plan-Execute 效率高但缺乏适应性；Reflexion 适合需要迭代优化的场景。我的心理陪伴系统选用 ReAct+状态机的混合模式，是因为危机干预需要精确控制流程，同时需要 RAG 检索提供专业知识。"

---

### 6.7 LATS (Language Agent Tree Search)

**核心：蒙特卡洛树搜索 + ReAct + Reflexion**

```
                    用户问题
                        │
                   ┌────▼────┐
                   │ 根节点  │
                   │ Thought │
                   └────┬────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    ┌───────┐       ┌───────┐       ┌───────┐
    │Action1│       │Action2│       │Action3│
    │Observe│       │Observe│       │Observe│
    └───────┘       └───────┘       └───────┘
        │               │               │
        ▼               ▼               ▼
    ┌───────┐       ┌───────┐       ┌───────┐
    │Reflect│       │Reflect│       │Reflect│
    │评估1  │       │评估2  │       │评估3  │
    └───────┘       └───────┘       └───────┘
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 选择最优路径
```

**原理：** LATS 将 MCTS（蒙特卡洛树搜索）与 LLM 结合，在每个决策点生成多个可能的行动分支，通过价值评估选择最优路径，并支持回溯。

```python
# LATS 模式（简化版）
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random

class LATSState(TypedDict):
    messages: list
    tree: dict                    # 决策树结构
    current_node: str             # 当前节点ID
    best_path: List[str]          # 最优路径
    depth: int                    # 当前深度

def think_node(state: LATSState) -> LATSState:
    """Think: 生成多个可能的行动分支"""
    node_id = state["current_node"]
    context = get_node_context(state["tree"], node_id)
    
    # LLM 生成多个候选行动
    candidates = llm_generate_actions(context, num=3)
    
    # 创建子节点
    child_ids = []
    for i, action in enumerate(candidates):
        child_id = f"{node_id}_child_{i}"
        state["tree"][child_id] = {
            "action": action,
            "parent": node_id,
            "observation": None,
            "evaluation": None,
            "depth": state["depth"] + 1
        }
        child_ids.append(child_id)
    
    state["tree"][node_id]["children"] = child_ids
    return {"depth": state["depth"] + 1}

def act_observe_node(state: LATSState) -> LATSState:
    """Act + Observe: 执行每个候选行动"""
    node_id = state["current_node"]
    children = state["tree"][node_id].get("children", [])
    
    for child_id in children:
        action = state["tree"][child_id]["action"]
        # 执行行动（工具调用）
        observation = execute_action(action)
        state["tree"][child_id]["observation"] = observation
    
    return state

def reflect_evaluate_node(state: LATSState) -> LATSState:
    """Reflect + Evaluate: 评估每个分支的价值"""
    node_id = state["current_node"]
    children = state["tree"][node_id].get("children", [])
    
    for child_id in children:
        obs = state["tree"][child_id]["observation"]
        # LLM 评估该分支的价值
        evaluation = llm_evaluate(obs)
        state["tree"][child_id]["evaluation"] = evaluation
    
    return state

def select_best_node(state: LATSState) -> LATSState:
    """Select: 选择最优子节点，继续探索或回溯"""
    node_id = state["current_node"]
    children = state["tree"][node_id].get("children", [])
    
    # 选择评估分数最高的子节点
    best_child = max(children, key=lambda c: state["tree"][c]["evaluation"])
    
    # 检查是否达到终止条件
    if state["tree"][best_child]["evaluation"] > 0.9 or state["depth"] >= 5:
        # 找到目标，返回最优路径
        return {"best_path": reconstruct_path(state["tree"], best_child)}
    
    # 继续向下探索
    return {"current_node": best_child, "depth": state["depth"] + 1}

def reconstruct_path(tree: dict, node_id: str) -> List[str]:
    """回溯重构最优路径"""
    path = []
    while node_id:
        path.append(tree[node_id]["action"])
        node_id = tree[node_id].get("parent")
    return list(reversed(path))

# LATS 图结构
graph = StateGraph(LATSState)
graph.add_node("think", think_node)
graph.add_node("act_observe", act_observe_node)
graph.add_node("reflect_evaluate", reflect_evaluate_node)
graph.add_node("select_best", select_best_node)

graph.add_edge(START, "think")
graph.add_edge("think", "act_observe")
graph.add_edge("act_observe", "reflect_evaluate")
graph.add_edge("reflect_evaluate", "select_best")
graph.add_conditional_edges("select_best", should_continue_lats, {"continue": "think", "end": END})
```

**LATS vs 其他模式：**

| 维度 | ReAct | Plan-Execute | Reflexion | LATS |
|------|-------|--------------|-----------|------|
| 规划方式 | 单步动态 | 一次性静态 | 无规划 | 树搜索多路径 |
| 反馈来源 | 外部工具 | 无 | 自我评估 | 外部+自我 |
| 探索能力 | 单线路 | 单线路 | 单线路 | 多路径并行 |
| Token消耗 | 高 | 低 | 中 | 极高 |
| 灵活性 | 高 | 低 | 中 | 高 |

**面试话术：** "LATS 是目前最强大的 Agent 架构，它结合了 ReAct 的行动能力、Reflexion 的反思能力和树搜索的规划能力。但其代价是 Token 消耗极高，因为需要探索多条路径并评估。在我的心理陪伴场景中，不需要这么复杂的架构，四级危机干预的确定性流程用 LangGraph 状态机更合适。"

---

### 6.8 Human-in-the-Loop (人机交互)

**核心：Agent 可在任意节点暂停，等待人类审批后再继续**

```
用户输入 → Agent执行 → [暂停等待审批] → 人类确认 → 继续执行 → 返回结果
```

**典型场景：**
- 高风险操作需要人工确认
- 关键决策需要人类把关
- 复杂任务需要人类提供额外信息

```python
# LangGraph Human-in-the-Loop 实战
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class ApprovalState(TypedDict):
    messages: list
    pending_action: str
    approval_status: str  # "pending", "approved", "rejected"
    user_feedback: str

def process_task(state: ApprovalState) -> ApprovalState:
    """处理任务，但在关键步骤暂停等待审批"""
    user_request = state["messages"][-1].content
    
    # 执行一些处理
    result = do_processing(user_request)
    
    # 这是一个高风险操作，需要人类审批
    if result["requires_approval"]:
        # interrupt 会暂停执行，等待外部触发
        interrupt({
            "action": result["action"],
            "details": result["details"],
            "message": "此操作需要人工审批"
        })
    
    return {"pending_action": result["action"]}

def after_approval(state: ApprovalState) -> ApprovalState:
    """审批通过后的处理"""
    if state["approval_status"] == "approved":
        # 执行被暂停的操作
        execute(state["pending_action"])
        return {"messages": state["messages"] + [AIMessage(content="操作已完成")] }
    else:
        return {"messages": state["messages"] + [AIMessage(content="操作已拒绝")]}

# 编译时添加 interrupt 处理
graph = StateGraph(ApprovalState)
graph.add_node("process", process_task)
graph.add_node("after_approval", after_approval)

graph.add_edge(START, "process")
graph.add_edge("process", "after_approval")
graph.add_edge("after_approval", END)

app = graph.compile()

# 调用时处理 interrupt
def handle_user_approval(user_input: str, approval: bool, feedback: str = ""):
    """用户审批后恢复执行"""
    command = Command(
        resume={
            "approval_status": "approved" if approval else "rejected",
            "user_feedback": feedback
        }
    )
    return app.invoke(user_input, config=command)
```

**你的项目中的实际应用：**

```python
# 你的四级危机干预系统中的 Human-in-the-Loop
from langgraph.types import interrupt

class CrisisState(TypedDict):
    messages: list
    risk_level: str
    safety_check_passed: bool

def safety_check_node(state: CrisisState) -> CrisisState:
    """安全审核节点：高风险内容需要人工介入"""
    response = state.get("final_response", "")
    
    # 检测敏感内容
    if contains_sensitive(response):
        # 暂停，等待人工审核或自动插入热线
        interrupt({
            "type": "safety_review",
            "content": response,
            "suggestion": "建议插入心理援助热线"
        })
    
    return {"safety_check_passed": True}

# 面试话术
"""
面试官：你们的危机干预系统如何处理高风险情况？
我：我们的系统有四级危机干预机制，前三级（normal/warning/urgent）由 AI 自动处理，
但对于最高级别的 crisis 内容，系统会触发 interrupt，强制插入心理援助热线和
紧急联系信息，确保用户能够获得专业帮助。这种设计既保证了效率，又守住了安全底线。
"""
```

**Human-in-the-Loop 的三种模式：**

| 模式 | 说明 | 示例 |
|------|------|------|
| **Review** | Agent 生成结果，人类审核后返回 | 内容审核、合同审批 |
| **Edit** | 人类编辑 Agent 的输出 | 文案修改、代码调整 |
| **Execute** | 人类批准后才执行危险操作 | 转账、删除、数据导出 |

**面试话术：**
> "我在项目中实现了类似 Human-in-the-Loop 的机制。在四级危机干预系统中，高风险内容会被拦截并自动插入心理援助热线，这本质上是自动化的审批流程。对于更复杂的场景，LangGraph 的 interrupt 支持暂停后由外部系统触发恢复，可以实现完整的人工审批工作流。"

---

### 6.9 完整设计模式知识图谱

```
                        ┌─────────────────┐
                        │   Agent 设计    │
                        │    模式体系      │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  规划执行类    │      │   反思增强类     │      │   层级协作类     │
├───────────────┤      ├─────────────────┤      ├─────────────────┤
│ • ReAct       │      │ • Basic         │      │ • Supervisor    │
│ • Plan-Execute│      │   Reflection    │      │ • Swarm         │
│ • ReWOO       │      │ • Reflexion     │      │ • Multi-Agent   │
│ • LLM Compiler│      │ • LATS          │      │   Handoff       │
└───────────────┘      └─────────────────┘      └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   动态规划模式              自我优化模式              多Agent协作

选择依据：
• 需要灵活调整 → ReAct
• 流程固定效率优先 → Plan-Execute
• 链式工具调用 → ReWOO
• 需要迭代优化 → Reflexion
• 复杂决策探索 → LATS
• 多Agent分工 → Supervisor
• 需要人工把关 → Human-in-loop
```

## 七、实战代码片段

### 7.1 完整 Agent 示例

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Weather in {city}: sunny, 25°C"

@tool
def search_wiki(query: str) -> str:
    """Search Wikipedia for information."""
    return f"Results for: {query}"

# 创建 Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather, search_wiki],
    system_prompt="You are a helpful research assistant.",
    checkpointer=InMemorySaver(),
)

# 调用
config = {"configurable": {"thread_id": str(uuid7())}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]},
    config=config
)
```

### 7.2 自定义 Middleware

```python
from langchain.agents.middleware import BaseMiddleware
from langchain_core.messages import HumanMessage

class CrisisDetectionMiddleware(BaseMiddleware):
    def __init__(self):
        self.crisis_keywords = ["自杀", "割腕", "安眠药"]
    
    async def on_message(self, context, message, next):
        if any(kw in message.content for kw in self.crisis_keywords):
            context["risk_level"] = "urgent"
        return await next()

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    middleware=[CrisisDetectionMiddleware()],
)
```

### 7.3 条件分支状态机

```python
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    messages: list
    risk_level: str
    should_escalate: bool

def risk_node(state: AgentState) -> AgentState:
    risk = detect_risk(state["messages"][-1].content)
    return {"risk_level": risk, "should_escalate": risk == "urgent"}

def escalate_node(state: AgentState) -> AgentState:
    return {"messages": state["messages"] + [SystemMessage(content="Escalated!")]}

def normal_node(state: AgentState) -> AgentState:
    return {"messages": state["messages"] + [AIMessage(content="Normal response")]}

graph = StateGraph(AgentState)
graph.add_node("risk", risk_node)
graph.add_node("escalate", escalate_node)
graph.add_node("normal", normal_node)

graph.add_edge(START, "risk")
graph.add_conditional_edges(
    "risk",
    lambda s: "escalate" if s["should_escalate"] else "normal"
)
graph.add_edge("escalate", END)
graph.add_edge("normal", END)
```

---

## 八、学习路径建议

### 第一阶段：LangChain 基础（1-2天）
- [x] 安装 `pip install langchain`
- [x] 掌握 `create_agent` API
- [x] 理解 Model/Tools/Prompt 三大组件
- [x] 实现简单 Tool 调用

### 第二阶段：LangGraph 进阶（2-3天）
- [x] StateGraph 状态机
- [x] Nodes 和 Edges 定义
- [x] Checkpoint 持久化
- [x] Streaming 流式输出
- [x] Multi-Agent Supervisor 模式

### 第二阶段半：Agent 设计模式（2-3天）
- [x] ReAct 模式（Thought→Action→Observation）
- [x] Plan-Execute 模式（先规划后执行）
- [x] ReWOO 模式（带变量的计划）
- [x] Reflexion 模式（自我反思+记忆）
- [x] LATS 模式（树搜索+反思）
- [x] Human-in-the-Loop（人机交互）
- [x] 设计模式选择依据与面试话术

### 第三阶段：生产实战（3-5天）
- [x] 你的项目：四级危机干预状态机
- [x] RAG 集成（Vector + Graph + BM25）
- [x] Langfuse/LangSmith 追踪
- [x] 故障降级与灰度发布
- [x] 全链路可观测性

### 第四阶段：面试冲刺
- [x] 理解 Agent = Model + Harness
- [x] 掌握 Middleware 扩展机制
- [x] 理解 LangChain/LangGraph/LangSmith 三者关系
- [x] 掌握所有设计模式对比
- [x] 能够画出你的项目架构图
- [x] 能回答上面的高频问题

---

## 九、参考资料

- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangSmith Observability](https://docs.langchain.com/langsmith/observability)
- [langgraph (GitHub)](https://github.com/langchain-ai/langgraph) - 33.2k stars
- [langgraph-supervisor-py (GitHub)](https://github.com/langchain-ai/langgraph-supervisor-py) - 1.6k stars

---

## 十、求职亮点提炼

| 项目亮点 | 对应岗位能力 |
|----------|--------------|
| LangGraph 4节点状态机设计 | 复杂工作流编排能力 |
| 1840条生产请求零故障 | 工程化可靠性 |
| 三混合 RAG（82%精准度） | RAG 与知识库设计 |
| 四级危机干预 SOP | 业务场景落地能力 |
| Langfuse 全链路追踪 | 可观测性与问题排查 |
| 双链路灰度发布 | 安全生产与发布能力 |

**一句话总结：**
> "我在大学生心理陪伴系统中全程使用 LangGraph 设计状态机，实现了 RAG 检索增强、四级危机干预、全链路可观测性，生产环境 1840 条请求零故障，充分体现了 AI Agent 工程化能力。"