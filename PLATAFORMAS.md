# 📱 Plataformas Suportadas

Este documento lista todas as plataformas de mídia social suportadas pelo Social Media Downloader e exemplos de URLs válidas.

---

## 🎬 YouTube
**Status:** ✅ Totalmente Suportado

### Tipos de Conteúdo:
- ✅ Vídeos normais (qualquer duração)
- ✅ YouTube Shorts (vídeos curtos verticais)
- ✅ Transmissões ao vivo (arquivadas)
- ✅ Vídeos de playlists

### Exemplos de URLs:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
https://www.youtube.com/shorts/BNZs70LwTZM
https://www.youtube.com/watch?v=ID&t=120s
```

### Qualidades Disponíveis:
- 🎥 Full HD 1080p
- 🎥 HD 720p
- 🎥 SD 480p
- 🎥 Low 360p
- 🎵 MP3 (apenas áudio)

### Notas:
- Vídeos privados ou com restrição de idade não são suportados
- Velocidade de download limitada pelo YouTube (~7-12 MB/s)

---

## 📷 Instagram
**Status:** ✅ Totalmente Suportado

### Tipos de Conteúdo:
- ✅ Reels (vídeos curtos)
- ✅ Posts com vídeos
- ✅ IGTV
- ✅ Stories (públicos)

### Exemplos de URLs:
```
https://www.instagram.com/reel/DRS52EWjYMA/
https://www.instagram.com/p/ABC123xyz/
https://www.instagram.com/tv/ABC123xyz/
```

### Qualidades Disponíveis:
- Baixa automaticamente na melhor qualidade disponível
- Geralmente HD 720p ou Full HD 1080p

### Notas:
- Apenas conteúdo público pode ser baixado
- Contas privadas não são suportadas sem autenticação
- Alguns Reels podem ter restrições geográficas

---

## 🎵 TikTok
**Status:** ✅ Totalmente Suportado (com API Alternativa)

### Tipos de Conteúdo:
- ✅ Vídeos públicos
- ✅ Vídeos com música
- ✅ Vídeos em alta qualidade

### Exemplos de URLs:
```
https://www.tiktok.com/@username/video/1234567890123456789
https://www.tiktok.com/@ema_bb0/video/7573877016353639711
https://vm.tiktok.com/ABC123/ (link curto)
```

### Qualidades Disponíveis:
- Baixa automaticamente na melhor qualidade disponível
- Geralmente HD 720p ou 1080p (vertical)

### Tecnologia Utilizada:
- 🔄 **API Alternativa (TikWM)**: Download direto sem necessidade de login
- 🔄 **Fallback yt-dlp**: Tentado caso API alternativa falhe
- ⚡ **Download Rápido**: Conexão direta com servidores do TikTok

### Notas:
- ✅ **Funciona sem login** - Usa API alternativa para bypass
- Vídeos privados não são suportados
- Marca d'água do TikTok permanece no vídeo
- Links curtos (vm.tiktok.com) são automaticamente expandidos
- Sistema tenta múltiplas APIs se uma falhar

---

## 🐦 Twitter / X
**Status:** ✅ Totalmente Suportado

### Tipos de Conteúdo:
- ✅ Vídeos em tweets
- ✅ GIFs animados
- ✅ Vídeos em respostas
- ✅ Transmissões ao vivo (arquivadas)

### Exemplos de URLs:
```
https://twitter.com/username/status/1234567890123456789
https://x.com/username/status/1234567890123456789
https://x.com/PatriotaWil/status/1991608603640565794
https://mobile.twitter.com/username/status/123...
```

### Qualidades Disponíveis:
- Baixa automaticamente na melhor qualidade disponível
- Geralmente HD 720p ou 1080p

### Notas:
- Tweets protegidos não são suportados
- Ambos os domínios (twitter.com e x.com) funcionam
- Vídeos com restrição de idade podem não funcionar

---

## 📘 Facebook
**Status:** ✅ Suportado (Limitado)

### Tipos de Conteúdo:
- ✅ Vídeos públicos
- ✅ Facebook Watch
- ⚠️ Vídeos em páginas (limitado)

### Exemplos de URLs:
```
https://www.facebook.com/watch/?v=1234567890
https://www.facebook.com/username/videos/1234567890
https://fb.watch/ABC123/
```

### Qualidades Disponíveis:
- Baixa automaticamente na melhor qualidade disponível
- Varia entre SD e HD

### Notas:
- Apenas vídeos completamente públicos são suportados
- Vídeos de grupos privados não funcionam
- Pode haver limitações por região

---

## 🤖 Reddit
**Status:** ✅ Totalmente Suportado

### Tipos de Conteúdo:
- ✅ Vídeos em posts
- ✅ Vídeos do v.redd.it
- ✅ GIFs animados

### Exemplos de URLs:
```
https://www.reddit.com/r/subreddit/comments/abc123/title/
https://v.redd.it/abc123xyz
https://old.reddit.com/r/subreddit/comments/...
```

### Qualidades Disponíveis:
- Baixa automaticamente na melhor qualidade disponível
- Geralmente SD 480p ou HD 720p

### Notas:
- Subreddits NSFW funcionam normalmente
- Vídeos hospedados externamente (YouTube, Imgur) redirecionam para suas plataformas

---

## 🚀 Como Usar

### Download Individual:
1. Copie o link completo do post/vídeo
2. Cole no campo de busca
3. Clique em "Buscar"
4. Selecione a qualidade desejada
5. Clique em "Download"

### Download em Lote (Batch):
1. Acesse a aba "Download em Lote"
2. Cole múltiplas URLs (uma por linha)
3. Selecione qualidade e formato padrão
4. Clique em "Adicionar à Fila"
5. Clique em "Iniciar Downloads"

---

## ⚠️ Limitações Gerais

### Restrições de Plataforma:
- ❌ Conteúdo privado ou protegido
- ❌ Vídeos com DRM (proteção de cópia)
- ❌ Transmissões ao vivo em andamento
- ❌ Conteúdo que requer autenticação/login

### Velocidade de Download:
- YouTube: ~7-12 MB/s (limitado pelo servidor)
- Instagram: ~5-15 MB/s
- TikTok: ~10-20 MB/s
- Twitter: ~5-10 MB/s
- Facebook: ~3-8 MB/s
- Reddit: ~5-10 MB/s

### Formatos Disponíveis:
- 🎥 **Vídeo:** MP4 apenas (melhor compatibilidade)
- 🎵 **Áudio:** MP3 apenas (extraído do vídeo)

---

## 🔧 Solução de Problemas

### "Vídeo não encontrado"
- Verifique se o link está completo
- Confirme que o vídeo é público
- Tente acessar o vídeo no navegador primeiro

### "URL não suportada"
- Certifique-se de usar o link correto da plataforma
- Evite links encurtados (bit.ly, etc) - use o link direto
- Verifique se a plataforma está na lista suportada

### Download muito lento
- Isso é normal para YouTube (limitação do servidor)
- Tente baixar em horários de menor tráfego
- Verifique sua conexão com a internet

### "Erro ao processar vídeo"
- O vídeo pode ter restrições regionais
- Tente novamente em alguns minutos
- Verifique se o vídeo ainda existe na plataforma

---

## 📊 Estatísticas de Compatibilidade

| Plataforma | Compatibilidade | Qualidade | Velocidade |
|-----------|-----------------|-----------|------------|
| YouTube   | ⭐⭐⭐⭐⭐ (100%) | Até 4K    | Média      |
| Instagram | ⭐⭐⭐⭐⭐ (100%) | Até 1080p | Boa        |
| TikTok    | ⭐⭐⭐⭐⭐ (100%) | Até 1080p | Excelente  |
| Twitter/X | ⭐⭐⭐⭐⭐ (100%) | Até 1080p | Boa        |
| Facebook  | ⭐⭐⭐⭐ (85%)    | Até 720p  | Média      |
| Reddit    | ⭐⭐⭐⭐⭐ (100%) | Até 720p  | Boa        |

---

## 🆕 Atualizações Futuras

Plataformas em consideração:
- 🔄 Twitch (clips e VODs)
- 🔄 Vimeo
- 🔄 Dailymotion
- 🔄 Spotify (podcasts em vídeo)
- 🔄 LinkedIn (vídeos de posts)

---

## 📝 Notas Legais

Este software é fornecido apenas para uso pessoal. Respeite os direitos autorais e termos de serviço de cada plataforma. Não use este software para:
- Violar direitos autorais
- Redistribuir conteúdo protegido
- Uso comercial sem autorização
- Assédio ou spam

**Use com responsabilidade! 🙏**
