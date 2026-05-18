import { motion } from 'framer-motion'
import {
  AlertTriangle, Brain, CheckCircle, Code2,
  Database, Droplets, Layers, Server, TrendingUp,
} from 'lucide-react'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.5, delay },
})

const stack = [
  {
    icon: Code2, title: 'Frontend',
    items: ['React 18 + Vite', 'Tailwind CSS v4', 'Framer Motion', 'Recharts', 'Axios'],
    color: 'sky',
  },
  {
    icon: Server, title: 'Backend',
    items: ['Flask 3', 'Flask-CORS', 'REST API', 'Gunicorn', 'Python 3.14'],
    color: 'indigo',
  },
  {
    icon: Brain, title: 'ML Stack',
    items: ['Scikit-learn', 'Pandas / NumPy', 'Random Forest', 'HistGradientBoosting', 'Joblib'],
    color: 'cyan',
  },
]

const workflow = [
  { step: '01', title: 'Data Collection',     desc: '550K+ CGWB groundwater monitoring records across 28+ Indian states.' },
  { step: '02', title: 'Preprocessing',        desc: 'Chronological sorting, date feature extraction, percentile-based labelling.' },
  { step: '03', title: 'Feature Engineering',  desc: '13 features: depth, location, temporal, and categorical station identifiers.' },
  { step: '04', title: 'Model Training',        desc: 'Random Forest (sampled) and HistGradientBoosting (full set) trained and compared.' },
  { step: '05', title: 'Evaluation',            desc: 'Accuracy, precision, recall, F1 score, confusion matrix on 20% test split.' },
  { step: '06', title: 'Deployment',            desc: 'Best model serialised with Joblib, served via Flask REST API.' },
]

const future = [
  'Real-time weather API integration for live predictions',
  'Map visualisation of groundwater levels across India',
  'LSTM-based time series forecasting for long-term trends',
  'Mobile application for field workers and farmers',
  'Multi-language support for regional accessibility',
  'Integration with government water management portals',
]

const colorMap = {
  sky:    { text: 'text-sky-400',    bg: 'bg-sky-500/10',    border: 'border-sky-500/20' },
  indigo: { text: 'text-indigo-400', bg: 'bg-indigo-500/10', border: 'border-indigo-500/20' },
  cyan:   { text: 'text-cyan-400',   bg: 'bg-cyan-500/10',   border: 'border-cyan-500/20' },
}

export default function About() {
  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
          <div className="inline-flex items-center gap-2 glass px-3 py-1.5 rounded-full text-xs text-sky-400 mb-4 border border-sky-500/20">
            <Droplets size={12} /> About the Project
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">AquaVision AI</h1>
          <p className="text-slate-500 text-sm max-w-xl">
            A machine learning–powered system for predicting groundwater availability across India,
            built to support farmers, communities, and water resource authorities.
          </p>
        </motion.div>

        {/* Problem + Solution */}
        <div className="grid md:grid-cols-2 gap-5 mb-8">
          <motion.div {...fadeUp(0.05)} className="card border border-red-500/15" style={{ boxShadow: '0 0 30px rgba(239,68,68,0.05)' }}>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-red-500/10 flex items-center justify-center">
                <AlertTriangle size={16} className="text-red-400" />
              </div>
              <h2 className="text-white font-semibold">Problem Statement</h2>
            </div>
            <p className="text-slate-500 text-sm leading-relaxed mb-4">
              Water availability is becoming unpredictable due to climate variation, rainfall inconsistencies,
              groundwater depletion, and environmental changes. Communities and farmers struggle to plan
              irrigation, storage, and resource distribution.
            </p>
            <div className="glass rounded-xl p-3 border-l-2 border-sky-500">
              <p className="text-sky-300 text-xs italic leading-relaxed">
                "Predict water availability using machine learning based on environmental and climatic parameters."
              </p>
            </div>
          </motion.div>

          <motion.div {...fadeUp(0.08)} className="card border border-sky-500/15" style={{ boxShadow: '0 0 30px rgba(56,189,248,0.05)' }}>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-sky-500/10 flex items-center justify-center">
                <CheckCircle size={16} className="text-sky-400" />
              </div>
              <h2 className="text-white font-semibold">Proposed Solution</h2>
            </div>
            <div className="space-y-3">
              {[
                { icon: Database, t: 'Dataset',     d: '550K+ CGWB records across 28+ Indian states, cleaned and preprocessed.' },
                { icon: Brain,    t: 'ML Model',    d: 'HistGradientBoosting on 13 features — depth, location, temporal data.' },
                { icon: TrendingUp,t:'Prediction',  d: 'Classifies next reading as High (≤3.65m), Medium, or Low (>7.76m).' },
              ].map(item => (
                <div key={item.t} className="flex gap-3">
                  <div className="w-7 h-7 rounded-lg bg-sky-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <item.icon size={13} className="text-sky-400" />
                  </div>
                  <div>
                    <span className="text-sky-400 text-xs font-semibold">{item.t} — </span>
                    <span className="text-slate-500 text-xs">{item.d}</span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Tech Stack */}
        <motion.div {...fadeUp(0.1)} className="mb-8">
          <h2 className="text-white font-semibold mb-5 flex items-center gap-2">
            <Layers size={16} className="text-sky-400" /> Technologies Used
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {stack.map(s => {
              const col = colorMap[s.color]
              return (
                <div key={s.title} className={`card border ${col.border}`}>
                  <div className="flex items-center gap-2 mb-4">
                    <div className={`w-8 h-8 rounded-lg ${col.bg} flex items-center justify-center`}>
                      <s.icon size={15} className={col.text} />
                    </div>
                    <h3 className="text-white font-medium text-sm">{s.title}</h3>
                  </div>
                  <ul className="space-y-1.5">
                    {s.items.map(item => (
                      <li key={item} className="flex items-center gap-2 text-xs text-slate-500">
                        <span className={`w-1 h-1 rounded-full ${col.bg.replace('/10','')} flex-shrink-0`} style={{ background: col.text.includes('sky') ? '#38bdf8' : col.text.includes('indigo') ? '#818cf8' : '#06b6d4' }} />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )
            })}
          </div>
        </motion.div>

        {/* ML Workflow */}
        <motion.div {...fadeUp(0.12)} className="mb-8">
          <h2 className="text-white font-semibold mb-5 flex items-center gap-2">
            <Brain size={16} className="text-sky-400" /> ML Workflow
          </h2>
          <div className="relative">
            <div className="absolute left-5 top-5 bottom-5 w-px bg-gradient-to-b from-sky-500/40 via-indigo-500/20 to-transparent" />
            <div className="space-y-4">
              {workflow.map((w, i) => (
                <motion.div
                  key={w.step}
                  initial={{ opacity: 0, x: -16 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.07 }}
                  className="flex gap-4 pl-2"
                >
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sky-500/20 to-indigo-500/20 border border-sky-500/20 flex items-center justify-center text-sky-400 text-xs font-bold flex-shrink-0 z-10">
                    {w.step}
                  </div>
                  <div className="card flex-1 py-3 px-4">
                    <h3 className="text-white text-sm font-medium mb-0.5">{w.title}</h3>
                    <p className="text-slate-500 text-xs leading-relaxed">{w.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Future Scope */}
        <motion.div {...fadeUp(0.14)} className="card card-glow-blue">
          <h2 className="text-white font-semibold mb-5 flex items-center gap-2">
            <TrendingUp size={16} className="text-sky-400" /> Future Scope
          </h2>
          <div className="grid sm:grid-cols-2 gap-3">
            {future.map((f, i) => (
              <div key={i} className="flex items-start gap-2.5 glass rounded-xl p-3">
                <div className="w-5 h-5 rounded-full bg-sky-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <CheckCircle size={11} className="text-sky-400" />
                </div>
                <p className="text-slate-400 text-xs leading-relaxed">{f}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
