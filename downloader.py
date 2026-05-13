from yt_dlp import YoutubeDL
from pathlib import Path
import os

TEMP_DIR = Path("temp")

def download_video(url):
    # Opciones pro para evitar el Error 403
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': str(TEMP_DIR / '%(id)s.%(ext)s'),
        'quiet': True,
        'nocheckcertificate': True,
        # Estas líneas son las que saltan el bloqueo:
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Asegurar extensión mp4
            if not filename.endswith(".mp4"):
                filename = os.path.splitext(filename)[0] + ".mp4"
                
            return {
                "path": filename,
                "title": info.get("title"),
                "duration": info.get("duration")
            }
        except Exception as e:
            # Si falla, lanzamos el error para que app.py lo cachee
            raise Exception(f"YouTube bloqueó la conexión (403). Intenta actualizar yt-dlp. Detalle: {e}")