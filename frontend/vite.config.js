import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const BACKEND = process.env.VITE_API_URL || 'http://localhost:5001'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  server: {
    port: 5173,
    proxy: {
      '/predict': BACKEND,
      '/explain': BACKEND,
      '/forecast': BACKEND,
      '/recommend': BACKEND,
      '/health': BACKEND,
      '/metrics': BACKEND,
      '/auth': BACKEND,
      '/history': BACKEND,
      '/weather': BACKEND,
      '/crops': BACKEND,
      '/irrigation': BACKEND,
      '/reports': BACKEND,
      '/models': BACKEND,
      '/admin': BACKEND,
    },
  },
})
