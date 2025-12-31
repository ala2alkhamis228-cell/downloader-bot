import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

# كود لإبقاء البوت حياً على الخطة المجانية
app = Flask('')
@app.route('/')
def home():
    return "البوت يعمل!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! أرسل لي الرابط وسأقوم بالتحميل.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    msg = await update.message.reply_text('⏳ جاري التحميل...')
    ydl_opts = {'format': 'best', 'outtmpl': f'video_{chat_id}.%(ext)s'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as video:
                await context.bot.send_video(chat_id=chat_id, video=video)
            os.remove(filename)
    except Exception as e:
        await msg.edit_text(f'❌ خطأ: {str(e)}')

def main():
    keep_alive() # تشغيل السيرفر الوهمي
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    bot_app.run_polling()

if __name__ == '__main__':
    main()
