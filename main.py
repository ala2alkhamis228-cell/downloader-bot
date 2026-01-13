import os
import telebot
from yt_dlp import YoutubeDL

# التوكن الخاص بك
API_TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت متصل الآن! أرسل لي رابط فيديو من Instagram أو YouTube.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "http" in url:
        # إشعار المستخدم ببدء العمل
        msg = bot.reply_to(message, "⏳ جاري محاولة جلب الفيديو من إنستغرام... قد يستغرق ذلك دقيقة.")
        
        ydl_opts = {
            'format': 'best',
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            # هوية متصفح حديثة جداً لتجاوز حماية إنستغرام
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'add_header': 'Accept-Language: en-US,en;q=0.9',
            'referer': 'https://www.instagram.com/',
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                
                # حذف الملف بعد الإرسال
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
        except Exception as e:
            bot.edit_message_text(f"❌ عذراً، لم أتمكن من تحميل هذا الفيديو.\nالسبب: {str(e)}", message.chat.id, msg.message_id)
            # تنظيف الملفات المؤقتة
            for f in os.listdir():
                if f.endswith((".mp4", ".mkv", ".webm", ".temp")):
                    os.remove(f)
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط صحيح.")

bot.polling(none_stop=True)
