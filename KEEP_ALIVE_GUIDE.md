# 🔄 Keep-Alive e Anti-Hibernação - Render

## 🚨 Problema: Hibernação do Render

**Render.com (plano gratuito):**
- Hiberna após **15 minutos** de inatividade
- Primeira requisição após hibernar demora **30-60 segundos** (cold start)
- Usuários têm experiência ruim ao aguardar

---

## ✅ Solução Implementada: Keep-Alive Automático

### Backend (FastAPI)

Criado endpoint `/api/health/ping`:
```python
@router.get("/ping")
async def ping():
    """Endpoint leve para keep-alive"""
    return {"status": "alive"}
```

### Frontend (React)

Serviço automático que faz ping a cada 10 minutos:
```javascript
// src/services/keepAlive.js
- Ping a cada 10 minutos (antes dos 15min de timeout)
- Apenas em produção (não em desenvolvimento)
- Console logs para monitoramento
```

### Como Funciona:

1. Usuário acessa site
2. Frontend carrega
3. Keep-alive inicia automaticamente
4. Faz ping para `/api/health/ping` a cada 10min
5. Backend permanece ativo ✅

---

## 🎯 Alternativas (Mais Eficientes)

### 1. **Cron Jobs Externos** (RECOMENDADO) ⭐

Use serviços gratuitos para fazer ping:

#### a) **UptimeRobot** (Grátis)
```
https://uptimerobot.com

Configuração:
- Monitor Type: HTTP(s)
- URL: https://mediavid-backend.onrender.com/api/health/ping
- Interval: 5 minutos
- Limit: 50 monitors grátis
```

#### b) **Cron-Job.org** (Grátis)
```
https://cron-job.org

Configuração:
- URL: https://mediavid-backend.onrender.com/api/health/ping
- Interval: */10 * * * * (a cada 10 min)
- Limit: Ilimitado grátis
```

#### c) **Better Stack** (Grátis)
```
https://betterstack.com

Configuração:
- URL: https://mediavid-backend.onrender.com/api/health/ping
- Interval: 10 minutos
- Bonus: Alertas se servidor cair
```

#### d) **GitHub Actions** (Grátis)
```yaml
# .github/workflows/keep-alive.yml
name: Keep Backend Alive

on:
  schedule:
    - cron: '*/10 * * * *' # A cada 10 minutos

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Backend
        run: curl -f https://mediavid-backend.onrender.com/api/health/ping
```

### 2. **Upgrade para Render Paid** ($7/mês)

**Vantagens:**
- Sem hibernação
- Sempre online
- Cold start eliminado
- 750 horas/mês → ilimitado

**Quando vale a pena:**
- 1000+ usuários/dia
- Receita de AdSense > $20/mês
- Experiência profissional necessária

### 3. **Migrar para Fly.io** (Grátis)

**Vantagens sobre Render:**
- 3 VMs grátis sempre ativas
- Sem hibernação no plano grátis
- Cold start mais rápido

**Desvantagens:**
- Setup mais complexo
- Precisa Dockerfile

---

## 📊 Comparação de Soluções

| Solução | Custo | Complexidade | Eficiência |
|---------|-------|--------------|------------|
| Keep-alive Frontend | $0 | Baixa ⭐ | Média |
| UptimeRobot | $0 | Muito Baixa ⭐⭐⭐ | Alta |
| Cron-Job.org | $0 | Muito Baixa ⭐⭐⭐ | Alta |
| GitHub Actions | $0 | Média | Alta |
| Render Paid | $7/mês | Nenhuma | Máxima |
| Fly.io | $0 | Alta | Máxima |

---

## 🚀 Recomendação

### Curto Prazo (AGORA):
1. ✅ Keep-alive no frontend (já implementado)
2. ✅ Configurar **UptimeRobot** (5 minutos)
   - Grátis, fácil, eficiente
   - Monitora + keep-alive

### Médio Prazo (Depois de 100 usuários/dia):
- ✅ Adicionar **Better Stack** para alertas
- ✅ Monitorar custos vs benefícios

### Longo Prazo (Depois de 1000 usuários/dia):
- ✅ Upgrade Render Paid ($7/mês)
- ✅ Experiência profissional garantida

---

## 🔧 Setup Rápido: UptimeRobot

### Passo 1: Criar Conta
```
1. Acessar: https://uptimerobot.com
2. Sign Up (grátis)
3. Confirmar email
```

### Passo 2: Criar Monitor
```
Dashboard → Add New Monitor

Monitor Type: HTTP(s)
Friendly Name: MediaVid Backend
URL: https://mediavid-backend.onrender.com/api/health/ping
Monitoring Interval: 5 minutes
Monitor Timeout: 30 seconds
Alert Contacts: seu@email.com
```

### Passo 3: Verificar
```
- Aguardar 5 minutos
- Verificar "Up" no dashboard
- Backend nunca mais hibernará! ✅
```

---

## 📊 Monitoramento

### Verificar Keep-Alive Funcionando:

**Console do Navegador (Frontend):**
```javascript
// Deve aparecer a cada 10min:
✅ Ping bem-sucedido - Uptime: 600s
```

**Logs do Render (Backend):**
```
GET /api/health/ping - 200 OK
```

**UptimeRobot Dashboard:**
```
✅ Up - 99.9% uptime
🟢 Response time: 50-200ms
```

---

## ⚠️ Validação de Plataforma

### Problema Resolvido: YouTube e Plataformas Não Suportadas

**Antes:**
- Tentava processar YouTube (desabilitado)
- Demorava 30-60s para falhar
- Usuário esperando sem feedback

**Agora:**
```python
# Valida ANTES de processar
platform = detect_platform(url)
if platform == 'Unknown':
    return "Plataforma não suportada. 
            Suportamos: Instagram, TikTok, Twitter, Facebook, Reddit"
```

**Resultado:**
- ✅ Resposta instantânea (<100ms)
- ✅ Mensagem clara
- ✅ Sem espera desnecessária

---

## 🎯 Checklist de Implementação

### Backend:
- [x] Endpoint `/api/health/ping` criado
- [x] Validação de plataforma implementada
- [x] Mensagem para plataformas não suportadas

### Frontend:
- [x] Serviço keep-alive criado
- [x] Auto-start em produção
- [x] Console logs para debug

### Externo (Fazer Agora):
- [ ] Criar conta UptimeRobot
- [ ] Adicionar monitor (5min)
- [ ] Verificar funcionamento
- [ ] (Opcional) GitHub Actions cron

### Futuro:
- [ ] Monitorar uptime
- [ ] Avaliar upgrade Render
- [ ] Considerar Fly.io

---

## 💡 Dicas Extras

### 1. Múltiplos Monitores
```
UptimeRobot pode monitorar:
- Backend: /api/health/ping
- Frontend: https://mediavid.site
- APIs específicas: /api/video/info
```

### 2. Alertas
```
Configurar alertas se:
- Backend ficar offline > 5min
- Response time > 2000ms
- Erro 500 detectado
```

### 3. Status Page Pública
```
UptimeRobot oferece:
- Página de status pública
- https://stats.uptimerobot.com/seu-id
- Transparência para usuários
```

---

**Última atualização:** 24/11/2025  
**Status:** ✅ Keep-Alive Implementado  
**Próximo Passo:** Configurar UptimeRobot (5 minutos)
