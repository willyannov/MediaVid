"""
Script de teste para verificar compatibilidade com plataformas
"""
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.downloader import VideoDownloader
from app.models.video import DownloadRequest

def test_platforms():
    """Testa URLs de todas as plataformas"""
    
    test_urls = [
        ("YouTube Shorts", "https://www.youtube.com/shorts/BNZs70LwTZM"),
        ("Twitter/X", "https://x.com/PatriotaWil/status/1991608603640565794"),
        ("TikTok", "https://www.tiktok.com/@ema_bb0/video/7573877016353639711"),
        ("Instagram Reel", "https://www.instagram.com/reel/DRS52EWjYMA/")
    ]
    
    downloader = VideoDownloader()
    
    print("="*70)
    print("TESTE DE COMPATIBILIDADE DE PLATAFORMAS")
    print("="*70)
    print()
    
    results = []
    
    for platform, url in test_urls:
        print(f"[TESTANDO] {platform}")
        print(f"URL: {url}")
        print("-" * 70)
        
        try:
            # Tenta extrair informações (não faz download)
            info = downloader.get_video_info(url)
            
            if info:
                print(f"[OK] Suportado!")
                print(f"  Titulo: {info.title[:60]}")
                print(f"  Plataforma: {info.platform}")
                print(f"  Duracao: {info.duration}s" if info.duration else "  Duracao: N/A")
                print(f"  Uploader: {info.uploader}" if info.uploader else "  Uploader: N/A")
                print(f"  Formatos disponiveis: {len(info.formats)}")
                results.append((platform, True, "OK"))
            else:
                print(f"[ERRO] Nao foi possivel extrair informacoes")
                results.append((platform, False, "Sem informacoes"))
                
        except Exception as e:
            error_msg = str(e)[:100]
            print(f"[ERRO] {error_msg}")
            results.append((platform, False, error_msg))
        
        print()
    
    # Resumo
    print("="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    for platform, success, message in results:
        status = "[OK]" if success else "[FALHOU]"
        print(f"{status} {platform}: {message}")
    
    print()
    print(f"Taxa de sucesso: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print("="*70)

if __name__ == "__main__":
    test_platforms()
