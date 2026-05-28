---
title: Cursor IDE
type: entity
tags: [tool, ide, editor, llm]
sources: [README.zh.md]
created: 2026-04-29
updated: 2026-04-29
---

# Cursor IDE

## 描述
Cursor 是一款专为 AI 辅助编程设计的集成开发环境（IDE），内置了强大的 AI 功能，支持与 LLM 深度集成进行代码生成、重构和调试。

## 属性
- **类型**：集成开发环境（IDE）
- **主要特性**：AI 辅助编程、代码生成、智能重构
- **LLM 集成**：内置 AI 功能，支持与大型语言模型深度协作
- **规则系统**：支持通过规则文件（如 `.cursor/rules/`）定制 AI 行为

## 与 CLAUDE.md 指南的集成
Cursor 支持通过规则文件集成 [[wiki/sources/CLAUDE]]：

### 规则文件
- **位置**：`.cursor/rules/karpathy-guidelines.mdc`
- **作用**：在 Cursor 中应用 Karpathy 启发的编码指南
- **内容**：包含与 CLAUDE.md 类似的行为指导原则

### 集成方式
1. **项目级规则**：在项目根目录的 `.cursor/rules/` 文件夹中添加规则文件
2. **全局规则**：可在多个项目中共享相同的规则
3. **与 Claude Code 的关系**：两者可以互补使用，提供一致的 LLM 编码体验

## 优势
1. **深度 AI 集成**：专门为 AI 辅助编程设计
2. **可定制行为**：通过规则文件控制 AI 的编码风格
3. **一致性**：与 [[wiki/sources/CLAUDE]] 保持一致的编码原则
4. **开发效率**：减少 LLM 编码中的常见错误

## 使用场景
1. **遵循最佳实践**：确保 LLM 生成的代码符合 [[wiki/concepts/llm-编码最佳实践]]
2. **团队协作**：统一团队的 LLM 编码标准
3. **复杂项目**：在大型项目中保持代码质量和一致性
4. **教育用途**：学习如何与 AI 协作编程

## 配置示例
在 Cursor 项目中添加 `.cursor/rules/karpathy-guidelines.mdc`：
```markdown
# Karpathy 启发的编码指南

基于 CLAUDE.md 的原则：
1. 编码前思考：明确假设，呈现权衡
2. 简洁优先：用最少的代码解决问题
3. 精准修改：只碰必须碰的
4. 目标驱动执行：定义成功标准，循环验证
```

## References
- [[wiki/sources/CLAUDE]] - 行为指导原则
- [[wiki/concepts/llm-编码最佳实践]] - 相关概念
- [[wiki/entities/andrej-karpathy]] - 指南灵感来源