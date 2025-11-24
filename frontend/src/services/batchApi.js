import axios from 'axios'

const API_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 300000, // 5 minutos para downloads grandes
})

export const batchAPI = {
  // Adiciona múltiplos itens à fila
  addToBatch: async (items) => {
    const response = await api.post('/api/batch/add', items)
    return response.data
  },

  // Obtém estado da fila
  getQueue: async () => {
    const response = await api.get('/api/batch/queue')
    return response.data
  },

  // Inicia processamento da fila
  startBatch: async () => {
    const response = await api.post('/api/batch/start')
    return response.data
  },

  // Cancela um item
  cancelItem: async (itemId) => {
    const response = await api.post(`/api/batch/item/${itemId}/cancel`)
    return response.data
  },

  // Pausa um item
  pauseItem: async (itemId) => {
    const response = await api.post(`/api/batch/item/${itemId}/pause`)
    return response.data
  },

  // Resume um item
  resumeItem: async (itemId) => {
    const response = await api.post(`/api/batch/item/${itemId}/resume`)
    return response.data
  },

  // Limpa itens completados
  clearCompleted: async () => {
    const response = await api.delete('/api/batch/clear/completed')
    return response.data
  },

  // Limpa toda a fila
  clearAll: async () => {
    const response = await api.delete('/api/batch/clear/all')
    return response.data
  },

  // Download de item específico
  downloadItem: (itemId) => {
    return `${API_URL}/api/batch/item/${itemId}/download`
  }
}

export default batchAPI
