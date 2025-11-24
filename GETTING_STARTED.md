# 🚀 Início Rápido - Social Media Downloader

## Passo a Passo para Começar

### 1️⃣ Configurar o Backend (Python/FastAPI)

Abra um terminal no diretório do projeto e execute:

```powershell
# Navegar para o backend
cd backend

# Criar ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual (Windows)
.\venv\Scripts\activate

# Instalar todas as dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
copy .env.example .env

# Rodar o servidor (com hot reload)
python run.py
```

✅ **Backend estará rodando em:** http://localhost:8000
📚 **Documentação da API:** http://localhost:8000/docs

---

### 2️⃣ Configurar o Frontend (React/Vite)

Abra **OUTRO** terminal e execute:

```powershell
# Navegar para o frontend
cd frontend

# Instalar dependências do Node.js
npm install

# Rodar o servidor de desenvolvimento (com hot reload)
npm run dev
```

✅ **Frontend estará rodando em:** http://localhost:5173

---

### 3️⃣ Acessar a Aplicação

Abra seu navegador e acesse: **http://localhost:5173**

Você verá a interface inicial com:
- ✨ Dark mode / Light mode funcionando
- 🎨 Design responsivo
- 🔄 Hot reload ativo (mudanças aparecem automaticamente)

---

## 🔥 Comandos Rápidos

### Backend
```powershell
cd backend
.\venv\Scripts\activate
python run.py
```

### Frontend
```powershell
cd frontend
npm run dev
```

---

## ❓ Problemas Comuns

### "python não é reconhecido"
- Instale Python 3.9+ de https://www.python.org/downloads/
- Marque "Add Python to PATH" durante instalação

### "npm não é reconhecido"
- Instale Node.js 18+ de https://nodejs.org/

### Erro ao instalar dependências Python
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Porta já em uso
Mude a porta no arquivo de configuração:
- Backend: `backend/.env` (PORT=8000)
- Frontend: `frontend/vite.config.js` (server.port)

---

## 📖 Próximos Passos

1. ✅ Aplicação base está rodando
2. 📝 Veja o [ROADMAP.md](./ROADMAP.md) para entender a arquitetura
3. 🔨 Comece implementando as rotas da API (Fase 2 do roadmap)
4. 💡 Leia o código nos arquivos criados para entender a estrutura

---

## 🎯 Status do Projeto

| Componente | Status |
|------------|--------|
| ✅ Estrutura de pastas | Completo |
| ✅ Backend base FastAPI | Completo |
| ✅ Frontend base React | Completo |
| ✅ Hot reload | Completo |
| ✅ Dark/Light mode | Completo |
| ⏳ API de download | Pendente |
| ⏳ Sistema de fila | Pendente |
| ⏳ Conversão de formatos | Pendente |

**Bora começar a codar! 🚀**
