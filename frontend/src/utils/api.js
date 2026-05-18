import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: BASE,
  timeout: 20000,
  headers: { 'Content-Type': 'application/json' },
})

export const predict   = (data) => api.post('/predict',   data)
export const health    = ()     => api.get('/health')
export const metrics   = ()     => api.get('/metrics')
export const explain   = (data) => api.post('/explain',   data)
export const forecast  = (data) => api.post('/forecast',  data)
export const recommend = (data) => api.post('/recommend', data)

export default api
