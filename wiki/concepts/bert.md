---
title: BERT
type: concept
tags: [NLP, transformer, language-model]
sources: [transformer-paper]
created: 2026-04-29
updated: 2026-04-29
---

# BERT

## 定义
BERT（Bidirectional Encoder Representations from Transformers）是由Google开发的基于Transformer的双向语言模型，能够同时考虑左右上下文。

## 核心创新
1. **双向编码**：使用Transformer编码器，同时考虑左右上下文
2. **掩码语言建模（MLM）**：随机掩码输入中的一些token，预测被掩码的token
3. **下一句预测（NSP）**：预测两个句子是否连续出现

## 架构
- 基于Transformer编码器堆叠
- 使用位置编码
- 多头自注意力机制
- 前馈神经网络

## 应用
- 自然语言理解任务
- 问答系统
- 情感分析
- 命名实体识别

## 与其他模型的关系
- [[wiki/concepts/gpt]]：单向（仅左上下文）生成模型
- [[wiki/concepts/transformer]]：基础架构
- [[wiki/concepts/参数高效微调]]：可用于高效适配BERT

## References
- [[wiki/concepts/transformer]] - Transformer 架构
- [[wiki/concepts/gpt]] - 生成式预训练变换器
- [[wiki/concepts/rag]] - RAG（检索增强生成）
- [[wiki/sources/transformer-paper]] - Attention Is All You Need 论文摘要