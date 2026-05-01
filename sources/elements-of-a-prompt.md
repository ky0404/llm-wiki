---
title: "Elements of a Prompt"
type: source
tags: [prompt-engineering, llm]
sources: [Elements of a Prompt.md]
created: 2026-04-30
updated: 2026-04-30
---

## 核心要点
提示词通常包含以下四个要素，但并非所有任务都需要全部要素：
- **Instruction（指令）**：希望模型执行的特定任务或指令。
- **Context（上下文）**：可以引导模型给出更好回复的外部信息或额外背景。
- **Input Data（输入数据）**：我们感兴趣并期望得到回复的输入或问题。
- **Output Indicator（输出指示器）**：输出的类型或格式。

示例：`Classify the text into neutral, negative, or positive. Text: I think the food was okay. Sentiment:` 其中包含了指令、输入数据和输出指示器，但没有上下文。可以通过添加额外示例作为上下文来帮助模型更好地理解任务。

## References
- [[concepts/提示词工程]]
- [[sources/prompt-engineering-tools]]
