---
title: 代码仓库知识图谱 - 边定义
type: synthesis
tags: [code-graph, edges, knowledge-graph]
sources: [RAG混合检索核心原理]
created: 2026-05-01
updated: 2026-05-01
---

# 代码仓库知识图谱 - 边定义

## 核心边类型

### 1. 代码结构边

| 边类型 | 描述 | 方向 | 示例 |
|--------|------|------|------|
| `CONTAINS` | 文件包含模块 | File → Module | main.py contains app module |
| `DEFINES` | 文件定义函数/类 | File → Function/Class | utils.py defines parse_json |
| `NESTED_IN` | 嵌套关系 | Function → Function | inner_func nested_in outer_func |

### 2. 调用关系边

| 边类型 | 描述 | 方向 | 示例 |
|--------|------|------|------|
| `CALLS` | 函数调用 | Function → Function | handle_request calls parse_input |
| `IMPORTED_BY` | 导入关系 | Module → Module | logger imported_by processor |
| `INHERITS` | 继承关系 | Class → Class | CustomError inherits Exception |

### 3. 语义关联边

| 边类型 | 描述 | 方向 | 示例 |
|--------|------|------|------|
| `DOCUMENTED_BY` | 文档关联 | CodeElement → DocString | process documented_by docstring |
| `ANNOTATED_BY` | 注释关联 | CodeElement → Comment | function annotated_by comment |
| `RELATED_TO` | 语义相关 | Node → Node | login related_to authentication |

### 4. 检索相关边

| 边类型 | 描述 | 方向 | 示例 |
|--------|------|------|------|
| `EMBEDDED_IN` | 代码块属于文件 | CodeChunk → File | chunk embedded_in main.py |
| `REFERENCES` | 引用关系 | CodeChunk → Function | chunk references parse_func |
| `SIMILAR_TO` | 相似性关系 | CodeChunk → CodeChunk | chunk1 similar_to chunk2 |

## 数据流转

```
用户查询
    ↓
┌─────────────────────────────────────────────────────────────┐
│                    检索流程                                 │
├─────────────────────────────────────────────────────────────┤
│  1. 解析Query → Intent节点                                  │
│       ↓                                                    │
│  2. Intent → SIMILAR_TO → 候选CodeChunk                    │
│       ↓                                                    │
│  3. CodeChunk → EMBEDDED_IN → File                         │
│       ↓                                                    │
│  4. File → CONTAINS → 关联Module/Function                  │
│       ↓                                                    │
│  5. Function → CALLS → 调用链                               │
│       ↓                                                    │
│  6. 收集完整上下文 → LLM生成答案                            │
└─────────────────────────────────────────────────────────────┘
```

## 边属性定义

```json
{
  "edge_types": {
    "CALLS": {
      "required_fields": ["source", "target"],
      "optional_fields": ["call_count", "line_number", "is_recursive"]
    },
    "CONTAINS": {
      "required_fields": ["source", "target"],
      "optional_fields": ["count", "is_recursive"]
    },
    "SIMILAR_TO": {
      "required_fields": ["source", "target"],
      "optional_fields": ["similarity_score", "method"]
    }
  }
}
```

---

## RAG知识图谱实例（来自rag-theory.md文档）

### 提取的边关系

| 边ID | 边类型 | 源节点 | 目标节点 | 描述 |
|------|--------|--------|----------|------|
| `E001` | RELATED_TO | 向量检索(C001) | RRF融合(C003) | 向量检索结果送入RRF融合 |
| `E002` | RELATED_TO | BM25关键词检索(C002) | RRF融合(C003) | BM25结果送入RRF融合 |
| `E003` | NESTED_IN | RRF融合(C003) | 混合检索流程(P001) | RRF是混合检索的核心组件 |
| `E004` | RELATED_TO | 向量检索(C001) | 混合检索流程(P001) | 向量检索是混合检索的一部分 |
| `E005` | RELATED_TO | BM25关键词检索(C002) | 混合检索流程(P001) | BM25是混合检索的一部分 |
| `E006` | RELATED_TO | 重排序(C005) | RRF融合(C003) | 重排序作为RRF的后处理 |
| `E007` | RELATED_TO | 查询改写(C006) | 向量检索(C001) | 改写后的查询送入向量检索 |
| `E008` | NESTED_IN | 向量检索(C001) | RAG工作流(P002) | 向量检索是RAG流程的检索环节 |
| `E009` | NESTED_IN | RRF调优流程(P003) | RRF融合(C003) | 调优流程针对RRF参数 |

### 边关系图

```
                    ┌─────────────────────────────────────────┐
                    │           混合检索流程 (P001)            │
                    │  ┌───────────────────────────────────┐  │
                    │  │  向量检索(C001) ──RELATED_TO──►   │  │
                    │  │      │                    │        │  │
                    │  │      │ RELATED_TO         ▼        │  │
                    │  │      │           RRF融合(C003)     │  │
                    │  │      │           │        ▲        │  │
                    │  │      │ RELATED_TO │        │        │  │
                    │  │      ▼           │        │        │  │
                    │  │  BM25(C002) ──RELATED_TO────┘        │  │
                    │  └───────────────────────────────────┘  │
                    └─────────────────────────────────────────┘
                              │
                              │ NESTED_IN
                              ▼
                    ┌─────────────────────┐
                    │    RAG工作流 (P002) │
                    └─────────────────────┘
                              │
                              │ RELATED_TO
                              ▼
                    ┌─────────────────────┐
                    │   查询改写 (C006)   │
                    └─────────────────────┘
```

### 边属性示例

```json
{
  "edges": [
    {
      "id": "E001",
      "type": "RELATED_TO",
      "source": "C001",
      "target": "C003",
      "description": "向量检索结果送入RRF融合进行结果合并",
      "attributes": {
        "flow": "向量检索输出 → RRF融合输入",
        "data_format": "排名列表 + 得分"
      }
    },
    {
      "id": "E003",
      "type": "NESTED_IN",
      "source": "C003",
      "target": "P001",
      "description": "RRF是混合检索流程的核心融合组件",
      "attributes": {
        "role": "融合引擎",
        "formula": "Score = Σ(1/(k+rank))"
      }
    }
  ]
}
```

## References

- [[wiki/my-learning-path/practice/code-graph-agent/graph/nodes|图谱节点定义]]
- [[wiki/my-learning-path/practice/code-graph-agent/index|Code Graph Agent项目索引]]
- [[wiki/my-learning-path/theory/rag-theory|RAG技术原理]]