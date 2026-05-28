#!/usr/bin/env python3
"""
路径保护工具 - 用于保护治理性文件不被误修改

功能：
- 判断路径是否受保护
- 安全写入封装（受保护路径需要授权）
- 日志记录
- 授权版本号管理

用法：
    from path_guard import is_protected_path, safe_write, authorize_write, revoke_authorization
    
    if is_protected_path("AGENTS.md"):
        print("受保护路径，禁止直接写入")
    
    # 方式1：手动授权
    safe_write("AGENTS.md", new_content, authorized=True)
    
    # 方式2：使用授权版本号（推荐）
    auth_version = authorize_write("AGENTS.md", "修改原因说明")
    if auth_version:
        safe_write("AGENTS.md", new_content, authorized=True, auth_version=auth_version)
"""

import os
import sys
import json
import uuid
import shutil
import fcntl
from pathlib import Path
from datetime import datetime
from typing import Optional

# 项目根目录
PROJECT_ROOT = Path("/home/dukkha/wiki")

# 受保护路径列表
PROTECTED_PATHS = [
    "AGENTS.md",
    "skills/",
    "synthesis/knowledge-base-evolution-",
]

# 日志文件
LOG_FILE = PROJECT_ROOT / "log.md"

# 授权状态文件
AUTH_FILE = PROJECT_ROOT / ".guard_authorizations.json"

# 锁文件
LOCK_FILE = PROJECT_ROOT / ".guard.lock"

# 全局开关：允许临时绕过保护（需配合授权版本号使用）
ALLOW_GUARD_OVERRIDE = os.environ.get("ALLOW_GUARD_OVERRIDE", "").lower() == "true"


class LockError(Exception):
    """锁获取失败异常"""
    pass


class GuardLock:
    """全局锁管理器 - 防止并发写入冲突"""
    
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.lock_file = None
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
    
    def acquire(self):
        """获取锁"""
        self.lock_file = open(LOCK_FILE, "w")
        try:
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock_file.close()
            raise LockError(f"无法获取锁，另一个进程可能正在写入")
    
    def release(self):
        """释放锁"""
        if self.lock_file:
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
            self.lock_file.close()
            self.lock_file = None


def safe_write_with_lock(path: str, content: str, authorized: bool = False, auth_version: str = "") -> bool:
    """
    带锁的安全写入（防止并发写入冲突）
    
    Args:
        path: 文件路径
        content: 要写入的内容
        authorized: 是否已获得授权
        auth_version: 授权版本号
    
    Returns:
        bool: True 表示写入成功，False 表示被拦截或失败
    """
    try:
        with GuardLock():
            return safe_write(path, content, authorized, auth_version)
    except LockError as e:
        print(f"错误：{e}", file=sys.stderr)
        log_protection(path, "并发拦截", str(e), authorized=False)
        return False


def load_authorizations() -> dict:
    """加载授权状态"""
    if AUTH_FILE.exists():
        try:
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}


def save_authorizations(auths: dict):
    """保存授权状态"""
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(auths, f, indent=2, ensure_ascii=False)


def generate_auth_version() -> str:
    """生成授权版本号"""
    return f"guard-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"


def authorize_write(path: str, reason: str) -> str:
    """
    授予写入授权
    
    Args:
        path: 文件路径
        reason: 授权原因
    
    Returns:
        str: 授权版本号，如果失败返回空字符串
    """
    if not is_protected_path(path):
        print(f"警告：{path} 不在保护名单内，无需授权")
        return ""
    
    auth_version = generate_auth_version()
    auths = load_authorizations()
    
    auths[auth_version] = {
        "path": path,
        "reason": reason,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    save_authorizations(auths)
    
    # 记录到日志
    log_protection(
        path,
        "授权",
        f"授权版本号: {auth_version}, 原因: {reason}",
        authorized=True
    )
    
    return auth_version


def revoke_authorization(auth_version: str) -> bool:
    """
    撤销授权
    
    Args:
        auth_version: 授权版本号
    
    Returns:
        bool: True 表示撤销成功
    """
    auths = load_authorizations()
    
    if auth_version in auths:
        auths[auth_version]["status"] = "revoked"
        auths[auth_version]["revoked_at"] = datetime.now().isoformat()
        save_authorizations(auths)
        
        log_protection(
            auths[auth_version].get("path", "unknown"),
            "撤销授权",
            f"撤销授权版本号: {auth_version}",
            authorized=False
        )
        return True
    
    return False


def is_authorized(auth_version: str, target_path: str) -> bool:
    """
    检查授权版本号是否对目标路径有效
    
    Args:
        auth_version: 授权版本号
        target_path: 目标文件路径
    
    Returns:
        bool: True 表示授权有效
    """
    if ALLOW_GUARD_OVERRIDE:
        return True
    
    auths = load_authorizations()
    auth = auths.get(auth_version, {})
    
    if auth.get("status") != "active":
        return False
    
    # 检查路径是否匹配
    auth_path = auth.get("path", "")
    if auth_path and auth_path != target_path:
        return False
    
    return True


def is_protected_path(path: str) -> bool:
    """
    判断路径是否受保护
    
    Args:
        path: 文件路径（相对或绝对）
    
    Returns:
        bool: True 表示受保护，False 表示可自由写入
    """
    path_obj = Path(path)
    
    # 转换为相对路径
    if path_obj.is_absolute():
        try:
            path_obj = path_obj.relative_to(PROJECT_ROOT)
        except ValueError:
            return False
    
    path_str = str(path_obj)
    
    # 检查是否匹配受保护路径
    for protected in PROTECTED_PATHS:
        if protected.endswith("/"):
            # 目录前缀匹配
            if path_str.startswith(protected) or path_str.startswith(protected.rstrip("/")):
                return True
        else:
            # 完整文件名匹配（含通配符支持）
            if protected.endswith("*"):
                prefix = protected[:-1]
                if path_str.startswith(prefix):
                    return True
            elif path_str == protected:
                return True
    
    return False


def log_protection(path: str, action: str, reason: str = "", authorized: bool = False, auth_version: str = ""):
    """
    记录保护操作到 log.md
    
    Args:
        path: 文件路径
        action: 操作类型（拦截/授权/回滚）
        reason: 原因说明
        authorized: 是否已获得授权
        auth_version: 授权版本号
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "已通过" if authorized else "待审"
    
    log_entry = f"""
---

{timestamp} 保护操作
操作对象：{path}
触发原因：{reason}
拦截结果：{'已拦截' if not authorized else '已放行'}
授权状态：{status}
授权版本号：{auth_version if auth_version else '-'}
下一步计划：{'执行修改' if authorized else '提交演化提议等待审批'}
"""
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"警告：无法写入日志 - {e}", file=sys.stderr)


def backup_file(path: str) -> str:
    """
    备份文件到 .gc_backups/
    
    Args:
        path: 文件路径
    
    Returns:
        str: 备份文件路径
    """
    backup_dir = PROJECT_ROOT / ".gc_backups"
    backup_dir.mkdir(exist_ok=True)
    
    path_obj = Path(path)
    if path_obj.is_absolute():
        path_obj = path_obj.relative_to(PROJECT_ROOT)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path_obj.name}.{timestamp}.bak"
    backup_path = backup_dir / backup_name
    
    try:
        src = PROJECT_ROOT / path_obj
        if src.exists():
            shutil.copy2(src, backup_path)
            return str(backup_path)
    except Exception as e:
        print(f"警告：备份失败 - {e}", file=sys.stderr)
    
    return ""


def safe_write(path: str, content: str, authorized: bool = False, auth_version: str = "") -> bool:
    """
    安全写入封装
    
    Args:
        path: 文件路径
        content: 要写入的内容
        authorized: 是否已获得授权（默认 False）
        auth_version: 授权版本号（如果使用版本号授权）
    
    Returns:
        bool: True 表示写入成功，False 表示被拦截
    """
    # 检查是否需要授权
    if is_protected_path(path):
        # 如果提供了授权版本号，验证授权
        if auth_version and is_authorized(auth_version, path):
            authorized = True
            authorized = True  # 使用版本号验证通过
        
        if not authorized:
            log_protection(
                path, 
                "拦截", 
                f"尝试写入受保护路径 {path}，未获得授权",
                authorized=False,
                auth_version=auth_version
            )
            print(f"错误：{path} 是受保护路径，需要授权才能写入", file=sys.stderr)
            print(f"提示：使用 authorize_write('{path}', '原因') 获取授权版本号", file=sys.stderr)
            return False
        
        # 已授权，写入前先备份
        backup_file(path)
        log_protection(
            path,
            "授权写入",
            f"已获得授权，写入受保护路径 {path}",
            authorized=True,
            auth_version=auth_version
        )
    
    # 执行写入
    try:
        path_obj = Path(path)
        if path_obj.is_absolute():
            path_obj = path_obj.relative_to(PROJECT_ROOT)
        
        full_path = PROJECT_ROOT / path_obj
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"错误：写入失败 - {e}", file=sys.stderr)
        return False


def test_all():
    """运行所有测试"""
    test_paths = [
        "AGENTS.md",
        "skills/wiki-maintainer.md",
        "wiki/skills/context-engineer.md",
        "wiki/synthesis/knowledge-base-evolution-20260430.md",
        "wiki/sources/test.md",
        "wiki/my-learning-path/test.md",
    ]
    
    print("=" * 50)
    print("路径保护工具测试")
    print("=" * 50)
    
    print("\n【测试1】路径保护判断：")
    print("-" * 40)
    for p in test_paths:
        protected = is_protected_path(p)
        status = "🔴 受保护" if protected else "🟢 可写入"
        print(f"  {p}: {status}")
    
    print("\n【测试2】授权流程：")
    print("-" * 40)
    auth_version = authorize_write("AGENTS.md", "测试授权")
    print(f"  获得授权版本号: {auth_version}")
    
    print("\n【测试3】使用授权版本号写入：")
    print("-" * 40)
    result = safe_write("AGENTS.md", "# Test Content\n", authorized=True, auth_version=auth_version)
    print(f"  写入结果: {'成功' if result else '失败'}")
    
    print("\n【测试4】撤销授权：")
    print("-" * 40)
    revoked = revoke_authorization(auth_version)
    print(f"  撤销结果: {'成功' if revoked else '失败'}")
    
    print("\n【测试5】环境变量覆盖：")
    print("-" * 40)
    print(f"  ALLOW_GUARD_OVERRIDE = {ALLOW_GUARD_OVERRIDE}")
    print("  (设置环境变量 ALLOW_GUARD_OVERRIDE=true 可临时绕过保护)")


def cli():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("""
路径保护工具 CLI
用法:
    python path_guard.py authorize <path> <原因>     - 授予写入授权
    python path_guard.py revoke <授权版本号>          - 撤销授权
    python path_guard.py check <路径>                 - 检查路径是否受保护
    python path_guard.py list                         - 列出所有有效授权
    python path_guard.py status                       - 显示保护状态
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "authorize":
        if len(sys.argv) < 4:
            print("用法: path_guard.py authorize <path> <原因>")
            sys.exit(1)
        path = sys.argv[2]
        reason = sys.argv[3]
        auth_version = authorize_write(path, reason)
        if auth_version:
            print(f"✅ 授权成功")
            print(f"   授权版本号: {auth_version}")
            print(f"   使用方式: safe_write('{path}', content, authorized=True, auth_version='{auth_version}')")
        else:
            print(f"❌ 授权失败: {path} 不在保护名单内")
    
    elif command == "revoke":
        if len(sys.argv) < 3:
            print("用法: path_guard.py revoke <授权版本号>")
            sys.exit(1)
        auth_version = sys.argv[2]
        if revoke_authorization(auth_version):
            print(f"✅ 撤销成功: {auth_version}")
        else:
            print(f"❌ 撤销失败: 未找到授权版本号 {auth_version}")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("用法: path_guard.py check <路径>")
            sys.exit(1)
        path = sys.argv[2]
        protected = is_protected_path(path)
        print(f"{path}: {'🔴 受保护' if protected else '🟢 可写入'}")
    
    elif command == "list":
        auths = load_authorizations()
        active = [(k, v) for k, v in auths.items() if v.get("status") == "active"]
        if active:
            print("有效授权列表:")
            for auth_version, info in active:
                print(f"  {auth_version}")
                print(f"    路径: {info.get('path')}")
                print(f"    原因: {info.get('reason')}")
                print(f"    创建: {info.get('created_at')}")
        else:
            print("无有效授权")
    
    elif command == "status":
        print("=" * 50)
        print("保护状态")
        print("=" * 50)
        print(f"受保护路径数: {len(PROTECTED_PATHS)}")
        auths = load_authorizations()
        active = sum(1 for v in auths.values() if v.get("status") == "active")
        print(f"有效授权数: {active}")
        print(f"环境变量覆盖: {ALLOW_GUARD_OVERRIDE}")
        print(f"全局锁: 已启用")
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] not in ["test", "tests"]:
        cli()
    else:
        test_all()