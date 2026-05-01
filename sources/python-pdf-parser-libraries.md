---
title: 盘点 Python 中那些 PDF 解析库
type: source
tags: [pdf, python, rag, data-extraction]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

PDF 解析是 RAG 系统中的关键环节，本文盘点了 Python 中常用的 PDF 解析库，包括 pypdf、pdfminer.six、pypdfium2、pdfplumber 等，并对各库的功能、适用场景和性能进行了对比分析，为技术选型提供参考。

## 核心要点

- pypdf：纯 Python 实现，适合内容规整的简单 PDF 场景
- pdfminer.six：可提取文本位置、字体、大小等详细信息，支持布局分析
- pypdfium2：基于 C++ 的 PDFium 引擎，性能优于纯 Python 库，支持渲染为图片
- pdfplumber：基于 pdfminer.six，表格提取能力强，提供可视化调试功能

## 布局分析

- PDF 由一系列对象及其结构信息组成，不包含段落、句子等语义结构
- 布局分析三阶段：字符→单词/行→文本框→层次结构
- 关键参数：字符间距、行间距、行重叠（LAParams 类）

## References

- [[concepts/检索增强生成]]
- [[concepts/高级-rag]]
- [[entities/llamaindex]]