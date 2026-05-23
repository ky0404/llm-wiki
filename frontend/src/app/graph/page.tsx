"use client"

import { useEffect, useState, useRef, useCallback, useMemo } from "react"
import dynamic from "next/dynamic"
import { getKnowledgeGraph } from "@/lib/api"
import { RefreshCw, ZoomIn, ZoomOut, Maximize2, Search, X, ExternalLink, Filter } from "lucide-react"

// ─── 动态加载（SSR 禁用）────────────────────────────────────────────────────────
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => <GraphSkeleton />,
})

// ─── 类型 ────────────────────────────────────────────────────────────────────────
interface GraphNode {
  id: string
  title: string
  type: string
  tags: string[]
  // 运行时追加字段（力导向引擎写入）
  x?: number
  y?: number
  vx?: number
  vy?: number
}

interface RichNode extends GraphNode {
  color: string
  radius: number   // 按出度动态调整节点大小
}

interface GraphEdge {
  source: string
  target: string
}

interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

// ─── 颜色 & 配置 ─────────────────────────────────────────────────────────────────
const TYPE_META: Record<string, { color: string; label: string }> = {
  concept:   { color: "#3b82f6", label: "概念" },
  entity:    { color: "#8b5cf6", label: "实体" },
  source:    { color: "#10b981", label: "来源" },
  synthesis: { color: "#f59e0b", label: "综合" },
  index:     { color: "#ef4444", label: "索引" },
  unknown:   { color: "#94a3b8", label: "其他" },
}

const getColor  = (type: string) => TYPE_META[type]?.color  ?? TYPE_META.unknown.color
const getLabel  = (type: string) => TYPE_META[type]?.label  ?? type
const BG_COLOR  = "#0f1117"
const LINK_COLOR = "rgba(99,102,241,0.25)"
const LINK_HOVER = "rgba(99,102,241,0.7)"

// ─── 子组件 ──────────────────────────────────────────────────────────────────────
function GraphSkeleton() {
  return (
    <div className="flex items-center justify-center h-full bg-[#0f1117] rounded-2xl">
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-12 h-12">
          <div className="absolute inset-0 rounded-full border-4 border-indigo-500/30" />
          <div className="absolute inset-0 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin" />
        </div>
        <span className="text-slate-400 text-sm">构建知识图谱…</span>
      </div>
    </div>
  )
}

function ErrorState({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-full bg-[#0f1117] rounded-2xl gap-4">
      <p className="text-red-400 text-sm">{message}</p>
      <button
        onClick={onRetry}
        className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg transition-colors"
      >
        <RefreshCw className="w-4 h-4" /> 重试
      </button>
    </div>
  )
}

// ─── 主组件 ──────────────────────────────────────────────────────────────────────
export default function GraphPage() {
  const [graphData,    setGraphData]    = useState<GraphData | null>(null)
  const [loading,      setLoading]      = useState(true)
  const [error,        setError]        = useState<string | null>(null)
  const [selectedNode, setSelectedNode] = useState<RichNode | null>(null)
  const [hoveredNode,  setHoveredNode]  = useState<RichNode | null>(null)
  const [searchQuery,  setSearchQuery]  = useState("")
  const [activeTypes,  setActiveTypes]  = useState<Set<string>>(new Set())
  const [hideIsolated, setHideIsolated] = useState(false)
  const [dimensions,   setDimensions]   = useState({ width: 800, height: 600 })

  const fgRef        = useRef<any>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // ── 数据加载 ─────────────────────────────────────────────────────────────────
  const fetchGraph = useCallback(async () => {
    let cancelled = false
    setLoading(true)
    setError(null)
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000)
      
      const data = await getKnowledgeGraph()
      clearTimeout(timeoutId)
      
      if (!cancelled) {
        setGraphData(data)
      }
    } catch (e) {
      if (!cancelled) {
        setError(e instanceof Error ? e.message : "加载图谱失败")
      }
    } finally {
      if (!cancelled) {
        setLoading(false)
      }
    }
    return () => { cancelled = true }
  }, [])

  useEffect(() => { fetchGraph() }, [fetchGraph])

  // ── 自适应容器尺寸 ───────────────────────────────────────────────────────────
  useEffect(() => {
    const update = () => {
      if (!containerRef.current) return
      const { width, height } = containerRef.current.getBoundingClientRect()
      setDimensions({ width: Math.max(width, 400), height: Math.max(height, 300) })
    }
    update()
    const t = setTimeout(update, 120)
    window.addEventListener("resize", update)
    return () => { window.removeEventListener("resize", update); clearTimeout(t) }
  }, [])

  // ── 力导向参数调整（挂载后通过 ref 操作，避免无效 prop）───────────────────
  const handleEngineRef = useCallback((fg: any) => {
    fgRef.current = fg
    if (!fg) return
    fg.d3Force("charge")?.strength(-180)
    fg.d3Force("link")?.distance(80)
  }, [])

  // ── 数据过滤 & 丰富 ───────────────────────────────────────────────────────────
  const { nodes, links, connectedIds, degreeMap } = useMemo(() => {
    if (!graphData) return { nodes: [], links: [], connectedIds: new Set<string>(), degreeMap: new Map<string, number>() }

    // 统计每个节点的度（出度 + 入度）
    const degreeMap = new Map<string, number>()
    graphData.edges.forEach(e => {
      degreeMap.set(e.source, (degreeMap.get(e.source) ?? 0) + 1)
      degreeMap.set(e.target, (degreeMap.get(e.target) ?? 0) + 1)
    })

    const connectedIds = new Set<string>([
      ...graphData.edges.map(e => e.source),
      ...graphData.edges.map(e => e.target),
    ])

    // 节点过滤
    let filtered = graphData.nodes
    if (hideIsolated)        filtered = filtered.filter(n => connectedIds.has(n.id))
    if (activeTypes.size > 0) filtered = filtered.filter(n => activeTypes.has(n.type))
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      filtered = filtered.filter(n =>
        n.title.toLowerCase().includes(q) ||
        n.tags?.some(t => t.toLowerCase().includes(q))
      )
    }

    const filteredIds = new Set(filtered.map(n => n.id))

    // 丰富节点数据
    const richNodes: RichNode[] = filtered.map(n => {
      const degree = degreeMap.get(n.id) ?? 0
      return {
        ...n,
        color:  getColor(n.type),
        radius: Math.max(4, Math.min(14, 4 + degree * 0.8)),
      }
    })

    // 边过滤（两端都在过滤结果中才保留）
    const filteredLinks = graphData.edges.filter(
      e => filteredIds.has(e.source) && filteredIds.has(e.target)
    )

    return { nodes: richNodes, links: filteredLinks, connectedIds, degreeMap }
  }, [graphData, hideIsolated, activeTypes, searchQuery])

  // ── 自适应 zoomToFit ─────────────────────────────────────────────────────────
  useEffect(() => {
    if (!fgRef.current || nodes.length === 0) return
    const t = setTimeout(() => fgRef.current?.zoomToFit(600, 80), 300)
    return () => clearTimeout(t)
  }, [nodes.length])

  // ── 键盘关闭 ─────────────────────────────────────────────────────────────────
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") setSelectedNode(null) }
    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [])

  // ── 图谱交互 ────────────────────────────────────────────────────────────────
  const handleZoomIn  = () => fgRef.current?.zoom((fgRef.current.zoom() ?? 1) * 1.4, 250)
  const handleZoomOut = () => fgRef.current?.zoom((fgRef.current.zoom() ?? 1) / 1.4, 250)
  const handleFit     = () => fgRef.current?.zoomToFit(400, 80)

  // ── 类型过滤切换 ─────────────────────────────────────────────────────────────
  const toggleType = (type: string) => {
    setActiveTypes(prev => {
      const next = new Set(prev)
      next.has(type) ? next.delete(type) : next.add(type)
      return next
    })
  }

  // ── 所有页面中出现的 type 种类 ───────────────────────────────────────────────
  const allTypes = useMemo(() => {
    if (!graphData) return []
    return [...new Set(graphData.nodes.map(n => n.type))]
  }, [graphData])

  // ── 自定义节点 Canvas 绘制（带光晕 + 标签）──────────────────────────────────
  const paintNode = useCallback(
    (rawNode: object, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const node = rawNode as RichNode
      const { x = 0, y = 0 } = node
      const r      = node.radius ?? 5
      const color  = node.color
      const isHov  = hoveredNode?.id === node.id
      const isSel  = selectedNode?.id === node.id

      // 光晕（选中 / 悬停）
      if (isSel || isHov) {
        const glow = ctx.createRadialGradient(x, y, r * 0.8, x, y, r * 3)
        glow.addColorStop(0, color + "55")
        glow.addColorStop(1, "transparent")
        ctx.fillStyle = glow
        ctx.beginPath()
        ctx.arc(x, y, r * 3, 0, 2 * Math.PI)
        ctx.fill()
      }

      // 节点主体
      ctx.beginPath()
      ctx.arc(x, y, r, 0, 2 * Math.PI)
      ctx.fillStyle = isSel ? "#fff" : color
      ctx.fill()
      ctx.strokeStyle = isSel ? color : color + "99"
      ctx.lineWidth   = isSel ? 2 : 1
      ctx.stroke()

      // 标签（缩放够大才显示，避免噪声）
      if (globalScale >= 1.2 || isHov || isSel) {
        const fontSize = Math.max(10 / globalScale, 3)
        ctx.font        = `${fontSize}px 'PingFang SC', 'Microsoft YaHei', sans-serif`
        ctx.textAlign   = "center"
        ctx.textBaseline = "top"
        const label     = node.title.length > 14 ? node.title.slice(0, 13) + "…" : node.title
        ctx.fillStyle   = isSel ? "#fff" : "#e2e8f0"
        ctx.fillText(label, x, y + r + 2)
      }
    },
    [hoveredNode, selectedNode]
  )

  // ── 邻居计算（详情面板用）────────────────────────────────────────────────────
  const neighbors = useMemo(() => {
    if (!selectedNode || !graphData) return []
    const relatedIds = new Set<string>()
    graphData.edges.forEach(e => {
      if (e.source === selectedNode.id) relatedIds.add(e.target)
      if (e.target === selectedNode.id) relatedIds.add(e.source)
    })
    return graphData.nodes
      .filter(n => relatedIds.has(n.id))
      .slice(0, 8)
  }, [selectedNode, graphData])

  // ─────────────────────────────────────────────────────────────────────────────

  if (loading) return <div className="h-[calc(100vh-6rem)]"><GraphSkeleton /></div>
  if (error)   return <div className="h-[calc(100vh-6rem)]"><ErrorState message={error} onRetry={fetchGraph} /></div>
  if (!graphData) return null

  const isolatedCount = graphData.nodes.length - connectedIds.size

  return (
    <div className="h-[calc(100vh-6rem)] flex flex-col gap-3">

      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <div className="flex-shrink-0 flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-xl font-bold text-slate-800 leading-tight">知识图谱</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            {nodes.length} / {graphData.nodes.length} 节点 · {links.length} 条边
            {isolatedCount > 0 && <span className="ml-2 text-slate-300">（{isolatedCount} 个孤立）</span>}
          </p>
        </div>

        {/* 搜索框 */}
        <div className="relative w-48">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
          <input
            type="text"
            placeholder="搜索节点…"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 text-sm bg-slate-100 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 transition"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              <X className="w-3 h-3" />
            </button>
          )}
        </div>

        {/* 隐藏孤立 */}
        <button
          onClick={() => setHideIsolated(v => !v)}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border transition-colors ${
            hideIsolated
              ? "bg-indigo-50 border-indigo-300 text-indigo-700"
              : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
          }`}
        >
          <Filter className="w-3.5 h-3.5" />
          {hideIsolated ? "含孤立" : "隐孤立"}
        </button>

        {/* 刷新 */}
        <button
          onClick={fetchGraph}
          className="p-2 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 transition-colors"
          title="刷新数据"
        >
          <RefreshCw className="w-4 h-4 text-slate-500" />
        </button>
      </div>

      {/* ── 类型过滤标签 ────────────────────────────────────────────────────── */}
      <div className="flex-shrink-0 flex items-center gap-2 flex-wrap">
        <span className="text-xs text-slate-400">类型</span>
        {allTypes.map(type => {
          const meta    = TYPE_META[type] ?? TYPE_META.unknown
          const active  = activeTypes.has(type)
          const count   = graphData.nodes.filter(n => n.type === type).length
          return (
            <button
              key={type}
              onClick={() => toggleType(type)}
              className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-full border transition-all ${
                active
                  ? "border-transparent text-white shadow-sm"
                  : "border-slate-200 text-slate-600 hover:border-slate-300 bg-white"
              }`}
              style={active ? { backgroundColor: meta.color } : {}}
            >
              <span
                className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                style={{ backgroundColor: active ? "#fff" : meta.color }}
              />
              {meta.label}
              <span className={`${active ? "text-white/70" : "text-slate-400"}`}>
                {count}
              </span>
            </button>
          )
        })}
        {activeTypes.size > 0 && (
          <button
            onClick={() => setActiveTypes(new Set())}
            className="text-xs text-slate-400 hover:text-slate-600 underline underline-offset-2"
          >
            清除
          </button>
        )}
      </div>

      {/* ── 图谱主体 ────────────────────────────────────────────────────────── */}
      <div
        ref={containerRef}
        className="flex-1 relative rounded-2xl overflow-hidden"
        style={{ background: BG_COLOR }}
      >
        {nodes.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-500 text-sm">
            没有匹配的节点
          </div>
        ) : (
          <ForceGraph2D
            ref={handleEngineRef}
            graphData={{ nodes, links }}
            width={dimensions.width}
            height={dimensions.height}
            backgroundColor={BG_COLOR}
            // 节点
            nodeCanvasObject={paintNode}
            nodeCanvasObjectMode={() => "replace"}
            nodeRelSize={5}
            nodeVal={n => (n as RichNode).radius ?? 5}
            nodeLabel={n => (n as RichNode).title}
            onNodeClick={node => setSelectedNode(node as RichNode)}
            onNodeHover={node => setHoveredNode(node as RichNode | null)}
            // 边
            linkColor={() => LINK_COLOR}
            linkHoverPrecision={6}
            linkWidth={1}
            linkDirectionalArrowLength={3}
            linkDirectionalArrowRelPos={1}
            linkDirectionalArrowColor={() => LINK_COLOR}
            onLinkHover={() => {}}
            // 力导向
            cooldownTicks={120}
            d3AlphaDecay={0.025}
            d3VelocityDecay={0.35}
          />
        )}

        {/* ── 缩放控制 ────────────────────────────────────────────────────── */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-1.5">
          {[
            { icon: ZoomIn,   handler: handleZoomIn,  title: "放大" },
            { icon: ZoomOut,  handler: handleZoomOut, title: "缩小" },
            { icon: Maximize2, handler: handleFit,     title: "适应窗口" },
          ].map(({ icon: Icon, handler, title }) => (
            <button
              key={title}
              onClick={handler}
              title={title}
              className="p-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-lg border border-white/10 transition-colors"
            >
              <Icon className="w-4 h-4 text-slate-300" />
            </button>
          ))}
        </div>

        {/* ── 图例（左下角）────────────────────────────────────────────────── */}
        <div className="absolute bottom-4 left-4 flex flex-col gap-1.5 bg-black/30 backdrop-blur-sm rounded-xl border border-white/10 px-3 py-2.5">
          {Object.entries(TYPE_META).map(([type, { color, label }]) => (
            <div key={type} className="flex items-center gap-2 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
              {label}
            </div>
          ))}
        </div>

        {/* ── 节点详情面板 ─────────────────────────────────────────────────── */}
        {selectedNode && (
          <div
            className="absolute top-4 right-4 w-72 rounded-xl border border-white/10 shadow-2xl overflow-hidden"
            style={{ background: "rgba(15,17,23,0.92)", backdropFilter: "blur(16px)" }}
          >
            {/* 顶色条 */}
            <div className="h-1 w-full" style={{ backgroundColor: selectedNode.color }} />

            <div className="p-4">
              {/* 标题行 */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0 pr-2">
                  <h3 className="font-semibold text-white leading-snug break-words">
                    {selectedNode.title}
                  </h3>
                  <span
                    className="inline-block mt-1 px-2 py-0.5 text-xs rounded-full font-medium"
                    style={{
                      backgroundColor: selectedNode.color + "25",
                      color: selectedNode.color,
                    }}
                  >
                    {getLabel(selectedNode.type)}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="flex-shrink-0 p-1 rounded-lg text-slate-500 hover:text-slate-300 hover:bg-white/10 transition-colors"
                  title="关闭 (Esc)"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* 路径 */}
              <div className="mb-3">
                <p className="text-xs text-slate-500 mb-1">路径</p>
                <code className="text-xs text-slate-300 break-all leading-relaxed">
                  {selectedNode.id}
                </code>
              </div>

              {/* 标签 */}
              {selectedNode.tags?.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-slate-500 mb-1.5">标签</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedNode.tags.map(tag => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-white/8 text-slate-400 rounded text-xs border border-white/10"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* 关联节点 */}
              {neighbors.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-slate-500 mb-1.5">
                    关联节点 <span className="text-slate-600">({neighbors.length})</span>
                  </p>
                  <div className="flex flex-col gap-1">
                    {neighbors.map(n => (
                      <button
                        key={n.id}
                        onClick={() => setSelectedNode({ ...n, color: getColor(n.type), radius: 5 })}
                        className="flex items-center gap-2 px-2 py-1.5 rounded-lg text-left hover:bg-white/8 transition-colors group"
                      >
                        <span
                          className="w-2 h-2 rounded-full flex-shrink-0"
                          style={{ backgroundColor: getColor(n.type) }}
                        />
                        <span className="text-xs text-slate-300 truncate group-hover:text-white transition-colors">
                          {n.title}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* 打开页面 */}
              <a
                href={`/wiki/${encodeURIComponent(selectedNode.id)}`}
                className="flex items-center justify-center gap-2 w-full py-2 mt-1 text-xs font-medium rounded-lg transition-colors"
                style={{
                  backgroundColor: selectedNode.color + "20",
                  color: selectedNode.color,
                }}
              >
                <ExternalLink className="w-3.5 h-3.5" />
                打开页面
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}