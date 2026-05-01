---
title: Code Graph Agent 功能测试报告
type: synthesis
tags: [code-graph, test, report]
sources: [code_parser.py, code_hybrid_retriever.py, github_cloner.py]
created: 2026-05-01
updated: 2026-05-01
---

# Code Graph Agent 功能测试报告

## 测试时间
2026-05-01

## 测试环境
- Python 3.x
- 系统：Linux
- 测试路径：`/mnt/d/projects/wiki/wiki/my-learning-path/practice/code-graph-agent/upgrade/`

---

## 功能清单与测试结果

### 1. 代码解析功能 ✓

| 测试项 | 结果 | 说明 |
|--------|------|------|
| AST解析 | ✓ 通过 | 正确解析Python代码的模块、类、函数 |
| 节点提取 | ✓ 通过 | 提取module、class、function、method |
| 边提取 | ✓ 通过 | 提取defines、calls、inherits关系 |
| 目录解析 | ✓ 通过 | 支持递归解析整个目录 |

**测试数据**：
- 解析目录：`/mnt/d/projects/wiki/wiki/scripts`
- 节点数：30
- 边数：292
- 模块：7个
- 函数：23个

### 2. GitHub仓库拉取 ✓

| 测试项 | 结果 | 说明 |
|--------|------|------|
| URL解析 | ✓ 通过 | 支持 https://github.com/xxx/yyy 格式 |
| URL解析 | ⚠️ 部分 | 不支持 xxx/yyy 格式（需手动加前缀） |
| Git克隆 | ✗ 失败 | 网络问题/需要token |

**支持的URL格式**：
- ✓ `https://github.com/owner/repo`
- ✓ `github.com/owner/repo`
- ✗ `owner/repo`（暂不支持）

### 3. 代码检索功能 ✓

| 测试项 | 结果 | 说明 |
|--------|------|------|
| 关键词检索 | ✓ 通过 | 基于代码内容匹配 |
| 图谱检索 | ✓ 通过 | 基于函数名/类名匹配 |
| 语义检索 | ✓ 通过 | 语义规则映射 |
| RRF融合 | ✓ 通过 | 多路结果融合排序 |

**检索类型**：
- `keyword`：关键词匹配
- `graph`：图谱结构匹配
- `semantic`：语义关联匹配

### 4. 问答系统 ✓

| 测试问题 | 结果 | 答案摘要 |
|----------|------|----------|
| 这个项目有哪些模块？ | ✓ | 7个模块列表 |
| 定义了哪些API接口？ | ✓ | 找到API相关函数 |
| 数据从输入到输出经过了哪几步？ | ✓ | 4步处理流程 |
| 知识图谱如何构建？ | ✓ | 代码结构说明 |

### 5. 图谱可视化 ✓

| 功能 | 状态 | 说明 |
|------|------|------|
| Mermaid生成 | ✓ | 生成流程图代码 |
| 路径高亮 | ✓ | 核心节点红色，起止节点绿色 |
| 图谱导出 | ✓ | JSON格式图谱数据 |

---

## 历史测试记录

### 测试1：Wiki代码解析
- 解析目标：`/mnt/d/projects/wiki/wiki`
- 节点数：144
- 边数：917
- 代码文件：14个
- 状态：✓ 通过

### 测试2：FastAPI示例仓库
- 仓库：模拟FastAPI simple示例
- 节点数：5
- 边数：3
- 问答测试：2/2通过
- 问题1：定义哪些API接口？→ 5个接口
- 问题2：请求处理流程？→ 7步流程
- 状态：✓ 通过

### 测试3：YuanXinYeYu仓库
- 仓库：https://github.com/ky0404/YuanXinYeYu
- 节点数：131
- 边数：729
- API接口：10+个
- 技术栈：FastAPI + Chroma + LangGraph
- 状态：✓ 通过

---

## 已知限制

1. **网络依赖**：Git克隆需要网络访问，部分环境可能失败
2. **URL格式**：暂不支持 `owner/repo` 短格式
3. **检索精度**：基于简化规则，非真实向量检索
4. **语言支持**：仅支持Python代码解析（其他语言需扩展）

---

## 核心文件

| 文件 | 功能 |
|------|------|
| `code_parser.py` | Python代码AST解析 |
| `code_hybrid_retriever.py` | 3路混合检索引擎 |
| `github_cloner.py` | GitHub仓库拉取 |
| `code_graph_system.py` | 集成系统 |

---

## References

- [[my-learning-path/practice/code-graph-agent/index|项目主页]]
- [[my-learning-path/practice/code-graph-agent/upgrade/fast-test/test_results.md|FastAPI测试]]
- [[my-learning-path/practice/code-graph-agent/upgrade/fast-test/yuanxinyeyu_analysis.md|YuanXinYeYu分析]]