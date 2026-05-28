#!/bin/bash
# 每次 opencode 启动任务前自动执行
# 1. 更新 FTS 索引（增量，通常 <1s）
python3 scripts/fts_index.py update 2>/dev/null

# 2. 根据用户输入生成精简 system prompt
# $1 = 用户输入（opencode 会传入）
if [ -n "$1" ]; then
    python3 scripts/slim_loader.py build "$1" > ~/wiki/opencode.md
else
    python3 scripts/slim_loader.py build "wiki维护" > ~/wiki/opencode.md
fi

echo "[pre_task] system_prompt 已更新，大小: $(wc -c < .opencode/system_prompt.txt) bytes"
