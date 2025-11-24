import { useState, useEffect } from 'react'
import { videoAPI } from '../../services/api'

function FormatSelector({ videoInfo, onSelectionChange }) {
  const [selectedQuality, setSelectedQuality] = useState('1080p')
  const [audioOnly, setAudioOnly] = useState(false)
  const [availableFormats, setAvailableFormats] = useState(null)

  // Detecta se é vídeo curto ou plataforma sem seleção de qualidade
  const isShortVideo = 
    videoInfo.platform === 'Instagram' || 
    videoInfo.platform === 'TikTok' || 
    videoInfo.platform === 'Twitter' ||
    videoInfo.platform === 'Reddit' ||
    videoInfo.platform === 'Facebook' ||
    (videoInfo.url && videoInfo.url.includes('/shorts/'))

  useEffect(() => {
    // Busca formatos disponíveis
    videoAPI.getFormats().then(setAvailableFormats)
  }, [])

  useEffect(() => {
    // Notifica mudanças
    onSelectionChange({
      quality: (audioOnly || isShortVideo) ? null : selectedQuality,
      output_format: audioOnly ? 'mp3' : 'mp4',
      audio_only: audioOnly,
      url: videoInfo.url
    })
  }, [selectedQuality, audioOnly, videoInfo.url, isShortVideo, onSelectionChange])

  if (!availableFormats) return null

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold mb-4">Opções de Download</h3>

      {/* Audio Only Toggle */}
      <div className="mb-6">
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={audioOnly}
            onChange={(e) => setAudioOnly(e.target.checked)}
            className="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
          />
          <span className="text-sm font-medium">
            🎵 Baixar apenas áudio (MP3)
          </span>
        </label>
      </div>

      {/* Quality Selector - Buttons */}
      {!audioOnly && !isShortVideo && (
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-3">
            Qualidade do Vídeo (MP4)
          </label>
          <div className="grid grid-cols-2 gap-3">
            {availableFormats.quality_options.map((quality) => (
              <button
                key={quality.value}
                onClick={() => setSelectedQuality(quality.value)}
                className={`px-4 py-3 rounded-lg font-medium transition-all ${
                  selectedQuality === quality.value
                    ? 'bg-primary-600 text-white shadow-lg scale-105'
                    : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                📹 {quality.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Mensagem para vídeos curtos */}
      {!audioOnly && isShortVideo && (
        <div className="mb-6 bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
          <p className="text-sm text-green-800 dark:text-green-200">
            ✨ Este vídeo será baixado automaticamente na <strong>melhor qualidade disponível</strong>
          </p>
          <p className="text-xs text-green-700 dark:text-green-300 mt-1">
            {videoInfo.platform === 'Instagram' && '📷 Instagram Reels'}
            {videoInfo.platform === 'TikTok' && '🎵 TikTok'}
            {videoInfo.platform === 'Twitter' && '🐦 Twitter/X'}
            {videoInfo.platform === 'Reddit' && '🤖 Reddit'}
            {videoInfo.platform === 'Facebook' && '📘 Facebook'}
            {videoInfo.url?.includes('/shorts/') && '▶️ YouTube Shorts'}
          </p>
        </div>
      )}

      {/* Info sobre formato */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          {audioOnly ? (
            <>💿 O áudio será baixado em formato <strong>MP3</strong></>
          ) : isShortVideo ? (
            <>🎬 O vídeo será baixado na <strong>melhor qualidade</strong> em formato <strong>MP4</strong></>
          ) : (
            <>🎬 O vídeo será baixado em <strong>{selectedQuality}</strong> formato <strong>MP4</strong></>
          )}
        </p>
      </div>
    </div>
  )
}

export default FormatSelector
