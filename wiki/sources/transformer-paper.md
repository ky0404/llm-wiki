---
title: Attention Is All You Need
type: source
tags: [论文, transformer, 注意力机制]
sources: [1706.03762v7.pdf]
created: 2026-04-29
updated: 2026-04-29
---

# Attention Is All You Need 论文摘要

## 核心要点
- 提出 Transformer 架构，完全基于注意力机制
- 摒弃循环和卷积结构，实现完全并行化训练
- 使用多头注意力机制捕捉不同子空间的信息
- 在机器翻译任务上达到 SOTA 性能

## 关键创新
- **自注意力机制**：允许模型关注序列中的所有位置
- **多头注意力**：并行运行多个注意力函数
- **位置编码**：为序列顺序信息提供表示
- **残差连接与层归一化**：稳定深度网络训练

## 架构要点
- 编码器-解码器结构
- 6层编码器，6层解码器
- 8个注意力头，512维模型
- 使用缩放点积注意力

## References
- [[wiki/concepts/transformer]] - Transformer 架构概念
- [[wiki/concepts/注意力机制]] - 注意力机制详解
- [[wiki/concepts/多头注意力]] - 多头注意力机制
- [[wiki/concepts/缩放点积注意力]] - 缩放点积注意力
- [[wiki/entities/ashish-vaswani]] - 第一作者
- [[wiki/entities/noam-shazeer]] - 关键贡献者
- [[wiki/entities/google-brain]] - 研究机构
