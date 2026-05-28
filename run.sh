#!/bin/bash
# Wiki 统一启动脚本
# 用法: ./run.sh [frontend|backend|all]

MODE="${1:-all}"
LOG_FILE="/home/dukkha/wiki/logs/run.log"

mkdir -p /home/dukkha/wiki/logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Wiki 启动模式: $MODE ==="

case "$MODE" in
    frontend)
        log "[FRONTEND] 启动前端..."
        cd /home/dukkha/wiki/frontend
        npm run dev >> "$LOG_FILE" 2>&1 &
        log "[FRONTEND] 前端已启动 (PID: $!)"
        ;;
    backend)
        log "[BACKEND] 启动后端..."
        cd /home/dukkha/wiki/api
        python3 main.py >> "$LOG_FILE" 2>&1 &
        log "[BACKEND] 后端已启动 (PID: $!)"
        ;;
    all)
        log "[ALL] 启动前后端..."
        cd /home/dukkha/wiki/frontend
        npm run dev >> "$LOG_FILE" 2>&1 &
        FRONTEND_PID=$!
        
        cd /home/dukkha/wiki/api
        python3 main.py >> "$LOG_FILE" 2>&1 &
        BACKEND_PID=$!
        
        log "[ALL] 前端 PID: $FRONTEND_PID, 后端 PID: $BACKEND_PID"
        log "[ALL] 前端: http://localhost:3000, 后端: http://localhost:8000"
        ;;
    stop)
        pkill -f "next dev" && log "[STOP] 前端已停止" || log "[STOP] 前端未运行"
        pkill -f "python3 main.py" && log "[STOP] 后端已停止" || log "[STOP] 后端未运行"
        ;;
    *)
        echo "用法: $0 [frontend|backend|all|stop]"
        exit 1
        ;;
esac