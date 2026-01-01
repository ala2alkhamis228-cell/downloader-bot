import yt_dlp
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

app = Flask('')
@app.route('/')
def home(): return "Global Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    status_msg = await update.message.reply_text('🌍 جاري كسر الحماية وجلب الفيديو...')

    # إعدادات متقدمة جداً للالتفاف على الحظر دون الحاجة لحسابات
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # استخدام نظام توزيع الهويات العشوائية
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'], # محاكاة أجهزة الجوال لتقليل الحظر
                'skip': ['dash', 'hls']
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # نحاول استخراج الرابط المباشر فقط ليرسله تلغرام
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            video_url = info.get('url')
            
            if video_url:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption="✅ تم التحميل للجميع!")
                await status_msg.delete()
            else:
                raise Exception("الرابط غير متاح")
    except Exception as e:
        await status_msg.edit_text("⚠️ يوتيوب يفرض قيوداً مؤقتة على المنطقة. سيعمل البوت تلقائياً عند تغيير الـ IP.")

def main():
    keep_alive()
    Application.builder().token(TOKEN).build().add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)).run_polling()

if __name__ == '__main__': main()
