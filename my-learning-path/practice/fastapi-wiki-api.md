---
title: FastAPI Wiki接口实现原理与过程
type: synthesis
tags: [fastapi, backend, api, wiki]
sources: [wiki/api/main.py, wiki/api/routes/wiki_route.py]
created: 2026-05-01
updated: 2026-05-01
---

# FastAPI Wiki接口实现原理与过程

## 一、核心前置知识

### FastAPI基础原理

FastAPI是基于**Starlette**和**Pydantic**的现代Python Web框架，核心优势：
- 原生支持异步，高并发性能优异
- 自动生成OpenAPI文档
- 类型提示驱动的参数校验
- 支持模块化路由（APIRouter）

## 二、代码整体架构

| 文件 | 角色 |
|------|------|
| `wiki/api/main.py` | API主入口 |
| `wiki/api/routes/wiki_route.py` | Wiki业务路由 |

## 三、启动流程

```bash
cd /mnt/d/projects/wiki/wiki/api
python3 main.py
```

服务启动后监听 `http://0.0.0.0:8000`

## 四、接口清单

| 接口 | 方法 | 功能 |
|------|------|------|
| `/wiki/stats` | GET | 知识库统计 |
| `/wiki/graph` | GET | 图谱数据 |
| `/wiki/search` | GET | 全文搜索 |
| `/wiki/pages` | GET | 页面列表 |
| `/wiki/health` | GET | 健康检查 |

## 五、核心实现

### 1. 路由注册
```python
app.include_router(wiki_router, prefix="/wiki")
```

### 2. 缓存加载
```python
def load_cache():
    with open(CACHE_FILE, "r") as f:
        return json.load(f)
```

### 3. 搜索（grep命令）
```python
subprocess.run(["grep", "-rni", q, str(WIKI_ROOT), "--include=*.md"])
```

### 4. 页面列表（find命令）
```python
subprocess.run(["find", str(WIKI_ROOT), "-name", "*.md"])
```

## 六、测试验证

- `/wiki/stats`: 108文件, 581边, 健康分99
- `/wiki/search?q=RAG`: 30条结果
- `/wiki/pages`: 50个页面

## 七、关键注意事项

1. **环境依赖**: `pip install fastapi uvicorn`
2. **路径配置**: WIKI_ROOT = Path("/mnt/d/projects/wiki")
3. **文档调试**: 访问 http://localhost:8000/docs

## References

- [[my-learning-path/practice/code-graph-agent/index]]
- [[my-learning-path/theory/rag-theory]]