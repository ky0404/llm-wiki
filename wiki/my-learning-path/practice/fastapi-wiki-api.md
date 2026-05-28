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

### 1. FastAPI基础原理

FastAPI是基于**Starlette（异步Web框架）** 和**Pydantic（数据验证）** 的现代Python Web框架，核心优势：
- 原生支持异步，高并发性能优异；
- 自动生成OpenAPI文档（访问`/docs`即可查看）；
- 类型提示驱动的参数校验，无需手动写校验逻辑；
- 支持模块化路由（APIRouter），便于业务解耦。

### 2. 核心概念

| 概念 | 作用 |
|------|------|
| FastAPI实例 | 整个API的核心入口，所有路由、中间件都挂载在该实例上 |
| APIRouter | 模块化路由容器，可拆分不同业务的接口 |
| 路径装饰器 | 如`@app.get("/path")`，定义HTTP方法+路径 |
| 中间件 | 全局拦截请求/响应（如CORS跨域中间件） |
| HTTPException | FastAPI标准化异常类 |

## 二、代码整体架构

| 文件 | 角色 |
|------|------|
| `api/main.py` | API主入口，创建FastAPI实例、配置中间件、注册子路由 |
| `api/routes/wiki_route.py` | Wiki业务路由模块，封装所有`/wiki`前缀的接口 |

## 三、启动流程

```bash
cd /mnt/d/projects/wiki/wiki/api
python3 main.py
```

服务启动后监听 `http://0.0.0.0:8000`

## 四、接口清单

| 接口 | 方法 | 功能 |
|------|------|------|
| `/wiki/stats` | GET | 知识库统计（文件数、边数、健康分） |
| `/wiki/graph` | GET | 图谱数据（节点+边） |
| `/wiki/search` | GET | 全文搜索（grep命令） |
| `/wiki/pages` | GET | 页面列表（find命令） |
| `/wiki/health` | GET | 健康检查 |

## 五、核心实现原理

### 1. 路由注册

```python
# main.py
from routes.wiki_route import router as wiki_router
app.include_router(wiki_router, prefix="/wiki")
```

### 2. 缓存加载

```python
# wiki_route.py
def load_cache():
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
```

### 3. 搜索实现

调用Linux `grep`命令实现全文搜索：
```python
subprocess.run(
    ["grep", "-rni", q, str(WIKI_ROOT), "--include=*.md"],
    capture_output=True, text=True, timeout=15
)
```

### 4. 页面列表

调用Linux `find`命令：
```python
subprocess.run(
    ["find", str(WIKI_ROOT), "-name", "*.md", "-not", "-path", "*/.obsidian/*"],
    capture_output=True, text=True, timeout=10
)
```

## 六、测试验证

```bash
# 启动服务
python3 main.py

# 测试接口
curl http://localhost:8000/wiki/stats
curl http://localhost:8000/wiki/graph
curl "http://localhost:8000/wiki/search?q=RAG"
curl http://localhost:8000/wiki/pages
```

### 测试结果

- `/wiki/stats`: 108文件, 581边, 健康分99
- `/wiki/search?q=RAG`: 30条搜索结果
- `/wiki/pages`: 50个页面

## 七、关键注意事项

1. **环境依赖**: 需安装 `pip install fastapi uvicorn`
2. **路径配置**: `WIKI_ROOT = Path("/mnt/d/projects/wiki")`
3. **跨平台**: grep/find是Linux命令，Windows需替换
4. **文档调试**: 访问 `http://localhost:8000/docs` 查看Swagger UI

## References

- [[wiki/my-learning-path/practice/code-graph-agent/index|Code Graph Agent项目]]
- [[wiki/my-learning-path/theory/rag-theory|RAG技术原理]]
