## Compaction 触发规则

当以下任一条件满足时，**立即**执行 /compact 并重置上下文：
1. 完成一个独立子任务（ingest / health-check / 理论学习 / 面试准备 任意一个）
2. 对话轮次 ≥ 15 轮
3. 上下文占用估算 ≥ 70%（不要等到 92%）

Compaction 前必须：
- 将本轮核心结论写入 scratchpad.md
- 确认 log.md 已更新
- 确认 FTS 索引已同步（python3 scripts/fts_index.py update）

Compaction 后自动执行：
- python3 scripts/slim_loader.py build "<下一个任务描述>" > .opencode/system_prompt.txt
