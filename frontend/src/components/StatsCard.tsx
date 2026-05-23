"use client"

import { LucideIcon } from "lucide-react"

interface StatsCardProps {
  title: string
  value: number | string
  suffix?: string
  subtitle?: string
  icon: LucideIcon
  color?: "blue" | "indigo" | "green" | "purple" | "orange" | "red"
}

const colorClasses = {
  blue: "from-blue-500 to-blue-600 bg-blue-50 text-blue-600",
  indigo: "from-indigo-500 to-indigo-600 bg-indigo-50 text-indigo-600",
  green: "from-green-500 to-green-600 bg-green-50 text-green-600",
  purple: "from-purple-500 to-purple-600 bg-purple-50 text-purple-600",
  orange: "from-orange-500 to-orange-600 bg-orange-50 text-orange-600",
  red: "from-red-500 to-red-600 bg-red-50 text-red-600",
}

export default function StatsCard({ 
  title, 
  value, 
  suffix, 
  subtitle,
  icon: Icon, 
  color = "blue" 
}: StatsCardProps) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="text-3xl font-bold text-slate-900 mt-2">
            {value}
            {suffix && <span className="text-lg font-normal text-slate-400">{suffix}</span>}
          </p>
          {subtitle && (
            <p className="text-sm text-slate-400 mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  )
}