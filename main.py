import yt_dlp
import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    status_msg = await update.message.reply_text('⚙️ جاري المعالجة... انتظر ثواني.')

    # إعدادات مبسطة جداً لضمان النجاح بدون تعقيد
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': f'vid_{update.effective_chat.id}.mp4',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # التحميل الفعلي للملف على السيرفر
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            filename = ydl.prepare_filename(info)
            
            # إرسال الفيديو للمستخدم
            with open(filename, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id, 
                    video=video_file, 
                    caption="✅ تم التحميل بنجاح!"
                )
            
            # تنظيف السيرفر
            if os.path.exists(filename): os.remove(filename)
            await status_msg.delete()

    except Exception as e:
        # إرسال سبب الفشل الحقيقي لنفهمه
        await status_msg.edit_text(f"❌ خطأ تقني: {str(e)[:100]}")

def main():
    keep_alive()
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

if __name__ == '__main__': main()
