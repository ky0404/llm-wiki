#!/usr/bin/env python3
"""
Code Graph Agent - 代码仓库3路混合检索引擎（升级版）
功能：适配代码仓库的检索场景，优化代码片段的向量化、关键词检索、图谱检索逻辑
"""

import os
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
import json


@dataclass
class CodeSearchResult:
    """代码搜索结果"""
    content: str
    file_path: str
    line_range: str
    score: float
    retrieval_type: str  # vector/bm25/graph


class CodeHybridRetriever:
    """代码仓库3路混合检索器"""

    def __init__(self, repo_path: str, k: int = 60):
        self.repo_path = repo_path
        self.k = k
        self.code_files = []
        self.graph_data = None
        
        self._load_code_files()
        self._load_graph_data()

    def _load_code_files(self):
        """加载代码文件"""
        supported_exts = ['.py', '.js', '.ts', '.java', '.go', '.rs', '.c', '.cpp']
        
        for root, dirs, files in os.walk(self.repo_path):
            # 跳过系统目录
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'venv', 'node_modules', 'test'}]
            
            for file in files:
                if any(file.endswith(ext) for ext in supported_exts):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.repo_path)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取代码片段（函数、类）
                        chunks = self._extract_code_chunks(content, rel_path)
                        
                        self.code_files.append({
                            'path': rel_path,
                            'content': content,
                            'chunks': chunks
                        })
                    except:
                        pass

    def _extract_code_chunks(self, content: str, file_path: str) -> List[Dict]:
        """提取代码块（函数、类）"""
        chunks = []
        
        # 匹配函数定义
        func_pattern = r'def (\w+)\([^)]*\):'
        class_pattern = r'class (\w+)[^:]*:'
        
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 函数
            func_match = re.match(func_pattern, line)
            if func_match:
                func_name = func_match.group(1)
                # 提取函数体（简化版：取接下来20行）
                chunk_content = '\n'.join(lines[i:i+20])
                chunks.append({
                    'type': 'function',
                    'name': func_name,
                    'content': chunk_content,
                    'start_line': i + 1
                })
            
            # 类
            class_match = re.match(class_pattern, line)
            if class_match:
                class_name = class_match.group(1)
                chunk_content = '\n'.join(lines[i:i+30])
                chunks.append({
                    'type': 'class',
                    'name': class_name,
                    'content': chunk_content,
                    'start_line': i + 1
                })
            
            i += 1
        
        return chunks

    def _load_graph_data(self):
        """加载图谱数据（从代码解析结果）"""
        # 尝试加载已有的图谱数据
        graph_file = os.path.join(self.repo_path, ".code_graph.json")
        
        if os.path.exists(graph_file):
            try:
                with open(graph_file, 'r') as f:
                    self.graph_data = json.load(f)
            except:
                self.graph_data = None

    def search(self, query: str, top_k: int = 5) -> List[CodeSearchResult]:
        """执行3路混合检索"""
        
        results = []
        
        # 1. 关键词检索（代码特征匹配）
        keyword_results = self._keyword_search(query, top_k * 2)
        results.extend(keyword_results)
        
        # 2. 图谱检索（函数/类名匹配）
        graph_results = self._graph_search(query, top_k * 2)
        results.extend(graph_results)
        
        # 3. 语义检索（简化版：基于函数/类名的模糊匹配）
        semantic_results = self._semantic_search(query, top_k * 2)
        results.extend(semantic_results)
        
        # 4. RRF融合
        final_results = self._rrf_fusion(results, top_k)
        
        return final_results

    def _keyword_search(self, query: str, limit: int) -> List[CodeSearchResult]:
        """关键词搜索"""
        results = []
        query_words = query.lower().split()
        
        for cf in self.code_files:
            content = cf['content'].lower()
            
            # 计算匹配分数
            match_count = sum(1 for word in query_words if word in content)
            
            if match_count > 0:
                # 提取相关片段
                for chunk in cf['chunks']:
                    chunk_content = chunk['content'].lower()
                    chunk_match = sum(1 for word in query_words if word in chunk_content)
                    
                    if chunk_match > 0:
                        results.append(CodeSearchResult(
                            content=chunk['content'][:500],
                            file_path=cf['path'],
                            line_range=f"{chunk['start_line']}-{chunk['start_line']+20}",
                            score=float(chunk_match),
                            retrieval_type='keyword'
                        ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def _graph_search(self, query: str, limit: int) -> List[CodeSearchResult]:
        """图谱检索：基于函数名/类名匹配"""
        results = []
        query_lower = query.lower()
        
        # 提取查询中的关键词（函数名/类名）
        # 例如："数据从传感器到数据库经过了哪几步" -> 提取"传感器"、"数据库"等
        
        for cf in self.code_files:
            for chunk in cf['chunks']:
                chunk_name = chunk['name'].lower()
                
                # 精确匹配
                if query_lower in chunk_name or chunk_name in query_lower:
                    results.append(CodeSearchResult(
                        content=chunk['content'][:500],
                        file_path=cf['path'],
                        line_range=f"{chunk['start_line']}-{chunk['start_line']+20}",
                        score=2.0,  # 高分
                        retrieval_type='graph'
                    ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def _semantic_search(self, query: str, limit: int) -> List[CodeSearchResult]:
        """语义检索（简化版）"""
        results = []
        
        # 简单的语义规则匹配
        semantic_rules = {
            '数据': ['data', 'database', 'db', 'storage', 'save'],
            '传感器': ['sensor', 'adc', 'gpio', 'input'],
            '网络': ['network', 'wifi', 'http', 'request', 'api'],
            '处理': ['process', 'handle', 'parse', 'transform'],
            'API': ['api', 'endpoint', 'route', 'view'],
            'FastAPI': ['fastapi', 'app', 'router', 'endpoint'],
            'ESP32': ['esp', 'uart', 'i2c', 'spi', 'ble'],
        }
        
        query_lower = query.lower()
        
        for cf in self.code_files:
            content_lower = cf['content'].lower()
            
            # 检查语义关联
            for key, keywords in semantic_rules.items():
                if key in query_lower:
                    for kw in keywords:
                        if kw in content_lower:
                            # 找到语义关联
                            for chunk in cf['chunks']:
                                if kw in chunk['content'].lower():
                                    results.append(CodeSearchResult(
                                        content=chunk['content'][:500],
                                        file_path=cf['path'],
                                        line_range=f"{chunk['start_line']}-{chunk['start_line']+20}",
                                        score=1.5,
                                        retrieval_type='semantic'
                                    ))
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r.file_path}:{r.line_range}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        return unique_results[:limit]

    def _rrf_fusion(self, results: List[CodeSearchResult], top_k: int) -> List[CodeSearchResult]:
        """RRF融合"""
        
        doc_scores = {}
        doc_info = {}
        
        for r in results:
            key = f"{r.file_path}:{r.line_range}"
            
            # 根据检索类型分配排名
            if r.retrieval_type == 'graph':
                rank = 1
            elif r.retrieval_type == 'keyword':
                rank = results.index(r) + 1
            else:
                rank = results.index(r) + 2
            
            rrf_score = 1 / (self.k + rank)
            
            if key in doc_scores:
                doc_scores[key] += rrf_score
            else:
                doc_scores[key] = rrf_score
                doc_info[key] = r
        
        # 排序
        sorted_keys = sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)
        
        final_results = []
        for key in sorted_keys[:top_k]:
            r = doc_info[key]
            r.score = doc_scores[key]
            final_results.append(r)
        
        return final_results


def main():
    """测试代码检索功能"""
    
    # 模拟测试
    retriever = CodeHybridRetriever("/mnt/d/projects/wiki/wiki")
    
    # 测试查询
    test_queries = [
        "数据从传感器到数据库经过了哪几步",
        "FastAPI如何处理请求",
        "ESP32传感器数据采集"
    ]
    
    print("=== 代码仓库检索测试 ===\n")
    
    for query in test_queries:
        print(f"问题: {query}")
        results = retriever.search(query)
        
        print(f"结果: {len(results)} 个\n")
        
        for i, r in enumerate(results[:3], 1):
            print(f"{i}. [{r.retrieval_type}] {r.file_path}:{r.line_range}")
            print(f"   分数: {r.score:.2f}")
            print(f"   内容: {r.content[:100]}...")
            print()


if __name__ == "__main__":
    main()