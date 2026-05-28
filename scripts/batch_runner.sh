#!/bin/bash
# batch_runner.sh — 批量任务执行器
# 用法: bash scripts/batch_runner.sh "任务描述" [--dry-run]
#
# 原理：让 GLM 生成完整 bash 脚本，再一次性执行，避免边想边执行的卡顿

set -euo pipefail

TASK_DESC="${1:-wiki维护}"
DRY_RUN="${2:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPT_PATH="/tmp/wiki_task_${TIMESTAMP}.sh"
LOG_PATH="log.md"

echo "========================================="
echo "批量任务执行器"
echo "任务：${TASK_DESC}"
echo "时间：$(date)"
echo "========================================="

# 1. 更新 FTS 索引（增量）
echo "[1/4] 更新 FTS 索引..."
rtk python3 scripts/fts_index.py update 2>&1 | tail -5

# 2. 生成精简系统提示词
echo "[2/4] 生成系统提示词..."
python3 scripts/slim_loader.py build "${TASK_DESC}" > ~/wiki/opencode.md
PROMPT_SIZE=$(wc -c < .opencode/system_prompt.txt)
echo "      系统提示词大小：${PROMPT_SIZE} bytes"

# 3. 输出 RTK 累计节省
echo "[3/4] RTK 节省统计："
rtk gain 2>/dev/null || echo "      RTK 统计不可用"

# 4. 启动 opencode（非 dry-run 模式）
echo "[4/4] 启动 OpenCode..."
if [ "${DRY_RUN}" = "--dry-run" ]; then
    echo "      [DRY RUN] 跳过实际启动"
    echo "      系统提示词预览："
    head -20 .opencode/system_prompt.txt
else
    opencode --dangerously-skip-permissions 2>&1
fi

echo "========================================="
echo "任务完成：$(date)"
