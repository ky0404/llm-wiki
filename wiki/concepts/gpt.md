---
title: GPT
type: concept
tags: [NLP, transformer, language-model, generative]
sources: [transformer-paper]
created: 2026-04-29
updated: 2026-04-29
---

# GPT

## 定义
GPT（Generative Pre-trained Transformer）是由OpenAI开发的基于Transformer的自回归语言模型，仅使用解码器部分，通过左上下文生成文本。

## 核心创新
1. **自回归建模**：仅利用左上下文预测下一个token
2. **预训练-微调范式**：在大规模语料上预训练，然后在下游任务上微调
3. **Transformer解码器堆叠**：多层Transformer解码器堆叠
4. **规模效应**：模型性能随参数量、数据量和计算量呈幂律增长

## 架构
- 基于Transformer解码器（仅保留解码器部分）
- 掩码自注意力（仅关注左侧和当前位置）
- 位置编码
- 前馈神经网络
- 层归一化

## 应用
- 文本生成
- 机器翻译
- 问答系统
- 代码生成（如GitHub Copilot）

## 与其他模型的关系
- [[wiki/concepts/bert]]：双向编码器 vs GPT的单向解码器
- [[wiki/concepts/transformer]]：基础架构
- [[wiki/concepts/参数高效微调]]：可用于高效适配GPT模型

## References
- [[wiki/concepts/transformer]] - Transformer 架构
- [[wiki/concepts/bert]] - 双向编码器表示来自Transformer
- [[wiki/sources/transformer-paper]] - Attention Is All You Need 论文摘要