"use client"

import { useState, FormEvent, useEffect } from "react"
import { Search, FileText, Hash, Clock, X, ArrowRight } from "lucide-react"
import { searchWiki, SearchResult } from "@/lib/api"

function SearchInput({ 
  value, 
  onChange, 
  onSubmit,
  loading 
}: { 
  value: string
  onChange: (v: string) => void
  onSubmit: () => void
  loading: boolean
}) {
  return (
    <form onSubmit={(e: FormEvent) => { e.preventDefault(); onSubmit() }} className="relative">
      <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
      <input
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder="搜索关键词..."
        className="w-full pl-12 pr-24 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm 
          focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
          text-base placeholder:text-slate-400 transition-all"
      />
      <button
        type="submit"
        disabled={loading || !value.trim()}
        className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 
          bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-medium rounded-xl
          hover:from-blue-600 hover:to-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed
          transition-all duration-200"
      >
        {loading ? (
          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        ) : (
          '搜索'
        )}
      </button>
    </form>
  )
}

function SearchResultCard({ result, index }: { result: SearchResult; index: number }) {
  const handleClick = () => {
    window.open(`/wiki/${result.file.replace(/\.md$/, '')}`, '_blank')
  }
  return (
    <div onClick={handleClick} className="group bg-white rounded-xl border border-slate-200/80 p-4 hover:shadow-md hover:border-blue-200 transition-all duration-200 cursor-pointer">
      <div className="flex items-start gap-3">
        <div className="w-9 h-9 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
          <FileText className="w-4 h-4 text-blue-500" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-medium text-slate-800 truncate group-hover:text-blue-600 transition-colors">
              {result.title || result.file}
            </span>
            <span className="flex items-center gap-1 text-xs text-slate-400 bg-slate-50 px-2 py-0.5 rounded">
              <Hash className="w-3 h-3" />
              {result.line}
            </span>
          </div>
          <p className="text-xs text-slate-400 truncate mb-1">{result.file}</p>
          <p className="text-sm text-slate-600 line-clamp-2 leading-relaxed">
            {result.snippet}
          </p>
        </div>
        <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-blue-500 transition-colors flex-shrink-0" />
      </div>
    </div>
  )
}

function EmptyState({ query }: { query: string }) {
  return (
    <div className="text-center py-16">
      <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <Search className="w-7 h-7 text-slate-300" />
      </div>
      <p className="text-slate-500 mb-2">未找到与 "{query}" 相关的内容</p>
      <p className="text-sm text-slate-400">试试其他关键词</p>
    </div>
  )
}

function InitialState() {
  return (
    <div className="text-center py-16">
      <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <Search className="w-7 h-7 text-slate-300" />
      </div>
      <p className="text-slate-500">输入关键词开始搜索</p>
      <p className="text-sm text-slate-400 mt-1">支持模糊匹配</p>
      
      <div className="mt-8 flex flex-wrap justify-center gap-2">
        {['RAG', 'LLM', 'Transformer', 'Agent'].map(tag => (
          <span 
            key={tag}
            className="px-3 py-1 bg-slate-100 text-slate-500 rounded-full text-sm"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  )
}

export default function SearchPage() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<SearchResult[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    setHasSearched(true)

    try {
      setError(null)
      const data = await searchWiki(query)
      setResults(data.results)
      setTotal(data.total)
    } catch (err) {
      console.error("Search error:", err)
      setError(err instanceof Error ? err.message : "搜索失败")
      setResults([])
      setTotal(0)
    } finally {
      setLoading(false)
    }
  }

  // Clear results when query is empty
  useEffect(() => {
    if (!query.trim()) {
      setResults([])
      setHasSearched(false)
    }
  }, [query])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800">搜索</h1>
        <p className="text-slate-500 mt-1">全文搜索知识库</p>
      </div>

      {/* Search Input */}
      <SearchInput
        value={query}
        onChange={setQuery}
        onSubmit={handleSearch}
        loading={loading}
      />

      {/* Results */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
          错误: {error}
        </div>
      )}
      {hasSearched && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-500">
              找到 <span className="font-semibold text-blue-600">{total}</span> 个结果
            </p>
            {results.length > 0 && (
              <button
                onClick={() => { setQuery(""); setHasSearched(false) }}
                className="flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
                清除
              </button>
            )}
          </div>

          {results.length === 0 && !loading ? (
            <EmptyState query={query} />
          ) : (
            <div className="space-y-3">
              {results.map((result, idx) => (
                <SearchResultCard key={idx} result={result} index={idx} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Initial State */}
      {!hasSearched && !loading && (
        <InitialState />
      )}
    </div>
  )
}