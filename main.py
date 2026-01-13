import os
import telebot
from yt_dlp import YoutubeDL

API_TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت يعمل! أرسل رابط فيديو للتحميل.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "http" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط والتحميل...")
        ydl_opts = {
            'format': 'best',
            'nocheckcertificate': True,
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)
                with open(file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                if os.path.exists(file):
                    os.remove(file)
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")
            # تنظيف أي ملفات عالقة في حال الخطأ
            for f in os.listdir():
                if f.endswith((".mp4", ".mkv", ".webm")):
                    os.remove(f)

bot.polling(none_stop=True)
