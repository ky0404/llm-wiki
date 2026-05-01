---
title: Knowledge Base Evolution Rules — 2026-04-30
type: synthesis
tags: [evolution, rules, governance, meta]
sources: [AGENTS.md]
created: 2026-04-30
updated: 2026-04-30
---

# Knowledge Base Evolution Rules — 2026-04-30

## 1) 知识库的最优状态定义
指标与目标（可重复计算）：
- **页面完整性**：> 95%
- **链接健康度**：> 99%
- **平均出边密度**：每页 5-10（可定量调整）
- **孤岛率**：< 5%
- **枢纽度均衡**：最高连接数 / 平均连接数 < 5

解释：目标确保知识库结构完整、链接健康且不过度依赖单点。

## 2) 自我修复触发条件与优先级
触发条件（自动检测）：
- 链接健康度低于阈值（< 95%）时触发断链修复
- 孤岛率超出阈值（> 5%）时触发孤岛救援
- frontmatter 不完整时触发元数据补全

优先级分配：
- **高**：断链修复、孤岛救援
- **中**：元数据补全、链接补全
- **低**：结构优化与梳理类改动

## 3) 知识库演化方向
未来 3-6 个月发展方向：
- 跨模态知识点的引入
- 产业级应用案例的 syntheses
- 概念合并与层级化管理
- 增量图谱更新策略
- 语义相似度自动补链

## 4) 禁忌清单
绝对不应该做的事：
- 删除页面除非重复或垃圾内容
- 修改已发布的 synthesis 页面，除非有重大更新
- 添加超过 3 级深度的链接嵌套
- 手动编辑 index-cache.json：必须通过 scripts/update_graph.py 全量重写
- 在 output/ 或 log.md 变动后触发级联同步：防死循环机制

## 5) 阶段日志模板
每次阶段性改动应追加日志段落：
```
阶段/日期：YYYY-MM-DD
操作对象：如 AGENTS.md、脚本、页面、边、节点、图谱输出
变更摘要（What/Why/How）
风险与回滚计划
结果摘要（边数、节点数、健康度、核心节点等）
下一步计划
```

## References
- [[AGENTS.md]] - 操作规范
- [[synthesis/knowledge-base-health-report-20260430]] - 健康度报告
- [[synthesis/graph-audit-20260430]] - 图谱审计
