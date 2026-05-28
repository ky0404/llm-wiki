#!/bin/bash
cd ~/wiki
TASK="${1:-}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
opencode stats 2>/dev/null | grep -E "Avg|Sessions|Total Input" | head -3
echo "提示：任务完成后输入 /clear 清空上下文"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/2] 更新 FTS 索引..."
python3 scripts/fts_index.py update 2>&1 | tail -2
echo "[2/2] 生成系统提示词..."
python3 scripts/slim_loader.py build "${TASK:-wiki维护}" > ~/wiki/opencode.md
echo "✓ 就绪，启动 opencode"
opencode