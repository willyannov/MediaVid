import { useState } from 'react'
import { Download, Loader2, CheckCircle } from 'lucide-react'
import { videoAPI } from '../../services/api'
import { downloadBlob } from '../../utils/formatters'

function DownloadButton({ downloadRequest, disabled }) {
  const [downloading, setDownloading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)

  const handleDownload = async () => {
    setDownloading(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await videoAPI.download(downloadRequest)
      
      // Extrai filename do header Content-Disposition
      let filename = 'video.mp4' // Default com extensão
      const contentDisposition = response.headers['content-disposition']
      
      if (contentDisposition) {
        // Tenta extrair o filename do header
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '').trim()
        }
      }
      
      // Se não tem extensão, tenta detectar do content-type
      if (!filename.includes('.')) {
        const contentType = response.headers['content-type']
        if (contentType) {
          if (contentType.includes('mp4')) filename += '.mp4'
          else if (contentType.includes('webm')) filename += '.webm'
          else if (contentType.includes('mkv')) filename += '.mkv'
          else filename += '.mp4' // fallback
        }
      }

      // Baixa o arquivo
      downloadBlob(response.data, filename)
      
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div>
      <button
        onClick={handleDownload}
        disabled={disabled || downloading}
        className={`w-full py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-3 transition-all ${
          success
            ? 'bg-green-600 hover:bg-green-700 text-white'
            : 'bg-primary-600 hover:bg-primary-700 text-white disabled:bg-gray-400 disabled:cursor-not-allowed'
        }`}
      >
        {downloading ? (
          <>
            <Loader2 className="w-6 h-6 animate-spin" />
            Baixando...
          </>
        ) : success ? (
          <>
            <CheckCircle className="w-6 h-6" />
            Download Concluído!
          </>
        ) : (
          <>
            <Download className="w-6 h-6" />
            Baixar Vídeo
          </>
        )}
      </button>

      {error && (
        <div className="mt-3 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-800 dark:text-red-200">
            ❌ Erro: {error}
          </p>
        </div>
      )}
    </div>
  )
}

export default DownloadButton
