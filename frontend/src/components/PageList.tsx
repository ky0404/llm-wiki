"use client"

import { FileText, Tag } from "lucide-react"

interface PageItem {
  path: string
  title: string
  type?: string
  tags?: string[]
}

interface PageListProps {
  pages: PageItem[]
  limit?: number
}

const typeColors: Record<string, string> = {
  concept: "bg-blue-100 text-blue-700",
  entity: "bg-purple-100 text-purple-700",
  source: "bg-green-100 text-green-700",
  synthesis: "bg-amber-100 text-amber-700",
  index: "bg-red-100 text-red-700",
  unknown: "bg-slate-100 text-slate-700",
}

export default function PageList({ pages, limit }: PageListProps) {
  const displayPages = limit ? pages.slice(0, limit) : pages

  if (displayPages.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500">
        暂无数据
      </div>
    )
  }

  return (
    <div className="divide-y divide-slate-100">
      {displayPages.map((page, index) => (
        <div
          key={index}
          className="px-6 py-4 hover:bg-slate-50 transition-colors cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 min-w-0">
              <FileText className="w-4 h-4 text-slate-400 flex-shrink-0" />
              <div className="min-w-0">
                <p className="font-medium text-slate-900 truncate">
                  {page.title || page.path}
                </p>
                <p className="text-sm text-slate-400 truncate">
                  {page.path}
                </p>
              </div>
            </div>
            {page.type && (
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${typeColors[page.type] || typeColors.unknown}`}>
                {page.type}
              </span>
            )}
          </div>
          {page.tags && page.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2 ml-7">
              {page.tags.slice(0, 3).map(tag => (
                <span 
                  key={tag}
                  className="inline-flex items-center gap-1 px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-xs"
                >
                  <Tag className="w-3 h-3" />
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}