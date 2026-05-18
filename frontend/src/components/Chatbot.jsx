import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, X, Send, Droplets, Bot } from 'lucide-react'

/* ── Knowledge base ───────────────────────────────────────────────────────── */
const KB = [
  { q: ['high', 'high availability', 'what is high'],
    a: 'High water availability means groundwater depth is ≤3.65m — close to the surface. Conditions are favourable for irrigation and normal water use.' },
  { q: ['medium', 'moderate', 'what is medium'],
    a: 'Medium availability means depth is between 3.65m and 7.76m. Water is accessible but conservation measures are recommended.' },
  { q: ['low', 'low availability', 'critical', 'scarcity'],
    a: 'Low availability means depth exceeds 7.76m — a critical threshold. Immediate water rationing and alternative sourcing is strongly advised.' },
  { q: ['confidence', 'confidence score', 'what is confidence'],
    a: 'Confidence score is the probability the model assigns to its predicted class. A score of 80%+ indicates high certainty in the prediction.' },
  { q: ['model', 'which model', 'algorithm', 'ml model'],
    a: 'AquaVision uses HistGradientBoosting (68.5% accuracy) as the primary model, trained on 550K+ CGWB groundwater records across 28+ Indian states.' },
  { q: ['features', 'inputs', 'what features', 'parameters'],
    a: 'The model uses 13 features: groundwater depth, level change, latitude, longitude, year, month, day, day-of-year, state, district, basin, sub-basin, and station.' },
  { q: ['save', 'conserve', 'conservation', 'tips'],
    a: 'Key conservation tips: (1) Fix leaks immediately, (2) Use drip irrigation, (3) Harvest rainwater, (4) Reuse greywater, (5) Plant native species, (6) Monitor groundwater weekly.' },
  { q: ['cgwb', 'dataset', 'data', 'training data'],
    a: 'The dataset comes from the Central Ground Water Board (CGWB) of India — 550K+ monitoring records from stations across all major states and river basins.' },
  { q: ['forecast', '7 day', 'future', 'prediction trend'],
    a: 'The 7-day forecast simulates future groundwater levels using seasonal drift patterns and your observed level change trend. It gives a probabilistic outlook for the coming week.' },
  { q: ['xai', 'explain', 'explainable', 'why', 'reason'],
    a: 'The AI Explanation tab shows which features contributed most to the prediction. Groundwater depth and level change are typically the strongest drivers.' },
  { q: ['accuracy', 'how accurate', 'performance'],
    a: 'The best model (HistGradientBoosting) achieves 68.5% accuracy on the test set. Precision is 71.2%, Recall 66.8%, and F1 Score 68.9%.' },
  { q: ['hello', 'hi', 'hey', 'help'],
    a: 'Hello! I\'m AquaBot 🤖 — your water intelligence assistant. Ask me about predictions, the model, conservation tips, or how to interpret results.' },
]

function getResponse(input) {
  const lower = input.toLowerCase().trim()
  for (const entry of KB) {
    if (entry.q.some(k => lower.includes(k))) return entry.a
  }
  return "I'm not sure about that. Try asking about: prediction results, model accuracy, water conservation tips, the dataset, or how to interpret confidence scores."
}

export default function Chatbot() {
  const [open, setOpen]       = useState(false)
  const [messages, setMessages] = useState([
    { from: 'bot', text: "Hi! I'm AquaBot 🤖 — your water intelligence assistant. Ask me anything about AquaVision AI, predictions, or water conservation." }
  ])
  const [input, setInput]     = useState('')
  const bottomRef             = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, open])

  const send = () => {
    const text = input.trim()
    if (!text) return
    const userMsg  = { from: 'user', text }
    const botReply = { from: 'bot',  text: getResponse(text) }
    setMessages(prev => [...prev, userMsg, botReply])
    setInput('')
  }

  const handleKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }

  return (
    <>
      {/* Floating button */}
      <motion.button
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center shadow-2xl shadow-sky-500/30 hover:scale-110 transition-transform"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        aria-label="Open AI chatbot"
      >
        <AnimatePresence mode="wait">
          {open
            ? <motion.div key="x"  initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }}><X size={22} className="text-white" /></motion.div>
            : <motion.div key="msg" initial={{ rotate: 90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: -90, opacity: 0 }}><MessageCircle size={22} className="text-white" /></motion.div>
          }
        </AnimatePresence>
        {/* Pulse ring */}
        {!open && <span className="absolute inset-0 rounded-2xl border-2 border-sky-400/40 animate-ping" />}
      </motion.button>

      {/* Chat window */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', bounce: 0.25, duration: 0.4 }}
            className="fixed bottom-24 right-6 z-50 w-80 sm:w-96 flex flex-col"
            style={{ height: '480px' }}
          >
            <div className="flex flex-col h-full rounded-2xl overflow-hidden border border-sky-500/20 shadow-2xl shadow-black/50"
              style={{ background: 'rgba(2,8,23,0.95)', backdropFilter: 'blur(20px)' }}>

              {/* Header */}
              <div className="flex items-center gap-3 px-4 py-3 border-b border-white/5 bg-gradient-to-r from-sky-500/10 to-indigo-500/10">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center">
                  <Bot size={16} className="text-white" />
                </div>
                <div>
                  <div className="text-white text-sm font-semibold">AquaBot</div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-emerald-400 text-[10px]">Online</span>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
                {messages.map((m, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {m.from === 'bot' && (
                      <div className="w-6 h-6 rounded-lg bg-sky-500/20 flex items-center justify-center mr-2 flex-shrink-0 mt-0.5">
                        <Droplets size={12} className="text-sky-400" />
                      </div>
                    )}
                    <div className={`max-w-[80%] px-3 py-2 rounded-xl text-xs leading-relaxed ${
                      m.from === 'user'
                        ? 'bg-sky-500/20 text-sky-100 border border-sky-500/20'
                        : 'bg-slate-800/80 text-slate-300 border border-white/5'
                    }`}>
                      {m.text}
                    </div>
                  </motion.div>
                ))}
                <div ref={bottomRef} />
              </div>

              {/* Suggestions */}
              <div className="px-4 pb-2 flex gap-1.5 overflow-x-auto">
                {['High vs Low?', 'Conservation tips', 'Model accuracy'].map(s => (
                  <button key={s} onClick={() => { setInput(s); setTimeout(send, 50) }}
                    className="flex-shrink-0 text-[10px] text-sky-400 border border-sky-500/20 px-2 py-1 rounded-lg hover:bg-sky-500/10 transition-colors">
                    {s}
                  </button>
                ))}
              </div>

              {/* Input */}
              <div className="px-4 pb-4 flex gap-2">
                <input
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Ask about predictions..."
                  className="flex-1 bg-slate-800/60 border border-slate-700/40 rounded-xl px-3 py-2 text-xs text-slate-200 placeholder-slate-600 outline-none focus:border-sky-500/50"
                />
                <button onClick={send}
                  className="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center hover:scale-105 transition-transform flex-shrink-0">
                  <Send size={14} className="text-white" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
