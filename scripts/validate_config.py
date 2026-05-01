#!/usr/bin/env python3
"""
本地验证脚本 - 仅验证配置格式，不连接任何服务器
"""

import os
import sys
import re
from pathlib import Path

def check_token_format(token: str) -> dict:
    """验证Token格式"""
    result = {"valid": False, "type": "unknown", "message": ""}
    
    if not token:
        result["message"] = "Token为空"
        return result
    
    # GitHub Token格式
    if token.startswith("ghp_"):
        result["valid"] = True
        result["type"] = "Personal Access Token"
        result["message"] = f"Token长度: {len(token)}"
    elif token.startswith("github_pat_"):
        result["valid"] = True
        result["type"] = "Fine-grained PAT"
        result["message"] = f"Token长度: {len(token)}"
    elif re.match(r"^gho_[a-zA-Z0-9]{36}$", token):
        result["valid"] = True
        result["type"] = "OAuth Token"
        result["message"] = "OAuth格式"
    else:
        result["message"] = "Token格式不符合常见类型"
    
    return result

def check_repo_format(repo: str) -> dict:
    """验证Repo格式"""
    result = {"valid": False, "message": ""}
    
    if not repo:
        result["message"] = "Repo为空"
        return result
    
    # 格式: owner/repo
    if "/" in repo:
        parts = repo.split("/")
        if len(parts) == 2 and parts[0] and parts[1]:
            result["valid"] = True
            result["message"] = f"Owner: {parts[0]}, Repo: {parts[1]}"
        else:
            result["message"] = "格式错误，应为 owner/repo"
    else:
        result["message"] = "缺少分隔符/，应为 owner/repo"
    
    return result

def main():
    print("=" * 60)
    print("本地配置验证（不连接服务器）")
    print("=" * 60)
    
    # 方法1：检查环境变量
    token = os.environ.get('GITHUB_TOKEN', '')
    repo = os.environ.get('REPO_PATH', '')
    branch = os.environ.get('BRANCH_NAME', 'main')
    
    print("\n【方法1】环境变量")
    print(f"  GITHUB_TOKEN: {'已配置' if token else '未配置'}")
    print(f"  REPO_PATH: {'已配置' if repo else '未配置'}")
    print(f"  BRANCH_NAME: {branch}")
    
    # 方法2：检查.env文件
    possible_paths = [
        Path(__file__).parent.parent / '.env',
        Path.home() / '.wiki-env',
    ]
    
    print("\n【方法2】.env文件")
    env_found = False
    for p in possible_paths:
        if p.exists():
            print(f"  找到: {p}")
            env_found = True
            with open(p) as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        print(f"    {line.strip()}")
    
    if not env_found:
        print("  未找到.env文件")
    
    # 验证
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    
    # 优先使用环境变量
    config_source = "环境变量"
    if not token:
        # 尝试从文件读取
        for p in possible_paths:
            if p.exists():
                with open(p) as f:
                    for line in f:
                        if line.startswith('GITHUB_TOKEN='):
                            token = line.split('=')[1].strip()
                        if line.startswith('REPO_PATH='):
                            repo = line.split('=')[1].strip()
                config_source = ".env文件"
                break
    
    if token:
        token_result = check_token_format(token)
        print(f"\nToken ({config_source}):")
        print(f"  格式: {token_result['type']}")
        print(f"  有效: {'✓' if token_result['valid'] else '✗'} {token_result['message']}")
    else:
        print("\nToken: ✗ 未配置")
    
    if repo:
        repo_result = check_repo_format(repo)
        print(f"\nRepo ({config_source}):")
        print(f"  有效: {'✓' if repo_result['valid'] else '✗'} {repo_result['message']}")
    else:
        print("\nRepo: ✗ 未配置")
    
    print("\n" + "=" * 60)
    print("安全说明")
    print("=" * 60)
    print("""
本验证脚本：
  ✓ 不连接任何服务器
  ✓ 不推送任何数据
  ✓ 仅检查格式有效性
  ✓ 本地执行，隐私安全
""")

if __name__ == "__main__":
    main()