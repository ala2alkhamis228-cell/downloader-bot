import os
import telebot
from yt_dlp import YoutubeDL

# تأكد من إضافة API_TOKEN في إعدادات Render (Environment Variables)
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت جاهز! أرسل رابط فيديو للتحميل.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "http" in url:
        bot.reply_to(message, "جاري التحميل...")
        ydl_opts = {
            'format': 'best',
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)
                with open(file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                os.remove(file)
        except Exception as e:
            bot.reply_to(message, f"خطأ: {str(e)}")

bot.polling(none_stop=True)
