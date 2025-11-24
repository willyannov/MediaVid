import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // 5 minutos para downloads grandes
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Erro desconhecido'
    return Promise.reject(new Error(message))
  }
)

// API Functions
export const videoAPI = {
  // Obter informações do vídeo
  getInfo: async (url) => {
    const response = await api.post('/video/info', { url })
    return response.data
  },

  // Baixar vídeo
  download: async (downloadRequest) => {
    const response = await api.post('/video/download', downloadRequest, {
      responseType: 'blob',
    })
    return response
  },

  // Obter formatos disponíveis
  getFormats: async () => {
    const response = await api.get('/video/formats')
    return response.data
  }
}

export default api
