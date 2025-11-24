# 🚀 Checklist de Deploy - Social Media Downloader

## 📝 Pré-Deploy

### 1. Preparação do Código
- [ ] Todo código commitado no Git
- [ ] Dependências atualizadas (requirements.txt e package.json)
- [ ] Variáveis de ambiente configuradas
- [ ] Testes básicos funcionando localmente

### 2. Criar Repositório GitHub
```powershell
# Inicializar Git (se ainda não fez)
git init
git add .
git commit -m "Initial commit - Social Media Downloader"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/seu-usuario/social-media-downloader.git
git branch -M main
git push -u origin main
```

---

## 🌐 Deploy no Render.com

### Passo 1: Criar Conta
- [ ] Acessar https://render.com
- [ ] Fazer login com GitHub
- [ ] Autorizar acesso ao repositório

### Passo 2: Deploy do Backend
- [ ] New + → Web Service
- [ ] Conectar repositório
- [ ] Configurar:
  - Nome: `social-downloader-api`
  - Root Directory: `backend`
  - Environment: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Instance Type: `Free`
- [ ] Adicionar variável de ambiente:
  - `ENVIRONMENT` = `production`
- [ ] Clicar "Create Web Service"
- [ ] ⏱️ Aguardar build (5-10 min)
- [ ] ✅ Copiar URL gerada (ex: `https://social-downloader-api.onrender.com`)

### Passo 3: Deploy do Frontend
- [ ] New + → Static Site
- [ ] Conectar mesmo repositório
- [ ] Configurar:
  - Nome: `social-downloader`
  - Root Directory: `frontend`
  - Build Command: `npm install && npm run build`
  - Publish Directory: `dist`
- [ ] Adicionar variável de ambiente:
  - `VITE_API_URL` = `[URL do backend copiada acima]`
- [ ] Clicar "Create Static Site"
- [ ] ⏱️ Aguardar build
- [ ] ✅ Anotar URL do frontend (ex: `https://social-downloader.onrender.com`)

### Passo 4: Configurar CORS no Backend
Atualizar `backend/app/main.py`:
```python
# Adicionar URL do frontend no CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://social-downloader.onrender.com"],  # Sua URL do Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- [ ] Fazer commit e push
- [ ] Render fará redeploy automaticamente

---

## 🔍 SEO e Indexação

### Passo 1: Atualizar URLs
- [ ] Substituir `https://seu-dominio.com` pela URL real em:
  - [ ] `frontend/index.html` (meta tags)
  - [ ] `frontend/public/sitemap.xml`
  - [ ] `frontend/public/robots.txt`

### Passo 2: Google Search Console
- [ ] Acessar https://search.google.com/search-console
- [ ] Adicionar propriedade (sua URL do Render)
- [ ] Verificar propriedade:
  - [ ] Opção 1: Upload arquivo HTML na pasta `public/`
  - [ ] Opção 2: Meta tag no `<head>`
- [ ] Enviar sitemap: `https://sua-url.onrender.com/sitemap.xml`
- [ ] Solicitar indexação da página principal

### Passo 3: Google Analytics
- [ ] Criar conta em https://analytics.google.com
- [ ] Criar propriedade
- [ ] Copiar código de rastreamento (G-XXXXXXXXXX)
- [ ] Descomentar código no `frontend/index.html`
- [ ] Substituir `G-XXXXXXXXXX` pelo seu ID
- [ ] Fazer commit e push

---

## 💰 Monetização com AdSense

### Passo 1: Criar Conta AdSense
- [ ] Acessar https://www.google.com/adsense
- [ ] Fazer login com conta Google
- [ ] Adicionar site: URL do Render
- [ ] Preencher informações de pagamento
- [ ] Adicionar código AdSense no `<head>`

### Passo 2: Aguardar Aprovação
- [ ] ⏱️ Tempo de aprovação: 1-3 dias (pode levar até 2 semanas)
- [ ] Receber email de aprovação

### Passo 3: Adicionar Anúncios
Após aprovação:
- [ ] Copiar `data-ad-client` (ca-pub-XXXXXXXXXX)
- [ ] Atualizar `frontend/src/components/Ads/AdBanner.jsx`
- [ ] Criar unidades de anúncio no painel AdSense
- [ ] Copiar `data-ad-slot` para cada posição
- [ ] Adicionar componente `<AdBanner />` nas páginas:
  - [ ] Topo da Home
  - [ ] Entre input e resultado
  - [ ] Rodapé
  - [ ] Página Batch
- [ ] Fazer commit e push
- [ ] Aguardar 24-48h para anúncios começarem a aparecer

---

## 📱 Divulgação e Marketing

### Redes Sociais
- [ ] Criar página no Facebook
- [ ] Criar perfil no Instagram
- [ ] Criar conta no Twitter/X
- [ ] Fazer post inicial em todas

### Comunidades
- [ ] Reddit:
  - [ ] r/software
  - [ ] r/webdev
  - [ ] r/InternetIsBeautiful
  - [ ] r/brasil
- [ ] Facebook Groups (buscar "download videos")
- [ ] Discord (servidores de tech)

### Plataformas de Lançamento
- [ ] Product Hunt: https://www.producthunt.com
- [ ] BetaList: https://betalist.com
- [ ] AlternativeTo: https://alternativeto.net

### Conteúdo
- [ ] Escrever artigo no Medium
- [ ] Criar vídeo tutorial no YouTube
- [ ] Post no LinkedIn

---

## 🔧 Manutenção e Monitoramento

### Monitoramento
- [ ] Configurar alertas no Render (email se serviço cair)
- [ ] Verificar logs diariamente (primeiros dias)
- [ ] Monitorar Google Analytics

### Performance
- [ ] Testar velocidade: https://pagespeed.web.dev
- [ ] Testar mobile: https://search.google.com/test/mobile-friendly
- [ ] Otimizar imagens se necessário

### Backup
- [ ] Código está no GitHub ✅
- [ ] Fazer backup semanal de dados (se tiver)

---

## ✅ Pós-Deploy

### Testes Finais
- [ ] Testar download de vídeos de todas plataformas
- [ ] Testar em desktop
- [ ] Testar em mobile
- [ ] Testar em diferentes navegadores
- [ ] Verificar se anúncios aparecem (após aprovação)
- [ ] Verificar Google Analytics rastreando visitas

### Legal
- [ ] Termos de Uso visíveis no site
- [ ] Política de Privacidade visível no site
- [ ] Adicionar link de contato

---

## 📊 Metas

### Semana 1
- [ ] 100 visitas
- [ ] 500 downloads
- [ ] Compartilhar em 5 comunidades

### Mês 1
- [ ] 1.000 visitas
- [ ] Aprovação do AdSense
- [ ] Primeiros ganhos (R$ 10+)

### Mês 3
- [ ] 5.000 visitas/mês
- [ ] R$ 100+ AdSense
- [ ] Adicionar plano premium

---

## 🆘 Troubleshooting

### Build Falhou no Render
- Verificar logs de erro
- Confirmar requirements.txt correto
- Verificar sintaxe Python

### Frontend não conecta com Backend
- Verificar VITE_API_URL configurada
- Verificar CORS no backend
- Abrir DevTools e ver erros no console

### AdSense Rejeitado
- Adicionar mais conteúdo (páginas de ajuda, FAQ)
- Adicionar Termos e Privacidade
- Aguardar 7 dias e tentar novamente

### Não aparece no Google
- Demora até 2 semanas
- Verificar se sitemap foi enviado
- Criar conteúdo relevante (blog posts)

---

## 🎯 Status Atual

Data: ___/___/2025

- [ ] Código no GitHub
- [ ] Backend no ar
- [ ] Frontend no ar
- [ ] SEO configurado
- [ ] Google Search Console
- [ ] Google Analytics
- [ ] AdSense aprovado
- [ ] Anúncios funcionando
- [ ] Primeira divulgação

**Próximo passo:** ___________________________________

---

**💡 Dica:** Marque os checkboxes conforme for completando cada etapa!
