import { Download, Pause, Play, X, Trash2, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react'

function BatchList({ items, onCancel, onPause, onResume, onDownload, onClearCompleted }) {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-5 h-5 text-gray-500" />
      case 'downloading':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'cancelled':
        return <X className="w-5 h-5 text-gray-500" />
      case 'paused':
        return <Pause className="w-5 h-5 text-yellow-500" />
      default:
        return <Clock className="w-5 h-5 text-gray-500" />
    }
  }

  const getStatusText = (status, downloaded) => {
    if (status === 'completed' && downloaded) {
      return 'Baixado ✓'
    }
    
    const statusMap = {
      'pending': 'Aguardando',
      'downloading': 'Baixando',
      'completed': 'Concluído',
      'failed': 'Falhou',
      'cancelled': 'Cancelado',
      'paused': 'Pausado'
    }
    return statusMap[status] || status
  }

  const getStatusColor = (status) => {
    const colorMap = {
      'pending': 'text-gray-600 dark:text-gray-400',
      'downloading': 'text-blue-600 dark:text-blue-400',
      'completed': 'text-green-600 dark:text-green-400',
      'failed': 'text-red-600 dark:text-red-400',
      'cancelled': 'text-gray-500 dark:text-gray-500',
      'paused': 'text-yellow-600 dark:text-yellow-400'
    }
    return colorMap[status] || 'text-gray-600'
  }

  const formatUrl = (url) => {
    try {
      const urlObj = new URL(url)
      return urlObj.hostname + urlObj.pathname
    } catch {
      return url
    }
  }

  if (items.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-12 text-center">
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          Nenhum item na fila. Adicione URLs acima para começar.
        </p>
      </div>
    )
  }

  const completedCount = items.filter(i => i.status === 'completed').length

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold">
          Fila de Downloads ({items.length} itens)
        </h3>
        
        {completedCount > 0 && (
          <button
            onClick={onClearCompleted}
            className="flex items-center gap-2 px-3 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm"
          >
            <Trash2 className="w-4 h-4" />
            Limpar Concluídos
          </button>
        )}
      </div>

      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item.id}
            className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
          >
            <div className="flex items-start gap-3">
              {/* Status Icon */}
              <div className="mt-1">
                {getStatusIcon(item.status)}
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`font-medium text-sm ${getStatusColor(item.status)}`}>
                    {getStatusText(item.status, item.downloaded)}
                  </span>
                  {item.audio_only && (
                    <span className="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-2 py-0.5 rounded">
                      🎵 MP3
                    </span>
                  )}
                  {!item.audio_only && item.quality && (
                    <span className="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2 py-0.5 rounded">
                      📹 {item.quality}
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-700 dark:text-gray-300 truncate mb-1">
                  {formatUrl(item.url)}
                </p>

                {/* Progress Bar */}
                {item.status === 'downloading' && (
                  <div className="mt-2">
                    <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary-600 transition-all duration-300"
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {item.message || `${item.progress}%`}
                    </p>
                  </div>
                )}

                {/* Error Message */}
                {item.status === 'failed' && item.error && (
                  <p className="text-xs text-red-600 dark:text-red-400 mt-1">
                    ❌ {item.error}
                  </p>
                )}
                
                {/* Auto-download Message */}
                {item.status === 'completed' && !item.downloaded && (
                  <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                    💾 Iniciando download automático...
                  </p>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-1">
                {item.status === 'pending' && (
                  <button
                    onClick={() => onPause(item.id)}
                    className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    title="Pausar"
                  >
                    <Pause className="w-4 h-4" />
                  </button>
                )}

                {item.status === 'paused' && (
                  <button
                    onClick={() => onResume(item.id)}
                    className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    title="Retomar"
                  >
                    <Play className="w-4 h-4" />
                  </button>
                )}

                {item.status === 'completed' && (
                  <a
                    href={onDownload(item.id)}
                    download
                    className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    title="Baixar"
                  >
                    <Download className="w-4 h-4 text-green-600" />
                  </a>
                )}

                {['pending', 'paused', 'downloading'].includes(item.status) && (
                  <button
                    onClick={() => onCancel(item.id)}
                    className="p-2 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 text-red-600 transition-colors"
                    title="Cancelar"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default BatchList
