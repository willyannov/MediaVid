# 📖 Guia Completo de Setup - MediaVid

Guia definitivo para clonar, configurar e colocar o projeto online.

---

## 📋 Índice

1. [Requisitos](#-requisitos)
2. [Instalação Local](#-instalação-local)
3. [Estrutura do Projeto](#-estrutura-do-projeto)
4. [Plataformas Suportadas](#-plataformas-suportadas)
5. [Deploy em Produção](#-deploy-em-produção)
6. [Problemas Conhecidos](#-problemas-conhecidos)
7. [Monetização](#-monetização)

---

## 📦 Requisitos

### Desenvolvimento Local:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **FFmpeg** (opcional) - Para merge de vídeo+áudio Reddit

### Produção:

- Conta no **GitHub** (grátis)
- Conta no **Render.com** (grátis)

---

## 🚀 Instalação Local

### 1. Clonar o Projeto

```bash
git clone https://github.com/willyannov/MediaVid.git
cd MediaVid
```

### 2. Configurar Backend (Python/FastAPI)

```bash
# Entrar na pasta backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo de configuração
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Rodar servidor
python run.py
```

✅ **Backend rodando em:** http://localhost:8000  
📚 **Documentação API:** http://localhost:8000/docs

### 3. Configurar Frontend (React/Vite)

Abra **OUTRO terminal**:

```bash
# Entrar na pasta frontend
cd frontend

# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

✅ **Frontend rodando em:** http://localhost:5173

### 4. Testar Aplicação

1. Abra http://localhost:5173 no navegador
2. Cole link de vídeo do TikTok, Instagram, Twitter, Facebook ou Reddit
3. Clique em "Buscar"
4. Selecione qualidade e formato
5. Clique em "Baixar"

---

## 📁 Estrutura do Projeto

```
MediaVid/
├── backend/                 # API Python FastAPI
│   ├── app/
│   │   ├── main.py         # Entrada da API
│   │   ├── config.py       # Configurações
│   │   ├── routes/         # Endpoints da API
│   │   ├── services/       # Lógica de negócio
│   │   │   ├── downloader.py      # Download de vídeos (yt-dlp)
│   │   │   ├── tiktok_fallback.py # API alternativa TikTok
│   │   │   └── browser_cookies.py # Extração de cookies
│   │   ├── models/         # Modelos Pydantic
│   │   └── utils/          # Validadores e helpers
│   ├── requirements.txt    # Dependências Python
│   └── run.py             # Iniciar servidor
│
├── frontend/               # UI React + Vite
│   ├── src/
│   │   ├── App.jsx        # Componente principal
│   │   ├── pages/         # Páginas (Home, Batch, etc)
│   │   ├── components/    # Componentes reutilizáveis
│   │   ├── services/      # Chamadas API
│   │   └── contexts/      # Context API (Theme)
│   ├── index.html         # HTML principal + Meta tags SEO
│   ├── package.json       # Dependências Node.js
│   └── vite.config.js     # Config Vite
│
├── README.md              # Visão geral do projeto
├── SETUP_GUIDE.md         # Este arquivo
├── PLATAFORMAS.md         # Detalhes das plataformas
└── render.yaml            # Config deploy Render
```

---

## 📱 Plataformas Suportadas

### ✅ Funcionando:

| Plataforma | Status | Qualidades | Notas |
|------------|--------|------------|-------|
| **Instagram** | ✅ | Auto (720p-1080p) | Apenas Reels públicos |
| **TikTok** | ✅ | Auto (720p-1080p) | API alternativa TikWM |
| **Twitter/X** | ✅ | Auto | Vídeos públicos |
| **Facebook** | ✅ | Auto | Vídeos públicos e Watch |
| **Reddit** | ✅ | Auto | Precisa FFmpeg para merge |

### ⚠️ Desabilitadas:

| Plataforma | Motivo | Solução Futura |
|------------|--------|----------------|
| **YouTube** | IP de datacenter bloqueado | Proxy/VPN ($50-200/mês) |

---

## 🌐 Deploy em Produção

### Passo 1: Preparar Repositório

```bash
# Fazer push para GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

### Passo 2: Deploy Backend no Render

1. Criar conta em https://render.com
2. "New +" → "Web Service"
3. Conectar repositório GitHub
4. Configurar:
   ```
   Name: mediavid-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```
5. Criar serviço (aguardar ~5-10 min)
6. **Copiar URL gerada** (ex: `https://mediavid-backend.onrender.com`)

### Passo 3: Deploy Frontend no Render

1. "New +" → "Static Site"
2. Conectar mesmo repositório
3. Configurar:
   ```
   Name: mediavid
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```
4. **Adicionar variável de ambiente:**
   ```
   VITE_API_URL = https://mediavid-backend.onrender.com
   ```
5. Criar site (aguardar ~3-5 min)
6. ✅ Site online em: `https://mediavid.onrender.com`

### Passo 4: Configurar Domínio Personalizado (Opcional)

1. No Render, ir em "Settings" → "Custom Domains"
2. Adicionar domínio (ex: `mediavid.site`)
3. Configurar DNS no provedor do domínio:
   ```
   Type: CNAME
   Name: @
   Value: mediavid.onrender.com
   ```
4. Aguardar propagação DNS (~5-30 min)

---

## 🚨 Problemas Conhecidos

### 1. YouTube Desabilitado

**Problema:** YouTube bloqueou IPs de datacenters (Render, Heroku, etc).

**Soluções:**

- ❌ **Criar novo projeto no Render** - Não funciona (mesmo problema)
- ❌ **Mudar provedor** - Todos datacenters são bloqueados
- ✅ **Usar proxy residencial** - Funciona mas custa $50-200/mês
- ✅ **Aceitar limitação** - Focar nas 5 plataformas que funcionam

**Status:** YouTube está **comentado no código** e pode ser reativado facilmente quando houver solução.

### 2. Instagram Login Required

**Problema:** Alguns Reels privados ou de contas privadas requerem login.

**Solução:** Apenas vídeos públicos são suportados. Avisar usuário.

### 3. FFmpeg Não Encontrado (Reddit)

**Problema:** Reddit precisa FFmpeg para merge de vídeo+áudio.

**Solução Local:**
```bash
# Windows (Chocolatey)
choco install ffmpeg

# Linux
sudo apt install ffmpeg

# Mac
brew install ffmpeg
```

**Solução Render:** FFmpeg já está instalado automaticamente no Render.

### 4. Rate Limiting (429 Errors)

**Problema:** Muitas requisições em pouco tempo.

**Solução:** Implementado rate limiting de 3s entre requisições YouTube (quando reativado).

---

## 💰 Monetização

### Google AdSense (Recomendado)

**Requisitos:**
- Domínio próprio (não pode usar `.onrender.com`)
- Conta AdSense aprovada
- Páginas de Privacidade e Termos

**Passos:**
1. Registrar em https://www.google.com/adsense
2. Adicionar código no `frontend/index.html`:
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-SEU_ID"
        crossorigin="anonymous"></script>
   ```
3. Criar componente `AdBanner.jsx` (já existe no projeto)
4. Adicionar banners nas páginas

**Estimativa de Ganhos:**
- 1.000 visitas/dia = $1-5/dia
- 10.000 visitas/dia = $10-50/dia
- 100.000 visitas/dia = $100-500/dia

### Outras Opções:

- **Doações:** Ko-fi, Buy Me a Coffee
- **Afiliados:** Amazon Associates
- **Premium:** Versão paga com mais funcionalidades

---

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

#### Backend (.env):
```bash
# Ambiente
ENVIRONMENT=production

# CORS (permitir frontend)
CORS_ORIGINS=https://mediavid.site,https://mediavid.onrender.com

# YouTube Cookies (se reativar YouTube)
YOUTUBE_COOKIES=  # Conteúdo do cookies.txt
```

#### Frontend (.env):
```bash
# URL da API
VITE_API_URL=https://mediavid-backend.onrender.com
```

### Render.yaml (Deploy Automático)

O arquivo `render.yaml` já está configurado para deploy automático de backend + frontend.

Para usar:
1. Ir em Render Dashboard → "Blueprints"
2. Conectar repositório
3. Aplicar blueprint `render.yaml`
4. Tudo será criado automaticamente

---

## 📊 Monitoramento

### Logs do Backend (Render):

1. Dashboard → Serviço → "Logs"
2. Ver requisições, erros, downloads

### Analytics (Google Analytics):

1. Criar conta em https://analytics.google.com
2. Adicionar código no `index.html`:
   ```html
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-SEU_ID"></script>
   ```

---

## 🔐 Segurança

### HTTPS

Render fornece HTTPS automático (certificado Let's Encrypt grátis).

### Rate Limiting

Já implementado no backend:
- 3s entre requisições YouTube (quando reativado)
- 30s de espera em caso de erro 429

### CORS

Configurado para aceitar apenas domínios específicos.

### Sanitização

URLs são validadas antes de processar.

---

## 🆘 Suporte

### Problemas Comuns:

**Erro: "Module not found"**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Erro: "Port already in use"**
```bash
# Mudar porta no backend (run.py)
uvicorn.run(app, host="0.0.0.0", port=8001)

# Mudar porta no frontend (vite.config.js)
server: { port: 5174 }
```

**Erro: "CORS policy"**
```bash
# Verificar CORS_ORIGINS no backend/.env
# Adicionar URL do frontend
```

### Contato:

- **Issues:** https://github.com/willyannov/MediaVid/issues
- **Email:** (adicionar seu email)

---

## 📝 Licença

MIT License - Livre para uso pessoal e comercial.

---

## ✅ Checklist de Deploy

- [ ] Código no GitHub
- [ ] Backend deployado no Render
- [ ] Frontend deployado no Render
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio personalizado (opcional)
- [ ] Google AdSense configurado (opcional)
- [ ] Analytics configurado (opcional)
- [ ] Páginas de Privacidade e Termos
- [ ] Testado todas plataformas
- [ ] Monitoramento ativo

---

**MediaVid © 2025** - Baixe vídeos de qualquer rede social 🎬
