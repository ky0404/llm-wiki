---
title: Edward Hu
type: entity
tags: [研究人员, ai, lora]
sources: [2106.09685v2.md]
created: 2026-04-29
updated: 2026-04-29
---

# Edward Hu

## 概述

Microsoft 研究员，LoRA（低秩适应）方法的主要贡献者。

## 教育背景

- 不详

## 职业经历

- Microsoft Research 研究员
- 专注于大规模语言模型的高效微调

## 主要贡献

### 1. LoRA（低秩适应）
- 提出参数高效的微调方法
- 通过低秩分解减少可训练参数
- 实现无推理延迟的适配

### 2. 核心创新
- 冻结预训练权重，注入可训练的低秩矩阵
- 可训练参数减少 10,000 倍
- GPU 内存需求减少 3 倍

## 技术特点

- **参数高效**：仅需微调 0.01% 的参数
- **无推理延迟**：权重可合并，无额外计算开销
- **快速任务切换**：替换低秩矩阵即可切换任务
- **广泛适用**：在 RoBERTa、DeBERTa、GPT-2、GPT-3 上验证有效

## 开源贡献

- 发布 LoRA 的 PyTorch 实现包
- 提供预训练模型检查点
- 促进参数高效微调的研究和应用

## 关联论文



## References


- [[concepts/参数高效微调]]
- [[concepts/低秩分解]]
- [[entities/microsoft]]