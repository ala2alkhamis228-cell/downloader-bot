import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# نجيب التوكن من Render Environment
BOT_TOKEN = os.getenv("'8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'")

# دالة التحميل
def download_media(url):
    ydl_opts = {
        "outtmpl": "download.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_
