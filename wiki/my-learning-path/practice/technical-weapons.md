---
title: 我的技术武器库
type: synthesis
tags: [技术武器, 求职, AI开发, RAG, Agent]
sources: [知识库核心技术内容]
created: 2026-05-01
updated: 2026-05-01
---

# 我的技术武器库

从Wiki知识库中提炼的可直接用于项目开发和求职面试的核心技术能力。

---

## 武器1：RAG混合检索系统

**来源**：知识库「高级RAG技术学习笔记」+「RAG混合检索核心原理」

**掌握程度**：⭐⭐⭐⭐⭐（已实战落地）

### 技术要点
- 向量检索（Chroma）+ BM25关键词检索 + RRF融合
- k值调优：40-80范围搜索，技术文档场景k=60
- 量化成果：文档召回率提升21%，回答准确率提升30%

### 面试话术
> 独立设计并实现RAG混合检索系统，将向量检索与BM25融合，文档召回率提升21%，大模型回答准确率提升30%，彻底解决技术文档专有名词召回难题

---

## 武器2：LangGraph工作流设计

**来源**：知识库「基于LangGraph创建智能体应用」+「AI Agent Workflow Design Patterns」

**掌握程度**：⭐⭐⭐⭐（项目已用）

### 技术要点
- 状态图（StateGraph）定义Agent行为
- 节点（Node）+ 边（Edge）构建工作流
- 支持条件分支和循环

### 可升级方向
在现有工作流中引入以下设计模式：

#### 2.1 ReAct模式
```
Thought → Action → Observation → Thought → ...
```
适用于：需要外部工具交互的任务

#### 2.2 Plan & Solve模式
```
Planner(生成计划) → Executor(执行) → Replanner(调整) → ...
```
适用于：复杂多步骤任务，减少Token消耗

#### 2.3 Reflexion模式
```
执行 → 反思 → 改进 → 重新执行 → ...
```
适用于：需要迭代优化的场景

### 面试话术
> 基于LangGraph构建智能文档问答Agent，使用状态图定义Agent行为，支持多轮对话和条件分支，可扩展集成ReAct/Plan & Solve等设计模式

---

## 武器3：上下文工程

**来源**：知识库「从提示工程到上下文工程的演进路线图」+「context-engineer.md」

**掌握程度**：⭐⭐⭐⭐（理论已掌握）

### 四大核心策略

| 策略 | 技术要点 | 落地场景 |
|------|----------|----------|
| **Write** | Scratchpads便笺、Memories记忆、文件系统 | 长时任务状态持久化 |
| **Select** | RAG检索、工具选择、渐进式披露 | 按需加载相关信息 |
| **Compress** | 上下文总结、裁剪、压缩 | 92%窗口阈值触发 |
| **Isolate** | 子智能体拆分、状态隔离 | 复杂任务分解 |

### 面试话术
> 熟悉上下文工程四大策略：Write（状态持久化）、Select（RAG检索）、Compress（窗口压缩）、Isolate（子智能体拆分），能够优化Agent的上下文管理能力

---

## 武器4：结构化提示词设计

**来源**：知识库「结构化提示词知识库」+「prompt-structurer.md」

**掌握程度**：⭐⭐⭐⭐（熟练使用）

### 核心模块
- **Role**：角色定义，聚焦领域
- **Profile**：元数据（作者、版本）
- **Goals**：一句话目标
- **Constraints**：限制条件
- **Skills**：技能强化
- **Workflow**：工作流
- **Initialization**：初始化对白

### 面试话术
> 掌握LangGPT结构化提示词方法论，能够设计模块化提示词（Role/Goals/Constraints/Skills/Workflow），曾在项目中优化Agent指令模板，提升任务完成率

---

## 武器5：Agent设计模式

**来源**：知识库「AI Agent Workflow Design Patterns」

**掌握程度**：⭐⭐⭐（理论储备）

### 设计模式图谱

#### 规划类模式
| 模式 | 核心优势 | 适用场景 |
|------|----------|----------|
| Plan & Execute | 先规划后执行，效率高 | 复杂多步骤任务 |
| REWOO | 一次性生成完整计划 | 工具间数据传递 |
| LLM Compiler | DAG并行执行 | 多独立任务并行 |

#### 反思类模式
| 模式 | 核心优势 | 适用场景 |
|------|----------|----------|
| Basic Reflection | 显式反思改进 | 迭代优化 |
| Reflexion | 跨试验试错学习 | 从失败中学习 |
| LATS | 树搜索+反思 | 深度探索 |

### 面试话术
> 熟悉主流Agent设计模式：ReAct（推理+行动）、Plan & Execute（规划执行）、Reflexion（反思学习），能够根据任务场景选择合适的模式

---

## 武器6：Function Calling

**来源**：知识库「Function calling OpenAI API」

**掌握程度**：⭐⭐⭐（基础会用）

### 技术要点
- JSON Schema定义工具
- 工具调用请求 + 结果回传
- 多轮对话循环

### 面试话术
> 能够使用Function Calling扩展LLM能力，让Agent调用外部API获取实时信息，实现与外部系统的集成

---

## 武器7：MCP协议（Model Context Protocol）

**来源**：知识库「Understanding Model Context Protocol (MCP)」

**掌握程度**：⭐⭐⭐（概念理解）

### 技术要点
- **定义**：AI应用与外部资源和工具通信的开放标准
- **架构**：MCP Client（AI应用端）+ MCP Server（连接各类资源）
- **核心优势**：供应商中立、安全第一、可扩展

### 解决的问题
| 传统方案问题 | MCP解决方案 |
|------------|------------|
| 供应商锁定 | 通用接口，一次编写到处使用 |
| 安全风险 | 设计即安全，精细权限控制 |
| 维护开销 | 共享服务器市场 |

### 面试话术
> 了解MCP（Model Context Protocol）开放标准，理解其解决AI系统数据统一接入问题的设计理念，熟悉Agent与外部系统集成的架构思路

---

## 武器8：Embedding向量化技术

**来源**：知识库「使用Embedding技术打造本地知识库助手」

**掌握程度**：⭐⭐⭐⭐（项目已用）

### 技术要点
- **原理**：将文本/图像/音视频转为数字向量，语义相似的内容向量距离近
- **核心模型**：text-embedding-ada-002（OpenAI第二代）
- **应用场景**：语义搜索、推荐、知识问答

### RAG中的位置
```
文档 → Embedding → 向量存储 → 相似度检索 → LLM生成
```

### 面试话术
> 熟悉Embedding向量化技术，能够将文本转为语义向量，理解向量检索的原理，曾使用text-embedding-ada-002模型构建本地知识库

---

## 武器9：Transformer架构

**来源**：知识库「Attention Is All You Need」（经典论文）

**掌握程度**：⭐⭐⭐（理论理解）

### 核心组件
- **Encoder**：6层，多头自注意力 + 前馈网络
- **Decoder**：6层，额外包含Encoder-Decoder注意力
- **核心公式**：`Attention(Q, K, V) = softmax(QK^T / √d_k)V`

### 关键技术
- Scaled Dot-Product Attention（缩放点积注意力）
- Multi-Head Attention（多头注意力，h=8）
- Positional Encoding（位置编码）

### 面试话术
> 理解Transformer架构核心原理，熟悉注意力机制（QKV、Multi-Head），了解位置编码和残差连接，能够解释Transformer相比RNN的并行化优势

---

## 武器10：容器技术基础

**来源**：知识库「容器运行时containerd学习笔记」+「Kubernetes GPU调度」

**掌握程度**：⭐⭐（概念理解）

### 技术要点
- **containerd**：CNCF容器运行时标准，从Docker分离
- **OCI标准**：Runtime、Image、Distribution三大标准
- **Kubernetes集成**：通过CRI接口原生支持

### 面试话术
> 了解容器技术基础，理解containerd与Docker、Kubernetes的关系，知道容器化部署的基本流程

---

## 武器11：多Agent系统架构

**来源**：知识库「你不知道的Agent：原理、架构与工程实践」

**掌握程度**：⭐⭐⭐（理论理解）

### 技术要点
- **单Agent架构**：简单任务，上下文限制
- **多Agent架构**：角色分工、协作与竞争
  - Planner-Executor模式
  - Peer-to-Peer模式
- **记忆机制**：短期记忆（对话历史）+ 长期记忆（向量检索）

### 面试话术
> 熟悉多Agent系统架构设计，理解单Agent与多Agent的适用场景，了解Agent间的协作模式（Planner-Executor、Peer-to-Peer），能够设计多Agent协作工作流

---

## 武器12：参数高效微调（PEFT）

**来源**：知识库「参数高效微调」（LoRA论文）

**掌握程度**：⭐⭐⭐（概念理解）

### 主流方法对比

| 方法 | 可训练参数 | 推理延迟 | 特点 |
|------|-----------|----------|------|
| **LoRA** | ~0.01% | 无 | 低秩矩阵分解，无推理延迟 |
| **Adapter** | ~1% | 有 | 瓶颈层 |
| **Prefix Tuning** | ~0.1% | 有 | 虚拟token |
| **BitFit** | ~0.1% | 无 | 仅偏置参数 |

### 面试话术
> 了解参数高效微调技术，熟悉LoRA原理（低秩矩阵分解），知道如何在消费级GPU上微调大模型

---

## 武器13：RLHF人类反馈强化学习

**来源**：知识库「RLHF」

**掌握程度**：⭐⭐（概念理解）

### 核心步骤
1. 预训练语言模型
2. 收集人类反馈数据
3. 训练奖励模型
4. 使用PPO优化策略

### 面试话术
> 理解RLHF（人类反馈强化学习）的基本流程，知道它用于模型对齐（ChatGPT、Claude安全对齐），了解其核心挑战

---

## 武器14：AI+搜索产品生态

**来源**：知识库「聊聊Deep Search和Deep Research」

**掌握程度**：⭐⭐⭐（概念理解）

### 技术演进
```
传统搜索 → RAG → AI+搜索（ChatGPT Search）→ 搜索+AI（Google AI Overviews）
```

### 代表产品
- ChatGPT Search
- Claude Search
- DeepSeek Search
- Kimi
- Google AI Overviews
- 百度AI+

### 面试话术
> 理解AI+搜索的技术演进路线，熟悉RAG在搜索场景的应用，知道主流AI搜索产品的技术特点

---

## 武器15：向量数据库

**来源**：知识库「高级RAG技术学习笔记」

**掌握程度**：⭐⭐⭐⭐（项目已用）

### 主流产品
- **Chroma**：轻量级开源，本地优先
- **Weaviate**：开源分布式
- **Pinecone**：云托管向量数据库

### 面试话术
> 熟悉向量数据库工作原理，能够使用Chroma/Weaviate构建向量检索系统，理解向量索引与相似度搜索的原理

---

## 武器16：提示工程核心原则

**来源**：知识库「提示工程学习笔记」+「Elements of a Prompt」

**掌握程度**：⭐⭐⭐⭐（熟练使用）

### 核心要素
- **指令（Instruction）**：希望模型执行的特定任务
- **上下文（Context）**：外部信息或背景
- **输入数据（Input Data）**：用户问题
- **输出指示（Output Indicator）**：输出格式

### 最佳实践
1. 从简单开始（Zero-shot → Few-shot）
2. 指令放开头，使用分隔符
3. 具体、详细、直接
4. 明确输出格式
5. 说"要做什么"而非"不要做什么"

### 面试话术
> 掌握提示工程核心原则和最佳实践，能够设计高效的提示词，理解Zero-shot、Few-shot的适用场景

---

## 技术成长路线

### 短期（1-2个月）
- [x] RAG混合检索 → 已在项目落地
- [ ] Agent设计模式 → 引入项目工作流
- [ ] 上下文工程 → 优化上下文管理

### 中期（3-4个月）
- [ ] RAG高级技术：查询改写、rerank、上下文压缩
- [ ] Agent进阶：LATS、LLM Compiler
- [ ] MCP协议深入

### 长期（5-6个月）
- [ ] 构建完整的AI Agent系统
- [ ] 积累Agent设计模式实战经验
- [ ] 形成可复用的技术方法论

---

## References

- [[wiki/my-learning-path/theory/rag-theory|RAG技术原理]]
- [[wiki/my-learning-path/practice/open-source-doc-agent/hybrid-retrieval-optimization|开源文档Agent混合检索优化方案]]
- [[wiki/my-learning-path/interview/technical-questions/rag-hybrid-retrieval|RAG混合检索面试题库]]