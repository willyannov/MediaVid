import { useState } from 'react'
import { Plus, X } from 'lucide-react'

function URLInput({ onAdd }) {
  const [urls, setUrls] = useState([''])
  const [quality, setQuality] = useState('720p')
  const [audioOnly, setAudioOnly] = useState(false)

  const addURLField = () => {
    setUrls([...urls, ''])
  }

  const removeURLField = (index) => {
    if (urls.length > 1) {
      const newUrls = urls.filter((_, i) => i !== index)
      setUrls(newUrls)
    }
  }

  const updateURL = (index, value) => {
    const newUrls = [...urls]
    newUrls[index] = value
    setUrls(newUrls)
  }

  const handleAddToBatch = () => {
    // Filtra URLs vazias
    const validUrls = urls.filter(url => url.trim() !== '')
    
    if (validUrls.length === 0) {
      return
    }

    // Cria array de items
    const items = validUrls.map(url => ({
      url: url.trim(),
      quality: audioOnly ? null : quality,
      output_format: audioOnly ? 'mp3' : 'mp4',
      audio_only: audioOnly
    }))

    onAdd(items)
    
    // Limpa campos
    setUrls([''])
  }

  const handlePaste = (e) => {
    const pastedText = e.clipboardData.getData('text')
    const lines = pastedText.split('\n').filter(line => line.trim() !== '')
    
    if (lines.length > 1) {
      e.preventDefault()
      setUrls(lines)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold mb-4">Adicionar URLs para Download em Lote</h3>

      {/* Opções Gerais */}
      <div className="mb-4 space-y-3">
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={audioOnly}
              onChange={(e) => setAudioOnly(e.target.checked)}
              className="w-4 h-4 text-primary-600 rounded"
            />
            <span className="text-sm">🎵 Apenas Áudio (MP3)</span>
          </label>

          {!audioOnly && (
            <select
              value={quality}
              onChange={(e) => setQuality(e.target.value)}
              className="px-3 py-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm"
            >
              <option value="1080p">Full HD 1080p</option>
              <option value="720p">HD 720p</option>
              <option value="480p">SD 480p</option>
              <option value="360p">Low 360p</option>
            </select>
          )}
        </div>
        
        {!audioOnly && (
          <p className="text-xs text-gray-500 dark:text-gray-400">
            💡 Reels, Shorts e TikTok serão baixados automaticamente na melhor qualidade disponível
          </p>
        )}
      </div>

      {/* Lista de URLs */}
      <div className="space-y-2 mb-4">
        {urls.map((url, index) => (
          <div key={index} className="flex gap-2">
            <input
              type="text"
              placeholder={`Cole a URL ${index + 1}...`}
              value={url}
              onChange={(e) => updateURL(index, e.target.value)}
              onPaste={index === 0 ? handlePaste : undefined}
              className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            {urls.length > 1 && (
              <button
                onClick={() => removeURLField(index)}
                className="p-2 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Botões */}
      <div className="flex gap-2">
        <button
          onClick={addURLField}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Adicionar Campo
        </button>

        <button
          onClick={handleAddToBatch}
          disabled={urls.every(url => url.trim() === '')}
          className="flex-1 px-6 py-2 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Adicionar à Fila ({urls.filter(u => u.trim()).length})
        </button>
      </div>

      <p className="text-xs text-gray-500 dark:text-gray-400 mt-3">
        💡 Dica: Cole múltiplas URLs separadas por linha no primeiro campo
      </p>
    </div>
  )
}

export default URLInput
