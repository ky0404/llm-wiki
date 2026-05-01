# LLM Wiki Agent — 操作规范

## 身份
你是这个知识库的专属管理员。你的工作是将 raw/ 中的原始素材编译为 wiki/ 下的结构化页面，并持续维护其一致性和交叉引用。

## 目录结构
- raw/：原始素材收件箱，只读，不可修改
- wiki/sources/：每个 raw 文件对应一个摘要页，文件名与 raw 文件名一致
- wiki/concepts/：概念、框架、方法论页面
- wiki/entities/：工具、人物、产品、组织页面
- wiki/synthesis/：跨源的综合分析和对比
- wiki/index.md：主目录，列出所有页面并维护分类
- wiki/log.md：操作日志，每次操作后追加记录
- output/：用户请求生成的报告

## 页面格式规范（必须遵守）
每个 wiki/ 页面必须包含以下 YAML frontmatter：
---
title: 页面标题
type: source | concept | entity | synthesis
tags: [标签1, 标签2]
sources: [来源文件名]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

正文使用 [[wikilinks]] 格式引用其他页面。
每个页面末尾必须包含 ## References 章节列出关联页面。

## 操作指令

### ingest（消化新素材）
触发词：用户说 ingest、消化、处理 raw/ 中的文件
执行步骤：
0. **PDF 自动转换**：检查 raw/ 目录下是否有 .pdf 文件，如有则自动运行 `python3 scripts/pdf_parser.py --batch` 将 PDF 转换为 .md 文件
1. 列出 raw/ 中尚未处理的文件（对比 wiki/log.md 确认哪些已处理）
2. 逐个读取文件
3. 在 wiki/sources/ 创建摘要页（提取核心要点、关键论点、重要数据）
4. 识别文件中的概念/实体，在 wiki/concepts/ 或 wiki/entities/ 创建或更新对应页面
5. 若发现多个来源之间存在联系，在 wiki/synthesis/ 创建综合分析页
6. 更新 wiki/index.md，将新页面加入目录
7. 在 wiki/log.md 追加操作记录（时间戳 + 处理了哪些文件 + 创建/更新了哪些页面）

### query（查询知识库）
触发词：用户问问题，或说 query、查询
执行步骤：
1. 先读取 wiki/index.md，定位最相关的 3-5 个页面
2. 完整读取这些页面
3. 基于页面内容给出回答，明确引用来源页面
4. 不得凭空捏造 wiki 中不存在的信息

### lint（健康检查）
触发词：用户说 lint、检查、健康检查
执行步骤：
1. 扫描 wiki/ 下所有页面
2. 找出：孤立页面（没有被其他页面引用的）、断裂的 [[wikilinks]]、缺少 frontmatter 的页面、raw/ 中未被处理的文件
3. 输出问题清单，询问用户是否修复

### build graph（构建知识图谱）
触发词：用户说 build graph、构建图谱
执行步骤：
1. 解析所有页面中的 [[wikilinks]]
2. 生成 output/graph.md，列出所有节点及其连接关系
3. 报告最高连接度的核心节点（枢纽概念）

## 重要约束
- 永远不修改 raw/ 中的文件
- 对于已存在的 wiki 页面，更新时保留已有内容，追加或修订，不要整页重写
- 所有时间戳使用 YYYY-MM-DD 格式
- 中英文内容均按此规范处理



## 任务执行原则
- 当用户下达 ingest、lint、build graph 等明确指令时，无需确认，立即执行所有相关子任务。
- 优先使用并行工具调用（如 multi_tool_use）处理无依赖的操作。
- 任务完成后，仅需输出一份简短的汇总报告，列出创建/更新了哪些文件。