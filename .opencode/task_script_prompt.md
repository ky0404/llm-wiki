# 任务脚本生成模式

当收到复杂多步骤任务时，必须按以下格式响应：

## 响应格式

### 1. 任务分析（3行以内）
[任务类型] ingest / lint / theory / practice / interview
[涉及文件] 预计操作的文件列表
[预计步骤] N 步

### 2. 生成可执行脚本
立即生成完整的 bash 脚本到 `/tmp/wiki_task.sh`，脚本必须包含：
- `set -euo pipefail`（错误立即退出）
- 每步操作前 `echo "[步骤N/总数] 描述..."`
- 每步完成后 `echo "✓ 完成"`
- 最后追加 log.md 记录
- 最后运行 `python3 scripts/fts_index.py update && python3 scripts/generate_graph_and_cache.py`

### 3. 一次性执行
```bash
bash /tmp/wiki_task.sh 2>&1 | tee /tmp/wiki_task_output.txt
```

### 4. 输出执行摘要
- 更新的文件：X 个
- 归档位置：my-learning-path/xxx/
- RTK 节省：运行 `rtk gain`
- 求职亮点：本次操作对应的面试价值

## 禁止行为
- 禁止一步一步交互式询问确认
- 禁止单次操作超过 5 个文件不拆分
- 禁止遇到小错误就停下来报告
