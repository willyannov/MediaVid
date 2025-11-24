import { useState, useEffect, useRef } from 'react'
import { PlayCircle, Trash2, Home, Moon, Sun } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import batchAPI from '../services/batchApi'
import URLInput from '../components/Batch/URLInput'
import BatchList from '../components/Batch/BatchList'
import Toast from '../components/UI/Toast'
import { VideoIcon } from '../components/UI/SocialIcons'

function Batch() {
  const { isDark, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const [queue, setQueue] = useState([])
  const [queueStatus, setQueueStatus] = useState(null)
  const [toast, setToast] = useState(null)
  const [loading, setLoading] = useState(false)
  const downloadedItemsRef = useRef(new Set()) // Rastreia itens já baixados

  // Atualiza fila a cada 2 segundos quando há downloads ativos
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const data = await batchAPI.getQueue()
        setQueue(data.items)
        setQueueStatus(data.status)
        
        // Verifica se há novos itens completados para download automático
        data.items.forEach(item => {
          if (
            item.status === 'completed' && 
            !item.downloaded && 
            !downloadedItemsRef.current.has(item.id)
          ) {
            // Marca como em processo de download para evitar duplicatas
            downloadedItemsRef.current.add(item.id)
            
            // Dispara download automático
            const url = `http://localhost:8000/api/batch/item/${item.id}/download`
            const link = document.createElement('a')
            link.href = url
            link.download = ''
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            
            setToast({ 
              message: `Download iniciado automaticamente`, 
              type: 'success' 
            })
          }
        })
      } catch (error) {
        console.error('Erro ao atualizar fila:', error)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const handleAddToBatch = async (items) => {
    try {
      const result = await batchAPI.addToBatch(items)
      setToast({ message: result.message, type: 'success' })
      
      // Atualiza fila
      const data = await batchAPI.getQueue()
      setQueue(data.items)
      setQueueStatus(data.status)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  const handleStartBatch = async () => {
    setLoading(true)
    try {
      const result = await batchAPI.startBatch()
      setToast({ message: result.message, type: 'success' })
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (itemId) => {
    try {
      await batchAPI.cancelItem(itemId)
      setToast({ message: 'Item cancelado', type: 'info' })
      
      // Atualiza fila
      const data = await batchAPI.getQueue()
      setQueue(data.items)
      setQueueStatus(data.status)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  const handlePause = async (itemId) => {
    try {
      await batchAPI.pauseItem(itemId)
      
      // Atualiza fila
      const data = await batchAPI.getQueue()
      setQueue(data.items)
      setQueueStatus(data.status)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  const handleResume = async (itemId) => {
    try {
      await batchAPI.resumeItem(itemId)
      
      // Atualiza fila
      const data = await batchAPI.getQueue()
      setQueue(data.items)
      setQueueStatus(data.status)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  const handleClearCompleted = async () => {
    try {
      await batchAPI.clearCompleted()
      setToast({ message: 'Itens completados removidos', type: 'success' })
      
      // Atualiza fila
      const data = await batchAPI.getQueue()
      setQueue(data.items)
      setQueueStatus(data.status)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  const handleClearAll = async () => {
    if (!window.confirm('Deseja limpar toda a fila? Downloads em andamento serão cancelados.')) {
      return
    }

    try {
      await batchAPI.clearAll()
      setToast({ message: 'Fila limpa', type: 'success' })
      setQueue([])
      setQueueStatus(null)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Toast */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <VideoIcon className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold">MediaVid</h1>
            </div>
            
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <Home className="w-5 h-5" />
              Download Simples
            </button>
          </div>
          
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            aria-label="Toggle theme"
          >
            {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">
              📦 Download em Lote
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Adicione múltiplas URLs e baixe todos os vídeos de uma vez
            </p>
          </div>

          {/* Status da Fila */}
          {queueStatus && (
            <div className="mb-6 grid grid-cols-2 md:grid-cols-6 gap-3">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-3 shadow">
                <p className="text-xs text-gray-500 dark:text-gray-400">Total</p>
                <p className="text-2xl font-bold">{queueStatus.total}</p>
              </div>
              <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 shadow">
                <p className="text-xs text-gray-500 dark:text-gray-400">Aguardando</p>
                <p className="text-2xl font-bold text-gray-600 dark:text-gray-300">{queueStatus.pending}</p>
              </div>
              <div className="bg-blue-100 dark:bg-blue-900/30 rounded-lg p-3 shadow">
                <p className="text-xs text-blue-600 dark:text-blue-400">Baixando</p>
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{queueStatus.downloading}</p>
              </div>
              <div className="bg-green-100 dark:bg-green-900/30 rounded-lg p-3 shadow">
                <p className="text-xs text-green-600 dark:text-green-400">Concluído</p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">{queueStatus.completed}</p>
              </div>
              <div className="bg-red-100 dark:bg-red-900/30 rounded-lg p-3 shadow">
                <p className="text-xs text-red-600 dark:text-red-400">Falhou</p>
                <p className="text-2xl font-bold text-red-600 dark:text-red-400">{queueStatus.failed}</p>
              </div>
              <div className="bg-yellow-100 dark:bg-yellow-900/30 rounded-lg p-3 shadow">
                <p className="text-xs text-yellow-600 dark:text-yellow-400">Pausado</p>
                <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">{queueStatus.paused}</p>
              </div>
            </div>
          )}

          {/* Controles Globais */}
          {queue.length > 0 && (
            <div className="mb-6 flex gap-3">
              <button
                onClick={handleStartBatch}
                disabled={loading || queueStatus?.pending === 0}
                className="flex items-center gap-2 px-6 py-3 rounded-lg bg-primary-600 text-white font-bold hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                <PlayCircle className="w-5 h-5" />
                Iniciar Todos ({queueStatus?.pending || 0})
              </button>

              <button
                onClick={handleClearAll}
                className="flex items-center gap-2 px-6 py-3 rounded-lg bg-red-600 text-white font-bold hover:bg-red-700 transition-colors"
              >
                <Trash2 className="w-5 h-5" />
                Limpar Tudo
              </button>
            </div>
          )}

          {/* URL Input */}
          <div className="mb-6">
            <URLInput onAdd={handleAddToBatch} />
          </div>

          {/* Batch List */}
          <BatchList
            items={queue}
            onCancel={handleCancel}
            onPause={handlePause}
            onResume={handleResume}
            onDownload={batchAPI.downloadItem}
            onClearCompleted={handleClearCompleted}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-gray-600 dark:text-gray-400">
            <p>MediaVid © 2025</p>
            <div className="flex gap-4">
              <a href="/terms" className="hover:text-primary-600 transition-colors">Termos de Uso</a>
              <span>•</span>
              <a href="/privacy" className="hover:text-primary-600 transition-colors">Política de Privacidade</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Batch
