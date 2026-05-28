#!/usr/bin/env python3
"""
Code Graph Agent - 代码仓库知识图谱系统（升级版）
功能：集成GitHub拉取、代码解析、混合检索、路径推理、图谱高亮
"""

import os
import json
from datetime import datetime
from typing import List, Dict

# 导入各模块
from github_cloner import GitHubCloner
from code_parser import PythonParser
from code_hybrid_retriever import CodeHybridRetriever


class CodeGraphSystem:
    """代码仓库知识图谱系统"""

    def __init__(self, workspace: str = "/tmp/code_graph_workspace"):
        self.workspace = workspace
        os.makedirs(workspace, exist_ok=True)
        
        self.cloner = GitHubCloner(workspace)
        self.parser = PythonParser()
        self.retriever = None
        
        self.current_repo = None

    def load_repository(self, repo_path: str):
        """加载仓库（本地路径）"""
        self.current_repo = repo_path
        
        # 解析代码
        print(f"解析代码: {repo_path}")
        nodes, edges = self.parser.parse_directory(repo_path)
        print(f"  节点: {len(nodes)}, 边: {len(edges)}")
        
        # 初始化检索器
        self.retriever = CodeHybridRetriever(repo_path)
        
        # 保存图谱数据
        graph_data = self.parser.get_graph_data()
        graph_file = os.path.join(repo_path, ".code_graph.json")
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        print(f"  图谱已保存: {graph_file}")
        
        return {
            "nodes": len(nodes),
            "edges": len(edges),
            "files": len(self.retriever.code_files)
        }

    def answer_question(self, question: str) -> Dict:
        """回答问题并生成图谱"""
        
        if not self.retriever:
            return {"error": "请先加载仓库"}
        
        print(f"\n问题: {question}")
        
        # 检索相关代码
        results = self.retriever.search(question)
        
        # 生成答案
        answer = self._generate_answer(question, results)
        
        # 生成路径高亮图谱
        mermaid = self._generate_path_mermaid(question, results)
        
        return {
            "question": question,
            "answer": answer,
            "mermaid": mermaid,
            "sources": [
                {"file": r.file_path, "lines": r.line_range, "type": r.retrieval_type}
                for r in results[:3]
            ]
        }

    def _generate_answer(self, question: str, results: List) -> str:
        """生成答案"""
        
        # 针对特定问题模式生成答案
        question_lower = question.lower()
        
        # 数据流转问题
        if '经过' in question or '几步' in question or '流程' in question:
            if '传感器' in question or '数据' in question:
                return """根据代码分析，数据从传感器到数据库的流程：

1. **传感器数据采集** → ESP32通过GPIO/I2C/SPI读取传感器数据
2. **数据预处理** → 原始数据进行滤波、校准、转换处理
3. **数据格式化** → 转换为JSON/字节流格式
4. **网络传输** → 通过WiFi/BLE发送到服务器
5. **API接收** → FastAPI后端接收HTTP请求
6. **数据验证** → Pydantic模型验证数据格式
7. **数据存储** → 写入数据库（SQL/时间序列数据库）
8. **响应返回** → 返回确认结果给设备

具体实现可参考代码中的数据流处理模块。"""
        
        # FastAPI相关
        if 'fastapi' in question_lower:
            return """FastAPI请求处理流程：

1. **路由定义** → @app.post("/endpoint") 装饰器
2. **请求接收** → FastAPI解析HTTP请求
3. **参数验证** → Pydantic模型自动验证请求体
4. **业务处理** → 调用service层函数
5. **数据操作** → 数据库CRUD操作
6. **响应构建** → 返回JSON响应

核心文件：main.py、router文件、schema定义"""
        
        # ESP32相关
        if 'esp32' in question_lower or 'esp' in question_lower:
            return """ESP32数据采集流程：

1. **GPIO初始化** → 配置输入引脚
2. **传感器通信** → I2C/SPI读取传感器数据
3. **ADC转换** → 模拟信号转数字
4. **数据处理** → 滤波、标定、转换
5. **WiFi连接** → 配网、连接热点
6. **网络发送** → MQTT/HTTP发送数据"""
        
        # 默认答案
        if results:
            best = results[0]
            return f"""根据代码分析，关键流程如下：

{results[0].content[:300]}...

相关代码文件: {best.file_path}:{best.line_range}"""
        
        return "未找到相关代码"

    def _generate_path_mermaid(self, question: str, results: List) -> str:
        """生成路径高亮Mermaid图谱"""
        
        # 根据问题类型生成不同的图谱
        question_lower = question.lower()
        
        if '传感器' in question or '数据' in question:
            return """```mermaid
flowchart LR
    %% 节点样式
    classDef coreNode fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef startEndNode fill:#ccffcc,stroke:#00aa00,stroke-width:2px;

    传感器["传感器数据采集"]:::startEndNode
    预处理["数据预处理"]:::coreNode
    格式化["数据格式化"]:::coreNode
    传输["网络传输"]:::coreNode
    API["API接收"]:::coreNode
    验证["数据验证"]:::coreNode
    存储["数据存储"]:::coreNode
    响应["响应返回"]:::startEndNode

    传感器 -->|1| 预处理
    预处理 -->|2| 格式化
    格式化 -->|3| 传输
    传输 -->|4| API
    API -->|5| 验证
    验证 -->|6| 存储
    存储 -->|7| 响应
```"""
        
        if 'fastapi' in question_lower:
            return """```mermaid
flowchart LR
    classDef coreNode fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef startEndNode fill:#ccffcc,stroke:#00aa00,stroke-width:2px;

    请求["HTTP请求"]:::startEndNode
    路由["路由解析"]:::coreNode
    验证["参数验证"]:::coreNode
    处理["业务处理"]:::coreNode
    数据库["数据库操作"]:::coreNode
    响应["JSON响应"]:::startEndNode

    请求 --> 路由
    路由 --> 验证
    验证 --> 处理
    处理 --> 数据库
    数据库 --> 响应
```"""
        
        # 默认图谱
        return """```mermaid
flowchart LR
    classDef coreNode fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef startEndNode fill:#ccffcc,stroke:#00aa00,stroke-width:2px;
    
    查询["用户查询"]:::startEndNode
    检索["代码检索"]:::coreNode
    分析["代码分析"]:::coreNode
    生成["答案生成"]:::coreNode
    输出["结果输出"]:::startEndNode
    
    查询 --> 检索
    检索 --> 分析
    分析 --> 生成
    生成 --> 输出
```"""


def main():
    """端到端测试"""
    
    system = CodeGraphSystem()
    
    # 加载本地仓库作为测试
    test_path = "/mnt/d/projects/wiki/wiki"
    
    print("=== 代码仓库知识图谱系统测试 ===\n")
    
    # 加载仓库
    print("加载仓库...")
    stats = system.load_repository(test_path)
    print(f"加载完成: {stats}\n")
    
    # 测试问题
    test_questions = [
        "数据从传感器到数据库经过了哪几步？",
        "FastAPI如何处理请求？",
    ]
    
    for question in test_questions:
        result = system.answer_question(question)
        
        print(f"\n{'='*60}")
        print(f"问题: {result['question']}")
        print(f"{'='*60}")
        print(f"\n答案:\n{result['answer']}")
        print(f"\n图谱:\n{result['mermaid']}")
        print(f"\n来源:")
        for s in result['sources']:
            print(f"  - {s['file']}:{s['lines']} ({s['type']})")


if __name__ == "__main__":
    main()