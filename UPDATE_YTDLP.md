# 🔄 Como Atualizar o yt-dlp

## Problema: YouTube retornando erro 500

O YouTube frequentemente muda suas APIs de proteção, fazendo com que versões antigas do yt-dlp parem de funcionar. A mensagem "Este vídeo requer autenticação" em vídeos públicos é um sintoma comum.

## Solução: Atualizar o yt-dlp

### 🖥️ Localmente (para testes)

```powershell
# Ativar ambiente virtual
cd backend
.\venv\Scripts\activate

# Atualizar yt-dlp para a versão mais recente
pip install -U yt-dlp

# Testar se funcionou
python -c "import yt_dlp; print(yt_dlp.version.__version__)"
```

### ☁️ No Render.com

O Render usa o arquivo `requirements.txt` para instalar as dependências. Já atualizei o arquivo para usar `yt-dlp>=2024.11.18`, que força a instalação de uma versão mais recente.

**Para aplicar no servidor:**

1. Faça commit e push das alterações:
   ```powershell
   git add .
   git commit -m "fix: atualiza yt-dlp para corrigir erro do YouTube"
   git push origin main
   ```

2. O Render vai detectar as mudanças e fazer redeploy automaticamente

3. Aguarde o deploy completar (1-3 minutos)

### 🔍 Verificar se funcionou

Após o deploy, teste com um vídeo público do YouTube no site:
- https://mediavid.onrender.com

Se ainda assim não funcionar, pode ser necessário:

1. **Limpar o cache do build no Render:**
   - Dashboard do Render → Seu serviço → Settings → "Clear build cache & deploy"

2. **Forçar reinstalação completa:**
   - Dashboard do Render → Manual Deploy → "Clear build cache"

## 📋 Alterações Feitas

### 1. `requirements.txt`
- Mudou de `yt-dlp` (qualquer versão) para `yt-dlp>=2024.11.18` (versão mínima)

### 2. `downloader.py`
- Adicionou `player_client: ['android', 'web']` para YouTube
- Adicionou headers HTTP mais completos
- Adicionou tratamento específico de erros do YouTube
- Configurações extras: `nocheckcertificate`, `age_limit: None`

### 3. Mensagens de Erro
- Mensagens mais claras quando YouTube bloqueia
- Instruções de como resolver incluídas no erro

## 🚨 Se AINDA não funcionar

O YouTube pode estar bloqueando o IP do servidor Render. Soluções:

1. **Usar proxy/VPN** (requer configuração avançada)
2. **Migrar para outro servidor** com IP diferente
3. **Usar API oficial do YouTube** (requer chave de API)
4. **Implementar fallback** para extração manual via scraping

## 📝 Monitoramento

Sempre que o YouTube mudar suas proteções:
- Atualize o yt-dlp: `pip install -U yt-dlp`
- Teste localmente antes de fazer deploy
- Verifique issues no GitHub do yt-dlp: https://github.com/yt-dlp/yt-dlp/issues
