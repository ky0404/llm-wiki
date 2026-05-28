#!/usr/bin/env python3
"""
Code Graph Agent - 3路混合检索脚本
基于RAG混合检索技术，增加图谱检索适配逻辑

检索通道：
1. 向量检索：语义理解
2. BM25检索：关键词匹配
3. 图谱检索：结构关系
"""

import os
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

# 尝试导入依赖库
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    print("警告：未安装 rank-bm25，请运行: pip install rank-bm25")
    BM25Okapi = None

try:
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    print("警告：未安装 langchain，请运行: pip install langchain langchain-community langchain-openai")
    Chroma = None
    OpenAIEmbeddings = None


@dataclass
class CodeSearchResult:
    """代码搜索结果"""
    content: str
    source: str
    score: float
    retrieval_type: str  # vector/bm25/graph


class CodeGraphHybridRetriever:
    """代码仓库3路混合检索器"""

    def __init__(self, repo_path: str, vector_store_path: str = None, k: int = 60):
        self.repo_path = repo_path
        self.k = k
        
        # 存储各通道的索引
        self.vectorstore = None
        self.bm25_index = None
        self.graph_index = None
        
        # 代码文件列表
        self.code_files = []
        
        self._init_indexes(vector_store_path)

    def _init_indexes(self, vector_store_path: str = None):
        """初始化各检索通道的索引"""
        
        # 1. 收集代码文件
        print("初始化检索索引...")
        self._collect_code_files()
        
        # 2. 初始化BM25索引
        if BM25Okapi:
            self._init_bm25()
        
        # 3. 初始化向量索引
        if vector_store_path and Chroma and OpenAIEmbeddings:
            self._init_vectorstore(vector_store_path)
        
        # 4. 初始化图谱索引
        self._init_graph_index()
        
        print(f"索引初始化完成：{len(self.code_files)} 个代码文件")

    def _collect_code_files(self):
        """收集代码仓库中的所有代码文件"""
        supported_exts = ['.py', '.js', '.ts', '.java', '.go', '.rs', '.c', '.cpp', '.h']
        
        for root, dirs, files in os.walk(self.repo_path):
            # 跳过系统目录
            if any(x in root for x in ['.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build']):
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in supported_exts):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.repo_path)
                    self.code_files.append({
                        'path': rel_path,
                        'abs_path': filepath
                    })

    def _init_bm25(self):
        """初始化BM25索引"""
        documents = []
        for cf in self.code_files:
            try:
                with open(cf['abs_path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(content)
            except:
                pass
        
        tokenized_docs = [doc.split() for doc in documents]
        self.bm25_index = BM25Okapi(tokenized_docs)
        print(f"BM25索引构建完成：{len(documents)} 个文档")

    def _init_vectorstore(self, vector_store_path: str):
        """初始化向量索引"""
        try:
            self.vectorstore = Chroma(
                persist_directory=vector_store_path,
                embedding_function=OpenAIEmbeddings()
            )
            print(f"向量索引加载完成")
        except Exception as e:
            print(f"向量索引加载失败: {e}")

    def _init_graph_index(self):
        """初始化图谱索引（简化版：从文件路径和函数名构建）"""
        self.graph_index = []
        
        for cf in self.code_files:
            try:
                with open(cf['abs_path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 提取函数名（简化版）
                    import re
                    functions = re.findall(r'def (\w+)\(|function (\w+)\(|class (\w+)', content)
                    
                    for func in functions:
                        func_name = func[0] or func[1] or func[2]
                        self.graph_index.append({
                            'file': cf['path'],
                            'function': func_name,
                            'content': content
                        })
            except:
                pass
        
        print(f"图谱索引构建完成：{len(self.graph_index)} 个函数/类")

    def search(self, query: str, top_k: int = 5) -> List[CodeSearchResult]:
        """执行3路混合检索"""
        
        results = []
        
        # 1. 向量检索
        if self.vectorstore:
            vector_results = self.vectorstore.similarity_search_with_score(query, k=top_k)
            for doc, score in vector_results:
                results.append(CodeSearchResult(
                    content=doc.page_content,
                    source=doc.metadata.get('source', 'unknown'),
                    score=score,
                    retrieval_type='vector'
                ))
        
        # 2. BM25检索
        if self.bm25_index:
            tokenized_query = query.split()
            bm25_scores = self.bm25_index.get_scores(tokenized_query)
            ranked = sorted(enumerate(bm25_scores), key=lambda x: x[1], reverse=True)
            
            for i, score in ranked[:top_k]:
                if i < len(self.code_files):
                    try:
                        with open(self.code_files[i]['abs_path'], 'r', encoding='utf-8') as f:
                            content = f.read()
                        results.append(CodeSearchResult(
                            content=content[:2000],  # 限制长度
                            source=self.code_files[i]['path'],
                            score=score,
                            retrieval_type='bm25'
                        ))
                    except:
                        pass
        
        # 3. 图谱检索（基于函数名/类名匹配）
        graph_results = self._graph_search(query, top_k)
        results.extend(graph_results)
        
        # 4. RRF融合
        final_results = self._rrf_fusion(results, top_k)
        
        return final_results

    def _graph_search(self, query: str, top_k: int) -> List[CodeSearchResult]:
        """图谱检索：基于函数名/类名匹配"""
        results = []
        query_lower = query.lower()
        
        for item in self.graph_index:
            # 函数名/类名匹配
            if query_lower in item['function'].lower():
                results.append(CodeSearchResult(
                    content=item['content'][:2000],
                    source=item['file'],
                    score=1.0,  # 高相关性
                    retrieval_type='graph'
                ))
        
        # 按相关性排序
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def _rrf_fusion(self, results: List[CodeSearchResult], top_k: int) -> List[CodeSearchResult]:
        """RRF融合：合并3路检索结果"""
        
        doc_scores = {}
        doc_contents = {}
        
        for r in results:
            # 去重：按source+content前100字符
            key = f"{r.source}:{r.content[:100]}"
            
            if r.retrieval_type == 'vector':
                rank = results.index(r) + 1
            elif r.retrieval_type == 'bm25':
                rank = results.index(r) + 1
            else:  # graph
                rank = 1  # 图谱结果优先
            
            rrf_score = 1 / (self.k + rank)
            
            if key in doc_scores:
                doc_scores[key] += rrf_score
            else:
                doc_scores[key] = rrf_score
                doc_contents[key] = r
        
        # 排序
        sorted_keys = sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)
        
        final_results = []
        for key in sorted_keys[:top_k]:
            r = doc_contents[key]
            r.score = doc_scores[key]
            final_results.append(r)
        
        return final_results


def main():
    """测试脚本"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python hybrid_retriever.py <代码仓库路径> [查询内容]")
        print("示例: python hybrid_retriever.py /path/to/repo \"用户认证函数\"")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    query = sys.argv[2] if len(sys.argv) > 2 else "测试查询"
    
    retriever = CodeGraphHybridRetriever(repo_path)
    results = retriever.search(query)
    
    print(f"\n查询: {query}")
    print(f"结果: {len(results)} 个\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r.retrieval_type}] {r.source}")
        print(f"   分数: {r.score:.4f}")
        print(f"   内容: {r.content[:100]}...")
        print()


if __name__ == "__main__":
    main()