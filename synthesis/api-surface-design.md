---
title: API 接口设计与规范
type: synthesis
tags: [api, openapi, fastapi, rest]
sources: []
created: 2026-04-29
updated: 2026-04-29
---

# API 接口设计与规范

## 概览

本系统采用 **FastAPI** 框架构建 RESTful API，支持：
- 知识库查询（三级披露）
- 文档摄入（ingest）
- 健康检查（lint）
- 知识图谱查询（graph）
- 管理操作（admin）

所有接口支持 JSON 格式，关键操作需鉴权。

## OpenAPI 规范（摘要）

完整 OpenAPI 3.0 规范见 `openapi.yaml`（附录A）

### 基本信息
```yaml
openapi: 3.0.3
info:
  title: LLM Wiki Knowledge API
  version: 2.0.0
  description: API for LLM Wiki knowledge base with graph and vector search
servers:
  - url: http://localhost:8000/api/v2
    description: Local development
  - url: https://wiki-api.example.com/api/v2
    description: Production
```

---

## 核心端点设计

### 1. 查询接口（Query）

#### `POST /query`
执行知识库查询，支持三级渐进披露。

**请求示例：**
```json
{
  "query": "对比RAG和CAG的优缺点",
  "level": "auto",  // auto | L1 | L2 | L3
  "top_k": 5,
  "filters": {
    "type": ["concept", "synthesis"],
    "tags": ["methodology"]
  },
  "include_graph": false,
  "budget_tokens": 2000
}
```

**响应示例（L1 - 元数据）：**
```json
{
  "query_id": "q-20260429-001",
  "level": "L1",
  "results": [
    {
      "page_id": "concepts/rag",
      "title": "RAG（检索增强生成）",
      "type": "concept",
      "tags": ["方法论", "知识管理"],
      "summary": "RAG是传统的AI知识处理方法...",
      "relevance_score": 0.95
    },
    {
      "page_id": "concepts/cag",
      "title": "CAG（编译增强生成）",
      "type": "concept",
      "tags": ["方法论", "知识管理"],
      "summary": "CAG是LLM Wiki采用的知识管理方法...",
      "relevance_score": 0.92
    }
  ],
  "total_tokens_used": 150,
  "processing_time_ms": 45
}
```

**响应示例（L3 - 完整内容）：**
```json
{
  "query_id": "q-20260429-002",
  "level": "L3",
  "answer": "基于知识库内容，RAG与CAG的主要区别...\n\n[[concepts/rag]]\n[[concepts/cag]]",
  "sources": [
    {
      "page_id": "concepts/rag",
      "title": "RAG（检索增强生成）",
      "content_snippet": "RAG（Retrieval-Augmented Generation）...",
      "relevance_score": 0.95
    }
  ],
  "graph_context": {
    "nodes": [{"id": "concepts/rag", "title": "RAG"}],
    "edges": [{"from": "concepts/rag", "to": "concepts/cag", "type": "COMPARES_TO"}]
  },
  "total_tokens_used": 1850,
  "processing_time_ms": 3200
}
```

**智能路由逻辑：**
```python
def query_handler(request):
    # L1: 仅查元数据
    if request.level == "L1" or (request.level == "auto" and is_simple_query(request.query)):
        return query_L1(request)
    
    # L2: 查摘要
    elif request.level == "L2" or (request.level == "auto" and request.budget_tokens < 500):
        return query_L2(request)
    
    # L3: 完整内容 + LLM生成
    else:
        return query_L3(request)
```

---

### 2. 摄入接口（Ingest）

#### `POST /ingest`
摄入新文档到知识库。

**请求示例（JSON）：**
```json
{
  "source": "raw/新文档.md",
  "options": {
    "auto_categorize": true,
    "extract_entities": true,
    "update_graph": true,
    "dry_run": false
  }
}
```

**请求示例（multipart/form-data，上传文件）：**
```bash
curl -X POST http://localhost:8000/api/v2/ingest \
  -F "file=@raw/新文档.md" \
  -F "auto_categorize=true" \
  -F "update_graph=true"
```

**响应示例：**
```json
{
  "task_id": "task-20260429-001",
  "status": "completed",
  "created_pages": [
    {"id": "sources/新文档", "type": "source", "title": "新文档摘要"},
    {"id": "concepts/新概念", "type": "concept", "title": "新概念"}
  ],
  "updated_pages": [
    {"id": "concepts/rag", "changes": "added link to 新概念"}
  ],
  "graph_updated": true,
  "warnings": [],
  "processing_time_ms": 5800
}
```

---

### 3. 健康检查接口（Lint）

#### `POST /lint`
执行知识库健康检查。

**请求示例：**
```json
{
  "checks": ["orphaned_pages", "broken_links", "missing_frontmatter", "unprocessed_raw"],
  "auto_fix": false,
  "report_format": "detailed"
}
```

**响应示例：**
```json
{
  "lint_id": "lint-20260429-001",
  "timestamp": "2026-04-29T21:43:57",
  "status": "issues_found",
  "summary": {
    "total_pages": 60,
    "orphaned_pages": 2,
    "broken_links": 3,
    "missing_frontmatter": 0,
    "unprocessed_raw": 5
  },
  "details": {
    "orphaned_pages": [
      {"id": "concepts/bert", "reason": "no incoming links"}
    ],
    "broken_links": [
      {"from": "concepts/wikilinks", "to": "页面名称", "error": "target not found"}
    ],
    "unprocessed_raw": [
      {"file": "raw/未处理文档.md", "added_at": "2026-04-28"}
    ]
  },
  "auto_fix_available": true
}
```

#### `POST /lint/fix`
自动修复检测到的问题。

**请求示例：**
```json
{
  "lint_id": "lint-20260429-001",
  "fix_types": ["broken_links", "orphaned_pages"]
}
```

---

### 4. 图谱查询接口（Graph）

#### `GET /graph/nodes`
查询图数据库中的节点。

**请求参数：**
```
GET /graph/nodes?type=concept&tags=methodology&limit=20
```

**响应示例：**
```json
{
  "nodes": [
    {
      "id": "concepts/rag",
      "title": "RAG（检索增强生成）",
      "type": "concept",
      "tags": ["方法论", "知识管理"],
      "degree": 15  // 连接度
    }
  ],
  "total": 25
}
```

#### `GET /graph/edges`
查询节点间关系。

**请求参数：**
```
GET /graph/edges?from=concepts/rag&to=concepts/cag&type=LINKS_TO
```

#### `POST /graph/traverse`
图遍历查询（发现相关知识）。

**请求示例：**
```json
{
  "start_node": "concepts/transformer",
  "max_depth": 2,
  "relationship_types": ["LINKS_TO", "RELATES_TO"],
  "limit": 50
}
```

---

### 5. 管理接口（Admin）

#### `GET /admin/stats`
获取知识库统计信息。

**响应示例：**
```json
{
  "total_pages": 60,
  "by_type": {
    "source": 13,
    "concept": 22,
    "entity": 15,
    "synthesis": 2
  },
  "total_edges": 200,
  "graph_density": 0.15,
  "storage_size_mb": 12.5,
  "last_updated": "2026-04-29T21:43:57"
}
```

#### `POST /admin/rebuild-cache`
重建三级缓存。

#### `POST /admin/backup`
触发备份操作。

---

## 鉴权与速率限制

### API Key 鉴权
```python
# 请求头
headers = {
    "X-API-Key": "your-api-key-here",
    "Content-Type": "application/json"
}
```

### 速率限制
| 用户类型 | 限制 | 说明 |
|----------|------|------|
| 管理员 | 1000 req/min | 无限制访问 |
| 常规用户 | 100 req/min | 标准访问 |
| 匿名用户 | 10 req/min | 仅查询接口 |

实现方式（FastAPI + Redis）：
```python
from fastapi import Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("100/minute")
async def query(request: Request, ...):
    ...
```

---

## 错误码规范

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 400 | 请求参数错误 | 400 |
| 401 | 未鉴权 | 401 |
| 403 | 无权限 | 403 |
| 404 | 资源不存在 | 404 |
| 429 | 速率限制 | 429 |
| 500 | 服务器内部错误 | 500 |
| 503 | 服务不可用（如模型加载中） | 503 |

**错误响应格式：**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Limit: 100/minute",
    "details": {
      "limit": "100/minute",
      "retry_after": 30
    }
  }
}
```

---

## SDK 示例（Python）

```python
from llm_wiki_client import WikiClient

# 初始化客户端
client = WikiClient(
    base_url="http://localhost:8000/api/v2",
    api_key="your-api-key"
)

# 查询（L1 - 快速元数据查询）
result = client.query(
    query="Transformer架构原理",
    level="L1",
    top_k=5
)

# 查询（L3 - 完整回答）
answer = client.query(
    query="对比RAG和CAG的优缺点",
    level="L3",
    budget_tokens=2000
)
print(answer['answer'])

# 摄入新文档
task = client.ingest(
    file_path="raw/新文档.md",
    auto_categorize=True
)

# 健康检查
lint_result = client.lint()
if lint_result['status'] == 'issues_found':
    print(f"发现 {lint_result['summary']['broken_links']} 个断链")
```

---

## 附录A：完整 OpenAPI 规范

文件路径：`/mnt/d/projects/wiki/wiki/openapi.yaml`

（因篇幅限制，完整的 OpenAPI 3.0 YAML 规范将单独存储）

---

## References

- [[llm-wiki-upgrade-plan]]
- [[architecture-options]]
- [[data-model-design]]
- [[testing-qa-strategy]]
