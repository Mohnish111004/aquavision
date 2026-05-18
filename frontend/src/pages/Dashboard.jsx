import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Activity, ArrowRight, BarChart3, Brain, CloudRain,
  Cpu, Database, Droplets, TrendingUp, Zap, CheckCircle,
} from 'lucide-react'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts'

/* ── Animated counter ─────────────────────────────────────────────────────── */
function Counter({ target, suffix = '', duration = 2000 }) {
  const [val, setVal] = useState(0)
  const ref = useRef(null)
  useEffect(() => {
    const observer = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return
      observer.disconnect()
      const start = performance.now()
      const tick = (now) => {
        const p = Math.min((now - start) / duration, 1)
        setVal(Math.floor(p * target))
        if (p < 1) requestAnimationFrame(tick)
        else setVal(target)
      }
      requestAnimationFrame(tick)
    })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, duration])
  return <span ref={ref}>{val}{suffix}</span>
}

/* ── Trend data ───────────────────────────────────────────────────────────── */
const trendData = [
  { m: 'Jan', high: 38, med: 35, low: 27 },
  { m: 'Feb', high: 35, med: 36, low: 29 },
  { m: 'Mar', high: 30, med: 37, low: 33 },
  { m: 'Apr', high: 25, med: 36, low: 39 },
  { m: 'May', high: 20, med: 34, low: 46 },
  { m: 'Jun', high: 28, med: 38, low: 34 },
  { m: 'Jul', high: 42, med: 36, low: 22 },
  { m: 'Aug', high: 50, med: 33, low: 17 },
  { m: 'Sep', high: 48, med: 34, low: 18 },
  { m: 'Oct', high: 44, med: 35, low: 21 },
  { m: 'Nov', high: 40, med: 36, low: 24 },
  { m: 'Dec', high: 36, med: 36, low: 28 },
]

const metrics = [
  { label: 'Model Accuracy',       value: 68,    suffix: '%',  icon: Brain,      color: 'sky',     desc: 'HistGradientBoosting' },
  { label: 'Dataset Records',      value: 550,   suffix: 'K',  icon: Database,   color: 'indigo',  desc: 'CGWB monitoring data' },
  { label: 'Prediction Classes',   value: 3,     suffix: '',   icon: Activity,   color: 'cyan',    desc: 'High · Medium · Low' },
  { label: 'States Covered',       value: 28,    suffix: '+',  icon: TrendingUp, color: 'violet',  desc: 'Across India' },
]

const colorMap = {
  sky:    { text: 'text-sky-400',    bg: 'bg-sky-500/10',    border: 'border-sky-500/20',    glow: 'rgba(56,189,248,0.15)' },
  indigo: { text: 'text-indigo-400', bg: 'bg-indigo-500/10', border: 'border-indigo-500/20', glow: 'rgba(99,102,241,0.15)' },
  cyan:   { text: 'text-cyan-400',   bg: 'bg-cyan-500/10',   border: 'border-cyan-500/20',   glow: 'rgba(6,182,212,0.15)' },
  violet: { text: 'text-violet-400', bg: 'bg-violet-500/10', border: 'border-violet-500/20', glow: 'rgba(139,92,246,0.15)' },
}

const steps = [
  { n: '01', icon: CloudRain,  title: 'Input Environmental Data',    desc: 'Enter groundwater level, location, date, and regional identifiers.' },
  { n: '02', icon: Cpu,        title: 'AI Model Processes Data',     desc: '13 features processed by HistGradientBoosting trained on 550K+ records.' },
  { n: '03', icon: CheckCircle,title: 'Predict Water Availability',  desc: 'Receive High / Medium / Low prediction with confidence score.' },
]

const perfMetrics = [
  { label: 'Accuracy',  value: 68.5, color: '#38bdf8' },
  { label: 'Precision', value: 71.2, color: '#818cf8' },
  { label: 'Recall',    value: 66.8, color: '#06b6d4' },
  { label: 'F1 Score',  value: 68.9, color: '#34d399' },
]

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.55, delay, ease: [0.4, 0, 0.2, 1] },
})

export default function Dashboard() {
  return (
    <div className="pt-16">

      {/* ── HERO ──────────────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex items-center overflow-hidden">
        {/* Animated blobs */}
        <div className="absolute inset-0 pointer-events-none">
          <motion.div
            className="absolute top-20 left-10 w-72 h-72 rounded-full bg-sky-600/12 blur-3xl blob"
            animate={{ scale: [1, 1.2, 1], x: [0, 30, 0] }}
            transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
          />
          <motion.div
            className="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-indigo-600/10 blur-3xl blob"
            animate={{ scale: [1.1, 1, 1.1], x: [0, -20, 0] }}
            transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut', delay: 2 }}
          />
          <motion.div
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-cyan-600/5 blur-[80px]"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
          />
          {/* Grid */}
          <div className="absolute inset-0 opacity-[0.025]"
            style={{
              backgroundImage: 'linear-gradient(rgba(56,189,248,1) 1px, transparent 1px), linear-gradient(90deg, rgba(56,189,248,1) 1px, transparent 1px)',
              backgroundSize: '80px 80px',
            }}
          />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 grid lg:grid-cols-2 gap-16 items-center">
          {/* Left */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 glass px-3 py-1.5 rounded-full text-xs text-sky-400 mb-6 border border-sky-500/20"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-pulse" />
              Powered by HistGradientBoosting · 68.5% Accuracy
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-5xl sm:text-6xl font-extrabold leading-[1.1] tracking-tight mb-6"
            >
              <span className="text-white">AI-Powered</span>
              <br />
              <span className="gradient-text">Water Availability</span>
              <br />
              <span className="text-white">Prediction</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-slate-400 text-lg leading-relaxed mb-10 max-w-lg"
            >
              Predict future water resource conditions using environmental and climatic intelligence.
              Built on 550K+ CGWB records across India.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-wrap gap-4"
            >
              <Link to="/predict" className="btn-primary">
                <Zap size={16} /> Start Prediction
              </Link>
              <Link to="/analytics" className="btn-ghost">
                View Analytics <ArrowRight size={15} />
              </Link>
            </motion.div>

            {/* Mini stats row */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex gap-6 mt-12 pt-8 border-t border-white/5"
            >
              {[['550K+','Records'],['68.5%','Accuracy'],['28+','States']].map(([v,l]) => (
                <div key={l}>
                  <div className="text-xl font-bold text-white">{v}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{l}</div>
                </div>
              ))}
            </motion.div>
          </div>

          {/* Right — floating dashboard cards */}
          <div className="relative hidden lg:block">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="relative"
            >
              {/* Central orb */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full bg-gradient-to-br from-sky-500/20 to-indigo-500/20 blur-2xl" />
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full border border-sky-500/20 flex items-center justify-center">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-sky-500/30 to-indigo-500/30 flex items-center justify-center">
                  <Droplets size={32} className="text-sky-400" />
                </div>
              </div>
              {/* Orbit ring */}
              <div className="w-80 h-80 mx-auto rounded-full border border-sky-500/10 spin-slow" />

              {/* Floating metric cards */}
              {[
                { label: 'Rainfall',    value: '142mm',  icon: CloudRain,  pos: 'top-0 left-0',     color: 'sky',    delay: 0 },
                { label: 'Humidity',    value: '68%',    icon: Droplets,   pos: 'top-0 right-0',    color: 'cyan',   delay: 0.5 },
                { label: 'Groundwater', value: '5.2m',   icon: TrendingUp, pos: 'bottom-0 left-0',  color: 'indigo', delay: 1 },
                { label: 'Accuracy',    value: '68.5%',  icon: Brain,      pos: 'bottom-0 right-0', color: 'violet', delay: 1.5 },
              ].map(c => {
                const col = colorMap[c.color]
                return (
                  <motion.div
                    key={c.label}
                    className={`absolute ${c.pos} card card-glow-blue flex items-center gap-3 px-4 py-3 min-w-[140px]`}
                    style={{ boxShadow: `0 0 20px ${col.glow}` }}
                    animate={{ y: [0, -8, 0] }}
                    transition={{ duration: 4 + parseFloat(c.delay), repeat: Infinity, ease: 'easeInOut', delay: c.delay }}
                  >
                    <div className={`w-8 h-8 rounded-lg ${col.bg} flex items-center justify-center`}>
                      <c.icon size={16} className={col.text} />
                    </div>
                    <div>
                      <div className="text-xs text-slate-500">{c.label}</div>
                      <div className={`text-sm font-bold ${col.text}`}>{c.value}</div>
                    </div>
                  </motion.div>
                )
              })}
            </motion.div>
          </div>
        </div>
      </section>

      {/* ── LIVE INSIGHT CARDS ────────────────────────────────────────────── */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div {...fadeUp()} className="text-center mb-12">
            <p className="text-xs text-sky-400 uppercase tracking-widest mb-3 font-medium">Live Insights</p>
            <h2 className="text-3xl font-bold text-white">Model Intelligence</h2>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {metrics.map((m, i) => {
              const col = colorMap[m.color]
              return (
                <motion.div
                  key={m.label}
                  {...fadeUp(i * 0.08)}
                  className={`card border ${col.border} group hover:scale-[1.02] transition-transform duration-300`}
                  style={{ boxShadow: `0 0 25px ${col.glow}` }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-10 h-10 rounded-xl ${col.bg} flex items-center justify-center`}>
                      <m.icon size={18} className={col.text} />
                    </div>
                    <span className={`text-xs ${col.text} ${col.bg} px-2 py-0.5 rounded-full`}>Live</span>
                  </div>
                  <div className={`text-3xl font-black ${col.text} mb-1`}>
                    <Counter target={m.value} suffix={m.suffix} />
                  </div>
                  <div className="text-sm font-medium text-slate-300 mb-1">{m.label}</div>
                  <div className="text-xs text-slate-600">{m.desc}</div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ──────────────────────────────────────────────────── */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.div {...fadeUp()} className="text-center mb-14">
            <p className="text-xs text-sky-400 uppercase tracking-widest mb-3 font-medium">Workflow</p>
            <h2 className="text-3xl font-bold text-white">How It Works</h2>
            <p className="text-slate-500 mt-3 max-w-md mx-auto text-sm">Three steps from raw environmental data to actionable water availability intelligence.</p>
          </motion.div>

          <div className="relative">
            {/* Connector line */}
            <div className="hidden md:block absolute top-10 left-[16.67%] right-[16.67%] h-px bg-gradient-to-r from-transparent via-sky-500/30 to-transparent" />

            <div className="grid md:grid-cols-3 gap-6">
              {steps.map((s, i) => (
                <motion.div key={s.n} {...fadeUp(i * 0.12)} className="relative">
                  <div className="card group hover:border-sky-500/20 transition-all duration-300 text-center">
                    <div className="relative inline-flex mb-5">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500/20 to-indigo-500/20 border border-sky-500/20 flex items-center justify-center group-hover:border-sky-500/40 transition-colors">
                        <s.icon size={22} className="text-sky-400" />
                      </div>
                      <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-sky-500 text-white text-[10px] font-bold flex items-center justify-center">
                        {i + 1}
                      </span>
                    </div>
                    <h3 className="text-white font-semibold mb-2">{s.title}</h3>
                    <p className="text-slate-500 text-sm leading-relaxed">{s.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── AI MODEL PERFORMANCE ──────────────────────────────────────────── */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div {...fadeUp()} className="text-center mb-12">
            <p className="text-xs text-sky-400 uppercase tracking-widest mb-3 font-medium">Performance</p>
            <h2 className="text-3xl font-bold text-white">AI Model Metrics</h2>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Metric bars */}
            <motion.div {...fadeUp(0.1)} className="card card-glow-blue space-y-5">
              <h3 className="text-white font-semibold mb-2">Classification Performance</h3>
              {perfMetrics.map((m, i) => (
                <div key={m.label}>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-slate-400">{m.label}</span>
                    <span className="font-semibold text-white">{m.value}%</span>
                  </div>
                  <div className="h-2 bg-slate-800/80 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${m.value}%` }}
                      viewport={{ once: true }}
                      transition={{ duration: 1, delay: i * 0.15, ease: 'easeOut' }}
                      className="h-full rounded-full"
                      style={{ background: `linear-gradient(90deg, ${m.color}88, ${m.color})` }}
                    />
                  </div>
                </div>
              ))}
            </motion.div>

            {/* Trend chart */}
            <motion.div {...fadeUp(0.15)} className="card card-glow-blue">
              <h3 className="text-white font-semibold mb-5">12-Month Water Availability Trend</h3>
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="gHigh" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#22c55e" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="gLow" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#ef4444" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="m" tick={{ fill: '#475569', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#475569', fontSize: 11 }} axisLine={false} tickLine={false} unit="%" />
                  <Tooltip
                    contentStyle={{ background: '#0f172a', border: '1px solid #1e3a5f', borderRadius: 10 }}
                    labelStyle={{ color: '#94a3b8' }}
                    formatter={(v, n) => [`${v}%`, n]}
                  />
                  <Area type="monotone" dataKey="high" stroke="#22c55e" strokeWidth={2} fill="url(#gHigh)" name="High" />
                  <Area type="monotone" dataKey="low"  stroke="#ef4444" strokeWidth={2} fill="url(#gLow)"  name="Low" />
                </AreaChart>
              </ResponsiveContainer>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ── CTA ───────────────────────────────────────────────────────────── */}
      <section className="py-20 px-4">
        <motion.div
          {...fadeUp()}
          className="max-w-3xl mx-auto text-center card border border-sky-500/15 bg-gradient-to-br from-sky-500/5 to-indigo-500/5 py-16"
          style={{ boxShadow: '0 0 60px rgba(56,189,248,0.06)' }}
        >
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500/20 to-indigo-500/20 border border-sky-500/20 flex items-center justify-center mx-auto mb-6">
            <Droplets size={26} className="text-sky-400" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Predict?</h2>
          <p className="text-slate-500 mb-8 max-w-md mx-auto text-sm leading-relaxed">
            Enter environmental parameters and get an instant AI-powered water availability forecast with confidence scoring.
          </p>
          <Link to="/predict" className="btn-primary">
            <Activity size={16} /> Launch Prediction Engine <ArrowRight size={15} />
          </Link>
        </motion.div>
      </section>
    </div>
  )
}
