// Keep-alive service para prevenir hibernação do backend no Render
// Faz ping a cada 10 minutos (Render hiberna após 15min de inatividade)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const PING_INTERVAL = 10 * 60 * 1000; // 10 minutos

class KeepAliveService {
  constructor() {
    this.intervalId = null;
    this.isRunning = false;
  }

  start() {
    if (this.isRunning) return;
    
    console.log('🟢 Keep-alive iniciado - Ping a cada 10 minutos');
    
    // Ping imediato
    this.ping();
    
    // Configura intervalo
    this.intervalId = setInterval(() => {
      this.ping();
    }, PING_INTERVAL);
    
    this.isRunning = true;
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.isRunning = false;
      console.log('🔴 Keep-alive parado');
    }
  }

  async ping() {
    try {
      const response = await fetch(`${API_URL}/api/health/ping`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`✅ Ping bem-sucedido - Uptime: ${data.uptime_seconds}s`);
      } else {
        console.warn('⚠️ Ping retornou status', response.status);
      }
    } catch (error) {
      console.error('❌ Erro no ping keep-alive:', error.message);
    }
  }
}

// Exporta instância única
export const keepAlive = new KeepAliveService();

// Auto-start quando importado
if (import.meta.env.PROD) {
  // Apenas em produção
  keepAlive.start();
}

export default keepAlive;
