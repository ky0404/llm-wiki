#!/bin/bash
# auto-sync.sh — Watch ~/wiki and auto-sync changes to D:\projects\wiki
# Usage: ./scripts/auto-sync.sh          (foreground)
#        ./scripts/auto-sync.sh daemon   (background)

WSL_DIR="$HOME/wiki"
WIN_DIR="/mnt/d/projects/wiki"
LOGFILE="$HOME/.wiki-autosync.log"

RSYNC_OPTS=(
    -a
    --update
    --exclude='.git'
    --exclude='node_modules'
    --exclude='__pycache__'
    --exclude='.obsidian'
    --exclude='.gc_backups'
    --exclude='.next'
    --exclude='frontend/node_modules'
    --exclude='frontend/.next'
)

echo "=== Wiki Auto-Sync Started ===" | tee -a "$LOGFILE"
echo "WSL:   $WSL_DIR" | tee -a "$LOGFILE"
echo "Win:   $WIN_DIR" | tee -a "$LOGFILE"
echo "Log:   $LOGFILE" | tee -a "$LOGFILE"
echo "=============================" | tee -a "$LOGFILE"

if [ "${1:-}" = "daemon" ]; then
    nohup "$0" >> "$LOGFILE" 2>&1 &
    echo "Running as PID $! (daemon mode)"
    exit 0
fi

inotifywait -m -r -q \
    --format '%w%f' \
    -e modify -e create -e delete -e moved_to -e moved_from \
    --exclude '(\.git/|__pycache__|\.gc_backups|node_modules|\.next|\.obsidian)' \
    "$WSL_DIR" | while read -r file; do
    echo "[$(date '+%H:%M:%S')] changed: $file" >> "$LOGFILE"
    rsync "${RSYNC_OPTS[@]}" "$WSL_DIR/" "$WIN_DIR/" >> "$LOGFILE" 2>&1
done
