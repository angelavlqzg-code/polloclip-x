from yt_dlp import YoutubeDL
from pathlib import Path
import subprocess
import tempfile
import os

TEMP_DIR = Path("temp")
COOKIES_FILE = Path(tempfile.gettempdir()) / "polloclip" / "yt_cookies.txt"

def get_node_path():
    for p in ['/usr/bin/nodejs', '/usr/local/bin/nodejs', '/usr/bin/node']:
        if Path(p).exists():
            return p
    r = subprocess.run(['which', 'nodejs'], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

NODE_PATH = get_node_path()

def get_ydl_opts(extra={}):
    opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': str(TEMP_DIR / '%(id)s.%(ext)s'),
        'quiet': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    if NODE_PATH:
        opts['js_runtimes'] = {'node': {'path': NODE_PATH}}
    if COOKIES_FILE.exists():
        opts['cookiefile'] = str(COOKIES_FILE)
    opts.update(extra)
    return opts

def save_cookies(cookie_bytes):
    """Guarda cookies desde el uploader de Streamlit."""
    COOKIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOKIES_FILE.write_bytes(cookie_bytes)

def cookies_loaded():
    return COOKIES_FILE.exists()

def download_video(url):
    TEMP_DIR.mkdir(exist_ok=True)
    with YoutubeDL(get_ydl_opts()) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename = os.path.splitext(filename)[0] + ".mp4"
            return {
                "path": filename,
                "title": info.get("title"),
                "duration": info.get("duration")
            }
        except Exception as e:
            raise Exception(f"YouTube bloqueó la conexión (403). Sube tu cookies.txt para continuar. Detalle: {e}")
