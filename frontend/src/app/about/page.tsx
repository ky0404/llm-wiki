"use client"

import { Github, BookOpen, Server, Database, Code2, Search } from "lucide-react"

const features = [
  {
    title: "仪表盘",
    description: "实时展示知识库统计信息，包括文件数量、边数、健康评分等",
    icon: BookOpen,
    color: "blue",
  },
  {
    title: "知识图谱",
    description: "交互式可视化知识图谱，支持缩放、拖拽、节点筛选",
    icon: Database,
    color: "indigo",
  },
  {
    title: "全文搜索",
    description: "快速检索知识库中的所有内容，支持高亮显示",
    icon: Search,
    color: "green",
  },
]

const techStack = [
  "Next.js 14", "TypeScript", "Tailwind CSS", "Shadcn/ui", 
  "FastAPI", "React Force Graph", "Lucide Icons"
]

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-800">关于</h1>
        <p className="text-slate-500 mt-2">Wiki 知识库管理系统</p>
      </div>

      {/* Info Cards */}
      <div className="grid gap-4">
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
              <Server className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-800">后端 API</h3>
              <p className="text-sm text-slate-500">localhost:8000</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center">
              <Github className="w-6 h-6 text-purple-500" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-800">GitHub</h3>
              <a 
                href="https://github.com/ky0404/llm-wiki" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-500 hover:underline"
              >
                ky0404/llm-wiki
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5">
        <h2 className="font-semibold text-slate-800 mb-4">功能特性</h2>
        <div className="space-y-4">
          {features.map((feature, idx) => (
            <div key={idx} className="flex items-start gap-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 bg-${feature.color}-50`}>
                <feature.icon className={`w-5 h-5 text-${feature.color}-500`} />
              </div>
              <div>
                <h3 className="font-medium text-slate-800">{feature.title}</h3>
                <p className="text-sm text-slate-500 mt-0.5">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-6 text-white">
        <div className="flex items-center gap-3 mb-4">
          <Code2 className="w-6 h-6" />
          <h2 className="font-semibold">技术栈</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {techStack.map(tech => (
            <span 
              key={tech}
              className="px-3 py-1.5 bg-white/10 rounded-full text-sm"
            >
              {tech}
            </span>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-sm text-slate-400">
        <p>© 2026 Wiki System. All rights reserved.</p>
      </div>
    </div>
  )
}