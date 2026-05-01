---
title: 受 Karpathy 启发的 Claude Code 指南
type: source
tags: [llm, coding, guidelines, karpathy, chinese]
sources: [README.zh.md]
created: 2026-04-29
updated: 2026-04-29
---

# 受 Karpathy 启发的 Claude Code 指南摘要

## 核心要点

这是 CLAUDE.md 指南的中文版本，专门为 Claude Code 设计，旨在解决 LLM 编码中的常见问题。该指南源自 Andrej Karpathy 对 LLM 编码陷阱的观察总结。

### 问题所在
LLM 编码存在以下问题：
1. **错误假设**：模型会代你做错误假设，然后不假思索地执行
2. **隐藏困惑**：不管理自身的困惑，不寻求澄清
3. **过度复杂**：喜欢把代码和 API 搞复杂，堆砌抽象概念
4. **无关修改**：有时会改动或删除自己理解不足的代码和注释

### 解决方案：四个原则
| 原则 | 解决什么问题 |
|------|------------|
| **编码前思考** | 错误假设、隐藏困惑、缺少权衡 |
| **简洁优先** | 过度复杂、臃肿抽象 |
| **精准修改** | 无关编辑、触碰不应碰的代码 |
| **目标驱动执行** | 通过测试优先、可验证的成功标准 |

### 核心洞察
来自 Andrej Karpathy 的关键洞察：
> "LLM 非常擅长循环执行直到达成特定目标……不要告诉它该做什么，给它成功标准，然后看着它完成。"

"目标驱动执行"原则正是捕捉了这一点：将指令式指令转化为带有验证循环的声明式目标。

## 关键数据
- 指南包含详细的中文解释和示例
- 提供两种安装方式：Claude Code 插件和 CLAUDE.md 文件
- 包含 Cursor 集成指南（通过 `.cursor/rules/karpathy-guidelines.mdc`）
- 支持项目特定定制，可与现有 CLAUDE.md 合并

## 安装方式
### 选项 A：Claude Code 插件（推荐）
1. 添加插件市场：`/plugin marketplace add forrestchang/andrej-karpathy-skills`
2. 安装插件：`/plugin install andrej-karpathy-skills@karpathy-skills`

### 选项 B：CLAUDE.md（按项目）
- 新项目：使用 curl 下载 CLAUDE.md
- 已有项目：追加到现有 CLAUDE.md 文件

## 定制指南
指南设计用于与项目特定指令合并。可添加项目特定章节，例如：
```markdown
## 项目特定指南
- 使用 TypeScript 严格模式
- 所有 API 端点必须有测试
- 遵循现有错误处理模式
```

## 权衡说明
这些指南倾向于**谨慎而非速度**。对于琐碎任务（简单的拼写错误修复、显而易见的一行修改），请自行判断。目标是减少非琐碎工作中的代价高昂的错误，而不是拖慢简单任务。

## References
- [[sources/CLAUDE]] - 英文原版指南
- [[entities/andrej-karpathy]] - 指南灵感来源
- [[concepts/llm-编码最佳实践]] - 相关概念
- [[concepts/目标驱动编程]] - 相关概念
- [[entities/cursor-ide]] - 集成支持