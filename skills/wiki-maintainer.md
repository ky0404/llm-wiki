---
name: wiki-maintainer
description: LLM Wiki 知识库维护与自优化。Use when performing ingest, lint, health checks, or structural hole repairs on the knowledge base. Covers autonomous diagnosis, graph synchronization, and garbage collection.
license: MIT
---

# Wiki Maintainer

基于 AGENTS.md 自治行动准则与演化规则，提供知识库维护的标准工作流。

## 1. Ingest Pipeline（摄入管线）

处理 raw/ 新文件时的标准流程：
1. 对比 `index-cache.json` 与 `raw/` 内容，识别新增文件
2. 读取文件内容，提取核心要点（5-8条）
3. 在 `wiki/sources/` 创建摘要页（含完整 frontmatter）
4. 识别概念/实体，创建或更新对应页面
5. 发现跨文件关联，创建综合分析页
6. 更新 `index.md`、`index-cache.json`、`log.md`
7. **自动执行** `python3 scripts/update_graph.py`

**约束**：不修改 raw/ 文件；新页面必须有 frontmatter 和 ## References。

## 2. Health Check（健康检查）

每次 lint 必须检查：
- **断链**：`[[wikilinks]]` 指向不存在的页面
- **幽灵条目**：缓存中有但文件不存在的条目
- **孤立页面**：无入链的页面（排除 index/log/AGENTS）
- **缺失 frontmatter**：不以 `---` 开头的页面
- **结构洞**：共享 ≥2 标签但无直接链接的页面

**工具**：优先使用 `python3 scripts/comprehensive_gc.py`。

## 3. Autonomous Fix Protocol（自主修复协议）

### 高自治权（自动执行，仅记录）
- 断链修复：寻找相关页面替换或创建占位页
- 元数据补全：根据正文自动补全 title、tags
- 图谱同步：任何业务页面修改后立即执行 build graph
- 语法污染清理：将示例 `[[页面名称]]` 替换为行内代码

### 中自治权（仅记录建议，等待批准）
- 结构洞填补（共享 ≥2 标签自动，<2 仅建议）
- 页面重构与合并
- 性能与查询优化

### 低自治权（严禁操作）
- 大规模重写（>5 文件）
- 修改本 Skill 或 AGENTS.md 本身

## 4. Evolution Protocol（演化协议）

每次操作后，若揭示新规则，在 log.md 追加：
```
[进化提议] 新增规则：规则标题。在 X 阶段/操作时，必须 Y。理由：Z。
```

## 5. Graph Synchronization（图谱同步）

**强制规则**：任何对 wikilinks 或页面内容的修改，在更新完 `index-cache.json` 后，必须立即执行：
```bash
python3 scripts/update_graph.py
```

## 6. Garbage Collection（垃圾回收）

定期执行（建议每周）：
```bash
python3 scripts/comprehensive_gc.py --auto
python3 scripts/verify_tools.py
```

检测六类问题：孤立文件、缺失节点、自环、重复边、孤立节点、悬空边。

## 7. Context Window Management

当执行复杂维护任务时，需注意：
- **92% 阈值**：Claude Code 自动触发压缩
- **信息分段**：将任务分解为可独立验证的子任务
- **状态持久化**：使用 `scratchpad.md` 记录进度

## 8. Quality Gates（质量门禁）

每个维护操作后验证：
- [ ] frontmatter 完整（title, type, tags, created, updated）
- [ ] wikilinks 无断裂
- [ ] 图谱同步完成
- [ ] log.md 已更新

## 9. Rollback Protocol（回滚协议）

操作失败时：
1. 停止当前操作
2. 记录错误到 log.md
3. 使用 `.gc_backups/` 回滚缓存
4. 报告问题，等待人工介入

## 10. Skill Metadata

**适用场景**：ingest、lint、health check、结构洞修复
**自治级别**：高（自动执行）+ 中（仅建议）
**关键工具**：update_graph.py, comprehensive_gc.py, verify_tools.py