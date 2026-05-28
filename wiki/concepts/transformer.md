---
title: Transformer
type: concept
tags: [模型架构, 深度学习, nlp]
sources: [1706.03762v7.md]
created: 2026-04-28
updated: 2026-04-29
---

# Transformer

## 概述

基于纯注意力机制的序列到序列架构。

## 核心组件

- **Multi-Head Self-Attention**：多头自注意力
- **Position-wise Feed-Forward**：逐位置前馈网络
- **Residual Connection**：残差连接
- **Layer Normalization**：层归一化
- **Positional Encoding**：位置编码

## 复杂度对比

| 层类型 | 复杂度 | 顺序操作 | 最大路径 |
| --- | --- | --- | --- |
| 自注意力 | O(n²·d) | O(1) | O(1) |
| 循环 | O(n·d²) | O(n) | O(n) |
| 卷积 | O(k·n·d²) | O(1) | O(log_k n) |

## 后续发展

- [[wiki/concepts/bert]]
- [[wiki/concepts/gpt]]
- [[wiki/concepts/参数高效微调]]

## References

- [[wiki/sources/transformer-paper]]
- [[wiki/entities/google-brain]]
- [[wiki/entities/google-research]]