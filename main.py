import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update, InputMediaPhoto
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
    msg = await update.message.reply_text('⏳ جاري جلب المحتوى (فيديو أو صور)...')

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # حالة صور تيك توك (Slideshow)
            if 'entries' in info or (not info.get('url') and info.get('thumbnails')):
                media = []
                # جلب أول 10 صور فقط لتجنب تعليق البوت
                images = info.get('entries', [info])[0].get('requested_formats', [])
                if not images: # محاولة بديلة لصور تيك توك
                    images = info.get('thumbnails', [])
                
                for img in images[:10]:
                    if img.get('url'):
                        media.append(InputMediaPhoto(img['url']))
                
                if media:
                    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
                    await msg.delete()
                    return

            # حالة الفيديو العادي
            ydl_opts['format'] = 'best'
            ydl_opts['outtmpl'] = f'file_{update.effective_chat.id}.%(ext)s'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                down_info = ydl_down.extract_info(url, download=True)
                filename = ydl_down.prepare_filename(down_info)
                with open(filename, 'rb') as f:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=f)
                os.remove(filename)
                await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ عذراً، هذا الرابط محمي أو يحتوي على صور لا يمكن معالجتها حالياً.")

def main():
    keep_alive()
    Application.builder().token(TOKEN).build().add_handler(MessageHandler(filters.TEXT, handle_message)).run_polling()

if __name__ == '__main__': main()
