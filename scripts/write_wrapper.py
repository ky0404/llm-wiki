#!/usr/bin/env python3
"""
统一写入封装 - 确保所有写入都经过路径保护检查

使用方法：
    from write_wrapper import write_file, write_text
    
    # 写入文件（自动检查是否受保护）
    write_file("AGENTS.md", content)  # 需要授权
    write_file("wiki/sources/test.md", content)  # 不需要授权
    
    # 写入文件（简化版）
    write_text("wiki/my-learning-path/test.md", "内容")

注意：此模块会自动加载 path_guard 的所有功能
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入 path_guard 的所有功能
from path_guard import (
    is_protected_path,
    safe_write,
    safe_write_with_lock,
    authorize_write,
    revoke_authorization,
    is_authorized,
    log_protection,
    ALLOW_GUARD_OVERRIDE,
    GuardLock
)


def write_file(path: str, content: str, authorized: bool = False, auth_version: str = "") -> bool:
    """
    统一文件写入入口 - 自动检查保护路径
    
    Args:
        path: 文件路径（相对或绝对）
        content: 要写入的内容
        authorized: 是否已获得授权
        auth_version: 授权版本号
    
    Returns:
        bool: True 写入成功，False 被拦截或失败
    
    使用示例：
        # 需要授权的写入
        auth_version = authorize_write("AGENTS.md", "更新规则")
        write_file("AGENTS.md", new_content, authorized=True, auth_version=auth_version)
        
        # 普通写入（不需要授权）
        write_file("wiki/my-learning-path/test.md", "内容")
    """
    return safe_write(path, content, authorized, auth_version)


def write_file_with_lock(path: str, content: str, authorized: bool = False, auth_version: str = "") -> bool:
    """
    带锁的文件写入 - 防止并发冲突
    
    Args:
        path: 文件路径
        content: 要写入的内容
        authorized: 是否已获得授权
        auth_version: 授权版本号
    
    Returns:
        bool: True 写入成功，False 被拦截或失败
    """
    return safe_write_with_lock(path, content, authorized, auth_version)


def write_text(path: str, content: str) -> bool:
    """
    简化的文本写入 - 用于非保护路径
    
    Args:
        path: 文件路径
        content: 要写入的文本
    
    Returns:
        bool: True 写入成功，False 失败
    """
    if is_protected_path(path):
        log_protection(path, "拦截", f"尝试写入受保护路径 {path}，未获得授权", authorized=False)
        print(f"错误：{path} 是受保护路径，需要授权才能写入", file=sys.stderr)
        return False
    
    try:
        path_obj = Path(path)
        PROJECT_ROOT = Path("/home/dukkha/wiki")
        
        if not path_obj.is_absolute():
            full_path = PROJECT_ROOT / path_obj
        else:
            full_path = path_obj
        
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"错误：写入失败 - {e}", file=sys.stderr)
        return False


def check_and_warn(path: str) -> bool:
    """
    检查路径是否受保护，给出警告
    
    Args:
        path: 文件路径
    
    Returns:
        bool: True 表示受保护，False 表示可自由写入
    """
    protected = is_protected_path(path)
    if protected:
        print(f"⚠️ 警告：{path} 是受保护路径", file=sys.stderr)
        print(f"   如需写入，请先获取授权：", file=sys.stderr)
        print(f"   python scripts/path_guard.py authorize \"{path}\" \"原因\"", file=sys.stderr)
    return protected


if __name__ == "__main__":
    print("统一写入封装 - write_wrapper.py")
    print("=" * 50)
    print("提供以下函数：")
    print("  write_file(path, content, authorized, auth_version)")
    print("  write_file_with_lock(path, content, authorized, auth_version)")  
    print("  write_text(path, content)")
    print("  check_and_warn(path)")
    print("")
    print("导入方式：")
    print("  from scripts.write_wrapper import write_file, write_text")