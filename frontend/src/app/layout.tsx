import type { Metadata } from "next"
import "./globals.css"
import DashboardLayout from "@/components/DashboardLayout"

export const metadata: Metadata = {
  title: "Wiki Dashboard - 知识库管理",
  description: "Wiki知识库管理系统",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">
        <DashboardLayout>{children}</DashboardLayout>
      </body>
    </html>
  )
}