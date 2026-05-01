---
title: Model Context Protocol (MCP)
type: concept
tags: [AI, protocol, integration]
sources: [understanding-model-context-protocol-mcp]
created: 2026-04-29
updated: 2026-04-29
---

# Model Context Protocol (MCP)

## 定义
Model Context Protocol (MCP) 是一个开放标准，旨在定义 AI 应用与外部资源和工具的通信方式，解决 AI 系统获取数据的统一接入问题。

## 核心设计原则
1. **安全第一**：细粒度权限控制，沙箱执行
2. **供应商中立**：适用于任何 AI 模型或平台
3. **开发者体验**：简单实现，强大可用
4. **可扩展性**：从单工具到企业级生态

## 架构组件
- **MCP Client**：运行在 AI 应用端（如 Claude、Custom Apps、IDEs）
- **MCP Server**：连接各类资源（数据库、文件系统、API 网关、工具）

## 解决的问题
| 传统方案问题 | MCP 解决方案 |
|------------|------------|
| 供应商锁定 | 通用接口，一次编写到处使用 |
| 安全风险 | 设计即安全，精细权限控制 |
| 维护开销 | 共享服务器市场 |
| 有限复用 | 协议演进不破坏兼容 |

## 企业收益
- 降低开发成本
- 加快上市时间
- 增强安全性
- 供应商灵活性

## References
- [[sources/understanding-model-context-protocol-mcp]] - MCP 协议学习笔记
- [[synthesis/llm-工作流对比]] - CLAUDE.md、README.zh.md、llm-wiki.md 工作流对比