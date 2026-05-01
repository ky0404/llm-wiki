---
title: "Best practices for prompt engineering with the OpenAI API"
type: source
tags: [prompt-engineering, openai, best-practices, api]
sources: [Best practices for prompt engineering with the OpenAI API.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
OpenAI 官方提示工程最佳实践指南。

### 核心原则
1. **使用最新模型**：最新模型更容易进行提示工程
2. **将指令放在开头**，使用 ### 或 """ 分隔指令和上下文
3. **具体、描述性且尽可能详细**：关于期望的上下文、结果、长度、格式、风格等
4. **通过示例说明期望的输出格式**：展示具体格式要求，便于程序化解析
5. **从 zero-shot 开始，然后 few-shot，都不行再微调**
6. **减少"冗长"和不精确的描述**：用具体数字替代"相当短"
7. **不说不要做什么，而是说应该做什么**
8. **代码生成：使用"leading words"引导模型**：如 import 提示 Python，SELECT 提示 SQL
9. **使用 Generate Anything 特性**：描述任务获取定制提示

### 参数建议
- **model**：更高性能模型通常更贵、延迟更高
- **temperature**：越高越随机（创意），越低越确定性。对于事实性任务（如数据提取、真实问答），最佳为 0
- **max_completion_tokens**：硬性截断限制，非输出长度控制
- **stop**：生成时遇到即停止的字符序列

## References
- [[concepts/提示词工程]]
- [[entities/openai]]