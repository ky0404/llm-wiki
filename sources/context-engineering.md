---
title: "Context Engineering（LangChain 博客）"
type: source
tags: [context-engineering, langchain, agents, memory]
sources: [Context Engineering.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
LangChain 团队发布的上下文工程策略详解。

### 上下文工程定义
正如 Andrej Karpathy 所说，LLM 像是新型操作系统：LLM 如 CPU，上下文窗口如 RAM。上下文工程是"在每一步填充恰好正确信息"的艺术和科学。

### 上下文类型
- **Instructions**：提示、记忆、few-shot 示例、工具描述等
- **Knowledge**：事实、记忆等
- **Tools**：工具调用的反馈

### 四大策略
1. **Write Context（写入上下文）**：将信息保存到上下文窗口外帮助智能体完成任务
   - **Scratchpads**：便笺式记录，持久化信息
   - **Memories**：跨会话的记忆机制

2. **Select Context（选择上下文）**：将相关信息拉入上下文窗口
   - 记忆选择：episodic、procedural、semantic
   - 工具选择：RAG 应用到工具描述
   - 知识选择：RAG 是核心挑战

3. **Compress Context（压缩上下文）**：仅保留执行任务所需的 token
   - **Context Summarization**：总结累积的交互轨迹
   - **Context Trimming**：使用硬编码启发式过滤或修剪上下文

4. **Isolate Context（隔离上下文）**：拆分上下文帮助智能体完成任务
   - **Multi-agent**：跨子智能体拆分上下文
   - **Context Isolation with Environments**：沙盒隔离
   - **State**：运行时状态对象隔离

### 长上下文的问题
- Context Poisoning：幻觉进入上下文
- Context Distraction：上下文压倒训练
- Context Confusion：冗余上下文影响响应
- Context Clash：上下文各部分不一致

## References
- [[concepts/上下文工程]]
- [[entities/langchain]]
- [[sources/浅谈上下文工程]]
- [[sources/effective-context-engineering-ai-agents]]