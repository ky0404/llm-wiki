#!/usr/bin/env python3
"""
Code Graph Agent - Python代码解析引擎
功能：解析Python代码，提取模块、类、函数、调用关系，生成知识图谱节点与边
"""

import os
import re
import ast
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class CodeNode:
    """代码节点"""
    id: str
    type: str  # module, class, function, method
    name: str
    file_path: str
    line_start: int = 0
    line_end: int = 0
    docstring: str = ""
    children: List[str] = field(default_factory=list)


@dataclass
class CodeEdge:
    """代码边"""
    source: str
    target: str
    type: str  # defines, calls, imports, inherits
    file_path: str = ""


class PythonParser:
    """Python代码解析器"""

    def __init__(self):
        self.nodes: Dict[str, CodeNode] = {}
        self.edges: List[CodeEdge] = []
        self.modules: Set[str] = set()
        self.imports: Dict[str, Set[str]] = {}  # file -> set of imports

    def parse_file(self, filepath: str) -> Tuple[List[CodeNode], List[CodeEdge]]:
        """解析单个Python文件"""
        nodes = []
        edges = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析AST
            tree = ast.parse(content, filename=filepath)
            
            file_name = os.path.basename(filepath)
            module_name = os.path.splitext(file_name)[0]
            
            # 创建模块节点
            module_id = f"module:{module_name}"
            module_node = CodeNode(
                id=module_id,
                type="module",
                name=module_name,
                file_path=filepath,
                docstring=ast.get_docstring(tree) or ""
            )
            nodes.append(module_node)
            self.modules.add(module_name)
            
            # 遍历AST节点
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # 类节点
                    class_id = f"class:{module_name}.{node.name}"
                    class_node = CodeNode(
                        id=class_id,
                        type="class",
                        name=node.name,
                        file_path=filepath,
                        line_start=node.lineno,
                        line_end=node.end_lineno or 0,
                        docstring=ast.get_docstring(node) or ""
                    )
                    nodes.append(class_node)
                    
                    # 类继承边
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            edges.append(CodeEdge(
                                source=class_id,
                                target=f"class:{module_name}.{base.id}",
                                type="inherits",
                                file_path=filepath
                            ))
                    
                    # 类方法
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_id = f"method:{module_name}.{node.name}.{item.name}"
                            method_node = CodeNode(
                                id=method_id,
                                type="method",
                                name=item.name,
                                file_path=filepath,
                                line_start=item.lineno,
                                line_end=item.end_lineno or 0,
                                docstring=ast.get_docstring(item) or ""
                            )
                            nodes.append(method_node)
                            
                            # 类定义边
                            edges.append(CodeEdge(
                                source=class_id,
                                target=method_id,
                                type="defines",
                                file_path=filepath
                            ))
                            
                            # 函数调用边
                            self._extract_calls(item, method_id, module_name, filepath, edges)
                
                elif isinstance(node, ast.FunctionDef):
                    # 顶层函数
                    func_id = f"function:{module_name}.{node.name}"
                    func_node = CodeNode(
                        id=func_id,
                        type="function",
                        name=node.name,
                        file_path=filepath,
                        line_start=node.lineno,
                        line_end=node.end_lineno or 0,
                        docstring=ast.get_docstring(node) or ""
                    )
                    nodes.append(func_node)
                    
                    # 模块定义边
                    edges.append(CodeEdge(
                        source=module_id,
                        target=func_id,
                        type="defines",
                        file_path=filepath
                    ))
                    
                    # 函数调用边
                    self._extract_calls(node, func_id, module_name, filepath, edges)
            
            # 提取imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.setdefault(module_name, set()).add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.imports.setdefault(module_name, set()).add(node.module)
            
        except Exception as e:
            print(f"解析失败 {filepath}: {e}")
        
        return nodes, edges

    def _extract_calls(self, func_node: ast.FunctionDef, func_id: str, module_name: str, 
                       filepath: str, edges: List[CodeEdge]):
        """提取函数调用"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                # 获取被调用的函数名
                if isinstance(node.func, ast.Name):
                    target_name = node.func.id
                    # 尝试匹配本地函数或类方法
                    target_id = f"function:{module_name}.{target_name}"
                    if target_id not in [e.source for e in edges if e.type == "defines"]:
                        # 可能是外部函数
                        target_id = f"external:{target_name}"
                    
                    edges.append(CodeEdge(
                        source=func_id,
                        target=target_id,
                        type="calls",
                        file_path=filepath
                    ))
                elif isinstance(node.func, ast.Attribute):
                    # 方法调用
                    if isinstance(node.func.value, ast.Name):
                        class_name = node.func.value.id
                        method_name = node.func.attr
                        target_id = f"method:{module_name}.{class_name}.{method_name}"
                        
                        edges.append(CodeEdge(
                            source=func_id,
                            target=target_id,
                            type="calls",
                            file_path=filepath
                        ))

    def parse_directory(self, dir_path: str) -> Tuple[List[CodeNode], List[CodeEdge]]:
        """解析整个目录"""
        all_nodes = []
        all_edges = []
        
        for root, dirs, files in os.walk(dir_path):
            # 跳过非代码目录
            dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', 'venv', 'tests', 'test'}]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    nodes, edges = self.parse_file(filepath)
                    all_nodes.extend(nodes)
                    all_edges.extend(edges)
        
        # 去重
        self.nodes = {n.id: n for n in all_nodes}
        self.edges = all_edges
        
        return all_nodes, all_edges

    def get_graph_data(self) -> Dict:
        """获取图谱数据"""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "type": n.type,
                    "name": n.name,
                    "file": n.file_path,
                    "doc": n.docstring[:100] if n.docstring else ""
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {"from": e.source, "to": e.target, "type": e.type}
                for e in self.edges
            ]
        }


def main():
    """测试代码解析功能"""
    parser = PythonParser()
    
    # 解析一个测试文件
    test_file = "/mnt/d/projects/wiki/wiki/scripts/update_graph.py"
    
    if os.path.exists(test_file):
        nodes, edges = parser.parse_file(test_file)
        
        print(f"=== 解析结果 ===")
        print(f"节点数: {len(nodes)}")
        print(f"边数: {len(edges)}")
        
        # 显示节点
        print("\n节点:")
        for n in nodes[:10]:
            print(f"  - {n.id} ({n.type})")
        
        # 显示边
        print("\n边:")
        for e in edges[:10]:
            print(f"  - {e.source[:50]} → {e.target[:50]} ({e.type})")
    
    # 显示图谱数据
    graph_data = parser.get_graph_data()
    print(f"\n图谱节点数: {len(graph_data['nodes'])}")
    print(f"图谱边数: {len(graph_data['edges'])}")


if __name__ == "__main__":
    main()