import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Activity, AlertTriangle, Brain, CheckCircle,
  Clock, Droplets, Send, Trash2, XCircle,
  Lightbulb, TrendingUp, ShieldAlert, BarChart2,
} from 'lucide-react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'
import toast from 'react-hot-toast'
import { predict, explain, forecast, recommend } from '../utils/api'
import { generatePDF } from '../utils/pdfExport'

/* ── Field config ─────────────────────────────────────────────────────────── */
const FIELDS = [
  { key: 'currentlevel', label: 'Groundwater Level', unit: 'm',   icon: Droplets,  type: 'number', placeholder: '5.2',      hint: 'Depth below ground (metres)' },
  { key: 'level_diff',   label: 'Level Difference',  unit: 'm',   icon: Activity,  type: 'number', placeholder: '-0.3',     hint: 'Change from previous reading' },
  { key: 'latitude',     label: 'Latitude',           unit: '°',   icon: Brain,     type: 'number', placeholder: '28.6139',  hint: 'Decimal degrees' },
  { key: 'longitude',    label: 'Longitude',          unit: '°',   icon: Brain,     type: 'number', placeholder: '77.2090',  hint: 'Decimal degrees' },
  { key: 'date',         label: 'Observation Date',   unit: '',    icon: Clock,     type: 'date',   placeholder: '',         hint: 'Date of measurement' },
  { key: 'state_name',   label: 'State',              unit: '',    icon: Activity,  type: 'text',   placeholder: 'Rajasthan',hint: 'Indian state name' },
  { key: 'district_name',label: 'District',           unit: '',    icon: Activity,  type: 'text',   placeholder: 'Jaipur',   hint: 'District name' },
  { key: 'basin',        label: 'River Basin',        unit: '',    icon: Droplets,  type: 'text',   placeholder: 'Indus',    hint: 'Major river basin' },
  { key: 'sub_basin',    label: 'Sub Basin',          unit: '',    icon: Droplets,  type: 'text',   placeholder: 'Beas',     hint: 'Sub-basin name' },
  { key: 'station_name', label: 'Station Name',       unit: '',    icon: Activity,  type: 'text',   placeholder: 'CGWB-001', hint: 'Monitoring station ID' },
]

const INITIAL = Object.fromEntries([
  ...FIELDS.map(f => [f.key, '']),
  ['date', new Date().toISOString().split('T')[0]],
])

/* ── Result config ────────────────────────────────────────────────────────── */
const RESULT_CFG = {
  High:   { icon: CheckCircle,   label: 'High Availability',   cls: 'card-glow-green', text: 'text-emerald-400', bar: 'bg-emerald-500', badge: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30', glow: '0 0 60px rgba(34,197,94,0.2)' },
  Medium: { icon: AlertTriangle, label: 'Medium Availability', cls: 'card-glow-amber', text: 'text-amber-400',   bar: 'bg-amber-500',   badge: 'bg-amber-500/15 text-amber-400 border-amber-500/30',     glow: '0 0 60px rgba(245,158,11,0.2)' },
  Low:    { icon: XCircle,       label: 'Low Availability',    cls: 'card-glow-red',   text: 'text-red-400',     bar: 'bg-red-500',     badge: 'bg-red-500/15 text-red-400 border-red-500/30',           glow: '0 0 60px rgba(239,68,68,0.2)' },
}

const HISTORY_KEY = 'aq_history'

/* ── Risk meter config ────────────────────────────────────────────────────── */
const RISK_CFG = {
  Safe:              { color: '#22c55e', bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
  'Moderate Risk':   { color: '#f59e0b', bg: 'bg-amber-500/10',   text: 'text-amber-400',   border: 'border-amber-500/20' },
  'Critical Scarcity':{ color: '#ef4444', bg: 'bg-red-500/10',    text: 'text-red-400',     border: 'border-red-500/20' },
}

/* ── Forecast color ───────────────────────────────────────────────────────── */
const FORECAST_COLOR = { High: '#22c55e', Medium: '#f59e0b', Low: '#ef4444' }

export default function Predict() {
  const [form, setForm]           = useState(INITIAL)
  const [errors, setErrors]       = useState({})
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState(null)
  const [xai, setXai]             = useState(null)
  const [forecastData, setForecastData] = useState(null)
  const [recs, setRecs]           = useState(null)
  const [activeTab, setActiveTab] = useState('result')
  const [history, setHistory]     = useState(() => {
    try { return JSON.parse(sessionStorage.getItem(HISTORY_KEY) || '[]') } catch { return [] }
  })

  const validate = () => {
    const e = {}
    FIELDS.forEach(f => { if (!form[f.key] && form[f.key] !== 0) e[f.key] = 'Required' })
    ;['latitude','longitude','currentlevel','level_diff'].forEach(k => {
      if (form[k] !== '' && isNaN(Number(form[k]))) e[k] = 'Must be a number'
    })
    return e
  }

  const handleSubmit = async (ev) => {
    ev.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }
    setErrors({})
    setLoading(true)
    setResult(null)
    setXai(null)
    setForecastData(null)
    setRecs(null)
    setActiveTab('result')
    try {
      const payload = {
        ...form,
        latitude:     parseFloat(form.latitude),
        longitude:    parseFloat(form.longitude),
        currentlevel: parseFloat(form.currentlevel),
        level_diff:   parseFloat(form.level_diff),
      }

      // Fire all 4 requests in parallel
      const [predRes, xaiRes, fcRes, recRes] = await Promise.allSettled([
        predict(payload),
        explain(payload),
        forecast(payload),
        predict(payload).then(r => recommend({ prediction: r.data.prediction })),
      ])

      const predData = predRes.status === 'fulfilled' ? predRes.value.data : null
      if (!predData) throw new Error('Prediction failed')

      setResult(predData)
      if (xaiRes.status === 'fulfilled')  setXai(xaiRes.value.data)
      if (fcRes.status === 'fulfilled')   setForecastData(fcRes.value.data)
      if (recRes.status === 'fulfilled')  setRecs(recRes.value.data)

      const entry = { ...predData, timestamp: new Date().toLocaleString(), state: form.state_name }
      const updated = [entry, ...history].slice(0, 15)
      setHistory(updated)
      sessionStorage.setItem(HISTORY_KEY, JSON.stringify(updated))
      toast.success(`Prediction: ${predData.prediction} water availability`)
    } catch (err) {
      toast.error(err.response?.data?.error || 'Backend unreachable. Is Flask running on port 5001?')
    } finally {
      setLoading(false)
    }
  }

  const cfg = result ? RESULT_CFG[result.prediction] || RESULT_CFG.Medium : null

  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10"
        >
          <div className="inline-flex items-center gap-2 glass px-3 py-1.5 rounded-full text-xs text-sky-400 mb-4 border border-sky-500/20">
            <Activity size={12} /> Prediction Engine
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Water Availability Predictor</h1>
          <p className="text-slate-500 text-sm">Enter environmental parameters to get an AI-powered groundwater forecast.</p>
        </motion.div>

        <div className="grid lg:grid-cols-5 gap-6">

          {/* ── INPUT PANEL ── */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-3"
          >
            <form onSubmit={handleSubmit} className="card card-glow-blue space-y-5">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-lg bg-sky-500/10 flex items-center justify-center">
                  <Brain size={16} className="text-sky-400" />
                </div>
                <h2 className="text-white font-semibold">Environmental Parameters</h2>
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                {FIELDS.map(f => (
                  <div key={f.key} className={f.key === 'station_name' ? 'sm:col-span-2' : ''}>
                    <label className="block text-xs font-medium text-slate-400 mb-1.5 uppercase tracking-wider">
                      {f.label} {f.unit && <span className="text-slate-600 normal-case">({f.unit})</span>}
                    </label>
                    <div className="relative">
                      <input
                        type={f.type}
                        value={form[f.key]}
                        onChange={e => setForm(p => ({ ...p, [f.key]: e.target.value }))}
                        placeholder={f.placeholder}
                        className={`input-field pr-4 ${errors[f.key] ? 'border-red-500/50 focus:border-red-500/70' : ''}`}
                      />
                    </div>
                    {errors[f.key]
                      ? <p className="text-red-400 text-xs mt-1">{errors[f.key]}</p>
                      : <p className="text-slate-600 text-xs mt-1">{f.hint}</p>
                    }
                  </div>
                ))}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full justify-center py-3.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    AI Analyzing...
                  </>
                ) : (
                  <><Send size={15} /> Run Prediction</>
                )}
              </button>
            </form>
          </motion.div>

          {/* ── RESULT PANEL ── */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.15 }}
            className="lg:col-span-2 space-y-4"
          >
            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="card card-glow-blue h-64 flex flex-col items-center justify-center gap-4"
                >
                  <div className="relative w-16 h-16">
                    <div className="absolute inset-0 rounded-full border-2 border-sky-500/20 animate-ping" />
                    <div className="absolute inset-2 rounded-full border-2 border-sky-500/40 animate-ping" style={{ animationDelay: '0.3s' }} />
                    <div className="w-16 h-16 rounded-full border-2 border-sky-500/30 border-t-sky-500 animate-spin" />
                  </div>
                  <p className="text-sky-400 text-sm font-medium">AI Processing...</p>
                  <p className="text-slate-600 text-xs">Analyzing 13 environmental features</p>
                </motion.div>
              ) : result && cfg ? (
                <motion.div key="result" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>

                  {/* ── Tabs ── */}
                  <div className="flex gap-1 mb-3 glass rounded-xl p-1">
                    {[
                      { id: 'result',   label: 'Result',      icon: Activity },
                      { id: 'xai',      label: 'AI Explain',  icon: Brain },
                      { id: 'forecast', label: '7-Day',       icon: TrendingUp },
                      { id: 'recs',     label: 'Actions',     icon: Lightbulb },
                    ].map(t => (
                      <button
                        key={t.id}
                        onClick={() => setActiveTab(t.id)}
                        className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-medium transition-all ${
                          activeTab === t.id
                            ? 'bg-sky-500/20 text-sky-400 border border-sky-500/30'
                            : 'text-slate-500 hover:text-slate-300'
                        }`}
                      >
                        <t.icon size={11} /> {t.label}
                      </button>
                    ))}
                  </div>

                  <AnimatePresence mode="wait">

                    {/* ── RESULT TAB ── */}
                    {activeTab === 'result' && (
                      <motion.div key="tab-result" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                        className={`card ${cfg.cls}`} style={{ boxShadow: cfg.glow }}>
                        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${cfg.badge} mb-4`}>
                          <cfg.icon size={13} /> {cfg.label}
                        </div>
                        <div className="mb-5">
                          <div className={`text-5xl font-black ${cfg.text} mb-1`}>{result.prediction}</div>
                          <div className="text-slate-500 text-sm">Water Availability Forecast</div>
                        </div>
                        <div className="mb-4">
                          <div className="flex justify-between text-xs mb-1.5">
                            <span className="text-slate-500">Confidence Score</span>
                            <span className={`font-bold ${cfg.text}`}>{result.confidence_label || `${result.confidence}%`}</span>
                          </div>
                          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <motion.div initial={{ width: 0 }} animate={{ width: `${result.confidence}%` }}
                              transition={{ duration: 0.8, ease: 'easeOut' }}
                              className={`h-full rounded-full ${cfg.bar}`} />
                          </div>
                        </div>

                        {/* Risk meter */}
                        {recs?.risk && (() => {
                          const r = recs.risk
                          const rc = RISK_CFG[r.level] || RISK_CFG['Moderate Risk']
                          return (
                            <div className={`glass rounded-xl p-3 mb-4 border ${rc.border}`}>
                              <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                  <ShieldAlert size={14} className={rc.text} />
                                  <span className={`text-xs font-semibold ${rc.text}`}>{r.level}</span>
                                </div>
                                <span className="text-xs text-slate-500">{r.score}/100</span>
                              </div>
                              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                <motion.div initial={{ width: 0 }} animate={{ width: `${r.score}%` }}
                                  transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
                                  className="h-full rounded-full"
                                  style={{ background: `linear-gradient(90deg, ${rc.color}88, ${rc.color})` }} />
                              </div>
                              <p className="text-slate-600 text-[10px] mt-1.5">{r.message}</p>
                            </div>
                          )
                        })()}

                        <div className="space-y-2 mb-5">
                          <p className="text-xs text-slate-600 uppercase tracking-wider mb-2">Probability Breakdown</p>
                          {Object.entries(result.probabilities || {}).map(([cls, pct]) => {
                            const c = RESULT_CFG[cls]
                            return (
                              <div key={cls}>
                                <div className="flex justify-between text-xs mb-1">
                                  <span className={c?.text || 'text-slate-400'}>{cls}</span>
                                  <span className="text-slate-500">{pct.toFixed(1)}%</span>
                                </div>
                                <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                  <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }}
                                    transition={{ duration: 0.6, delay: 0.2 }}
                                    className={`h-full rounded-full ${c?.bar || 'bg-slate-500'}`} />
                                </div>
                              </div>
                            )
                          })}
                        </div>
                        <button onClick={() => generatePDF(result)} className="btn-ghost w-full justify-center text-xs py-2.5">
                          Download PDF Report
                        </button>
                      </motion.div>
                    )}

                    {/* ── XAI TAB ── */}
                    {activeTab === 'xai' && (
                      <motion.div key="tab-xai" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                        className="card card-glow-blue space-y-4">
                        <div className="flex items-center gap-2 mb-1">
                          <Brain size={16} className="text-sky-400" />
                          <h3 className="text-white font-semibold text-sm">AI Explanation</h3>
                        </div>
                        {xai ? (
                          <>
                            <div className="glass rounded-xl p-4 border-l-2 border-sky-500">
                              <p className="text-slate-300 text-xs leading-relaxed">{xai.explanation?.summary}</p>
                            </div>
                            <div>
                              <p className="text-xs text-slate-600 uppercase tracking-wider mb-3">Top Contributing Features</p>
                              {(xai.explanation?.top_features || []).map((f, i) => (
                                <div key={f.feature} className="mb-3">
                                  <div className="flex justify-between text-xs mb-1">
                                    <span className="text-slate-300">{f.feature}</span>
                                    <span className="text-sky-400 font-mono">{f.value}</span>
                                  </div>
                                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                    <motion.div
                                      initial={{ width: 0 }}
                                      animate={{ width: `${Math.min(f.contribution * 200, 100)}%` }}
                                      transition={{ duration: 0.7, delay: i * 0.1 }}
                                      className="h-full rounded-full bg-gradient-to-r from-sky-600 to-sky-400"
                                    />
                                  </div>
                                  <div className="text-[10px] text-slate-600 mt-0.5">Importance: {(f.importance * 100).toFixed(1)}%</div>
                                </div>
                              ))}
                            </div>
                          </>
                        ) : (
                          <p className="text-slate-600 text-xs text-center py-8">XAI data unavailable — backend may not support /explain yet.</p>
                        )}
                      </motion.div>
                    )}

                    {/* ── FORECAST TAB ── */}
                    {activeTab === 'forecast' && (
                      <motion.div key="tab-forecast" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                        className="card card-glow-blue">
                        <div className="flex items-center gap-2 mb-4">
                          <TrendingUp size={16} className="text-sky-400" />
                          <h3 className="text-white font-semibold text-sm">7-Day Water Forecast</h3>
                        </div>
                        {forecastData ? (
                          <>
                            <ResponsiveContainer width="100%" height={160}>
                              <LineChart data={forecastData.forecast}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#0f172a" />
                                <XAxis dataKey="day" tick={{ fill: '#475569', fontSize: 10 }} axisLine={false} tickLine={false} />
                                <YAxis tick={{ fill: '#475569', fontSize: 10 }} axisLine={false} tickLine={false} unit="m" />
                                <Tooltip
                                  contentStyle={{ background: '#0f172a', border: '1px solid #1e3a5f', borderRadius: 8, fontSize: 11 }}
                                  formatter={(v, n) => [`${v}m`, 'Level']}
                                />
                                <ReferenceLine y={3.65} stroke="#22c55e" strokeDasharray="4 2" strokeOpacity={0.5} />
                                <ReferenceLine y={7.76} stroke="#ef4444" strokeDasharray="4 2" strokeOpacity={0.5} />
                                <Line type="monotone" dataKey="level" stroke="#38bdf8" strokeWidth={2} dot={{ fill: '#38bdf8', r: 3 }} />
                              </LineChart>
                            </ResponsiveContainer>
                            <div className="mt-3 space-y-1.5">
                              {forecastData.forecast.map(d => {
                                const c = RESULT_CFG[d.prediction]
                                return (
                                  <div key={d.date} className="flex items-center justify-between glass rounded-lg px-3 py-2">
                                    <span className="text-slate-500 text-xs w-10">{d.day}</span>
                                    <span className="text-slate-400 text-xs font-mono">{d.level}m</span>
                                    <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${c?.badge || ''}`}>{d.prediction}</span>
                                    <span className="text-slate-600 text-[10px]">{d.confidence}%</span>
                                  </div>
                                )
                              })}
                            </div>
                          </>
                        ) : (
                          <p className="text-slate-600 text-xs text-center py-8">Forecast unavailable — backend may not support /forecast yet.</p>
                        )}
                      </motion.div>
                    )}

                    {/* ── RECOMMENDATIONS TAB ── */}
                    {activeTab === 'recs' && (
                      <motion.div key="tab-recs" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                        className="card card-glow-blue space-y-3">
                        <div className="flex items-center gap-2 mb-1">
                          <Lightbulb size={16} className="text-sky-400" />
                          <h3 className="text-white font-semibold text-sm">AI Recommendations</h3>
                        </div>
                        {recs?.recommendations ? recs.recommendations.map((rec, i) => {
                          const priorityColor = rec.priority === 'critical' ? 'text-red-400 border-red-500/20 bg-red-500/5'
                            : rec.priority === 'high' ? 'text-amber-400 border-amber-500/20 bg-amber-500/5'
                            : rec.priority === 'medium' ? 'text-yellow-400 border-yellow-500/20 bg-yellow-500/5'
                            : 'text-emerald-400 border-emerald-500/20 bg-emerald-500/5'
                          return (
                            <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: i * 0.08 }}
                              className={`glass rounded-xl p-3 border ${priorityColor}`}>
                              <div className="flex items-start justify-between gap-2 mb-1">
                                <span className="text-white text-xs font-semibold">{rec.title}</span>
                                <span className={`text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded font-bold ${priorityColor}`}>
                                  {rec.priority}
                                </span>
                              </div>
                              <p className="text-slate-500 text-[11px] leading-relaxed">{rec.detail}</p>
                              <span className="text-[10px] text-slate-600 mt-1 block">{rec.category}</span>
                            </motion.div>
                          )
                        }) : (
                          <p className="text-slate-600 text-xs text-center py-8">Recommendations unavailable.</p>
                        )}
                      </motion.div>
                    )}

                  </AnimatePresence>
                </motion.div>
              ) : (
                <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  className="card h-64 flex flex-col items-center justify-center text-center">
                  <div className="w-14 h-14 rounded-2xl bg-sky-500/5 border border-sky-500/10 flex items-center justify-center mb-4">
                    <Droplets size={24} className="text-sky-500/40" />
                  </div>
                  <p className="text-slate-500 text-sm font-medium">Awaiting Input</p>
                  <p className="text-slate-700 text-xs mt-1">Fill the form and run prediction</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Quick tips */}
            <div className="card text-xs space-y-2">
              <p className="text-slate-500 uppercase tracking-wider text-[10px] mb-3">Prediction Guide</p>
              {[
                ['≤ 3.65m depth', 'High availability'],
                ['3.65 – 7.76m',  'Medium availability'],
                ['> 7.76m depth', 'Low availability'],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between">
                  <span className="text-slate-600">{k}</span>
                  <span className="text-slate-400">{v}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* ── HISTORY TABLE ── */}
        <AnimatePresence>
          {history.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-8 card card-glow-blue"
            >
              <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                  <Clock size={16} className="text-sky-400" />
                  <h2 className="text-white font-semibold text-sm">Prediction History</h2>
                  <span className="text-[10px] bg-sky-500/10 text-sky-400 border border-sky-500/20 px-2 py-0.5 rounded-full">{history.length}</span>
                </div>
                <button
                  onClick={() => { setHistory([]); sessionStorage.removeItem(HISTORY_KEY); toast.success('History cleared') }}
                  className="flex items-center gap-1 text-xs text-slate-600 hover:text-red-400 transition-colors"
                >
                  <Trash2 size={12} /> Clear
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="border-b border-white/5">
                      {['Time','State','Prediction','Confidence','Status'].map(h => (
                        <th key={h} className="text-left text-slate-600 font-medium pb-3 pr-6 uppercase tracking-wider text-[10px]">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((row, i) => {
                      const c = RESULT_CFG[row.prediction]
                      return (
                        <tr key={i} className="border-b border-white/3 hover:bg-white/2 transition-colors">
                          <td className="py-3 pr-6 text-slate-600">{row.timestamp}</td>
                          <td className="py-3 pr-6 text-slate-400">{row.state || '—'}</td>
                          <td className="py-3 pr-6">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium border ${c?.badge || ''}`}>
                              {row.prediction}
                            </span>
                          </td>
                          <td className="py-3 pr-6 text-slate-400">{row.confidence_label || `${row.confidence}%`}</td>
                          <td className="py-3 text-slate-400">{row.current_status}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
