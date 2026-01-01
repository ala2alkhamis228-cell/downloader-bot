import yt_dlp
import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

# نظام Keep Alive لضمان استمرار عمل السيرفر على Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Online in Frankfurt!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    status_msg = await update.message.reply_text('🛡️ جاري كسر الحماية والتحميل من سيرفر ألمانيا...')

    # إعدادات متطورة لتجاوز حظر الـ IP ورسائل التحقق
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # هوية متصفح أندرويد حقيقية لتجاوز الحظر
        'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        'nocheckcertificate': True,
        'outtmpl': f'video_{update.effective_chat.id}.%(ext)s',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج البيانات وتحميل الملف
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            filename = ydl.prepare_filename(info)
            
            # إرسال الفيديو للمستخدم في تلغرام
            with open(filename, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id, 
                    video=video_file,
                    caption="✅ تم التحميل بنجاح من المنطقة الجديدة!"
                )
            
            # حذف الملف من السيرفر لتوفير المساحة
            if os.path.exists(filename): os.remove(filename)
            await status_msg.delete()

    except Exception as e:
        # إظهار رسالة خطأ واضحة في حال وجود حماية مشددة
        error_text = str(e)
        if "confirm you're not a bot" in error_text.lower():
            await status_msg.edit_text("❌ يوتيوب لا يزال يكتشف السيرفر. جرب رابطاً من منصة أخرى أو انتظر قليلاً.")
        else:
            await status_msg.edit_text(f"❌ عذراً، حدث خطأ: {error_text[:50]}...")

def main():
    keep_alive()
    # بناء تطبيق التلغرام
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
