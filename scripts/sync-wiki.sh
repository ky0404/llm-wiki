#!/bin/bash
# sync-wiki.sh — Bidirectional sync between WSL and Windows
# Supports two modes: git (via GitHub) and rsync (local, no network needed)
#
# Usage:
#   ./scripts/sync-wiki.sh              # full local rsync sync (default)
#   ./scripts/sync-wiki.sh rsync        # same as default
#   ./scripts/sync-wiki.sh rsync-push   # WSL → Windows only
#   ./scripts/ssync-wiki.sh rsync-pull  # Windows → WSL only
#   ./scripts/sync-wiki.sh git-full     # git pull + push via GitHub
#   ./scripts/sync-wiki.sh git-push     # git push WSL → GitHub
#   ./scripts/sync-wiki.sh git-pull     # git pull GitHub → WSL
#   ./scripts/sync-wiki.sh status       # show sync status

set -euo pipefail

WSL_DIR="$HOME/wiki"
WIN_DIR="/mnt/d/projects/wiki"
BRANCH="main"

RSYNC_EXCLUDES=(
    --exclude='.git'
    --exclude='node_modules'
    --exclude='__pycache__'
    --exclude='.obsidian'
    --exclude='.gc_backups'
    --exclude='.next'
    --exclude='frontend/node_modules'
    --exclude='frontend/.next'
)

cd "$WSL_DIR"

cmd="${1:-rsync}"

info()  { echo -e "\033[36m[INFO]\033[0m $*"; }
ok()    { echo -e "\033[32m[OK]\033[0m $*"; }
warn()  { echo -e "\033[33m[WARN]\033[0m $*"; }
err()   { echo -e "\033[31m[ERROR]\033[0m $*"; }

commit_if_needed() {
    local dir="$1"
    local label="$2"
    if [ -n "$(git -C "$dir" status --porcelain 2>/dev/null)" ]; then
        info "$label has uncommitted changes — auto-committing..."
        git -C "$dir" add -A
        git -C "$dir" commit -m "sync: auto-commit $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
    fi
}

do_rsync_push() {
    info "RSync WSL → Windows (newer files only)..."
    rsync -av --update "${RSYNC_EXCLUDES[@]}" "$WSL_DIR/" "$WIN_DIR/" 2>&1 | tail -5
    commit_if_needed "$WIN_DIR" "Windows"
    ok "WSL → Windows sync done"
}

do_rsync_pull() {
    info "RSync Windows → WSL (newer files only)..."
    rsync -av --update "${RSYNC_EXCLUDES[@]}" "$WIN_DIR/" "$WSL_DIR/" 2>&1 | tail -5
    commit_if_needed "$WSL_DIR" "WSL"
    ok "Windows → WSL sync done"
}

do_rsync() {
    do_rsync_push
    do_rsync_pull
    ok "=== RSync sync complete ==="
}

do_git_push() {
    commit_if_needed "$WSL_DIR" "WSL"
    local ahead
    ahead=$(git rev-list --count "origin/$BRANCH..HEAD" 2>/dev/null || echo "0")
    if [ "$ahead" -gt 0 ]; then
        info "WSL is $ahead commit(s) ahead — pushing to GitHub..."
        git push origin "$BRANCH" 2>&1 || { err "Push failed"; return 1; }
        ok "Pushed to GitHub"
    else
        ok "WSL already in sync with GitHub"
    fi
}

do_git_pull() {
    commit_if_needed "$WSL_DIR" "WSL"
    info "Pulling from GitHub into WSL..."
    git pull origin "$BRANCH" --rebase 2>&1 || { err "Pull failed"; return 1; }
    ok "WSL repo is up to date with GitHub"
}

do_git_full() {
    do_git_pull
    do_git_push
    info "Pulling into Windows repo..."
    commit_if_needed "$WIN_DIR" "Windows"
    git -C "$WIN_DIR" pull origin "$BRANCH" --rebase 2>&1 || { err "Windows pull failed"; return 1; }
    ok "=== Git sync complete ==="
}

do_status() {
    echo ""
    echo "=== Wiki Sync Status ==="
    echo ""
    echo "WSL ($WSL_DIR):"
    if [ -n "$(git -C "$WSL_DIR" status --porcelain 2>/dev/null)" ]; then
        warn "  Uncommitted changes"
    else
        ok "  Clean working tree"
    fi
    local wsl_ahead wsl_behind
    wsl_ahead=$(git -C "$WSL_DIR" rev-list --count "origin/$BRANCH..HEAD" 2>/dev/null || echo "?")
    wsl_behind=$(git -C "$WSL_DIR" rev-list --count "HEAD..origin/$BRANCH" 2>/dev/null || echo "?")
    echo "  Ahead: $wsl_ahead  Behind: $wsl_behind"
    echo ""
    if [ -d "$WIN_DIR/.git" ]; then
        echo "Windows ($WIN_DIR):"
        if [ -n "$(git -C "$WIN_DIR" status --porcelain 2>/dev/null)" ]; then
            warn "  Uncommitted changes"
        else
            ok "  Clean working tree"
        fi
        local win_ahead win_behind
        win_ahead=$(git -C "$WIN_DIR" rev-list --count "origin/$BRANCH..HEAD" 2>/dev/null || echo "?")
        win_behind=$(git -C "$WIN_DIR" rev-list --count "HEAD..origin/$BRANCH" 2>/dev/null || echo "?")
        echo "  Ahead: $win_ahead  Behind: $win_behind"
    else
        warn "Windows repo not found at $WIN_DIR"
    fi
    echo ""
}

case "$cmd" in
    rsync)          do_rsync ;;
    rsync-push)     do_rsync_push ;;
    rsync-pull)     do_rsync_pull ;;
    git-full)       do_git_full ;;
    git-push)       do_git_push ;;
    git-pull)       do_git_pull ;;
    status)         do_status ;;
    full)           do_git_full ;;
    *)
        echo "Usage: $0 {rsync|rsync-push|rsync-pull|git-full|git-push|git-pull|status}"
        echo ""
        echo "  rsync        RSync bidirectional (default, no network needed)"
        echo "  rsync-push   RSync WSL → Windows only"
        echo "  rsync-pull   RSync Windows → WSL only"
        echo "  git-full     Git pull + push via GitHub"
        echo "  git-push     Git push WSL → GitHub"
        echo "  git-pull     Git pull GitHub → WSL"
        echo "  status       Show sync status"
        exit 1
        ;;
esac
