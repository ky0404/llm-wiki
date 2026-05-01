#!/bin/bash
#==============================================================================
# Wiki知识库统一执行入口 - run_all.sh
# 功能：一键执行知识库维护全流程（解析、验证、GC、同步）
# 环境变量：GITHUB_TOKEN, REPO_PATH, BRANCH_NAME
#==============================================================================

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WIKI_ROOT="$SCRIPT_DIR"
CACHE_FILE="$WIKI_ROOT/index-cache.json"
LOG_FILE="$WIKI_ROOT/log.md"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#==============================================================================
# 步骤1：解析文件并更新知识图谱
#==============================================================================
step_build_graph() {
    log_info "步骤1：更新知识图谱..."
    cd "$WIKI_ROOT"
    python3 scripts/update_graph.py
    log_info "知识图谱更新完成"
}

#==============================================================================
# 步骤2：工具验证
#==============================================================================
step_verify_tools() {
    log_info "步骤2：工具验证..."
    cd "$WIKI_ROOT"
    python3 scripts/verify_tools.py --root "$WIKI_ROOT" --log "$LOG_FILE"
    log_info "工具验证完成"
}

#==============================================================================
# 步骤3：垃圾回收
#==============================================================================
step_garbage_collection() {
    log_info "步骤3：垃圾回收..."
    cd "$WIKI_ROOT"
    python3 scripts/comprehensive_gc.py --log "$LOG_FILE" --out "synthesis/graph-audit-auto.md"
    log_info "垃圾回收完成"
}

#==============================================================================
# 步骤4：GitHub同步（可选）
#==============================================================================
step_github_sync() {
    if [ -z "$GITHUB_TOKEN" ]; then
        log_warn "未配置GITHUB_TOKEN，跳过GitHub同步"
        return 0
    fi
    
    if [ -z "$REPO_PATH" ]; then
        log_warn "未配置REPO_PATH，跳过GitHub同步"
        return 0
    fi
    
    log_info "步骤4：GitHub同步..."
    cd "$WIKI_ROOT"
    python3 scripts/github_sync.py
    log_info "GitHub同步完成"
}

#==============================================================================
# 主流程
#==============================================================================
main() {
    echo "============================================"
    echo "Wiki知识库自动化维护 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "============================================"
    
    # 显示配置
    echo ""
    log_info "当前配置："
    echo "  - Wiki目录: $WIKI_ROOT"
    echo "  - 缓存文件: $CACHE_FILE"
    echo "  - GitHub Token: ${GITHUB_TOKEN:+已配置}"
    echo "  - 仓库地址: ${REPO_PATH:-未配置}"
    echo "  - 分支: ${BRANCH_NAME:-main}"
    echo ""
    
    # 执行步骤
    START_TIME=$(date +%s)
    
    step_build_graph
    step_verify_tools
    step_garbage_collection
    step_github_sync
    
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo ""
    echo "============================================"
    log_info "全部任务完成！耗时: ${DURATION}秒"
    echo "============================================"
}

#==============================================================================
# 参数解析
#==============================================================================
usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --skip-verify    跳过工具验证"
    echo "  --skip-gc        跳过垃圾回收"
    echo "  --skip-sync      跳过GitHub同步"
    echo "  --dry-run        仅执行验证，不实际修改"
    echo "  -h, --help       显示帮助"
    echo ""
    echo "环境变量:"
    echo "  GITHUB_TOKEN    GitHub访问令牌（必填才同步）"
    echo "  REPO_PATH       远程仓库地址（格式：owner/repo）"
    echo "  BRANCH_NAME     分支名称（默认：main）"
}

SKIP_VERIFY=false
SKIP_GC=false
SKIP_SYNC=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-verify) SKIP_VERIFY=true; shift ;;
        --skip-gc) SKIP_GC=true; shift ;;
        --skip-sync) SKIP_SYNC=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "未知参数: $1"; usage; exit 1 ;;
    esac
done

# 覆盖函数
if [ "$SKIP_VERIFY" = true ]; then
    step_verify_tools() { log_info "跳过工具验证"; }
fi
if [ "$SKIP_GC" = true ]; then
    step_garbage_collection() { log_info "跳过垃圾回收"; }
fi
if [ "$SKIP_SYNC" = true ]; then
    step_github_sync() { log_info "跳过GitHub同步"; }
fi
if [ "$DRY_RUN" = true ]; then
    log_warn "Dry-run模式：仅验证，不实际修改"
    step_build_graph() { 
        log_info "Dry-run：跳过图谱更新"
        python3 scripts/verify_tools.py --dry-run
    }
fi

main