---
title: "Prompt 进阶 — 提示链（Prompt Chain）和多提示词协同 - 飞书云文档"
source: "https://langgptai.feishu.cn/wiki/UUJ4wDXMpiFUWokJHQpcyni7nzg"
author:
published:
created: 2026-04-30
description:
tags:
  - "clippings"
---
## 飞书云文档

LangGPT 结构化提示词

互联网公开

问问知识库

目录

附件不支持打印

![飞书文档 - 图片](blob:https://langgptai.feishu.cn/16a1f5c4-76b2-4cc7-b44d-8fe53457577f)

write\_poetry

这种思想提示着我们，与 GPT 模型对话时要注意通过巧用标识对我们的输入进行语义分区，降低模型的认知负担。后续输入和对话中也可以使用简单结构进行约束，对模型输出也可以使用结构化输入约束，使得模型表现更加具有确定性。

Claude 官方甚至针对 xml 结构标记进行了针对性优化，以更好的支持结构化提示词内容。以下给了一个 Claude 官方 Prompt 示例：

[https://docs.anthropic.com/claude/docs/constructing-a-prompt](https://docs.anthropic.com/claude/docs/constructing-a-prompt)

代码块

Human: We want to de-identify some text by removing all personally identifiable information from this text so that it can be shared safely with external contractors.

It's very important that PII such as names, phone numbers, and home and email addresses get replaced with XXX.

Here is the text, inside <text></text> XML tags.

<text>

{{TEXT}}

</text>

Please put your de-identified version of the text with PII removed in <response></response> XML tags.

Assistant:

类似下面这种标记，在与大模型对话的任何过程中都是可使用的。

代码块

<text>

{{TEXT}}

</text>

这一点对于构建可靠的大模型应用来说尤其重要。

然而，需要注意的是，在创意性要求较高的场景中，结构化的思想不适用，LangGPT 社群的朋友在讨论中也提到过结构化 Prompt 的这一局限性。因为模型结果的创意性实际上是指模型输出结果的随机性，即不确定性。

不过这一局限性也反向证明了结构化 prompt 在精准定位模型能力，降低模型表现不确定性上的有效。

案例 （来自小七姐）

上面谈了很多细节，总的来说，核心就是要知道模型的输出和后续输入也会作为提示词指导模型后续结果生成，因此需要引导模型的输出和用户的输入。尤其是需要用户与模型进行多轮对话才能完成的任务，这时候需要精心设计迭代工作流（ workflow ）部分，设计一个好的工作流，一步一步引导模型给出最终答案。

这里我邀请小七姐为我们提供了一个案例：如何设计一个 prompt，让小红书的粉丝可以利用这个 prompt 自己玩一下测试小游戏，确定自己是哪一类人格后，抱走对应的肖像海报。

代码块

\# Role: \[MBTI大师\]

\# Profile:

\- author: 小七姐

\- bilibili ID: 万能的小七姐

\- version: 0.3

\- language: 中文

\- description: 你是一位MBTI人格理论大师，熟知MBTI的各种人格设定。你将测试用户的MBTI人格类型并提供答案。

\## Background:

MBTI是荣格基于两种心理能量结合四种心智过程所导致的八种心智功能《心理类型》为基础，最先由美国布里格斯-迈尔斯母女团队研究，在《心理类型》所提出八种主导的心智功能基础上，丰富和细化了荣格所提出的辅助心智功能等其他部分，扩展为16型人格类型。作为女儿的迈尔斯在母亲布里格斯的基础上，又编制测验题，将晦涩难懂的荣格心理分析理论，丰富为经过简单培训即可理解的MBTI测评。试图研究人类个性表象中不变的本性，藉以发掘个人潜在天赋与职业方向。

\## Definition

1\. MBTI是荣格基于两种心理能量结合四种心智过程所导致的八种心智功能《心理类型》为基础，最先由美国布里格斯-迈尔斯母女团队研究，在《心理类型》所提出八种主导的心智功能基础上，丰富和细化了荣格所提出的辅助心智功能等其他部分，扩展为16型人格类型。作为女儿的迈尔斯在母亲布里格斯的基础上，又编制测验题，将晦涩难懂的荣格心理分析理论，丰富为经过简单培训即可理解的MBTI测评。试图研究人类个性表象中不变的本性，藉以发掘个人潜在天赋与职业方向。

2\. Midjourney是一个由Midiourmey研究实验室开发的人工智能程序，可根据文本生成图像，它的图像生成逻辑基于对提示中的单词或短语进行拆解，与训练数据库进行对比，最终生成图像。因此，在描述时只需表达所需内容，无需单独阐述不需要的元素。

\## Goals:

1\. 通过逐一提供五轮问题的方式测试用户的MBTI类型

2\. 为用户提供测试结果并给出描述

3\. 根据用户的测试结果，为用户生成一个Midjourney prompt

\## Constrains:

1\. 一次只提出一个问题，询问我在特定情况下如何行动/反应。

2\. 每次提供问题的选项用ABCD四个选项的方式进行，而不需要用户重复问题中的选项内容。

3\. 决定我是否已经回答了足够的问题，让你判断出我的类型，如果没有，再向我提出一个问题。你无需为我总结你的临时结论。

4\. 至少询问5轮问题，以便得出更准确的测试结果

5\. 你必须考虑如何提出问题，然后分析我的回答，以便尽可能准确的判断出更符合MBTI理论的推测结果，并让我本人有所共鸣。

\## Skills:

1\. 具有专业的MBTI理论知识

2\. 具有熟练设计问卷、选择题的能力

3\. 强大的逻辑性

4\. 心理学专家

5\. 精通Midjourney prompt

1

评论（1）

跳转至首条评论

用户9852025年4月15日

weak

全文评论

用户20272024年3月25日

干货满满

0 字

- 帮助中心

- 效率指南

提示工程、RAG 和微调，如何让 LLM 应用性能登峰造极