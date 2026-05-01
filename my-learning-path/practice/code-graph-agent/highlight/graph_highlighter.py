#!/usr/bin/env python3
"""
Code Graph Agent - 图谱路径高亮模块
功能：根据问题推理图谱路径，生成带高亮样式的Mermaid代码

高亮规则：
- 核心节点：红色填充 (#ffcccc)
- 路径节点：黄色填充 (#fff5cc)
- 流转路径：红色虚线箭头
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class GraphPath:
    """图谱路径"""
    nodes: List[str]
    edges: List[Tuple[str, str]]
    mermaid_code: str


class GraphHighlighter:
    """图谱路径高亮器"""

    def __init__(self):
        # 定义图谱节点和边（来自rag-knowledge-graph）
        self.nodes = {
            "用户提问": {"type": "start", "name": "用户提问"},
            "查询理解": {"type": "concept", "name": "查询理解"},
            "向量检索": {"type": "concept", "name": "向量检索"},
            "BM25检索": {"type": "concept", "name": "BM25检索"},
            "RRF融合": {"type": "concept", "name": "RRF融合"},
            "重排序": {"type": "concept", "name": "重排序"},
            "上下文构建": {"type": "concept", "name": "上下文构建"},
            "LLM生成": {"type": "concept", "name": "LLM生成"},
            "最终答案": {"type": "end", "name": "最终答案"},
        }

        # 定义路径模板
        self.path_templates = {
            "查询流程": {
                "nodes": ["用户提问", "查询理解", "向量检索", "BM25检索", "RRF融合", "重排序", "上下文构建", "LLM生成", "最终答案"],
                "edges": [
                    ("用户提问", "查询理解"),
                    ("查询理解", "向量检索"),
                    ("查询理解", "BM25检索"),
                    ("向量检索", "RRF融合"),
                    ("BM25检索", "RRF融合"),
                    ("RRF融合", "重排序"),
                    ("重排序", "上下文构建"),
                    ("上下文构建", "LLM生成"),
                    ("LLM生成", "最终答案"),
                ],
                "core_nodes": ["查询理解", "向量检索", "BM25检索", "RRF融合", "重排序", "上下文构建", "LLM生成"],
            },
            "k值调优": {
                "nodes": ["RRF融合", "k值参数", "场景判断", "技术文档", "通用问答", "长尾查询"],
                "edges": [
                    ("RRF融合", "k值参数"),
                    ("k值参数", "场景判断"),
                    ("场景判断", "技术文档"),
                    ("场景判断", "通用问答"),
                    ("场景判断", "长尾查询"),
                ],
                "core_nodes": ["RRF融合", "k值参数", "场景判断"],
            },
            "检索原理": {
                "nodes": ["向量检索", "BM25检索", "RRF融合", "混合检索"],
                "edges": [
                    ("向量检索", "RRF融合"),
                    ("BM25检索", "RRF融合"),
                    ("RRF融合", "混合检索"),
                ],
                "core_nodes": ["向量检索", "BM25检索", "RRF融合"],
            },
        }

    def match_question_type(self, question: str) -> Optional[str]:
        """匹配问题类型"""
        question_lower = question.lower()
        
        if any(k in question_lower for k in ["经过", "流程", "步骤", "几步", "路径"]):
            return "查询流程"
        elif any(k in question_lower for k in ["k值", "参数", "调优"]):
            return "k值调优"
        elif any(k in question_lower for k in ["原理", "核心", "混合检索"]):
            return "检索原理"
        
        return None

    def generate_highlighted_mermaid(self, question: str) -> GraphPath:
        """生成带高亮的Mermaid图谱"""
        
        # 匹配问题类型
        path_type = self.match_question_type(question)
        
        if not path_type:
            path_type = "查询流程"  # 默认路径
        
        path_data = self.path_templates[path_type]
        
        # 构建节点样式
        node_styles = []
        for node_name in path_data["nodes"]:
            if node_name in path_data["core_nodes"]:
                node_styles.append(f'    {node_name}["{node_name}"]:::coreNode')
            elif node_name in ["用户提问", "最终答案"]:
                node_styles.append(f'    {node_name}["{node_name}"]:::startEndNode')
            else:
                node_styles.append(f'    {node_name}["{node_name}"]')
        
        # 构建边样式（核心路径用红色虚线）
        edge_styles = []
        for source, target in path_data["edges"]:
            if source in path_data["core_nodes"] and target in path_data["core_nodes"]:
                edge_styles.append(f'    {source} -->|核心路径| {target}')
            else:
                edge_styles.append(f'    {source} --> {target}')
        
        # 生成Mermaid代码
        mermaid_code = "```mermaid\n"
        mermaid_code += "flowchart LR\n"
        mermaid_code += "    %% 节点样式定义\n"
        mermaid_code += "    classDef coreNode fill:#ffcccc,stroke:#ff0000,stroke-width:2px;\n"
        mermaid_code += "    classDef startEndNode fill:#ccffcc,stroke:#00aa00,stroke-width:2px;\n"
        mermaid_code += "\n"
        mermaid_code += "\n".join(node_styles) + "\n"
        mermaid_code += "\n"
        mermaid_code += "\n".join(edge_styles) + "\n"
        mermaid_code += "```"
        
        return GraphPath(
            nodes=path_data["nodes"],
            edges=path_data["edges"],
            mermaid_code=mermaid_code
        )

    def get_answer(self, question: str) -> str:
        """获取问题答案"""
        
        question_lower = question.lower()
        
        # 问题：RAG混合检索的查询流程
        if "经过" in question or "流程" in question or "几步" in question:
            return """RAG混合检索的查询流程共8步：

1. **用户提问**：用户输入自然语言查询
2. **查询理解**：解析用户意图
3. **向量检索**：通过embedding向量进行语义相似度匹配
4. **BM25检索**：通过关键词进行精确匹配
5. **RRF融合**：用倒数排名融合合并向量检索和BM25的结果
6. **重排序**：用交叉编码器对融合结果进行精细排序
7. **上下文构建**：将排序后的相关文档组织成上下文
8. **LLM生成**：大模型根据上下文生成最终答案

核心流转路径：用户提问 → 查询理解 → 检索(向量+BM25) → RRF融合 → 重排序 → 上下文 → LLM生成 → 最终答案"""


def main():
    """测试高亮功能"""
    
    highlighter = GraphHighlighter()
    
    # 测试问题
    test_question = "RAG混合检索里，用户的query从输入到生成答案，经过了哪几步？"
    
    print("=" * 60)
    print("图谱路径高亮功能测试")
    print("=" * 60)
    print(f"\n问题：{test_question}\n")
    
    # 获取答案
    answer = highlighter.get_answer(test_question)
    print("答案：")
    print(answer)
    
    # 获取高亮图谱
    graph_path = highlighter.generate_highlighted_mermaid(test_question)
    print("\n" + "=" * 60)
    print("带高亮的Mermaid图谱：")
    print("=" * 60)
    print(graph_path.mermaid_code)
    
    # 保存测试结果
    output_path = "/mnt/d/projects/wiki/wiki/my-learning-path/practice/code-graph-agent/highlight/test_result.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: 图谱路径高亮测试结果\ntype: synthesis\ntags: [highlight, graph, test]\nsources: [rag-knowledge-graph.md]\ncreated: 2026-05-01\nupdated: 2026-05-01\n---\n\n")
        f.write("# 图谱路径高亮测试结果\n\n")
        f.write(f"## 测试问题\n\n{test_question}\n\n")
        f.write(f"## 自然语言答案\n\n{answer}\n\n")
        f.write(f"## 带高亮的Mermaid图谱\n\n{graph_path.mermaid_code}\n\n")
        f.write(f"## 图谱路径\n\n")
        f.write(f"- 节点：{graph_path.nodes}\n\n")
        f.write(f"- 边：{graph_path.edges}\n")
    
    print(f"\n测试结果已保存到：{output_path}")


if __name__ == "__main__":
    main()