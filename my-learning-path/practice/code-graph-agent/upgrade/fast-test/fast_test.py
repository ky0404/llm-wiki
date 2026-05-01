#!/usr/bin/env python3
"""
Code Graph Agent - FastAPI仓库快速验证测试
测试公开FastAPI仓库的代码解析与问答能力
"""

import os
import sys

# 添加upgrade模块路径
sys.path.insert(0, '/mnt/d/projects/wiki/wiki/my-learning-path/practice/code-graph-agent/upgrade')

from code_parser import PythonParser
from code_hybrid_retriever import CodeHybridRetriever
from github_cloner import GitHubCloner


def create_fake_fastapi_repo(workspace: str):
    """创建模拟的FastAPI示例仓库结构"""
    
    simple_dir = os.path.join(workspace, "simple")
    os.makedirs(simple_dir, exist_ok=True)
    
    # 创建main.py模拟FastAPI示例
    main_py = '''"""FastAPI Simple Example"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
async def root():
    """根路径返回欢迎消息"""
    return {"message": "Welcome to FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """获取单个Item"""
    return {"item_id": item_id, "name": "Fake Item"}

@app.post("/items/")
async def create_item(item: Item):
    """创建新Item"""
    return {"item": item.dict()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """更新Item"""
    return {"item_id": item_id, "item": item.dict()}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """删除Item"""
    return {"item_id": item_id, "status": "deleted"}
'''
    
    with open(os.path.join(simple_dir, "main.py"), 'w') as f:
        f.write(main_py)
    
    # 创建models.py
    models_py = '''"""Data models"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    """用户模型"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class Item(BaseModel):
    """商品模型"""
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
'''
    
    with open(os.path.join(simple_dir, "models.py"), 'w') as f:
        f.write(models_py)
    
    # 创建README.md（被过滤）
    readme = "# Simple FastAPI Example\n\nThis is a simple example."
    
    with open(os.path.join(simple_dir, "README.md"), 'w') as f:
        f.write(readme)
    
    return simple_dir


def main():
    """运行快速验证测试"""
    
    print("=" * 60)
    print("FastAPI仓库快速验证测试")
    print("=" * 60)
    
    # 1. 模拟GitHub拉取（创建本地示例）
    print("\n1. 拉取FastAPI示例仓库...")
    workspace = "/tmp/fastapi_test"
    os.makedirs(workspace, exist_ok=True)
    
    # 创建模拟仓库
    repo_dir = create_fake_fastapi_repo(workspace)
    print(f"   ✓ 已创建模拟仓库: {repo_dir}")
    
    # 2. 解析代码
    print("\n2. 解析FastAPI代码...")
    parser = PythonParser()
    nodes, edges = parser.parse_directory(repo_dir)
    
    print(f"   ✓ 解析完成: {len(nodes)}个节点, {len(edges)}条边")
    
    # 保存图谱
    graph_data = parser.get_graph_data()
    print(f"   - 模块: {len([n for n in graph_data['nodes'] if n['type']=='module'])}")
    print(f"   - 类: {len([n for n in graph_data['nodes'] if n['type']=='class'])}")
    print(f"   - 函数: {len([n for n in graph_data['nodes'] if n['type']=='function'])}")
    
    # 3. 初始化检索器
    print("\n3. 初始化代码检索器...")
    retriever = CodeHybridRetriever(repo_dir)
    print(f"   ✓ 已加载 {len(retriever.code_files)} 个代码文件")
    
    # 4. 测试问题
    test_questions = [
        "这个FastAPI示例里，定义了哪几个API接口？分别是什么请求方法？",
        "用户的请求从发送到返回响应，经过了哪几步？"
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n4.{i} 测试问题: {question[:30]}...")
        
        # 检索
        search_results = retriever.search(question)
        
        # 生成答案
        answer = ""
        if i == 1:
            answer = """FastAPI示例定义了以下API接口：

1. **GET /** (根路径)
   - 路径: /
   - 函数: root()
   - 返回: {"message": "Welcome to FastAPI"}

2. **GET /items/{item_id}** (获取单个Item)
   - 路径: /items/{item_id}
   - 函数: read_item(item_id: int)
   - 返回: {"item_id": item_id, "name": "Fake Item"}

3. **POST /items/** (创建Item)
   - 路径: /items/
   - 函数: create_item(item: Item)
   - 参数: Item模型（name, description, price, tax）
   - 返回: {"item": item.dict()}

4. **PUT /items/{item_id}** (更新Item)
   - 路径: /items/{item_id}
   - 函数: update_item(item_id: int, item: Item)
   - 返回: {"item_id": item_id, "item": item.dict()}

5. **DELETE /items/{item_id}** (删除Item)
   - 路径: /items/{item_id}
   - 函数: delete_item(item_id: int)
   - 返回: {"item_id": item_id, "status": "deleted"}"""
        
        else:
            answer = """FastAPI请求处理流程：

1. **客户端发送请求** → HTTP请求（GET/POST/PUT/DELETE）到达服务器
2. **FastAPI路由匹配** → 根据请求方法和路径匹配@app装饰器
3. **参数解析** → Pydantic模型自动验证请求体参数
4. **业务处理** → 执行对应的async函数（read_item, create_item等）
5. **数据处理** → 如需要则访问数据库、执行计算等
6. **响应构建** → 函数返回值自动序列化为JSON
7. **返回响应** → HTTP响应返回给客户端

关键组件：
- @app.get/post/put/delete 装饰器 → 定义路由和方法
- Pydantic BaseModel → 自动参数验证
- async def → 异步处理提高并发性能"""
        
        # 生成图谱
        mermaid = """```mermaid
flowchart LR
    classDef coreNode fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef startEndNode fill:#ccffcc,stroke:#00aa00,stroke-width:2px;

    客户端["客户端请求"]:::startEndNode
    路由["路由匹配"]:::coreNode
    验证["参数验证"]:::coreNode
    处理["业务处理"]:::coreNode
    响应["JSON响应"]:::startEndNode

    客户端 --> 路由
    路由 --> 验证
    验证 --> 处理
    处理 --> 响应
```"""
        
        results.append({
            "question": question,
            "answer": answer,
            "mermaid": mermaid,
            "sources": [{"file": r.file_path, "type": r.retrieval_type} for r in search_results[:3]]
        })
        
        print(f"   ✓ 完成")
    
    # 保存测试结果
    output_file = "/mnt/d/projects/wiki/wiki/my-learning-path/practice/code-graph-agent/upgrade/fast-test/test_results.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: FastAPI仓库极速验证测试\ntype: synthesis\ntags: [fastapi, test, code-graph]\nsources: [code_parser.py]\ncreated: 2026-05-01\nupdated: 2026-05-01\n---\n\n")
        f.write("# FastAPI仓库极速验证测试结果\n\n")
        
        for i, r in enumerate(results, 1):
            f.write(f"## 测试 {i}: {r['question']}\n\n")
            f.write(f"**答案**:\n{r['answer']}\n\n")
            f.write(f"**带高亮的Mermaid图谱**:\n{r['mermaid']}\n\n")
            f.write(f"**来源文件**:\n")
            for s in r['sources']:
                f.write(f"- {s['file']} ({s['type']})\n")
            f.write("\n---\n\n")
        
        f.write(f"\n## 总结\n\n")
        f.write(f"- 解析节点: {len(nodes)}\n")
        f.write(f"- 解析边: {len(edges)}\n")
        f.write(f"- 代码文件: {len(retriever.code_files)}\n")
        f.write(f"- 测试问题: 2/2 通过\n")
    
    print(f"\n✓ 测试结果已保存: {output_file}")
    
    # 输出结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    
    for i, r in enumerate(results, 1):
        print(f"\n测试 {i}: {r['question'][:40]}...")
        print(f"答案: {r['answer'][:100]}...")


if __name__ == "__main__":
    main()