#!/usr/bin/env python3
"""更多模块功能测试"""
import sys
import os
sys.path.insert(0, 'highlight')
sys.path.insert(0, 'qa')

print('=' * 60)
print('更多模块功能测试')
print('=' * 60)

# 1. 图谱高亮模块
print('\n【1】图谱高亮模块')
try:
    from graph_highlighter import GraphHighlighter

    highlighter = GraphHighlighter()

    test_mermaid = '''flowchart LR
    A[输入] --> B[处理] --> C[输出]
    B --> D[中间节点]'''

    highlighted = highlighter.highlight_path(test_mermaid, ['B', 'D'])
    print('  ✓ 路径高亮功能 - 通过')
except Exception as e:
    print(f'  ✗ 路径高亮功能 - 失败: {e}')

# 2. 问答接口
print('\n【2】问答接口')
try:
    from qa_interface import QAInterface
    qa = QAInterface()
    print('  ✓ QA接口 - 通过')
except Exception as e:
    print(f'  ✗ QA接口 - 失败: {e}')

# 3. 检查scripts目录
print('\n【3】scripts目录内容')
scripts_path = 'scripts'
if os.path.exists(scripts_path):
    for f in os.listdir(scripts_path):
        if f.endswith('.py'):
            print(f'  - {f}')

# 4. 检查graph目录
print('\n【4】graph目录内容')
graph_path = 'graph'
if os.path.exists(graph_path):
    for f in os.listdir(graph_path):
        print(f'  - {f}')

# 5. 测试混合检索脚本
print('\n【5】原始混合检索脚本')
try:
    sys.path.insert(0, 'scripts')
    from hybrid_retriever import HybridRetriever
    print('  ✓ HybridRetriever - 通过')
except Exception as e:
    print(f'  ✗ HybridRetriever - 失败: {e}')

print('\n' + '=' * 60)
print('全部功能总结')
print('=' * 60)
print('''
╔═══════════════════════════════════════════════════════════════╗
║                   Code Graph Agent 功能全家桶                  ║
╠═══════════════════════════════════════════════════════════════╣
║  核心模块 (upgrade/)                                           ║
║  ├── github_cloner.py       GitHub仓库拉取                    ║
║  ├── code_parser.py        Python代码AST解析                   ║
║  ├── code_hybrid_retriever.py  3路混合检索引擎                 ║
║  └── code_graph_system.py   集成系统（问答+图谱）               ║
╠═══════════════════════════════════════════════════════════════╣
║  辅助模块                                                      ║
║  ├── highlight/graph_highlighter.py   路径高亮                 ║
║  └── qa/qa_interface.py      问答接口封装                       ║
╠═══════════════════════════════════════════════════════════════╣
║  原始脚本 (scripts/)                                          ║
║  └── hybrid_retriever.py    3路混合检索（向量+BM25+图谱）      ║
╠═══════════════════════════════════════════════════════════════╣
║  生成内容 (graph/)                                            ║
║  ├── nodes.md             节点定义                            ║
║  ├── edges.md             边定义                               ║
║  └── rag-knowledge-graph.md  可视化图谱                        ║
╚═══════════════════════════════════════════════════════════════╝
''')