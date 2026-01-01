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
def home(): return "Bot is Online & Ready!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    msg = await update.message.reply_text('🚀 جاري اختراق حماية المنصة والتحميل...')

    # إعدادات متطورة جداً لتجاوز الحظر
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language: en-US,en;q=0.5',
        ],
        'outtmpl': f'video_{update.effective_chat.id}.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # محاولة الاستخراج مع "صبر" قليل
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=f, caption="✅ تم بنجاح!")
            
            os.remove(filename)
            await msg.delete()
    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text("❌ المنصة شددت الحماية. جرب رابطاً آخر أو انتظر قليلاً.")

def main():
    keep_alive()
    Application.builder().token(TOKEN).read_timeout(30).write_timeout(30).build().add_handler(MessageHandler(filters.TEXT, handle_message)).run_polling()

if __name__ == '__main__': main()
