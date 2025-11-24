import { Moon, Sun, Home as HomeIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { VideoIcon } from '../components/UI/SocialIcons'

function Terms() {
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
          <h1 className="text-4xl font-bold mb-4">Termos de Uso</h1>
          <p className="text-gray-500 dark:text-gray-400 mb-8">Última atualização: 24 de Novembro de 2025</p>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">1. Aceitação dos Termos</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Ao acessar e usar o MediaVid, você concorda com estes Termos de Uso. Se você não concorda, não use este serviço.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">2. Descrição do Serviço</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              O MediaVid é uma ferramenta gratuita que permite baixar vídeos de redes sociais públicas para uso pessoal.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">3. Uso Aceitável</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Você concorda em:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>✅ Usar o serviço apenas para fins legais</li>
              <li>✅ Respeitar direitos autorais e propriedade intelectual</li>
              <li>✅ Baixar apenas conteúdo que você tem permissão para usar</li>
              <li>✅ Não redistribuir conteúdo protegido por direitos autorais</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">4. Restrições</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Você NÃO pode:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>❌ Usar o serviço para violar direitos autorais</li>
              <li>❌ Fazer download de conteúdo privado sem autorização</li>
              <li>❌ Usar o serviço para spam ou atividades ilegais</li>
              <li>❌ Tentar sobrecarregar ou hackear o sistema</li>
              <li>❌ Revender ou redistribuir conteúdo baixado sem permissão</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">5. Direitos Autorais</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>Todo conteúdo baixado pertence aos seus respectivos criadores</li>
              <li>Você é responsável por garantir que tem direito de usar o conteúdo</li>
              <li>Não nos responsabilizamos pelo uso indevido de conteúdo baixado</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">6. Isenção de Responsabilidade</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>⚠️ O serviço é fornecido "como está", sem garantias</li>
              <li>⚠️ Não garantimos disponibilidade 100% do tempo</li>
              <li>⚠️ Não nos responsabilizamos por conteúdo de terceiros</li>
              <li>⚠️ Use por sua conta e risco</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">7. Limitação de Responsabilidade</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">Não somos responsáveis por:</p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>Perdas ou danos decorrentes do uso do serviço</li>
              <li>Conteúdo de terceiros</li>
              <li>Interrupções no serviço</li>
              <li>Uso indevido por parte dos usuários</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">8. Modificações</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Podemos modificar estes termos a qualquer momento. Continue usando o serviço após mudanças significa que você aceita os novos termos.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">9. Lei Aplicável</h2>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              Estes termos são regidos pelas leis do Brasil.
            </p>
          </section>

          <div className="mt-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <p className="text-gray-700 dark:text-gray-300 font-semibold">
              ⚠️ IMPORTANTE: Este serviço é uma ferramenta. O usuário é totalmente responsável pelo uso que faz do conteúdo baixado. Respeite sempre os direitos autorais e propriedade intelectual.
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

export default Terms
