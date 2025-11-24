import { Moon, Sun, Home as HomeIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { VideoIcon } from '../components/UI/SocialIcons'

function Privacy() {
  const { isDark, toggleTheme } = useTheme()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <VideoIcon className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold">MediaVid</h1>
            </a>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <HomeIcon className="w-5 h-5" />
              Início
            </button>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
          <h1 className="text-4xl font-bold mb-4">Política de Privacidade</h1>
          <p className="text-gray-500 dark:text-gray-400 mb-8">Última atualização: 24 de Novembro de 2025</p>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">1. Informações que Coletamos</h2>
            
            <h3 className="text-xl font-semibold mb-2 mt-4">1.1 Dados Fornecidos por Você</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300 mb-4">
              <li>URLs de vídeos que você deseja baixar</li>
              <li>Nenhum dado pessoal é necessário para usar o serviço</li>
            </ul>

            <h3 className="text-xl font-semibold mb-2 mt-4">1.2 Dados Coletados Automaticamente</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300 mb-4">
              <li><strong>Endereço IP:</strong> Para prevenir abuso e limitar requisições</li>
              <li><strong>Cookies:</strong> Para melhorar a experiência do usuário</li>
              <li><strong>Dados de Uso:</strong> Páginas visitadas, tempo de uso, tipo de navegador</li>
              <li><strong>Google Analytics:</strong> Estatísticas anônimas de visitação</li>
            </ul>

            <h3 className="text-xl font-semibold mb-2 mt-4">1.3 Google AdSense</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>Usamos Google AdSense para exibir anúncios</li>
              <li>O Google pode coletar cookies e dados para personalizar anúncios</li>
              <li>Você pode desativar anúncios personalizados em: <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">https://www.google.com/settings/ads</a></li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">2. Como Usamos Seus Dados</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Usamos seus dados para:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>✅ Processar downloads de vídeos</li>
              <li>✅ Melhorar o serviço</li>
              <li>✅ Prevenir abuso e fraude</li>
              <li>✅ Exibir anúncios relevantes (via Google AdSense)</li>
              <li>✅ Analisar estatísticas de uso (via Google Analytics)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">3. Compartilhamento de Dados</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>❌ <strong>NÃO vendemos</strong> seus dados pessoais</li>
              <li>⚠️ Podemos compartilhar com: Google (Analytics, AdSense), servidores de hospedagem</li>
              <li>⚠️ Podemos divulgar dados se exigido por lei</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">4. Cookies</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Usamos cookies para:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300 mb-4">
              <li>Lembrar preferências (tema escuro/claro)</li>
              <li>Google Analytics (estatísticas)</li>
              <li>Google AdSense (anúncios)</li>
            </ul>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              <strong>Como desativar cookies:</strong> Configure seu navegador para bloquear cookies. Nota: Isso pode afetar a funcionalidade do site.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">5. Serviços de Terceiros</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">Google Analytics</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Coleta dados anônimos de uso. <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Política de Privacidade</a>
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Google AdSense</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Exibe anúncios personalizados. <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Política de Anúncios</a>
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">6. Retenção de Dados</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li><strong>URLs:</strong> Não armazenamos permanentemente</li>
              <li><strong>Vídeos:</strong> Deletados automaticamente após download</li>
              <li><strong>Logs:</strong> Mantidos por até 30 dias para segurança</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">7. Seus Direitos (LGPD/GDPR)</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Você tem direito de:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>✅ Acessar seus dados</li>
              <li>✅ Corrigir dados incorretos</li>
              <li>✅ Solicitar exclusão de dados</li>
              <li>✅ Revogar consentimento</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">8. Segurança</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>🔒 Usamos HTTPS para criptografar dados em trânsito</li>
              <li>🔒 Não armazenamos senhas (não requeremos login)</li>
              <li>🔒 Implementamos medidas para prevenir acesso não autorizado</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">9. Crianças</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>Este serviço não é direcionado a menores de 13 anos</li>
              <li>Não coletamos intencionalmente dados de crianças</li>
            </ul>
          </section>

          <div className="mt-8 p-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <h3 className="text-xl font-bold mb-4">📌 Resumo Simplificado</h3>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li><strong>O que coletamos:</strong> URLs de vídeos, IP, cookies, dados de uso</li>
              <li><strong>Por que coletamos:</strong> Processar downloads, melhorar serviço, prevenir abuso</li>
              <li><strong>Compartilhamos?</strong> Apenas com Google (Analytics/AdSense) e hospedagem</li>
              <li><strong>Vendemos dados?</strong> Não!</li>
              <li><strong>Seus direitos:</strong> Acesso, correção, exclusão de dados</li>
            </ul>
          </div>

          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="text-gray-700 dark:text-gray-300">
              <strong>Ao usar este serviço, você concorda com esta Política de Privacidade.</strong>
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-gray-600 dark:text-gray-400">
            <p>MediaVid © 2025 - Feito com ❤️</p>
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

export default Privacy
