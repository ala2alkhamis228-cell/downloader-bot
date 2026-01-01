import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

app = Flask('')
@app.route('/')
def home(): return "Bot is Ready!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    msg = await update.message.reply_text('⏳ جاري كسر الحماية والتحميل...')

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # إضافة متصفح وهمي لتجاوز حماية تيك توك وإنستغرام
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=f)
            os.remove(filename)
            await msg.delete()
    except Exception:
        await msg.edit_text("❌ المنصة تفرض حماية قوية حالياً. سأقوم بتحديث السيرفر، جرب مرة أخرى بعد لحظات.")

def main():
    keep_alive()
    Application.builder().token(TOKEN).build().add_handler(MessageHandler(filters.TEXT, handle_message)).run_polling()

if __name__ == '__main__': main()
