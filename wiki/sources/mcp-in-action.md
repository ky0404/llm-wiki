---
title: 实战 Model Context Protocol
type: source
tags: [mcp, protocol, ai-agent, tools]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

## 摘要

Model Context Protocol（MCP）是 Anthropic 推出的开放协议，用于标准化大模型与外部工具和数据源的交互。本文介绍 MCP 的 C/S 架构、与传统 API 的区别，并实战演示在 Claude Desktop 中配置 MCP Server 以及使用 Python SDK 开发自定义 MCP Server。

## 核心要点

- MCP 架构：主机（Host）+ 客户端（Client）+ 服务器（Server）
- MCP vs API：MCP 如同万能钥匙，统一不同外部资源的接入方式
- MCP Server 提供三种能力：资源（Resources）、工具（Tools）、提示（Prompts）
- 传输协议支持 stdio 和 SSE 两种类型
- 常用 MCP Server：Filesystem、GitHub、Brave Search 等

## 开发 MCP Server

- 使用 FastMCP 简化开发：`@mcp.tool()` 装饰器定义工具
- 通过 `mcp.run(transport='stdio')` 启动服务
- 配置镜像源解决 npx 下载慢的问题

## References

- [[wiki/entities/anthropic]]
- [[wiki/concepts/agent-智能体]]
- [[wiki/concepts/context-engineering]]