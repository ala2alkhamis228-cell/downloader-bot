import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# توكن البوت
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

app = Flask('')
@app.route('/')
def home(): return "Global Downloader is Active!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🚀 أهلاً بك في بوت التحميل العالمي!\nأرسل أي رابط من (يوتيوب، تيك توك، إنستغرام، تويتر) وسأقوم بالتحميل فوراً.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith('http'): return
    keyboard = [[
        InlineKeyboardButton("🎬 فيديو / صور", callback_data=f"vid|{url}"),
        InlineKeyboardButton("🎵 صوت MP3", callback_data=f"aud|{url}")
    ]]
    await update.message.reply_text('إختر الصيغة المطلوبة:', reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('|')
    action, url = data[0], data[1]
    msg = await query.edit_message_text('⏳ جاري كسر القيود وتحميل المحتوى...')

    # إعدادات احترافية لمحاكاة متصفح حقيقي وتجاوز الحظر
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # معالجة الصور (تيك توك أو بوستات إنستغرام)
            if action == "vid" and ('entries' in info or not info.get('formats')):
                entries = info.get('entries', [info])
                media = [InputMediaPhoto(e['url']) for e in entries if e.get('url')]
                if media:
                    await context.bot.send_media_group(chat_id=query.message.chat_id, media=media[:10])
                    await msg.delete()
                    return

            # إعدادات التحميل (فيديو أو صوت)
            ydl_opts['format'] = 'best' if action == "vid" else 'bestaudio/best'
            if action == "aud":
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
            
            ydl_opts['outtmpl'] = f'file_{query.message.chat_id}.%(ext)s'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                down_info = ydl_down.extract_info(url, download=True)
                path = ydl_down.prepare_filename(down_info)
                if action == "aud" and not path.endswith('.mp3'): path = os.path.splitext(path)[0] + '.mp3'
                
                with open(path, 'rb') as f:
                    if action == "vid": await context.bot.send_video(chat_id=query.message.chat_id, video=f)
                    else: await context.bot.send_audio(chat_id=query.message.chat_id, audio=f)
                
                os.remove(path)
                await msg.delete()

    except Exception:
        await msg.edit_text('❌ فشل التحميل. المنصة تفرض حماية قوية على هذا الرابط حالياً. جرب رابطاً آخر.')

def main():
    keep_alive()
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.run_polling()

if __name__ == '__main__': main()
