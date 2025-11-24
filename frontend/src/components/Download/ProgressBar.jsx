import { useState, useEffect, useRef } from 'react';

export default function ProgressBar({ clientId, onComplete, onError }) {
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [message, setMessage] = useState('');
  const [isVisible, setIsVisible] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!clientId) return;

    // Conecta ao WebSocket
    const ws = new WebSocket(`ws://localhost:8000/ws/progress/${clientId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket conectado');
      setIsVisible(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Progresso recebido:', data);

        setStage(data.stage);
        setProgress(data.progress);
        setMessage(data.message);

        // Se completou
        if (data.stage === 'complete') {
          setTimeout(() => {
            setIsVisible(false);
            if (onComplete) onComplete();
          }, 1000);
        }

        // Se deu erro
        if (data.stage === 'error') {
          setTimeout(() => {
            setIsVisible(false);
            if (onError) onError(data.message);
          }, 2000);
        }
      } catch (error) {
        console.error('Erro ao processar mensagem WebSocket:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('Erro no WebSocket:', error);
      setIsVisible(false);
    };

    ws.onclose = () => {
      console.log('WebSocket desconectado');
    };

    // Cleanup
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [clientId, onComplete, onError]);

  if (!isVisible) return null;

  // Mapeia estágios para cores
  const getStageColor = () => {
    switch (stage) {
      case 'starting':
        return 'bg-blue-500';
      case 'downloading':
        return 'bg-blue-600';
      case 'complete':
        return 'bg-green-600';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-primary-500';
    }
  };

  const getStageLabel = () => {
    switch (stage) {
      case 'starting':
        return 'Preparando...';
      case 'downloading':
        return 'Baixando';
      case 'complete':
        return 'Pronto!';
      case 'error':
        return 'Erro';
      default:
        return 'Conectando...';
    }
  };

  return (
    <div className="fixed bottom-4 right-4 w-96 bg-white dark:bg-gray-800 rounded-lg shadow-2xl p-4 border border-gray-200 dark:border-gray-700 z-50">
      <div className="mb-2">
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
            {getStageLabel()}
          </span>
          <span className="text-sm font-bold text-primary-600 dark:text-primary-400">
            {progress}%
          </span>
        </div>
        
        {/* Barra de progresso */}
        <div className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            className={`h-full ${getStageColor()} transition-all duration-300 ease-out rounded-full`}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Mensagem detalhada */}
      <p className="text-xs text-gray-600 dark:text-gray-400 mt-2 truncate">
        {message}
      </p>
    </div>
  );
}
