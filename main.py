import os
import telebot
from yt_dlp import YoutubeDL

# حط توكن البوت تبعك هون
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو من يوتيوب أو إنستغرام لتحميله.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url:
        bot.reply_to(message, "جاري معالجة الرابط، انتظر قليلاً...")
        
        # إعدادات التحميل الذكية لتجنب الحظر وبدون حسابات شخصية
        ydl_opts = {
            'format': 'best',
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                with open(filename, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                
                # حذف الملف بعد الإرسال لتوفير المساحة
                os.remove(filename)
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء التحميل: {str(e)}")
    else:
        bot.reply_to(message, "عذراً، هذا الرابط غير مدعوم.")

# تشغيل البوت
if __name__ == "__main__":
    bot.polling(none_stop=True)
