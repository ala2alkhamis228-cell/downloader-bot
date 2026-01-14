import os
import telebot
from yt_dlp import YoutubeDL

# التوكن الخاص بك
API_TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أنا جاهز! أرسل أي رابط فيديو من أي موقع (TikTok, Instagram, YouTube, FB) وسأحضره لك.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "⏳ جاري محاولة سحب الفيديو من الرابط... انتظرني قليلاً.")
        
        ydl_opts = {
            'format': 'best', # سحب أفضل جودة متاحة
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            # هوية متصفح عالمية لتجاوز حظر جميع المواقع
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # إرسال الفيديو للمستخدم
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                
                # حذف الملف فوراً لتنظيف السيرفر
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            bot.delete_message(message.chat.id, msg.message_id)
                    
        except Exception as e:
            bot.edit_message_text(f"❌ عذراً، هذا الموقع محمي أو الرابط غير مدعوم حالياً.\nالسبب: {str(e)}", message.chat.id, msg.message_id)
            # تنظيف أي بقايا ملفات
            for f in os.listdir():
                if f.endswith((".mp4", ".mkv", ".webm", ".temp", ".jpg", ".png")):
                    os.remove(f)
    else:
        bot.reply_to(message, "⚠️ من فضلك أرسل رابطاً صحيحاً يبدأ بـ http")

bot.polling(none_stop=True)
