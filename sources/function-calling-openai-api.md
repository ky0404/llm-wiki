---
title: Function calling | OpenAI API
type: source
tags: [clippings, openai, function-calling]
sources: []
created: 2026-04-29
updated: 2026-04-29
---

# Function calling | OpenAI API

## 核心要点

Function calling（工具调用）使 OpenAI 模型能够连接外部系统并访问训练数据之外的信息。

### 工具调用流程

1. 向模型发送包含工具定义的请求
2. 接收模型的工具调用请求
3. 在应用端执行代码
4. 再次发送请求并附上工具输出
5. 接收模型最终响应（或更多调用）

### 工具类型

1. **Function Tool**：使用 JSON Schema 定义输入参数
2. **Custom Tool**：使用自由文本输入，适合自定义语法约束

### 关键概念

- **Tool**：提供给模型的功能
- **Tool Call**：模型调用工具的请求
- **Tool Call Output**：工具执行结果
- **Namespace**：用于分组相关工具

### 最佳实践

1. **清晰定义**：详细描述函数和参数的用途、格式
2. **遵循工程实践**：使用 enums 使无效状态不可表示
3. **减少模型负担**：已知的参数用代码传递而非让模型填写
4. **控制工具数量**：初始不超过 20 个可用工具
5. **使用 Tool Search**：延迟加载不常用工具

### 高级特性

- **Strict Mode**：强制函数调用符合 schema
- **Parallel Calling**：模型可并行调用多个工具
- **Streaming**：实时显示工具调用进度
- **Tool Choice**：强制/限制工具调用
- **Lark/Regex CFG**：自定义文法约束

## Reference

- [[concepts/llm-编码最佳实践]]
- [[synthesis/提示技术对比-种子]]