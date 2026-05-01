---
title: "结构化提示词系统论述： 构建高性能 Prompt 之路 - 飞书云文档"
type: source
tags: ["prompt"]
sources: ["\u7ed3\u6784\u5316\u63d0\u793a\u8bcd\u7cfb\u7edf\u8bba\u8ff0\uff1a \u6784\u5efa\u9ad8\u6027\u80fd Prompt \u4e4b\u8def - \u98de\u4e66\u4e91\u6587\u6863.md"]
created: 2026-04-30
updated: 2026-04-30
---


## 飞书云文档

LangGPT 结构化提示词

互联网公开

问问知识库

目录

LangGPT

1️⃣

结构化提示词系统论述： 构建高性能 Prompt 之路

最新修改时间为10月23日

附件不支持打印

•

作者：云中江树

前言

我算是最早在国内提结构化、模板化编写大模型 Prompt 范式的人之一。2023 年 4 月在我自己的个人实践中发现这种结构化、模板化的方式对编写 prompt 十分友好，并且在大多数时候都表现不俗。2023 年 5 月份我将这种方法开源成 LangGPT 项目并在国内写文公开，受到了许多人的认可和喜爱，尤其在 GitHub、即刻、知乎等社区都有不小的反响。由于结构化 Prompt 的出色性能表现，很多朋友都开始在实践中应用这种方法写 Prompt ，其中不乏许多来自网易字节等互联网大厂的朋友。

虽然结构化 prompt 的思想目前已经广为传播并应用，但是缺乏全面系统的资料。虽然也有许多解读文章传播，但内容质量良莠不齐，并且知识也较为破碎。于是写作本文，希望能成为一篇较为系统的高质量的结构化 Prompt 论述文章，为学习 Prompt 编写的朋友提供一些参考借鉴。

什么是结构化 Prompt ？

结构化的思想很普遍，结构化内容也很普遍，我们日常写作的文章，看到的书籍都在使用标题、子标题、段落、句子等语法结构。结构化 Prompt 的思想通俗点来说就是像写文章一样写 Prompt。

为了阅读、表达的方便，我们日常有各种写作的模板，用来控制内容的组织呈现形式。例如古代的八股文、现代的简历模板、学生实验报告模板、论文模板等等模板。所以结构化编写 Prompt 自然也有各种各样优质的模板帮助你把 Prompt 写的更轻松、性能更好。所以写结构化 Prompt 可以有各种各样的模板，你可以像用 PPT 模板一样选择或创造自己喜欢的模板。

在这之前，虽然也有类似结构化思想，但是更多体现在思维上，缺乏在 prompt 上的具体体现。

例如知名的 CRISPE 框架(\[3\])，CRISPE 分别代表以下含义：

•

CR：Capacity and Role（能力与角色）。你希望 ChatGPT 扮演怎样的角色。

•

I：Insight（洞察力），背景信息和上下文（坦率说来我觉得用 Context 更好）。

•

S：Statement（指令），你希望 ChatGPT 做什么。

•

P：Personality（个性），你希望 ChatGPT 以什么风格或方式回答你。

•

E：Experiment（尝试），要求 ChatGPT 为你提供多个答案。

最终写出来的 Prompt 是这样的：

代码块

Act as an expert on software development on the topic of machine learning frameworks, and an expert blog writer. The audience for this blog is technical professionals who are interested in learning about the latest advancements in machine learning. Provide a comprehensive overview of the most popular machine learning frameworks, including their strengths and weaknesses. Include real-life examples and case studies to illustrate how these frameworks have been successfully used in various industries. When responding, use a mix of the writing styles of Andrej Karpathy, Francois Chollet, Jeremy Howard, and Yann LeCun.

这类思维框架只呈现了 Prompt 的内容框架，但没有提供模板化、结构化的 prompt 形式。

而我们所提倡的结构化、模板化 Prompt，写出来是这样的1

该示例来自 LangGPT 项目: [https://github.com/yzfly/LangGPT/blob/main/README\_zh.md](https://github.com/yzfly/LangGPT/blob/main/README_zh.md)

代码块

\# Role: 诗人

\## Profile

评论（0）

跳转至首条评论

0 字

- 帮助中心

- 效率指南
