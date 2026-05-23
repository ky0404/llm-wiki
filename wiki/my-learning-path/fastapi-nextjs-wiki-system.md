---
title: FastAPI + Next.js Wiki 系统实现指南
type: source
tags: [fastapi, nextjs, wiki, react, fullstack, tutorial]
sources: []
created: 2026-05-01
updated: 2026-05-01
---

# FastAPI + Next.js Wiki 系统实现指南

## 一、系统架构概览

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 (Next.js 14)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Dashboard │  │ Graph    │  │ Search   │  │ Wiki Viewer  │   │
│  │  (/)     │  │ (/graph) │  │ (/search)│  │ (/wiki/:id) │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼  HTTP API (CORS)
┌─────────────────────────────────────────────────────────────────┐
│                         后端 (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    /wiki 路由组                           │   │
│  │  ├── /stats   - 知识库统计                                  │   │
│  │  ├── /graph   - 图谱数据                                    │   │
│  │  ├── /search  - 全文搜索                                    │   │
│  │  ├── /pages   - 页面列表                                    │   │
│  │  ├── /content - 内容获取                                    │   │
│  │  └── /health  - 健康检查                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼  文件系统
┌─────────────────────────────────────────────────────────────────┐
│                      Wiki 知识库 (/mnt/d/projects/wiki)         │
│  ├── concepts/    - 概念页面                                    │
│  ├── entities/    - 实体页面                                    │
│  ├── sources/     - 原始素材                                    │
│  ├── synthesis/   - 综合分析                                    │
│  └── index-cache.json - 图谱索引缓存                            │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈

| 层级 | 技术 | 版本 | 作用 |
|------|------|------|------|
| 前端框架 | Next.js | 14+ | React 全栈框架，App Router |
| UI 组件 | Tailwind CSS | 3.x | 原子化 CSS 样式 |
| 可视化 | react-force-graph-2d | 最新 | 知识图谱力导向布局 |
| 后端框架 | FastAPI | 最新 | 异步 API 框架 |
| Markdown | markdown | 3.x | Python Markdown 解析 |
| 数据格式 | JSON | - | 图谱索引缓存 |

---

## 二、后端实现 (FastAPI)

### 2.1 项目结构

```
wiki/api/
├── main.py              # FastAPI 入口
└── routes/
    └── wiki_route.py    # Wiki 业务路由
```

### 2.2 核心原理

#### 2.2.1 FastAPI 基础原理

FastAPI 是基于 **Starlette**（异步 Web 框架）和 **Pydantic**（数据验证）的现代 Python Web 框架：

- **原生异步支持**：基于 `asyncio`，高并发性能优异
- **自动生成文档**：访问 `/docs` 查看 OpenAPI 文档
- **类型提示驱动**：参数自动校验，无需手动写校验逻辑
- **模块化路由**：使用 `APIRouter` 拆分不同业务

#### 2.2.2 核心概念

| 概念 | 作用 |
|------|------|
| FastAPI 实例 | 整个 API 的核心入口，所有路由、中间件都挂载在该实例上 |
| APIRouter | 模块化路由容器，可拆分不同业务的接口 |
| 路径装饰器 | 如 `@app.get("/path")`，定义 HTTP 方法+路径 |
| 中间件 | 全局拦截请求/响应（如 CORS 跨域中间件） |
| HTTPException | FastAPI 标准化异常类 |

### 2.3 启动流程

```bash
# 1. 进入后端目录
cd /mnt/d/projects/wiki/wiki/api

# 2. 启动服务（后台运行）
python3 main.py

# 3. 服务启动后监听 http://127.0.0.1:8000
#    API 文档：http://127.0.0.1:8000/docs
```

### 2.4 接口清单

| 接口 | 方法 | 功能 | 实现原理 |
|------|------|------|----------|
| `/wiki/stats` | GET | 知识库统计 | 读取 index-cache.json，统计文件数、边数、健康分 |
| `/wiki/graph` | GET | 图谱数据 | 从缓存读取节点和边，过滤无效边（节点 ID 匹配） |
| `/wiki/search` | GET | 全文搜索 | 调用 Linux `grep` 命令搜索指定目录 |
| `/wiki/pages` | GET | 页面列表 | 调用 Linux `find` 命令列出 md 文件 |
| `/wiki/health` | GET | 健康检查 | 检查缓存文件是否存在 |
| `/wiki/content` | GET | 内容获取 | 读取 md 文件，解析 frontmatter，转 Markdown 为 HTML |

### 2.5 核心代码解析

#### 2.5.1 main.py - API 主入口

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.wiki_route import router as wiki_router

app = FastAPI(
    title="Wiki API",
    version="1.0.0",
    description="Wiki知识库API服务"
)

# CORS 中间件 - 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由，添加 /wiki 前缀
app.include_router(wiki_router, prefix="/wiki")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

**原理说明**：
- `CORSMiddleware`：解决前后端分离开发时的跨域问题
- `include_router(prefix="/wiki")`：所有 wiki_route 中的路由都会自动添加 `/wiki` 前缀

#### 2.5.2 wiki_route.py - 搜索实现

```python
@router.get("/search")
async def search_wiki(q: str = Query(..., description="搜索关键词")):
    """全局内容搜索"""
    # 定义搜索范围 - 排除 node_modules, .git, .obsidian
    search_paths = [
        str(WIKI_ROOT / "wiki"),
        str(WIKI_ROOT / "raw"),
        str(WIKI_ROOT / "my-learning-path"),
    ]
    # 使用 grep 命令进行全文搜索
    # -r: 递归搜索
    # -n: 显示行号
    # -i: 不区分大小写
    result = subprocess.run(
        ["grep", "-rni", "--include=*.md", 
         "--exclude-dir=node_modules", 
         "--exclude-dir=.git", 
         "--exclude-dir=.obsidian", 
         q] + search_paths,
        capture_output=True, text=True, timeout=15
    )
    
    # 去重：同一文件只保留一条结果
    file_results = {}
    for line in result.stdout.strip().split("\n"):
        parts = line.split(":", 2)
        if len(parts) >= 3:
            rel_path = parts[0].replace(str(WIKI_ROOT) + "/", "")
            if rel_path not in file_results:
                file_results[rel_path] = {
                    "file": rel_path,
                    "line": parts[1],
                    "snippet": parts[2][:300]
                }
    
    return {"total": len(results), "results": list(file_results.values())[:20]}
```

**原理说明**：
- 使用系统 `grep` 命令比纯 Python 实现更高效
- 去重逻辑：同一文件只显示一条结果，避免重复
- 路径处理：去除前缀，保持相对路径

#### 2.5.3 wiki_route.py - 内容获取

```python
@router.get("/content")
async def get_content(path: str = Query("", description="页面路径")):
    """获取页面内容"""
    path = urllib.parse.unquote(path)  # URL 解码
    if path.endswith(".md"):
        path = path[:-3]
    
    # 尝试多个路径：原始路径 + 去掉 "wiki/" 前缀的路径
    search_paths = [
        path,
        path.replace("wiki/", ""),
    ]
    
    for sp in search_paths:
        for search_dir in [WIKI_ROOT, WIKI_ROOT / "raw", WIKI_ROOT / "my-learning-path"]:
            file_path = search_dir / f"{sp}.md"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 解析 YAML frontmatter
                frontmatter = {}
                body = content
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        for line in parts[1].strip().split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                frontmatter[key.strip()] = val.strip()
                        body = parts[2].strip()
                
                # 转换为 HTML
                html = markdown.markdown(body, extensions=['fenced_code', 'tables', 'sane_lists'])
                
                return {"content": html, "frontmatter": frontmatter, "raw": body}
    
    raise HTTPException(status_code=404, detail="页面未找到")
```

**原理说明**：
- **URL 解码**：处理中文路径和特殊字符
- **多路径搜索**：兼容不同目录结构的文件
- **Frontmatter 解析**：提取 Markdown 文件的元数据
- **Markdown 渲染**：使用 Python markdown 库转换为 HTML

---

## 三、前端实现 (Next.js 14)

### 3.1 项目结构

```
frontend/src/
├── app/
│   ├── layout.tsx           # 根布局（含 DashboardLayout）
│   ├── page.tsx            # 仪表盘首页 (/)
│   ├── graph/page.tsx      # 知识图谱页面 (/graph)
│   ├── search/page.tsx     # 搜索页面 (/search)
│   └── wiki/[...slug]/page.tsx  # Wiki 文档查看页 (/wiki/:slug)
├── components/
│   └── DashboardLayout.tsx # 侧边栏布局组件
└── lib/
    └── api.ts              # API 请求封装
```

### 3.2 核心原理

#### 3.2.1 Next.js App Router

Next.js 14 使用 **App Router** 架构：
- `app/` 目录下的每个文件夹对应一个路由
- `page.tsx` 是页面入口组件
- `layout.tsx` 定义共享布局（侧边栏）
- `[...slug]` 是动态路由，捕获任意深度的路径

#### 3.2.2 客户端 vs 服务器组件

| 组件类型 | 关键字 | 特点 |
|----------|--------|------|
| 服务器组件 | 默认 | 在服务端渲染，无法使用 useState/useEffect |
| 客户端组件 | `"use client"` | 在浏览器执行，可使用 React  hooks |

#### 3.2.3 动态导入

```typescript
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,  // 禁用 SSR，因为库依赖浏览器 API
  loading: () => <GraphSkeleton />,
})
```

**原理**：force graph 库依赖 `canvas`，只能在浏览器环境运行，所以需要禁用 SSR。

### 3.3 启动流程

```bash
# 1. 进入前端目录
cd /mnt/d/projects/wiki/frontend

# 2. 开发模式启动
npm run dev
# 或
next dev

# 3. 访问 http://localhost:3000

# 4. 生产构建
npm run build
npm start
```

### 3.4 核心代码解析

#### 3.4.1 API 封装 (lib/api.ts)

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchApi<T>(endpoint: string): Promise<T> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 10000)

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    clearTimeout(timeoutId)
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new Error('请求超时，请检查后端服务是否启动')
      }
      throw error
    }
    throw new Error('未知错误')
  }
}

export async function searchWiki(query: string): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query })
  return fetchApi<SearchResponse>(`/wiki/search?${params}`)
}
```

**原理说明**：
- **超时控制**：使用 AbortController 实现 10 秒超时
- **错误处理**：区分超时错误和其他 HTTP 错误
- **环境变量**：支持通过 `NEXT_PUBLIC_API_URL` 切换 API 地址

#### 3.4.2 知识图谱 (graph/page.tsx)

```typescript
// 数据过滤 - 隐藏孤立节点
const { nodes, links, connectedIds, degreeMap } = useMemo(() => {
  if (!graphData) return { nodes: [], links: [], connectedIds: new Set(), degreeMap: new Map() }

  // 统计每个节点的度
  const degreeMap = new Map<string, number>()
  graphData.edges.forEach(e => {
    degreeMap.set(e.source, (degreeMap.get(e.source) ?? 0) + 1)
    degreeMap.set(e.target, (degreeMap.get(e.target) ?? 0) + 1)
  })

  // 找出有连接的节点
  const connectedIds = new Set([
    ...graphData.edges.map(e => e.source),
    ...graphData.edges.map(e => e.target),
  ])

  // 根据设置过滤
  let filtered = graphData.nodes
  if (hideIsolated) filtered = filtered.filter(n => connectedIds.has(n.id))
  if (activeTypes.size > 0) filtered = filtered.filter(n => activeTypes.has(n.type))

  // 过滤边（两端都必须在节点中）
  const filteredLinks = graphData.edges.filter(
    e => filteredIds.has(e.source) && filteredIds.has(e.target)
  )

  return { nodes: richNodes, links: filteredLinks, connectedIds, degreeMap }
}, [graphData, hideIsolated, activeTypes, searchQuery])
```

**原理说明**：
- **useMemo**：缓存计算结果，避免每次渲染重新计算
- **孤立节点过滤**：只显示在边中出现的节点
- **动态节点大小**：根据连接数（度）调整节点半径

#### 3.4.3 节点自定义绘制

```typescript
const paintNode = useCallback(
  (rawNode: object, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const node = rawNode as RichNode
    const { x = 0, y = 0 } = node
    const r = node.radius ?? 5
    const color = node.color
    
    // 绘制光晕（选中/悬停时）
    if (selectedNode?.id === node.id || hoveredNode?.id === node.id) {
      const glow = ctx.createRadialGradient(x, y, r * 0.8, x, y, r * 3)
      glow.addColorStop(0, color + "55")
      glow.addColorStop(1, "transparent")
      ctx.fillStyle = glow
      ctx.beginPath()
      ctx.arc(x, y, r * 3, 0, 2 * Math.PI)
      ctx.fill()
    }

    // 绘制节点主体
    ctx.beginPath()
    ctx.arc(x, y, r, 0, 2 * Math.PI)
    ctx.fillStyle = selectedNode?.id === node.id ? "#fff" : color
    ctx.fill()

    // 缩放够大时显示标签
    if (globalScale >= 1.2 || hoveredNode?.id === node.id) {
      ctx.font = `${Math.max(10 / globalScale, 3)}px sans-serif`
      ctx.fillText(node.title, x, y + r + 2)
    }
  },
  [hoveredNode, selectedNode]
)
```

**原理说明**：
- **Canvas 自定义渲染**：使用 `nodeCanvasObject` prop 自定义节点外观
- **光晕效果**：使用径向渐变实现选中/悬停时的发光效果
- **智能标签**：根据缩放级别决定是否显示标签，避免混乱

---

## 四、部署指南

### 4.1 后端部署

```bash
# 1. 安装依赖
pip3 install fastapi uvicorn markdown

# 2. 启动服务
cd /mnt/d/projects/wiki/wiki/api
python3 main.py

# 3. 验证服务
curl http://localhost:8000/health
# 返回: {"status":"ok"}
```

### 4.2 前端开发模式

```bash
# 1. 安装依赖
cd /mnt/d/projects/wiki/frontend
npm install

# 2. 启动开发服务器
npm run dev

# 3. 访问 http://localhost:3000
```

### 4.3 前端生产构建

```bash
# 1. 构建
npm run build

# 2. 启动生产服务器
npm start
# 或
PORT=3000 npm start
```

### 4.4 端口配置

| 服务 | 默认端口 | 环境变量 |
|------|----------|----------|
| FastAPI 后端 | 8000 | - |
| Next.js 前端 | 3000 | PORT |

### 4.5 常见问题

#### 问题 1：搜索超时

**原因**：搜索范围包含 node_modules 导致超时

**解决**：在 grep 命令中添加 `--exclude-dir=node_modules`

#### 问题 2：页面 404

**原因**：文件路径格式不匹配（如 `wiki/concepts/bert.md` vs `concepts/bert.md`）

**解决**：在 content 接口中尝试多个路径搜索

#### 问题 3：hydration 不匹配

**原因**：Dark Reader 等浏览器插件修改了 HTML 属性

**解决**：前端添加 mounted 状态判断，避免 SSR 和客户端属性不一致

---

## 五、API 响应格式

### 5.1 /wiki/stats

```json
{
  "total_files": 120,
  "total_edges": 350,
  "health_score": 85,
  "type_distribution": {
    "concept": 45,
    "entity": 30,
    "source": 35,
    "synthesis": 10
  },
  "recent_pages": [
    { "path": "wiki/concepts/rag.md", "title": "RAG", "type": "concept", "tags": ["ai"] }
  ]
}
```

### 5.2 /wiki/graph

```json
{
  "nodes": [
    { "id": "wiki/concepts/rag.md", "title": "RAG", "type": "concept", "tags": ["ai"] }
  ],
  "edges": [
    { "source": "wiki/concepts/rag.md", "target": "wiki/concepts/llm.md" }
  ]
}
```

### 5.3 /wiki/content

```json
{
  "content": "<h1>RAG</h1><p>...</p>",
  "frontmatter": { "title": "RAG", "type": "concept", "tags": ["ai"] },
  "raw": "# RAG\n\n..."
}
```

---

## 六、后续扩展

### 6.1 添加新接口

在 `wiki_route.py` 中添加：

```python
@router.get("/新接口名")
async def new_endpoint(param: str = Query(...)):
    # 实现逻辑
    return {"result": "..."}
```

### 6.2 添加新页面

在 `frontend/src/app/` 下创建新页面：

```bash
# 例如添加 /about 页面
mkdir -p frontend/src/app/about
echo '"use client"\nexport default function About() { return <div>About</div> }' > frontend/src/app/about/page.tsx
```

### 6.3 添加新功能组件

在 `frontend/src/components/` 下创建组件，在页面中导入使用。

---

## 七、相关文件路径

| 功能 | 文件路径 |
|------|----------|
| 后端入口 | `/mnt/d/projects/wiki/wiki/api/main.py` |
| 后端路由 | `/mnt/d/projects/wiki/wiki/api/routes/wiki_route.py` |
| 前端 API | `/mnt/d/projects/wiki/frontend/src/lib/api.ts` |
| 仪表盘 | `/mnt/d/projects/wiki/frontend/src/app/page.tsx` |
| 知识图谱 | `/mnt/d/projects/wiki/frontend/src/app/graph/page.tsx` |
| 搜索页面 | `/mnt/d/projects/wiki/frontend/src/app/search/page.tsx` |
| Wiki 查看 | `/mnt/d/projects/wiki/frontend/src/app/wiki/[...slug]/page.tsx` |
| 布局组件 | `/mnt/d/projects/wiki/frontend/src/components/DashboardLayout.tsx` |