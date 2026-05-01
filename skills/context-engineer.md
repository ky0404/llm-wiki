---
name: context-engineer
description: 上下文工程策略顾问。Use when designing AI agent systems, optimizing context windows, or implementing retrieval-augmented generation. Covers Write/Select/Compress/Isolate four strategies and long-running task techniques.
license: MIT
---

# Context Engineer

基于 LangChain 团队四大策略与 Anthropic 官方实践，提供上下文工程指导。

## 1. The Core Principle

> "找到最小可能的高信号 token 集，最大化期望结果的可能性"

上下文工程不是堆砌信息，而是在每一步填充**恰好正确的信息**。

## 2. Four Strategies（四大策略）

### Write（写入）
将信息保存到上下文窗口外：
- **Scratchpads**：便笺式记录，持久化信息
- **Memories**：跨会话的记忆机制
- **Filesystem**：文件系统作为终极上下文存储

### Select（选择）
将相关信息拉入上下文窗口：
- **RAG**：检索增强生成
- **工具选择**：RAG 应用到工具描述
- **渐进式披露**：分阶段按需加载

### Compress（压缩）
仅保留执行任务所需的 token：
- **Context Summarization**：总结累积交互
- **Context Trimming**：硬编码启发式过滤
- **Compaction**：接近窗口限制时，用摘要重新初始化

### Isolate（隔离）
拆分上下文帮助完成任务：
- **Multi-agent**：跨子智能体拆分
- **Sub-agent Architectures**：专门子智能体处理专注任务
- **State**：运行时状态对象隔离

## 3. Long-Running Task Techniques（长时任务技术）

### Compaction（压缩）
当对话接近上下文窗口限制时：
1. 将消息历史发送给模型
2. 模型保留关键信息（架构决策、未解决 bug、实现细节）
3. 丢弃冗余的工具输出或消息
4. 重新初始化上下文窗口 + 最近访问的 5 个文件

### Structured Note-taking（结构化笔记）
智能体定期：
1. 写笔记持久化到外部内存（NOTES.md）
2. 在后续步骤中按需读取
3. 追踪进度、依赖关系、关键上下文

### Sub-agent Architectures（子智能体架构）
主智能体：
1. 协调高级计划
2. 分配子任务给专门子智能体
3. 汇总子智能体的精简摘要（通常 1k-2k tokens）

子智能体：
1. 在独立上下文窗口中探索
2. 使用大量 tokens（甚至数万）
3. 仅返回 distilled summary

## 4. Context Anti-Patterns（上下文反模式）

- **Context Poisoning**：幻觉进入上下文 → 解决方案：压缩时移除可疑内容
- **Context Distraction**：上下文压倒训练 → 解决方案：选择最相关的上下文
- **Context Confusion**：冗余上下文影响响应 → 解决方案：隔离冲突的上下文
- **Context Clash**：上下文各部分不一致 → 解决方案：压缩/修剪

## 5. From Prompt Engineering to Context Engineering

| 维度 | 提示工程 | 上下文工程 |
|------|----------|------------|
| 关注点 | 词句技巧 | 全面上下文 |
| 作用范围 | 任务描述表达 | 文档、示例、规则、模式、验证 |
| 类比 | 贴一张便签 | 写一部详细剧本 |

## 6. System Prompt Design

系统提示应在"正确的高度"：
- **过低**：脆弱的 if-else 硬编码，缺乏灵活性
- **过高**：模糊的指导，假设共享上下文

**最佳实践**：
```markdown
<background_information>
  知识库维护的历史与规范
</background_information>
<instructions>
  具体的自治行动准则
</instructions>
<tool_guidance>
  工具使用规范
</tool_guidance>
<output_description>
  期望的输出格式
</output_description>
```

## 7. Tool Design Principles

好的工具定义：
- **自包含**：每个工具职责单一
- **清晰描述**：输入参数无歧义
- **无功能重叠**：最小化工具间重叠
- **Token 高效**：返回信息简洁

## 8. Hybrid Strategy（混合策略）

对于不太动态的内容（法律/金融）：
- 预加载相关数据（检索）
- 保留按需探索能力

对于代码/动态内容：
- 仅加载入口文件
- 让智能体按需探索

## 9. Skill Metadata

**适用场景**：Agent 系统设计、上下文窗口优化、RAG 实现
**核心原则**：最小高信号 token 集，最大化期望结果
**关键引用**：LangChain 博客、Anthropic 官方文档、Claude Code 实践