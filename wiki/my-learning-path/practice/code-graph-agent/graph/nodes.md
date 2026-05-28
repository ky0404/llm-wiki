---
title: 代码仓库知识图谱 - 节点定义
type: synthesis
tags: [code-graph, nodes, knowledge-graph]
sources: [RAG混合检索核心原理]
created: 2026-05-01
updated: 2026-05-01
---

# 代码仓库知识图谱 - 节点定义

## 核心节点类型

### 1. 代码元素节点

| 节点类型 | 描述 | 属性 |
|----------|------|------|
| `File` | 代码文件 | path, language, size, functions[] |
| `Function` | 函数/方法 | name, signature, params, return_type, file_path |
| `Class` | 类 | name, methods[], attributes[], file_path |
| `Module` | 模块/包 | name, path, files[], sub_modules[] |
| `Variable` | 变量/常量 | name, type, value, scope |

### 2. 检索相关节点

| 节点类型 | 描述 | 属性 |
|----------|------|------|
| `CodeChunk` | 代码块 | content, file_path, line_range, embedding |
| `DocString` | 文档字符串 | content, target_node_id |
| `Comment` | 代码注释 | content, line_number, target_node_id |

### 3. 语义理解节点

| 节点类型 | 描述 | 属性 |
|----------|------|------|
| `Concept` | 概念 | name, description, related_nodes[] |
| `Pattern` | 代码模式 | name, pattern_type, occurrences[] |
| `Intent` | 意图 | query, interpretation, confidence |

## 节点属性定义

```json
{
  "node_types": {
    "File": {
      "required_fields": ["path", "name"],
      "optional_fields": ["language", "size", "last_modified", "functions"]
    },
    "Function": {
      "required_fields": ["name", "file_path", "signature"],
      "optional_fields": ["params", "return_type", "docstring", "calls"]
    },
    "CodeChunk": {
      "required_fields": ["content", "file_path"],
      "optional_fields": ["line_start", "line_end", "embedding", "tokens"]
    }
  }
}
```

## 节点创建流程

```
代码仓库解析 → 元素识别 → 节点构建 → 属性填充 → 图谱入库
     ↓           ↓        ↓         ↓          ↓
  AST解析    函数/类/模块  ID生成    元数据填充  Neo4j/Milvus
```

---

## RAG知识图谱实例（来自rag-theory.md文档）

### 提取的Concept节点

| 节点ID | 节点名称 | 描述 | 来源 |
|--------|----------|------|------|
| `C001` | 向量检索 | 将文本转为embedding向量，用余弦相似度匹配 | 检索技术 |
| `C002` | BM25关键词检索 | 基于词项频率和逆文档频率的统计排序 | 检索技术 |
| `C003` | RRF融合 | 倒数排名融合，公式：Score = Σ(1/(k+rank))，k=60 | 混合检索 |
| `C004` | 混合检索 | 向量检索 + BM25，用RRF融合结果 | 核心概念 |
| `C005` | 重排序 | 用交叉编码器对检索结果统一相关性打分 | 高阶深挖题 |
| `C006` | 查询改写 | 用LLM重写用户查询，提升召回率 | 高阶深挖题 |
| `C007` | 上下文压缩 | 只提取与问题相关的段落，减少token浪费 | 技术演进 |

### 提取的Pattern节点

| 节点ID | 节点名称 | 描述 | 组成 |
|--------|----------|------|------|
| `P001` | 混合检索流程 | RAG的核心检索流程 | 向量检索 + BM25 → RRF融合 |
| `P002` | RAG工作流 | 检索增强生成的完整流程 | 用户提问 → 检索 → LLM生成 |
| `P003` | RRF调优流程 | k值调优的标准方法 | baseline(k=60) → 二分搜索 → 场景分层 |

### 节点属性示例

```json
{
  "nodes": [
    {
      "id": "C001",
      "type": "Concept",
      "name": "向量检索",
      "description": "将文本转为embedding向量，用余弦相似度匹配",
      "attributes": {
        "优势": ["捕捉语义相似性", "同义词", "上位词"],
        "劣势": ["对专有名词、代码术语效果差"]
      },
      "source": "my-learning-path/theory/rag-theory.md"
    },
    {
      "id": "C003",
      "type": "Concept",
      "name": "RRF融合",
      "description": "倒数排名融合，公式：Score = Σ(1/(k+rank))，k=60",
      "attributes": {
        "k值范围": "40-80",
        "技术文档推荐": "40-60",
        "通用问答推荐": "60-80"
      },
      "source": "my-learning-path/theory/rag-theory.md"
    }
  ]
}
```

## References

- [[wiki/my-learning-path/practice/code-graph-agent/index|Code Graph Agent项目索引]]
- [[wiki/my-learning-path/theory/rag-theory|RAG技术原理]]