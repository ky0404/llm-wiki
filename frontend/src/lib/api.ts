const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface WikiStats {
  total_files: number
  total_edges: number
  health_score: number
  type_distribution: Record<string, number>
  recent_pages: Array<{
    path: string
    title: string
    type: string
    tags: string[]
  }>
  metadata: Record<string, any>
}

export interface GraphNode {
  id: string
  title: string
  type: string
  tags: string[]
}

export interface GraphEdge {
  source: string
  target: string
}

export interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export interface SearchResult {
  file: string
  title: string
  line: string
  snippet: string
}

export interface SearchResponse {
  total: number
  results: SearchResult[]
}

export interface PageItem {
  path: string
  title: string
}

export interface PagesResponse {
  total: number
  pages: PageItem[]
}

async function fetchApi<T>(endpoint: string): Promise<T> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 10000)

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      },
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

export async function getWikiStats(): Promise<WikiStats> {
  return fetchApi<WikiStats>("/wiki/stats")
}

export async function getKnowledgeGraph(): Promise<GraphData> {
  return fetchApi<GraphData>("/wiki/graph")
}

export async function searchWiki(query: string): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query })
  return fetchApi<SearchResponse>(`/wiki/search?${params}`)
}

export async function getPages(limit: number = 50): Promise<PagesResponse> {
  const params = new URLSearchParams({ limit: limit.toString() })
  return fetchApi<PagesResponse>(`/wiki/pages?${params}`)
}

export async function getWikiHealth(): Promise<{ status: string; cache_exists: boolean }> {
  return fetchApi<{ status: string; cache_exists: boolean }>("/wiki/health")
}

export async function getWikiContent(path: string): Promise<{ content: string; frontmatter: Record<string, string>; raw: string }> {
  const params = new URLSearchParams({ path: decodeURIComponent(path) })
  return fetchApi<{ content: string; frontmatter: Record<string, string>; raw: string }>(`/wiki/content?${params}`)
}