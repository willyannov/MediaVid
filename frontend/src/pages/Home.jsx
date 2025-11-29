import { useState, useRef } from 'react'
import { Moon, Sun, Search, Loader2, List } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { videoAPI } from '../services/api'
import VideoCard from '../components/VideoInfo/VideoCard'
import FormatSelector from '../components/VideoInfo/FormatSelector'
import DownloadButton from '../components/Download/DownloadButton'
import Toast from '../components/UI/Toast'
import Loading from '../components/UI/Loading'
import { VideoIcon, YouTubeIcon, InstagramIcon, TikTokIcon, TwitterIcon, FacebookIcon, RedditIcon, PinterestIcon } from '../components/UI/SocialIcons'

function Home() {
  const { isDark, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [videoInfo, setVideoInfo] = useState(null)
  const [downloadRequest, setDownloadRequest] = useState(null)
  const [toast, setToast] = useState(null)
  
  // Gera ID único para WebSocket
  const generateClientId = () => {
    return `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  const handleSearch = async () => {
    if (!url.trim()) {
      setToast({ message: 'Por favor, cole um link válido', type: 'warning' })
      return
    }

    setLoading(true)
    setVideoInfo(null)
    setToast(null)

    try {
      const info = await videoAPI.getInfo(url)
      setVideoInfo(info)
      setToast({ message: 'Vídeo encontrado! Selecione as opções de download.', type: 'success' })
      
      // Remove o toast automaticamente após 5 segundos
      setTimeout(() => {
        setToast(null)
      }, 3000)
    } catch (error) {
      setToast({ message: error.message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
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
            <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <VideoIcon className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold">MediaVid</h1>
            </a>
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
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-4xl font-bold mb-4">
              Baixe vídeos de qualquer rede social
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-lg">
              Suporte para Instagram, TikTok, Twitter, Facebook, Reddit e Pinterest
            </p>
          </div>

          {/* URL Input Card */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
            <div className="flex flex-col sm:flex-row gap-2">
              <input
                type="text"
                placeholder="Cole o link do vídeo aqui..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              />
              <button
                onClick={handleSearch}
                disabled={loading}
                className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 whitespace-nowrap"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Buscando...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Buscar
                  </>
                )}
              </button>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              Cole o link completo do post ou vídeo
            </p>
          </div>

          {/* Loading */}
          {loading && <Loading text="Buscando informações do vídeo..." />}

          {/* Plataformas Suportadas */}
          {!videoInfo && !loading && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
              <h3 className="text-xl font-bold mb-4 text-center">📱 Plataformas Suportadas</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {/* YouTube TEMPORARIAMENTE DESABILITADO */}
                {/* <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <div className="font-semibold text-red-700 dark:text-red-400 mb-2 flex items-center gap-2">
                    <YouTubeIcon className="w-5 h-5" />
                    YouTube
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Vídeos normais e Shorts</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    youtube.com/watch?v=...
                    <br />
                    youtube.com/shorts/...
                  </code>
                </div> */}
                
                <div className="p-4 rounded-lg bg-pink-50 dark:bg-pink-900/20 border border-pink-200 dark:border-pink-800">
                  <div className="font-semibold text-pink-700 dark:text-pink-400 mb-2 flex items-center gap-2">
                    <InstagramIcon className="w-5 h-5" />
                    Instagram
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Reels</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    instagram.com/reel/...
                  </code>
                </div>
                
                <div className="p-4 rounded-lg bg-cyan-50 dark:bg-cyan-900/20 border border-cyan-200 dark:border-cyan-800">
                  <div className="font-semibold text-cyan-700 dark:text-cyan-400 mb-2 flex items-center gap-2">
                    <TikTokIcon className="w-5 h-5" />
                    TikTok
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Todos os vídeos públicos</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    tiktok.com/@.../video/...
                  </code>
                </div>
                
                <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <div className="font-semibold text-blue-700 dark:text-blue-400 mb-2 flex items-center gap-2">
                    <TwitterIcon className="w-5 h-5" />
                    Twitter/X
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Posts com vídeos</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    x.com/.../status/...
                    <br />
                    twitter.com/.../status/...
                  </code>
                </div>
                
                <div className="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800">
                  <div className="font-semibold text-indigo-700 dark:text-indigo-400 mb-2 flex items-center gap-2">
                    <FacebookIcon className="w-5 h-5" />
                    Facebook
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Vídeos públicos e Watch</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    facebook.com/watch/...
                  </code>
                </div>
                
                <div className="p-4 rounded-lg bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800">
                  <div className="font-semibold text-orange-700 dark:text-orange-400 mb-2 flex items-center gap-2">
                    <RedditIcon className="w-5 h-5" />
                    Reddit
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Vídeos de posts</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    reddit.com/r/.../comments/...
                  </code>
                </div>
                
                <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <div className="font-semibold text-red-700 dark:text-red-400 mb-2 flex items-center gap-2">
                    <PinterestIcon className="w-5 h-5" />
                    Pinterest
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Vídeos e Pins</p>
                  <code className="text-xs text-gray-500 dark:text-gray-500 mt-1 block">
                    pinterest.com/pin/...
                  </code>
                </div>
              </div>
            </div>
          )}

          {/* Video Info & Download */}
          {videoInfo && !loading && (
            <div className="space-y-6">
              {/* Video Card */}
              <VideoCard videoInfo={videoInfo} />

              {/* Format Selector */}
              <FormatSelector
                videoInfo={videoInfo}
                onSelectionChange={setDownloadRequest}
              />

              {/* Download Button */}
              {downloadRequest && (
                <DownloadButton
                  downloadRequest={downloadRequest}
                  disabled={!downloadRequest}
                />
              )}
            </div>
          )}

          {/* Seção SEO - Conteúdo Rico para Google */}
          {!videoInfo && !loading && (
            <div className="mt-12 space-y-8">
              {/* Como Funciona */}
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">📖 Como Baixar Vídeos?</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-3xl font-bold text-primary-600">1</span>
                    </div>
                    <h3 className="font-semibold mb-2">Cole o Link</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Copie a URL do vídeo do Instagram, TikTok, Twitter, Reddit ou Pinterest e cole acima
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-3xl font-bold text-primary-600">2</span>
                    </div>
                    <h3 className="font-semibold mb-2">Escolha a Qualidade</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Selecione HD, Full HD ou apenas áudio MP3 conforme sua preferência
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-3xl font-bold text-primary-600">3</span>
                    </div>
                    <h3 className="font-semibold mb-2">Baixe Grátis</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Clique em baixar e salve o vídeo sem marca d'água no seu dispositivo
                    </p>
                  </div>
                </div>
              </div>

              {/* Por que escolher MediaVid */}
              <div className="bg-gradient-to-r from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 rounded-xl shadow-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">⭐ Por que usar o MediaVid?</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="text-4xl mb-3">🆓</div>
                    <h3 className="font-semibold mb-2">100% Grátis</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Sem taxas, sem cadastro, sem limite de downloads
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-4xl mb-3">✨</div>
                    <h3 className="font-semibold mb-2">Sem Marca d'Água</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Vídeos limpos, sem logos ou marcas indesejadas
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-4xl mb-3">⚡</div>
                    <h3 className="font-semibold mb-2">Super Rápido</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Downloads em alta velocidade, sem espera
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-4xl mb-3">🔒</div>
                    <h3 className="font-semibold mb-2">Seguro e Privado</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Seus dados e downloads são completamente privados
                    </p>
                  </div>
                </div>
              </div>

              {/* FAQ */}
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">❓ Perguntas Frequentes</h2>
                <div className="space-y-4 max-w-3xl mx-auto">
                  <details className="group">
                    <summary className="font-semibold cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                      <span>Como baixar Reels do Instagram sem marca d'água?</span>
                      <span className="transition group-open:rotate-180">▼</span>
                    </summary>
                    <p className="mt-3 px-4 text-gray-600 dark:text-gray-400">
                      Basta copiar o link do Reel, colar no MediaVid, clicar em buscar e baixar. O vídeo será salvo sem marca d'água e em alta qualidade.
                    </p>
                  </details>
                  
                  <details className="group">
                    <summary className="font-semibold cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                      <span>É realmente grátis baixar vídeos do TikTok?</span>
                      <span className="transition group-open:rotate-180">▼</span>
                    </summary>
                    <p className="mt-3 px-4 text-gray-600 dark:text-gray-400">
                      Sim! O MediaVid é 100% gratuito. Baixe quantos vídeos quiser do TikTok, Instagram, Twitter e outras redes sociais sem pagar nada.
                    </p>
                  </details>
                  
                  <details className="group">
                    <summary className="font-semibold cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                      <span>Preciso instalar algum aplicativo?</span>
                      <span className="transition group-open:rotate-180">▼</span>
                    </summary>
                    <p className="mt-3 px-4 text-gray-600 dark:text-gray-400">
                      Não! O MediaVid funciona direto no seu navegador. Não precisa baixar nada, não precisa instalar aplicativos. Acesse, cole o link e baixe.
                    </p>
                  </details>
                  
                  <details className="group">
                    <summary className="font-semibold cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                      <span>Quais redes sociais são suportadas?</span>
                      <span className="transition group-open:rotate-180">▼</span>
                    </summary>
                    <p className="mt-3 px-4 text-gray-600 dark:text-gray-400">
                      Atualmente suportamos Instagram (Reels), TikTok, Twitter/X, Reddit, Facebook e Pinterest. Todos com download em alta qualidade e sem marca d'água.
                    </p>
                  </details>
                  
                  <details className="group">
                    <summary className="font-semibold cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                      <span>O download funciona no celular?</span>
                      <span className="transition group-open:rotate-180">▼</span>
                    </summary>
                    <p className="mt-3 px-4 text-gray-600 dark:text-gray-400">
                      Sim! O MediaVid funciona perfeitamente em celulares Android e iPhone. Abra no navegador do seu celular e baixe vídeos normalmente.
                    </p>
                  </details>
                </div>
              </div>
            </div>
          )}

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-gray-600 dark:text-gray-400">
            <p>MediaVid © 2025 - Baixar Vídeos Instagram, TikTok, Twitter, Reddit, Pinterest Grátis</p>
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

export default Home
