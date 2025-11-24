import { Play, Clock, Eye, User } from 'lucide-react'
import { formatDuration, formatViews } from '../../utils/formatters'

function VideoCard({ videoInfo }) {
  if (!videoInfo) return null

  // Detecta se é vídeo vertical (Reels, TikTok, Shorts)
  const isVerticalVideo = 
    videoInfo.platform === 'Instagram' || 
    videoInfo.platform === 'TikTok' || 
    (videoInfo.url && videoInfo.url.includes('/shorts/'))

  // Usar proxy para thumbnails (evita bloqueio CORS)
  const getThumbnailUrl = (originalUrl) => {
    if (!originalUrl) return null
    // Se for Instagram/TikTok, usa o proxy do backend
    if (videoInfo.platform === 'Instagram' || videoInfo.platform === 'TikTok') {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      return `${apiUrl}/api/video/proxy-thumbnail?url=${encodeURIComponent(originalUrl)}`
    }
    return originalUrl
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
      {/* Thumbnail */}
      {videoInfo.thumbnail && (
        <div className={`relative w-full bg-gray-200 dark:bg-gray-700 ${
          isVerticalVideo ? 'aspect-[9/16] max-h-[600px]' : 'aspect-video'
        }`}>
          <img
            src={getThumbnailUrl(videoInfo.thumbnail)}
            alt={videoInfo.title}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.style.display = 'none'
              e.target.parentElement.innerHTML = '<div class="w-full h-full flex items-center justify-center bg-gray-300 dark:bg-gray-600"><svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg></div>'
            }}
          />
          {videoInfo.duration && (
            <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formatDuration(videoInfo.duration)}
            </div>
          )}
        </div>
      )}

      {/* Info */}
      <div className="p-6">
        {/* Platform Badge */}
        {videoInfo.platform && (
          <span className="inline-block px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-semibold mb-3">
            {videoInfo.platform}
          </span>
        )}

        {/* Title */}
        <h3 className="text-xl font-bold mb-2 line-clamp-2">
          {videoInfo.title}
        </h3>

        {/* Description */}
        {videoInfo.description && (
          <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">
            {videoInfo.description}
          </p>
        )}

        {/* Metadata */}
        <div className="flex flex-wrap gap-4 text-sm text-gray-500 dark:text-gray-400">
          {videoInfo.uploader && (
            <div className="flex items-center gap-1">
              <User className="w-4 h-4" />
              <span>{videoInfo.uploader}</span>
            </div>
          )}
          {videoInfo.view_count && (
            <div className="flex items-center gap-1">
              <Eye className="w-4 h-4" />
              <span>{formatViews(videoInfo.view_count)} views</span>
            </div>
          )}
        </div>

        {/* Formats Count */}
        {videoInfo.formats && videoInfo.formats.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              <span className="font-semibold">{videoInfo.formats.length}</span> formatos disponíveis
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default VideoCard
