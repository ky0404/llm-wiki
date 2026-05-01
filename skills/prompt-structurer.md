---
name: prompt-structurer
description: 结构化提示词设计专家。Use when crafting complex prompts, designing AI agent system prompts, or building reusable prompt templates. Covers modular design with Role, Profile, Goals, Constraints, Skills, Workflow and Initialization.
license: MIT
---

# Prompt Structurer

基于 LangGPT 结构化提示词方法论，提供模块化提示词设计标准。

## 1. Core Modules（核心模块）

### Role（角色）
指定角色让模型聚焦对应领域：
```markdown
# Role: 知识库管理员
```

### Profile（档案）
作者、版本、描述等元数据：
```markdown
## Profile
- Author: YZFly
- Version: 1.0
- Description: 专精于知识库维护的AI助手
```

### Goals（目标）
一句话描述目标，聚焦 Attention：
```markdown
## Goals
维护知识库健康，确保链接完整、索引同步、内容一致
```

### Constraints（约束）
帮助模型"剪枝"，减少不必要分支：
```markdown
## Constraints
- 不修改 raw/ 目录中的原始文件
- 任何修改后必须同步图谱
- 大规模变更需先获取批准
```

### Skills（技能）
强化对应领域的信息权重：
```markdown
## Skills
- 检测断裂 wikilinks
- 补全缺失 frontmatter
- 识别知识结构洞
- 执行图谱同步
```

### Workflow（工作流）
**最重要的模块**，指定对话和输出方式：
```markdown
## Workflow
1. 诊断：扫描知识库状态
2. 报告：列出发现的问题
3. 修复：对高/中自治权问题执行修复
4. 验证：确保修复有效
5. 记录：追加 log.md
```

### Initialization（初始化）
冷启动对白，强调重点：
```markdown
## Initialization
作为知识库管理员，我必须遵守 AGENTS.md 规范。
所有操作必须记录到 log.md，包含回滚计划。
```

## 2. Design Principles（设计原则）

1. **模块化**：每个模块职责单一，可独立调整
2. **可验证**：每个约束都有明确的检查方法
3. **可复用**：模板化设计，一次创建多处使用
4. **渐进式**：从简单开始，根据反馈迭代

## 3. Anti-Patterns（避免）

- 模糊的约束（如"尽量做好"）
- 矛盾的指令
- 过长的工作流（超过7步需拆分）
- 缺少验证机制的目标

## 4. YAML Alternative（YAML 替代格式）

```yaml
name: 角色名称
description: 一句话描述角色和适用场景
context:
  - 上下文信息1
  - 上下文信息2
rules:
  - 规则1
  - 规则2
workflow:
  - 步骤1
  - 步骤2
```

## 5. Few-shot Examples

### 简单示例：翻译助手
```markdown
# Role: 翻译助手

## Profile
- language: 中文
- expertise: 中英互译

## Goals
准确、自然地将中文翻译为英文，或英文翻译为中文

## Constraints
- 保持原文风格
- 必要时添加脚注解释文化背景
- 不添加解释性内容

## Workflow
1. 识别文本类型（正式/口语/技术）
2. 执行翻译
3. 校对一致性

## Initialization
我是一个专业的翻译助手，擅长中英互译。请提供需要翻译的文本。
```

### 复杂示例：代码审查员
```markdown
# Role: 代码审查员

## Profile
- expertise: Python, JavaScript, 系统设计
- experience: 10年

## Goals
提供高质量代码审查，发现潜在问题并给出改进建议

## Constraints
- 识别安全漏洞
- 检查性能瓶颈
- 验证测试覆盖率
- 不修改代码，仅提供建议

## Skills
- 静态代码分析
- 模式识别
- 最佳实践建议

## Workflow
1. 理解代码功能
2. 逐函数审查
3. 识别问题
4. 提供修复建议
5. 总结改进点

## Initialization
请提供需要审查的代码，我将逐块分析并提供改进建议。
```

## 6. Quality Checklist

设计完成后验证：
- [ ] Role 明确且具体
- [ ] Goals 可度量
- [ ] Constraints 不模糊
- [ ] Skills 与 Goals 一致
- [ ] Workflow 可执行（步骤 ≤7）
- [ ] Initialization 引导清晰

## 7. Context Integration（上下文集成）

将结构化提示词与上下文工程结合：
```markdown
## Context Loading
- 启动时加载 CLAUDE.md
- 遇到代码时自动读取相关文件
- 使用渐进式披露加载技能

## Memory Strategy
- 短期：对话历史
- 长期：NOTES.md 文件系统
```

## 8. Skill Metadata

**适用场景**：复杂提示词设计、Agent 系统提示、模板构建
**核心方法**：模块化 + 可验证 + 可复用
**关键资源**：LangGPT 知识库