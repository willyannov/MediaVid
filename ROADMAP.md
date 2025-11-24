# 🎬 Social Media Video Downloader - Roadmap Completo

## 📋 Visão Geral do Projeto
Sistema web para download de vídeos de múltiplas redes sociais com suporte a conversão de formatos, download em lote e interface moderna.

### Tecnologias Escolhidas
- **Frontend**: React + Vite (hot reload)
- **Backend**: FastAPI (Python)
- **Download Engine**: yt-dlp
- **Estilo**: TailwindCSS + shadcn/ui
- **Gerenciamento de Estado**: React Context/Zustand
- **Requisições**: Axios

### Redes Sociais Suportadas
✅ YouTube | ✅ Instagram | ✅ TikTok | ✅ Twitter/X | ✅ Facebook | ✅ Reddit

---

## 🗺️ FASES DO PROJETO

### **FASE 1: Setup Inicial** ⏱️ 1-2 horas
- [x] Criar estrutura de pastas
- [ ] Configurar ambiente Python (venv)
- [ ] Instalar dependências backend (FastAPI, yt-dlp, uvicorn, python-multipart)
- [ ] Configurar React com Vite
- [ ] Instalar dependências frontend (React Router, Axios, TailwindCSS)
- [ ] Configurar CORS no backend
- [ ] Testar hot reload em ambos os ambientes

### **FASE 2: Backend Core** ⏱️ 3-4 horas ✅ EM ANDAMENTO
- [x] Criar estrutura de rotas FastAPI
  - `POST /api/video/info` - Obter informações do vídeo
  - `POST /api/video/download` - Iniciar download
  - `GET /api/formats` - Listar formatos disponíveis
  - `WebSocket /ws` - Status de download em tempo real (pendente)
- [x] Implementar serviço de extração de informações (yt-dlp)
- [x] Implementar serviço de download com streaming
- [ ] Sistema de fila para downloads em lote (Python Queue)
- [ ] Gerenciador de conversão de formatos (FFmpeg)
- [x] Tratamento de erros e validações

### **FASE 3: Frontend Base** ⏱️ 3-4 horas ✅ COMPLETO
- [x] Criar layout responsivo com header/footer
- [x] Implementar Dark/Light mode (Context API)
- [x] Página inicial com input de URL
- [x] Componente de validação de URL por rede social
- [x] Sistema de notificações/toasts
- [x] Loading states e skeleton screens

### **FASE 4: Features de Download** ⏱️ 4-5 horas ✅ COMPLETO
- [x] Interface de informações do vídeo
  - Thumbnail
  - Título e descrição
  - Duração
  - Autor/Canal
  - Visualizações
- [x] Seletor de qualidade (720p, 1080p, 4K, etc.)
- [x] Seletor de formato (MP4, WebM, AVI, MKV)
- [x] Opção "Apenas Áudio" (MP3, M4A, WAV)
- [x] Botão de download com progresso
- [ ] WebSocket para atualização de progresso em tempo real

### **FASE 5: Download em Lote** ⏱️ 3-4 horas ✅ COMPLETO
- [x] Interface para adicionar múltiplos URLs
- [x] Lista de URLs com validação individual
- [x] Gerenciador de fila visual
- [x] Indicador de progresso para cada item
- [x] Opção de pausar/cancelar downloads
- [x] Download simultâneo (configurável, máx 3-5)
- [x] Botão "Baixar Tudo"

### **FASE 6: Histórico Local** ⏱️ 2-3 horas
- [ ] Salvar histórico no localStorage
- [ ] Página de histórico com filtros
- [ ] Re-download de itens anteriores
- [ ] Limpeza de histórico
- [ ] Exportar/Importar histórico (JSON)

### **FASE 7: UI/UX Avançada** ⏱️ 3-4 horas
- [ ] Animações e transições suaves
- [ ] Drag & Drop de URLs
- [ ] Atalhos de teclado
- [ ] Modo compacto/expandido
- [ ] Responsividade mobile completa
- [ ] PWA (Progressive Web App) - funciona offline

### **FASE 8: Otimizações** ⏱️ 2-3 horas
- [ ] Cache de informações de vídeos
- [ ] Compressão de responses (gzip)
- [ ] Rate limiting para evitar abuso
- [ ] Logs estruturados
- [ ] Monitoramento de performance
- [ ] Limpeza automática de arquivos temporários

### **FASE 9: Testes e Deploy** ⏱️ 2-3 horas
- [ ] Testes unitários backend (pytest)
- [ ] Testes frontend (Vitest/Jest)
- [ ] Testes de integração
- [ ] Documentação da API (Swagger automático do FastAPI)
- [ ] Scripts de inicialização
- [ ] Documentação de uso

---

## 📁 Estrutura de Arquivos Final

```
social-media-downloader/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Entry point FastAPI
│   │   ├── config.py               # Configurações
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── video.py            # Modelos Pydantic
│   │   │   └── download.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── downloader.py       # Lógica yt-dlp
│   │   │   ├── converter.py        # Conversão de formatos
│   │   │   └── queue_manager.py    # Gerenciador de fila
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── video.py            # Rotas de vídeo
│   │   │   └── websocket.py        # WebSocket
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py       # Validações
│   │       └── helpers.py
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py                       # Script de inicialização
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Header.jsx
│   │   │   │   └── Footer.jsx
│   │   │   ├── VideoInfo/
│   │   │   │   ├── VideoCard.jsx
│   │   │   │   └── FormatSelector.jsx
│   │   │   ├── Download/
│   │   │   │   ├── DownloadButton.jsx
│   │   │   │   ├── ProgressBar.jsx
│   │   │   │   └── QueueManager.jsx
│   │   │   ├── Batch/
│   │   │   │   ├── URLInput.jsx
│   │   │   │   └── BatchList.jsx
│   │   │   └── UI/
│   │   │       ├── Toast.jsx
│   │   │       ├── ThemeToggle.jsx
│   │   │       └── Loading.jsx
│   │   ├── contexts/
│   │   │   ├── ThemeContext.jsx
│   │   │   └── DownloadContext.jsx
│   │   ├── services/
│   │   │   ├── api.js              # Axios config
│   │   │   └── websocket.js
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Batch.jsx
│   │   │   └── History.jsx
│   │   ├── utils/
│   │   │   ├── validators.js
│   │   │   └── formatters.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── .gitignore
├── README.md
└── ROADMAP.md (este arquivo)
```

---

## 🚀 Ordem de Implementação Recomendada

### Sprint 1 (Semana 1) - MVP Básico
1. Setup completo (Fase 1)
2. Backend core com rota de info + download simples (Fase 2 - parcial)
3. Frontend básico com input e exibição de info (Fase 3 - parcial)
4. Download simples funcionando

### Sprint 2 (Semana 2) - Features Core
1. Completar Backend (Fase 2)
2. Completar Frontend base (Fase 3)
3. Implementar seleção de qualidade e formato (Fase 4)
4. Implementar conversão de formatos

### Sprint 3 (Semana 3) - Features Avançadas
1. Sistema de fila e download em lote (Fase 5)
2. Histórico local (Fase 6)
3. Melhorias de UI/UX (Fase 7 - parcial)

### Sprint 4 (Semana 4) - Polimento
1. UI/UX avançada completa (Fase 7)
2. Otimizações (Fase 8)
3. Testes e documentação (Fase 9)

---

## 🛠️ Comandos Úteis

### Backend
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor (com hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Instalar dependências
npm install

# Rodar dev server (com hot reload)
npm run dev

# Build para produção
npm run build
```

---

## 📦 Dependências Principais

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
yt-dlp==2023.11.16
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
websockets==12.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.6"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

---

## 🎯 Próximos Passos Imediatos

1. ✅ Estrutura criada
2. ⏳ Configurar ambiente Python
3. ⏳ Instalar dependências backend
4. ⏳ Criar arquivo main.py básico
5. ⏳ Configurar React com Vite
6. ⏳ Testar comunicação frontend-backend

**Pronto para começar a implementação!** 🚀
