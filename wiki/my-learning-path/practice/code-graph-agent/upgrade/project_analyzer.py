#!/usr/bin/env python3
"""
Code Graph Agent - 工程能力模块
包含：配置文件解析、项目结构分析、README生成
"""

import os
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    language: str
    dependencies: List[str]
    test_framework: Optional[str]
    has_docker: bool
    has_requirements: bool


@dataclass
class ProjectStructure:
    """项目结构"""
    root_dirs: List[str]
    source_dirs: List[str]
    test_dirs: List[str]
    config_files: List[str]
    readme_exists: bool


class ProjectAnalyzer:
    """项目分析器"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze_structure(self) -> ProjectStructure:
        """分析项目结构"""
        root_dirs = []
        source_dirs = []
        test_dirs = []
        config_files = []

        try:
            for item in os.listdir(self.repo_path):
                path = os.path.join(self.repo_path, item)

                if os.path.isdir(path):
                    if item.startswith('.'):
                        continue

                    root_dirs.append(item)

                    # 源码目录
                    if item in ['src', 'lib', 'app', 'core', 'code', 'backend']:
                        source_dirs.append(item)

                    # 测试目录
                    if item in ['test', 'tests', '__test__', 'spec']:
                        test_dirs.append(item)

                    # 子目录检查
                    try:
                        for sub in os.listdir(path):
                            sub_path = os.path.join(path, sub)
                            if os.path.isdir(sub_path):
                                if sub in ['src', 'lib', 'app', 'source']:
                                    source_dirs.append(f"{item}/{sub}")
                                elif sub in ['test', 'tests', 'spec']:
                                    test_dirs.append(f"{item}/{sub}")
                    except:
                        pass
                else:
                    # 配置文件
                    if item in ['package.json', 'requirements.txt', 'pyproject.toml',
                               'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle',
                               'Dockerfile', 'docker-compose.yml', '.env.example']:
                        config_files.append(item)

        except Exception as e:
            print(f"分析错误: {e}")

        # 检查README
        readme_exists = any(os.path.exists(os.path.join(self.repo_path, f))
                           for f in ['README.md', 'README.txt', 'README'])

        return ProjectStructure(
            root_dirs=root_dirs,
            source_dirs=source_dirs,
            test_dirs=test_dirs,
            config_files=config_files,
            readme_exists=readme_exists
        )

    def parse_dependencies(self) -> ProjectConfig:
        """解析依赖配置"""
        config = ProjectConfig(
            name=os.path.basename(self.repo_path),
            language='unknown',
            dependencies=[],
            test_framework=None,
            has_docker=False,
            has_requirements=False
        )

        # Python
        if os.path.exists(os.path.join(self.repo_path, 'requirements.txt')):
            config.has_requirements = True
            config.language = 'Python'
            try:
                with open(os.path.join(self.repo_path, 'requirements.txt'), 'r') as f:
                    config.dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except:
                pass

        # JavaScript/TypeScript
        if os.path.exists(os.path.join(self.repo_path, 'package.json')):
            config.language = 'JavaScript/TypeScript'
            try:
                with open(os.path.join(self.repo_path, 'package.json'), 'r') as f:
                    data = json.load(f)
                    config.dependencies = list(data.get('dependencies', {}).keys()) + \
                                       list(data.get('devDependencies', {}).keys())
                    # 检测测试框架
                    if 'jest' in str(data.get('devDependencies', {})):
                        config.test_framework = 'Jest'
                    elif 'mocha' in str(data.get('devDependencies', {})):
                        config.test_framework = 'Mocha'
            except:
                pass

        # Go
        if os.path.exists(os.path.join(self.repo_path, 'go.mod')):
            config.language = 'Go'
            try:
                with open(os.path.join(self.repo_path, 'go.mod'), 'r') as f:
                    for line in f:
                        if line.startswith('require'):
                            parts = line.replace('require', '').strip().split()
                            if parts:
                                config.dependencies.append(parts[0])
            except:
                pass

        # Docker
        config.has_docker = os.path.exists(os.path.join(self.repo_path, 'Dockerfile')) or \
                           os.path.exists(os.path.join(self.repo_path, 'docker-compose.yml'))

        return config

    def generate_readme(self, config: ProjectConfig, structure: ProjectStructure) -> str:
        """生成README"""
        readme = f"""# {config.name}

## 项目信息

- **语言**: {config.language}
- **依赖数量**: {len(config.dependencies)}
- **测试框架**: {config.test_framework or '未检测'}
- **Docker支持**: {'是' if config.has_docker else '否'}

## 项目结构

```
{self.repo_path}/
"""
        for d in structure.root_dirs:
            readme += f"├── {d}/\n"

        readme += "```\n"

        if structure.source_dirs:
            readme += f"\n### 源码目录\n"
            for d in structure.source_dirs:
                readme += f"- `{d}/`\n"

        if structure.test_dirs:
            readme += f"\n### 测试目录\n"
            for d in structure.test_dirs:
                readme += f"- `{d}/`\n"

        if config.dependencies:
            readme += f"\n### 主要依赖 (前10个)\n"
            for dep in config.dependencies[:10]:
                readme += f"- {dep}\n"

        readme += f"""

## 使用说明

请参考项目文档或运行以下命令:

```bash
# 安装依赖
# 查看具体项目类型
```
"""

        return readme


def main():
    """测试项目分析"""
    analyzer = ProjectAnalyzer('/mnt/d/projects/wiki/wiki')

    print('=' * 60)
    print('项目分析功能测试')
    print('=' * 60)

    # 1. 项目结构
    print('\n【1】项目结构分析')
    structure = analyzer.analyze_structure()
    print(f'  根目录: {structure.root_dirs}')
    print(f'  源码目录: {structure.source_dirs}')
    print(f'  测试目录: {structure.test_dirs}')
    print(f'  配置文件: {structure.config_files}')
    print(f'  有README: {structure.readme_exists}')

    # 2. 依赖解析
    print('\n【2】依赖解析')
    config = analyzer.parse_dependencies()
    print(f'  语言: {config.language}')
    print(f'  依赖数: {len(config.dependencies)}')
    print(f'  Docker: {config.has_docker}')

    # 3. README生成
    print('\n【3】README生成')
    readme = analyzer.generate_readme(config, structure)
    print('  ✓ README已生成')
    print(readme[:500])


if __name__ == "__main__":
    main()