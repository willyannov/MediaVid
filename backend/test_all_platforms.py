"""
Script para testar todas as plataformas suportadas
"""
import sys
import traceback
from app.services.downloader import VideoDownloader

# URLs de teste (vídeos públicos conhecidos)
TEST_URLS = {
    'YouTube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Never Gonna Give You Up
    'YouTube Shorts': 'https://www.youtube.com/shorts/jfKfPfyJRdk',  # lofi beats
    'Instagram': 'https://www.instagram.com/p/CxOWiQNgwq7/',  # Post público (não reel)
    'TikTok': 'https://www.tiktok.com/@scout2015/video/6718335390845095173',
    'Twitter': 'https://x.com/SpaceX/status/1734990643683647488',  # SpaceX video tweet
    'Facebook': 'https://www.facebook.com/watch/?v=10155278547321729',
    'Reddit': 'https://www.reddit.com/r/videos/comments/6orunj/dogs_reaction_to_magic_trick/',
}

def test_platform(platform_name: str, url: str, downloader: VideoDownloader):
    """Testa uma plataforma específica"""
    print(f"\n{'='*60}")
    print(f"🧪 Testando: {platform_name}")
    print(f"📎 URL: {url}")
    print(f"{'='*60}")
    
    try:
        video_info = downloader.get_video_info(url)
        
        # Exibe informações do vídeo
        print(f"✅ SUCESSO - {platform_name}")
        print(f"   📺 Título: {video_info.title[:50]}...")
        print(f"   👤 Uploader: {video_info.uploader}")
        print(f"   ⏱️  Duração: {video_info.duration}s" if video_info.duration else "   ⏱️  Duração: N/A")
        print(f"   👁️  Views: {video_info.view_count:,}" if video_info.view_count else "   👁️  Views: N/A")
        print(f"   🎬 Formatos disponíveis: {len(video_info.formats)}")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FALHOU - {platform_name}")
        print(f"   Erro: {error_msg[:200]}")
        
        # Mostra traceback completo apenas se necessário
        if '--verbose' in sys.argv:
            print("\nTraceback completo:")
            traceback.print_exc()
        
        return False

def main():
    print("🚀 Iniciando testes de todas as plataformas...")
    print("=" * 60)
    
    downloader = VideoDownloader()
    results = {}
    
    for platform, url in TEST_URLS.items():
        results[platform] = test_platform(platform, url, downloader)
    
    # Resume dos resultados
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for platform, success in results.items():
        status = "✅ FUNCIONANDO" if success else "❌ COM PROBLEMA"
        print(f"{status:20} - {platform}")
    
    print(f"\n{'='*60}")
    print(f"Total: {success_count}/{total_count} plataformas funcionando")
    print(f"Taxa de sucesso: {(success_count/total_count)*100:.1f}%")
    print(f"{'='*60}")
    
    # Retorna código de saída baseado nos resultados
    return 0 if success_count == total_count else 1

if __name__ == '__main__':
    sys.exit(main())
