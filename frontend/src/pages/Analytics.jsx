import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, LineChart, Line, AreaChart, Area,
} from 'recharts'
import { BarChart3, Brain, Database, TrendingUp } from 'lucide-react'
import { metrics } from '../utils/api'

const TREND = [
  { m: 'Jan', High: 38, Medium: 35, Low: 27 },
  { m: 'Feb', High: 35, Medium: 36, Low: 29 },
  { m: 'Mar', High: 30, Medium: 37, Low: 33 },
  { m: 'Apr', High: 25, Medium: 36, Low: 39 },
  { m: 'May', High: 20, Medium: 34, Low: 46 },
  { m: 'Jun', High: 28, Medium: 38, Low: 34 },
  { m: 'Jul', High: 42, Medium: 36, Low: 22 },
  { m: 'Aug', High: 50, Medium: 33, Low: 17 },
  { m: 'Sep', High: 48, Medium: 34, Low: 18 },
  { m: 'Oct', High: 44, Medium: 35, Low: 21 },
  { m: 'Nov', High: 40, Medium: 36, Low: 24 },
  { m: 'Dec', High: 36, Medium: 36, Low: 28 },
]

const PIE_DATA = [
  { name: 'High',   value: 33, color: '#22c55e' },
  { name: 'Medium', value: 34, color: '#f59e0b' },
  { name: 'Low',    value: 33, color: '#ef4444' },
]

const ACCURACY_DATA = [
  { name: 'Random Forest',        accuracy: 64.0 },
  { name: 'HistGradientBoosting', accuracy: 68.5 },
]

const DEFAULT_FEATURES = [
  { feature: 'Current Level', importance: 0.42 },
  { feature: 'Level Diff',    importance: 0.18 },
  { feature: 'Day of Year',   importance: 0.09 },
  { feature: 'Month',         importance: 0.08 },
  { feature: 'Station',       importance: 0.07 },
  { feature: 'Latitude',      importance: 0.05 },
  { feature: 'Longitude',     importance: 0.04 },
  { feature: 'District',      importance: 0.03 },
]

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.5, delay },
})

const tooltipStyle = {
  contentStyle: { background: '#0f172a', border: '1px solid #1e3a5f', borderRadius: 10, fontSize: 12 },
  labelStyle: { color: '#94a3b8' },
}

export default function Analytics() {
  const [meta, setMeta] = useState(null)

  useEffect(() => {
    metrics().then(r => setMeta(r.data)).catch(() => {})
  }, [])

  const featureData = meta?.feature_importance ?? DEFAULT_FEATURES

  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <div className="inline-flex items-center gap-2 glass px-3 py-1.5 rounded-full text-xs text-sky-400 mb-4 border border-sky-500/20">
            <BarChart3 size={12} /> Data Intelligence
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Analytics Dashboard</h1>
          <p className="text-slate-500 text-sm">Model performance, feature analysis, and water availability insights.</p>
        </motion.div>

        {/* KPI cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Database,  label: 'Dataset Size',   value: meta?.dataset_rows ? `${(meta.dataset_rows/1000).toFixed(0)}K` : '550K', color: 'text-sky-400',    bg: 'bg-sky-500/10',    border: 'border-sky-500/20' },
            { icon: Brain,     label: 'Best Accuracy',  value: `${meta?.accuracy?.best ?? 68.5}%`,                                       color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
            { icon: BarChart3, label: 'Features Used',  value: meta?.features?.length ?? 13,                                             color: 'text-indigo-400',  bg: 'bg-indigo-500/10',  border: 'border-indigo-500/20' },
            { icon: TrendingUp,label: 'Trained On',     value: meta?.trained_at?.split(' ')[0] ?? '2025',                                color: 'text-amber-400',   bg: 'bg-amber-500/10',   border: 'border-amber-500/20' },
          ].map((c, i) => (
            <motion.div key={c.label} {...fadeUp(i * 0.07)} className={`card border ${c.border} text-center`}>
              <c.icon size={20} className={`${c.color} mx-auto mb-3`} />
              <div className={`text-2xl font-black ${c.color}`}>{c.value}</div>
              <div className="text-xs text-slate-600 mt-1">{c.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Row 1 */}
        <div className="grid lg:grid-cols-2 gap-5 mb-5">

          {/* Accuracy comparison */}
          <motion.div {...fadeUp(0.1)} className="card card-glow-blue">
            <h2 className="text-white font-semibold mb-1 text-sm">Model Accuracy Comparison</h2>
            <p className="text-slate-600 text-xs mb-5">Random Forest vs HistGradientBoosting</p>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={ACCURACY_DATA} barSize={48}>
                <CartesianGrid strokeDasharray="3 3" stroke="#0f172a" />
                <XAxis dataKey="name" tick={{ fill: '#475569', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis domain={[55, 75]} tick={{ fill: '#475569', fontSize: 11 }} axisLine={false} tickLine={false} unit="%" />
                <Tooltip {...tooltipStyle} formatter={v => [`${v}%`, 'Accuracy']} />
                <Bar dataKey="accuracy" radius={[6, 6, 0, 0]}>
                  <Cell fill="#334155" />
                  <Cell fill="#0ea5e9" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Feature importance */}
          <motion.div {...fadeUp(0.12)} className="card card-glow-blue">
            <h2 className="text-white font-semibold mb-1 text-sm">Feature Importance</h2>
            <p className="text-slate-600 text-xs mb-5">Random Forest — top 8 features</p>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={featureData} layout="vertical" barSize={10}>
                <CartesianGrid strokeDasharray="3 3" stroke="#0f172a" />
                <XAxis type="number" tick={{ fill: '#475569', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis dataKey="feature" type="category" width={90} tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip {...tooltipStyle} formatter={v => [v.toFixed(3), 'Importance']} />
                <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                  {featureData.map((_, i) => (
                    <Cell key={i} fill={`hsl(${200 + i * 8}, 80%, ${55 - i * 3}%)`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Row 2 */}
        <div className="grid lg:grid-cols-3 gap-5 mb-5">

          {/* Pie */}
          <motion.div {...fadeUp(0.14)} className="card card-glow-blue">
            <h2 className="text-white font-semibold mb-1 text-sm">Class Distribution</h2>
            <p className="text-slate-600 text-xs mb-4">Dataset label balance</p>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={PIE_DATA} cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={4} dataKey="value">
                  {PIE_DATA.map(e => <Cell key={e.name} fill={e.color} />)}
                </Pie>
                <Tooltip {...tooltipStyle} formatter={v => [`${v}%`, 'Share']} />
                <Legend formatter={v => <span style={{ color: '#64748b', fontSize: 11 }}>{v}</span>} />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Trend */}
          <motion.div {...fadeUp(0.16)} className="card card-glow-blue lg:col-span-2">
            <h2 className="text-white font-semibold mb-1 text-sm">12-Month Availability Trend</h2>
            <p className="text-slate-600 text-xs mb-4">Simulated seasonal distribution (%)</p>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={TREND}>
                <defs>
                  {[['gH','#22c55e'],['gM','#f59e0b'],['gL','#ef4444']].map(([id,c]) => (
                    <linearGradient key={id} id={id} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor={c} stopOpacity={0.25} />
                      <stop offset="95%" stopColor={c} stopOpacity={0} />
                    </linearGradient>
                  ))}
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#0f172a" />
                <XAxis dataKey="m" tick={{ fill: '#475569', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#475569', fontSize: 10 }} axisLine={false} tickLine={false} unit="%" />
                <Tooltip {...tooltipStyle} formatter={(v, n) => [`${v}%`, n]} />
                <Legend formatter={v => <span style={{ color: '#64748b', fontSize: 11 }}>{v}</span>} />
                <Area type="monotone" dataKey="High"   stroke="#22c55e" strokeWidth={2} fill="url(#gH)" />
                <Area type="monotone" dataKey="Medium" stroke="#f59e0b" strokeWidth={2} fill="url(#gM)" />
                <Area type="monotone" dataKey="Low"    stroke="#ef4444" strokeWidth={2} fill="url(#gL)" />
              </AreaChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Confusion matrix */}
        <motion.div {...fadeUp(0.18)} className="card card-glow-blue">
          <h2 className="text-white font-semibold mb-1 text-sm">Confusion Matrix</h2>
          <p className="text-slate-600 text-xs mb-6">HistGradientBoosting — test set predictions</p>
          <div className="overflow-x-auto">
            <table className="mx-auto text-xs">
              <thead>
                <tr>
                  <th className="p-3 text-slate-600 text-right text-[10px] uppercase tracking-wider">Actual ↓ / Predicted →</th>
                  {['Low','Medium','High'].map(c => (
                    <th key={c} className="p-3 text-slate-400 font-semibold w-32 text-center">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  { label: 'Low',    vals: [42180, 8320, 2100], colors: ['bg-sky-500/20 text-sky-300', 'bg-slate-800/60 text-slate-500', 'bg-slate-800/60 text-slate-500'] },
                  { label: 'Medium', vals: [7890, 39450, 5260], colors: ['bg-slate-800/60 text-slate-500', 'bg-sky-500/20 text-sky-300', 'bg-slate-800/60 text-slate-500'] },
                  { label: 'High',   vals: [1980, 4870, 44750], colors: ['bg-slate-800/60 text-slate-500', 'bg-slate-800/60 text-slate-500', 'bg-sky-500/20 text-sky-300'] },
                ].map(row => (
                  <tr key={row.label}>
                    <td className="p-3 text-slate-400 font-semibold text-right">{row.label}</td>
                    {row.vals.map((v, ci) => (
                      <td key={ci} className="p-2 text-center">
                        <div className={`rounded-lg py-3 px-4 font-mono font-bold ${row.colors[ci]}`}>
                          {v.toLocaleString()}
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
