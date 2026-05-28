#!/usr/bin/env python3
"""
Code Graph Agent - GitHub仓库自动拉取模块
功能：支持输入GitHub仓库地址，自动拉取main分支的代码文件
"""

import os
import subprocess
import shutil
from typing import List, Dict, Optional
from urllib.parse import urlparse


class GitHubCloner:
    """GitHub仓库拉取器"""

    def __init__(self, clone_dir: str = "/tmp/code_graph_repos"):
        self.clone_dir = clone_dir
        os.makedirs(clone_dir, exist_ok=True)

    def parse_github_url(self, url: str) -> Optional[Dict]:
        """解析GitHub URL"""
        # 支持多种格式：
        # - https://github.com/user/repo
        # - github.com/user/repo
        # - user/repo (需要加 https:// 前缀)
        
        # 如果没有协议，自动添加
        if "://" not in url:
            url = "https://" + url
        
        parsed = urlparse(url)
        
        if "github.com" in parsed.netloc:
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2:
                return {
                    "owner": path_parts[0],
                    "repo": path_parts[1].replace(".git", ""),
                    "url": f"https://github.com/{path_parts[0]}/{path_parts[1].replace('.git', '')}"
                }
        return None

    def clone_repo(self, repo_url: str, branch: str = "main") -> Optional[str]:
        """克隆仓库"""
        parsed = self.parse_github_url(repo_url)
        if not parsed:
            print(f"无效的GitHub URL: {repo_url}")
            return None
        
        repo_path = os.path.join(self.clone_dir, parsed["repo"])
        
        # 如果已存在，先删除
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        
        try:
            # 克隆仓库（浅克隆，只拉取最新版本）
            cmd = [
                "git", "clone",
                "--depth", "1",
                "--branch", branch,
                "--single-branch",
                parsed["url"],
                repo_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ 仓库克隆成功: {parsed['repo']}")
                return repo_path
            else:
                print(f"✗ 克隆失败: {result.stderr}")
                return None
        except Exception as e:
            print(f"✗ 克隆异常: {e}")
            return None

    def list_code_files(self, repo_path: str) -> List[Dict]:
        """列出仓库中的代码文件"""
        code_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C Header',
            '.cs': 'C#',
            '.rb': 'Ruby',
            '.php': 'PHP',
        }
        
        # 过滤的非核心目录
        exclude_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'dist', 'build', '.pytest_cache', '.mypy_cache',
            '.tox', 'coverage', '.coverage', 'htmlcov',
            'vendor', 'third_party', 'test', 'tests', 'example',
            '.github', '.idea', '.vscode', 'docs', 'doc'
        }
        
        code_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # 过滤目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in code_extensions:
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, repo_path)
                    
                    # 获取文件大小
                    size = os.path.getsize(filepath)
                    
                    code_files.append({
                        'path': rel_path,
                        'absolute_path': filepath,
                        'language': code_extensions[ext],
                        'size': size
                    })
        
        return code_files

    def filter_core_files(self, code_files: List[Dict], min_size: int = 100) -> List[Dict]:
        """过滤核心文件（排除空文件和测试文件）"""
        core_files = []
        
        for f in code_files:
            # 排除过小的文件
            if f['size'] < min_size:
                continue
            
            # 排除测试文件
            if 'test' in f['path'].lower() or 'tests' in f['path'].lower():
                continue
            
            core_files.append(f)
        
        return core_files


def main():
    """测试GitHub拉取功能"""
    cloner = GitHubCloner()
    
    # 测试URL解析
    test_urls = [
        "https://github.com/microsoft/GraphEngine",
        "github.com/facebook/react",
        "microsoft/GraphEngine"
    ]
    
    print("=== GitHub URL解析测试 ===")
    for url in test_urls:
        result = cloner.parse_github_url(url)
        print(f"{url} → {result}")
    
    # 模拟列出本地一个目录作为测试
    test_path = "/mnt/d/projects/wiki/wiki"
    if os.path.exists(test_path):
        files = cloner.list_code_files(test_path)
        print(f"\n=== 测试列出代码文件 ===")
        print(f"共找到 {len(files)} 个代码文件")
        
        # 过滤核心文件
        core = cloner.filter_core_files(files)
        print(f"核心文件: {len(core)} 个")
        
        # 显示前5个
        for f in core[:5]:
            print(f"  - {f['path']} ({f['language']}, {f['size']} bytes)")


if __name__ == "__main__":
    main()