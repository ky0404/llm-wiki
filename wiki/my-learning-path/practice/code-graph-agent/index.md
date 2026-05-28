---
title: Code Graph Agent - 代码仓库知识图谱智能体
type: project
tags: [code-graph, agent, RAG, knowledge-graph, 项目]
sources: [RAG混合检索核心原理, 知识库技术]
created: 2026-05-01
updated: 2026-05-01
---

# Code Graph Agent

代码仓库知识图谱智能体，基于RAG混合检索技术，实现代码仓库的语义理解与智能问答。

## 项目概述

让AI能够理解代码仓库的结构、模块关系、函数调用链，通过混合检索技术实现精准的代码知识问答。

## 核心功能

- 代码结构理解：解析仓库的目录结构、模块关系
- 语义检索：理解代码意图，而非仅匹配关键词
- 知识图谱：构建代码元素（函数、类、文件）的关系网络
- 智能问答：基于图谱回答技术问题

## 技术架构

- 混合检索：向量检索 + BM25 + 图关系
- 知识图谱：节点（代码元素）+ 边（调用/引用关系）
- LLM集成：代码理解与答案生成

## 目录结构

```
code-graph-agent/
├── index.md                 # 项目索引
├── graph/                   # 图谱定义
│   ├── nodes.md            # 节点定义
│   └── edges.md            # 边定义
├── scripts/                # 检索脚本
└── docs/                   # 文档
```

## 学习进度

| 模块 | 状态 |
|------|------|
| 项目初始化 | ✅ 完成 |
| 图谱节点定义 | ✅ 完成 |
| 图谱边定义 | ✅ 完成 |
| 混合检索脚本 | ✅ 完成 |
| 问答接口 | ✅ 完成 |
| 知识图谱问答测试 | ✅ 完成 |
| 图谱路径高亮 | ✅ 完成 |
| 代码仓库解析升级 | ✅ 完成 |
| 代码分析增强 | ✅ 完成 |
| 项目分析器 | ✅ 完成 |

## 生成的文件

```
code-graph-agent/
├── index.md                    # 项目索引 ✅
├── graph/
│   ├── nodes.md               # 节点定义 ✅
│   ├── edges.md               # 边定义 ✅
│   └── rag-knowledge-graph.md # 可视化图谱 ✅
├── scripts/
│   └── hybrid_retriever.py    # 3路混合检索脚本 ✅
├── qa/
│   ├── qa_interface.py       # 问答接口 ✅
│   └── test_results.md        # 测试结果 ✅
├── highlight/
│   ├── graph_highlighter.py # 路径高亮模块 ✅
│   └── test_result.md        # 高亮测试结果 ✅
├── upgrade/
│   ├── github_cloner.py      # GitHub拉取模块 ✅
│   ├── code_parser.py        # Python代码解析引擎 ✅
│   ├── code_hybrid_retriever.py # 代码混合检索引擎 ✅
│   ├── code_graph_system.py  # 集成系统 ✅
│   ├── code_analyzer.py      # 代码分析增强 ✅
│   ├── project_analyzer.py   # 项目分析器 ✅
│   └── fast-test/            # 快速测试目录
│       ├── feature_test_report.md
│       ├── yuanxinyeyu_analysis.md
│       └── test_results.md
└── deep_analysis.py           # 深度能力分析脚本 ✅
```

## 完整功能清单

### 核心能力
- Python代码AST解析（模块/类/函数/调用）
- 知识图谱生成（节点+边）
- 3路混合检索（关键词+图谱+语义）
- GitHub仓库拉取
- 智能问答系统

### 增强能力
- 代码统计（行数、文件数、复杂度）
- 依赖分析（import关系图）
- 调用链追踪（函数调用路径）
- TODO/FIXME提取
- 项目结构分析
- 配置文件解析
- README自动生成

## 升级功能

### 新增能力
1. **GitHub仓库拉取** - 自动解析URL、克隆仓库、过滤核心文件
2. **Python代码解析** - AST解析提取模块/类/函数/调用关系
3. **代码混合检索** - 关键词+图谱+语义3路检索
4. **数据流转推理** - 自动回答"数据从X到Y经过哪几步"

### 测试结果
- 解析节点: 144个
- 解析边: 917条
- 代码文件: 14个
- 问答测试: 2/2通过

## 问答测试结果

### 测试问题与答案

| 测试 | 问题 | 来源 | 置信度 |
|------|------|------|--------|
| 1 | RAG混合检索的核心原理是什么？ | rag-theory.md | 0.90 |
| 2 | RRF融合的k值怎么选？不同场景怎么调优？ | rag-theory.md | 0.90 |
| 3 | 混合检索里，向量检索和BM25检索分别解决什么问题？ | rag-theory.md | 0.90 |

### 测试结论
- 答案100%来自Wiki知识库
- 无外部内容、无幻觉

### 图谱路径高亮测试

| 测试 | 问题 | 输出 |
|------|------|------|
| 1 | RAG混合检索里，用户的query从输入到生成答案，经过了哪几步？ | 8步流程 + 带高亮Mermaid图谱 |

**高亮样式**：
- 核心节点：红色填充 (#ffcccc)
- 起始/结束节点：绿色填充 (#ccffcc)
- 核心路径：红色虚线箭头

## 知识图谱节点与边定义

### 节点（Nodes）
- **代码元素**：File, Function, Class, Module, Variable
- **检索相关**：CodeChunk, DocString, Comment
- **语义理解**：Concept, Pattern, Intent

### 边（Edges）
- **代码结构**：CONTAINS, DEFINES, NESTED_IN
- **调用关系**：CALLS, IMPORTED_BY, INHERITS
- **语义关联**：DOCUMENTED_BY, ANNOTATED_BY, RELATED_TO
- **检索相关**：EMBEDDED_IN, REFERENCES, SIMILAR_TO

### 3路混合检索
1. **向量检索**：语义理解（Chroma + Embedding）
2. **BM25检索**：关键词匹配（rank-bm25）
3. **图谱检索**：结构关系（函数名/类名匹配）
融合方式：RRF（k=60）

## 知识图谱访问

### 本次生成的图谱节点（来自rag-theory.md）
- 7个Concept节点：向量检索、BM25、RRF融合、混合检索、重排序、查询改写、上下文压缩
- 3个Pattern节点：混合检索流程、RAG工作流、RRF调优流程

### 可视化图谱
- 路径：`graph/rag-knowledge-graph.md`
- 格式：Mermaid + JSON数据
- 访问方式：Mermaid在线预览 / Neo4j导入

## References

- [[wiki/my-learning-path/theory/rag-theory|RAG技术原理]]
- [[wiki/my-learning-path/practice/wiki-rag-optimization|LLM Wiki RAG化优化方案]]
- [[wiki/my-learning-path/practice/technical-weapons|我的技术武器库]]