# 🔧 Configuração de Variáveis de Ambiente no Render

## Importante: Configurar API_URL

Para que as thumbnails dos vídeos funcionem corretamente em produção, você precisa adicionar a variável de ambiente `API_URL` no Render.

### Passo a passo:

1. Acesse o [Dashboard do Render](https://dashboard.render.com)

2. Selecione o serviço **backend** (mediavid-0bvc ou similar)

3. Clique em **Environment** no menu lateral

4. Clique em **Add Environment Variable**

5. Adicione a seguinte variável:
   - **Key:** `API_URL`
   - **Value:** `https://mediavid-0bvc.onrender.com`
   
   ⚠️ **Importante:** Use a URL do seu backend no Render (sem barra no final)

6. Clique em **Save Changes**

7. O Render irá automaticamente fazer o redeploy do serviço

### Por que isso é necessário?

O sistema usa um proxy para carregar thumbnails de vídeos e evitar problemas de CORS (Cross-Origin Resource Sharing). Em desenvolvimento, usa `http://localhost:8000`, mas em produção precisa da URL real do backend.

### Como verificar se está funcionando:

Após o deploy, cole um link de qualquer plataforma (Instagram, TikTok, Twitter, etc.) e verifique se a thumbnail do vídeo aparece corretamente.

### Outras variáveis de ambiente importantes:

- `DEBUG=False` (já configurado)
- `ALLOWED_ORIGINS` (já configurado com os domínios corretos)
- `YOUTUBE_COOKIES` (opcional, para melhorar extração do YouTube)

---

**Última atualização:** 29/11/2025
