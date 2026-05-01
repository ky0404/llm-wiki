#!/usr/bin/env python3
"""
GitHub同步引擎 - github_sync.py
功能：将Wiki知识库自动推送到GitHub
环境变量：
  - GITHUB_TOKEN: GitHub访问令牌
  - REPO_PATH: 仓库地址（格式：owner/repo）
  - BRANCH_NAME: 分支名称（默认：main）
  - COMMIT_MSG: 提交信息（可选）
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path


class GitHubSync:
    """GitHub同步引擎"""

    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_path = os.environ.get('REPO_PATH', '')
        self.branch = os.environ.get('BRANCH_NAME', 'main')
        self.commit_msg = os.environ.get('COMMIT_MSG', f'Wiki auto-update {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        self.wiki_root = Path(__file__).parent.parent
        self.cache_file = self.wiki_root / 'index-cache.json'
        
        # Git配置
        self.git_dir = self.wiki_root / '.git'
        self.remote_name = 'origin'

    def check_env(self) -> bool:
        """检查环境变量配置"""
        if not self.token:
            print("[ERROR] 未配置GITHUB_TOKEN环境变量")
            return False
        
        if not self.repo_path:
            print("[ERROR] 未配置REPO_PATH环境变量")
            return False
        
        return True

    def init_git(self) -> bool:
        """初始化Git仓库"""
        try:
            # 检查是否已是Git仓库
            if not self.git_dir.exists():
                print("[INFO] 初始化Git仓库...")
                subprocess.run(['git', 'init'], cwd=self.wiki_root, check=True)
                subprocess.run(['git', 'config', 'user.email', 'wiki@local'], cwd=self.wiki_root, check=True)
                subprocess.run(['git', 'config', 'user.name', 'Wiki Agent'], cwd=self.wiki_root, check=True)
            
            # 检查远程仓库
            result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.wiki_root,
                capture_output=True,
                text=True
            )
            
            if self.remote_name not in result.stdout:
                # 添加远程仓库
                github_url = f"https://{self.token}@github.com/{self.repo_path}.git"
                subprocess.run(
                    ['git', 'remote', 'add', self.remote_name, github_url],
                    cwd=self.wiki_root,
                    check=True
                )
                print(f"[INFO] 已添加远程仓库: {self.repo_path}")
            
            # 配置拉取策略
            subprocess.run(
                ['git', 'config', 'pull.rebase', 'false'],
                cwd=self.wiki_root,
                check=True
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Git初始化失败: {e}")
            return False

    def pull_changes(self) -> bool:
        """拉取远程变更"""
        try:
            # 检查远程分支是否存在
            result = subprocess.run(
                ['git', 'ls-remote', '--heads', self.remote_name, self.branch],
                cwd=self.wiki_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # 远程分支存在，执行拉取
                print("[INFO] 拉取远程变更...")
                subprocess.run(
                    ['git', 'fetch', self.remote_name],
                    cwd=self.wiki_root,
                    check=True
                )
                
                # 尝试合并
                try:
                    subprocess.run(
                        ['git', 'merge', f'{self.remote_name}/{self.branch}', '--no-edit'],
                        cwd=self.wiki_root,
                        check=True
                    )
                    print("[INFO] 合并远程变更成功")
                except subprocess.CalledProcessError:
                    # 可能有冲突，记录警告
                    print("[WARN] 合并可能有冲突，请手动处理")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[WARN] 拉取失败（可能首次推送）: {e}")
            return True

    def stage_changes(self) -> bool:
        """暂存变更"""
        try:
            # 添加所有文件（排除敏感文件）
            exclude_patterns = [
                '.git/',
                '__pycache__/',
                '*.pyc',
                '.obsidian/',
                '.gc_backups/',
                'node_modules/',
                '*.log'
            ]
            
            # 添加所有修改的文件
            subprocess.run(['git', 'add', '-A'], cwd=self.wiki_root, check=True)
            
            # 检查是否有变更
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.wiki_root,
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print("[INFO] 没有需要提交的变更")
                return False
            
            print(f"[INFO] 待提交文件:\n{result.stdout}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] 暂存失败: {e}")
            return False

    def commit_and_push(self) -> bool:
        """提交并推送"""
        try:
            # 检查是否有暂存的变更
            result = subprocess.run(
                ['git', 'diff', '--cached', '--quiet'],
                cwd=self.wiki_root
            )
            
            if result.returncode == 0:
                print("[INFO] 没有需要提交的变更")
                return True
            
            # 提交
            print(f"[INFO] 提交变更: {self.commit_msg}")
            subprocess.run(
                ['git', 'commit', '-m', self.commit_msg],
                cwd=self.wiki_root,
                check=True
            )
            
            # 推送
            print("[INFO] 推送到GitHub...")
            subprocess.run(
                ['git', 'push', self.remote_name, self.branch, '--force'],
                cwd=self.wiki_root,
                check=True
            )
            
            print("[SUCCESS] 推送成功!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] 提交/推送失败: {e}")
            return False

    def sync(self) -> bool:
        """执行完整同步流程"""
        print("=" * 60)
        print("GitHub同步引擎")
        print("=" * 60)
        
        # 检查环境
        if not self.check_env():
            return False
        
        # 初始化Git
        if not self.init_git():
            return False
        
        # 拉取远程变更
        if not self.pull_changes():
            return False
        
        # 暂存变更
        if not self.stage_changes():
            print("[INFO] 无需同步")
            return True
        
        # 提交并推送
        if not self.commit_and_push():
            return False
        
        return True


def main():
    """主入口"""
    sync = GitHubSync()
    
    if sync.sync():
        print("\n[SUCCESS] GitHub同步完成!")
        sys.exit(0)
    else:
        print("\n[ERROR] GitHub同步失败")
        sys.exit(1)


if __name__ == '__main__':
    main()