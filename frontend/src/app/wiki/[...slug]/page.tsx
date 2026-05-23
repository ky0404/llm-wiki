"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { getWikiContent } from "@/lib/api"

export default function WikiPage() {
  const params = useParams()
  const slug = Array.isArray(params.slug) ? params.slug.join("/") : params.slug
  const [data, setData] = useState<{ content: string; frontmatter: Record<string, string>; raw: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    async function fetchPage() {
      setLoading(true)
      setError(null)
      try {
        const json = await getWikiContent(slug || "")
        if (!cancelled) {
          setData(json)
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "加载失败")
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }
    if (slug) fetchPage()
    return () => { cancelled = true }
  }, [slug])

  if (loading) return <div className="p-8 text-slate-500">加载中...</div>
  if (error) return (
    <div className="max-w-lg mx-auto mt-16 p-8 text-center">
      <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center">
        <span className="text-3xl">📄</span>
      </div>
      <h2 className="text-xl font-semibold text-slate-800 mb-2">页面未找到</h2>
      <p className="text-slate-500 mb-4">{slug}</p>
      <p className="text-sm text-slate-400">该页面不存在或已被移动</p>
      <a href="/" className="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
        返回首页
      </a>
    </div>
  )
  if (!data) return <div className="p-8 text-slate-500">无内容</div>

  return (
    <div className="max-w-4xl mx-auto p-8">
      {data.frontmatter?.title && (
        <h1 className="text-3xl font-bold text-slate-800 mb-4">{data.frontmatter.title}</h1>
      )}
      {data.frontmatter?.tags && (
        <div className="flex gap-2 mb-6">
          {data.frontmatter.tags?.split(",").map((tag: string) => (
            <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
              {tag.trim()}
            </span>
          ))}
        </div>
      )}
      <article 
        className="wiki-content"
        dangerouslySetInnerHTML={{ __html: data.content }} 
      />
    </div>
  )
}