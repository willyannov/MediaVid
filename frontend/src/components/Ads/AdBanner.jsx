import { useEffect } from 'react';

export default function AdBanner({ 
  slot, 
  format = 'auto', 
  responsive = true,
  style = { display: 'block' }
}) {
  useEffect(() => {
    try {
      // Carregar anúncio após o componente montar
      if (window.adsbygoogle && window.adsbygoogle.loaded) {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    } catch (err) {
      console.error('AdSense error:', err);
    }
  }, []);

  return (
    <div className="ad-container my-6 flex justify-center">
      <ins 
        className="adsbygoogle"
        style={style}
        data-ad-client="ca-pub-1347935959137358"
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive={responsive.toString()}
      />
    </div>
  );
}
