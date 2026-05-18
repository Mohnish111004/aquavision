import { Link } from 'react-router-dom'
import { Droplets, GitBranch } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-white/5 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          {/* Brand */}
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center">
              <Droplets size={14} className="text-white" />
            </div>
            <span className="font-semibold gradient-text text-sm">AquaVision AI</span>
          </div>

          {/* Stack */}
          <div className="flex items-center gap-2 text-xs text-slate-600">
            <span>React</span><span>·</span>
            <span>Flask</span><span>·</span>
            <span>Scikit-learn</span><span>·</span>
            <span>Tailwind CSS</span>
          </div>

          {/* Links */}
          <div className="flex items-center gap-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-sky-400 transition-colors"
            >
              <GitBranch size={13} /> GitHub
            </a>
            <span className="text-slate-700 text-xs">© 2025 AquaVision AI</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
