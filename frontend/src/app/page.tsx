"use client"

import { useEffect, useState, useCallback, useRef } from "react"
import { 
  FileText, 
  GitBranch, 
  Activity, 
  Clock,
  TrendingUp,
  PieChart,
  RefreshCw,
  AlertCircle,
  Zap
} from "lucide-react"
import { getWikiStats, createSSEConnection, WikiStats } from "@/lib/api"

function StatsCard({ 
  title, 
  value, 
  icon: Icon, 
  color,
  trend,
  changed 
}: { 
  title: string
  value: number | string
  icon: any
  color: string
  trend?: string
  changed?: boolean
}) {
  const colors: Record<string, string> = {
    blue: "from-blue-500/10 to-blue-500/5 border-blue-200",
    indigo: "from-indigo-500/10 to-indigo-500/5 border-indigo-200",
    green: "from-green-500/10 to-green-500/5 border-green-200",
    purple: "from-purple-500/10 to-purple-500/5 border-purple-200",
    amber: "from-amber-500/10 to-amber-500/5 border-amber-200",
  }
  
  const iconColors: Record<string, string> = {
    blue: "text-blue-500 bg-blue-50",
    indigo: "text-indigo-500 bg-indigo-50",
    green: "text-green-500 bg-green-50",
    purple: "text-purple-500 bg-purple-50",
    amber: "text-amber-500 bg-amber-50",
  }

  return (
    <div className={`
      relative overflow-hidden rounded-2xl border bg-gradient-to-br ${colors[color]} p-5
      hover:shadow-lg transition-all duration-300 group
      ${changed ? 'ring-2 ring-blue-400 ring-opacity-80 animate-pulse' : ''}
    `}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className={`mt-2 text-3xl font-bold text-slate-800 ${changed ? 'scale-110 transition-transform duration-300' : ''}`}>
            {value}
          </p>
          {trend && (
            <p className="mt-1 text-xs text-green-600 flex items-center gap-1">
              <TrendingUp className="w-3 h-3" />
              {trend}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-xl ${iconColors[color]} group-hover:scale-110 transition-transform`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  )
}

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="relative">
        <div className="w-12 h-12 border-4 border-slate-200 rounded-full"></div>
        <div className="absolute top-0 left-0 w-12 h-12 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
      </div>
    </div>
  )
}

function ErrorMessage({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-64 text-center">
      <AlertCircle className="w-12 h-12 text-red-400 mb-3" />
      <p className="text-slate-600 mb-4">{message}</p>
      <button
        onClick={onRetry}
        className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        <RefreshCw className="w-4 h-4" />
        重试
      </button>
    </div>
  )
}

function PageList({ pages }: { pages: WikiStats['recent_pages'] }) {
  if (!pages || pages.length === 0) {
    return <div className="text-center py-8 text-slate-400">暂无数据</div>
  }

  const typeColors: Record<string, string> = {
    concept: "bg-blue-100 text-blue-700",
    entity: "bg-purple-100 text-purple-700",
    source: "bg-green-100 text-green-700",
    synthesis: "bg-amber-100 text-amber-700",
    index: "bg-red-100 text-red-700",
    unknown: "bg-slate-100 text-slate-600",
  }

  return (
    <div className="divide-y divide-slate-100">
      {pages.map((page, idx) => (
        <div 
          key={idx}
          className="px-5 py-3.5 hover:bg-slate-50 transition-colors cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="min-w-0 flex-1">
              <p className="font-medium text-slate-800 truncate">
                {page.title || page.path.split('/').pop() || '未命名'}
              </p>
              <p className="text-sm text-slate-400 truncate mt-0.5">{page.path}</p>
            </div>
            {page.type && (
              <span className={`ml-3 px-2.5 py-1 rounded-full text-xs font-medium ${typeColors[page.type] || typeColors.unknown}`}>
                {page.type}
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function DashboardPage() {
  const [stats, setStats] = useState<WikiStats | null>(null)
  const [prevStats, setPrevStats] = useState<WikiStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dataChanged, setDataChanged] = useState<Record<string, boolean>>({})
  const [isConnected, setIsConnected] = useState(false)
  const retryCount = useRef(0)

  const fetchStats = useCallback(async (showLoading = false) => {
    let cancelled = false
    if (showLoading) setLoading(true)
    setError(null)
    try {
      const data = await getWikiStats()
      if (!cancelled) {
        setStats(data)
      }
    } catch (err) {
      if (!cancelled) setError('无法加载数据，请确保后端服务已启动')
      console.error(err)
    } finally {
      if (!cancelled) setLoading(false)
    }
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    fetchStats(true)
  }, [fetchStats])

  useEffect(() => {
    if (prevStats && stats) {
      const changes: Record<string, boolean> = {}
      if (prevStats.total_files !== stats.total_files) changes.files = true
      if (prevStats.total_edges !== stats.total_edges) changes.edges = true
      if (prevStats.health_score !== stats.health_score) changes.health = true
      if (prevStats.recent_pages?.length !== stats.recent_pages?.length) changes.recent = true
      
      if (Object.keys(changes).length > 0) {
        setDataChanged(changes)
        setTimeout(() => setDataChanged({}), 1500)
      }
    }
    setPrevStats(stats)
  }, [stats, prevStats])

  useEffect(() => {
    const cleanup = createSSEConnection(async (data) => {
      if (data.type === 'wiki_change') {
        await fetchStats(false)
      }
    })

    const checkConnection = setInterval(() => {
      setIsConnected(true)
      retryCount.current = 0
    }, 5000)

    return () => {
      cleanup()
      clearInterval(checkConnection)
    }
  }, [fetchStats])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} onRetry={fetchStats} />
  if (!stats) return null

  const typeEntries = Object.entries(stats.type_distribution || {}).sort((a, b) => b[1] - a[1])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">仪表盘</h1>
          <p className="text-slate-500 mt-1">知识库实时状态</p>
        </div>
        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${
            isConnected 
              ? 'bg-green-100 text-green-700' 
              : 'bg-amber-100 text-amber-700'
          }`}>
            {isConnected ? (
              <>
                <Zap className="w-3.5 h-3.5" />
                <span className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                  实时同步中
                </span>
              </>
            ) : (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                连接中...
              </>
            )}
          </div>
          <button
            onClick={() => fetchStats(false)}
            className="p-2 rounded-lg hover:bg-slate-100 transition-colors"
            title="手动刷新"
          >
            <RefreshCw className={`w-5 h-5 text-slate-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="总文件数"
          value={stats.total_files}
          icon={FileText}
          color="blue"
          changed={dataChanged.files}
        />
        <StatsCard
          title="知识边数"
          value={stats.total_edges}
          icon={GitBranch}
          color="indigo"
          changed={dataChanged.edges}
        />
        <StatsCard
          title="健康评分"
          value={stats.health_score}
          icon={Activity}
          color={stats.health_score >= 80 ? "green" : "amber"}
          trend={stats.health_score >= 80 ? "状态良好" : "需要关注"}
          changed={dataChanged.health}
        />
        <StatsCard
          title="最近更新"
          value={stats.recent_pages?.length || 0}
          icon={Clock}
          color="purple"
          changed={dataChanged.recent}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5">
          <div className="flex items-center gap-2 mb-4">
            <PieChart className="w-5 h-5 text-slate-400" />
            <h2 className="font-semibold text-slate-800">文件类型分布</h2>
          </div>
          <div className="space-y-3">
            {typeEntries.map(([type, count]) => (
              <div key={type} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                  <span className="text-sm text-slate-600">{type}</span>
                </div>
                <span className="text-sm font-medium text-slate-800">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 overflow-hidden">
          <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
            <h2 className="font-semibold text-slate-800">最近更新</h2>
            <span className="text-xs text-slate-400">Top 10</span>
          </div>
          <PageList pages={stats.recent_pages?.slice(0, 10) || []} />
        </div>
      </div>
    </div>
  )
}