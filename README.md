# 🎬 Social Media Video Downloader

Sistema web completo para download de vídeos de múltiplas redes sociais com suporte a conversão de formatos, download em lote e interface moderna com dark mode.

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **yt-dlp** - Engine de download para múltiplas plataformas
- **Python 3.9+**
- **WebSockets** - Atualizações em tempo real

### Frontend
- **React 18** - Biblioteca UI
- **Vite** - Build tool com hot reload
- **TailwindCSS** - Estilização
- **React Router** - Navegação
- **Zustand** - Gerenciamento de estado

## 📦 Redes Sociais Suportadas

✅ **YouTube** (vídeos e Shorts) | ✅ **Instagram** (Reels, Posts, IGTV) | ✅ **TikTok** | ✅ **Twitter/X** | ✅ **Facebook** | ✅ **Reddit**

📚 **[Ver detalhes de todas as plataformas →](PLATAFORMAS.md)**

### Exemplos de URLs Suportadas:
- 🎬 YouTube: `youtube.com/watch?v=...` ou `youtube.com/shorts/...`
- 📷 Instagram: `instagram.com/reel/...` ou `instagram.com/p/...`
- 🎵 TikTok: `tiktok.com/@.../video/...`
- 🐦 Twitter: `x.com/.../status/...` ou `twitter.com/.../status/...`
- 📘 Facebook: `facebook.com/watch/...`
- 🤖 Reddit: `reddit.com/r/.../comments/...`

## ✨ Funcionalidades

- 🎥 **Download de vídeos** em várias qualidades (Full HD 1080p, HD 720p, SD 480p, Low 360p)
- 🎵 **Extração de áudio** em MP3 (apenas áudio)
- 📦 **Download em lote** - múltiplos vídeos simultâneos
- ⚡ **Sistema de fila** com controle de downloads paralelos
- 🌓 **Dark mode / Light mode** - tema adaptável
- 📊 **Progresso em tempo real** via WebSocket
- 💾 **Cache inteligente** - evita requisições duplicadas
- 📱 **Interface responsiva** - funciona em desktop e mobile
- 🚀 **Otimizado para velocidade** - downloads paralelos de fragmentos
- 📋 **Suporte a 6 plataformas** - YouTube, Instagram, TikTok, Twitter/X, Facebook, Reddit

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.9 ou superior
- Node.js 18 ou superior
- FFmpeg (para conversão de formatos)

### 1. Clone o repositório
```bash
git clone <repository-url>
cd social-media-downloader
```

### 2. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
copy .env.example .env
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependências
npm install
```

## 🚀 Executando o Projeto

### Opção 1: Executar Separadamente

#### Terminal 1 - Backend
```bash
cd c:\Estudo\download\social-media-downloader\backend ; python run.py
```
O backend estará rodando em `http://localhost:8000`

#### Terminal 2 - Frontend
```bash
cd c:\Estudo\download\social-media-downloader\frontend ; npm run dev
```
O frontend estará rodando em `http://localhost:5173`

### Opção 2: Script de Inicialização (em breve)
```bash
.\start.ps1
```

## 📁 Estrutura do Projeto

```
social-media-downloader/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point FastAPI
│   │   ├── config.py            # Configurações
│   │   ├── models/              # Modelos Pydantic
│   │   ├── routes/              # Rotas da API
│   │   ├── services/            # Lógica de negócio
│   │   └── utils/               # Utilitários
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   ├── contexts/            # Context API
│   │   ├── pages/               # Páginas
│   │   ├── services/            # API clients
│   │   └── utils/               # Utilitários
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🔧 Configuração

### Backend (.env)
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173
MAX_CONCURRENT_DOWNLOADS=3
TEMP_DOWNLOAD_PATH=./temp_downloads
MAX_FILE_SIZE_MB=500
```

### Frontend
O proxy para a API é configurado automaticamente no `vite.config.js` apontando para `http://localhost:8000`

## 📚 API Endpoints

### Documentação Interativa
Acesse `http://localhost:8000/docs` para ver a documentação completa gerada automaticamente pelo FastAPI (Swagger UI).

### Principais Endpoints

```
GET  /                          # Status da API
GET  /health                    # Health check
POST /api/video/info            # Obter informações do vídeo
POST /api/video/download        # Iniciar download
GET  /api/formats               # Listar formatos disponíveis
WS   /ws                        # WebSocket para status
```

## 🎯 Roadmap

Veja o arquivo [ROADMAP.md](./ROADMAP.md) para detalhes completos sobre o plano de desenvolvimento.

### Próximos Passos
- [ ] Implementar rotas de download
- [ ] Sistema de fila
- [ ] Conversão de formatos
- [ ] Interface de download em lote
- [ ] PWA e offline support
- [ ] Testes automatizados

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais. Respeite os termos de serviço das plataformas e direitos autorais dos criadores de conteúdo. Baixe apenas conteúdo que você tem permissão para usar.

## 🐛 Problemas Conhecidos

- FFmpeg precisa estar instalado separadamente para conversão de formatos
- Alguns vídeos privados ou com restrição de idade podem não funcionar
- Rate limiting pode ser aplicado por algumas plataformas

## 📧 Suporte

Para questões e suporte, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ usando React e FastAPI**
