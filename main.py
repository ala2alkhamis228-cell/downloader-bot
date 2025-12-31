import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# توكن البوت الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🚀 أهلاً بك! أرسل لي أي رابط (YouTube, TikTok, Instagram) وسأقوم بتحميله لك.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # عرض أزرار الاختيار للمستخدم لضمان تحميل الصوت أو الفيديو
    keyboard = [[
        InlineKeyboardButton("🎬 فيديو/صور", callback_data=f"vid|{url}"),
        InlineKeyboardButton("🎵 صوت MP3", callback_data=f"aud|{url}")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('إختر ماذا تريد استخراجه من الرابط:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('|')
    action, url = data[0], data[1]
    chat_id = query.message.chat_id
    msg = await query.edit_message_text('⏳ جاري المعالجة... يرجى الانتظار.')

    # إعدادات متقدمة جداً لتجاوز حظر إنستغرام
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.instagram.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 1. معالجة صور تيك توك وإنستغرام (Slideshow/Posts)
            if action == "vid" and ('entries' in info or not info.get('formats')):
                entries = info.get('entries', [info])
                photos = [InputMediaPhoto(e['url']) for e in entries if e.get('url')]
                if photos:
                    await context.bot.send_media_group(chat_id=chat_id, media=photos[:10])
                    await msg.delete()
                    return

            # 2. إعدادات تحميل الفيديو أو الصوت
            if action == "vid":
                ydl_opts['format'] = 'best'
            else:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
            
            ydl_opts['outtmpl'] = f'file_{chat_id}.%(ext)s'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                info_dict = ydl_down.extract_info(url, download=True)
                filename = ydl_down.prepare_filename(info_dict)
                if action == "aud" and not filename.endswith('.mp3'):
                    filename = os.path.splitext(filename)[0] + '.mp3'
                
                with open(filename, 'rb') as f:
                    if action == "vid": await context.bot.send_video(chat_id=chat_id, video=f)
                    else: await context.bot.send_audio(chat_id=chat_id, audio=f)
                os.remove(filename)
                await msg.delete()

    except Exception as e:
        await msg.edit_text(f'❌ فشل التحميل. إنستغرام يفرض حماية قوية حالياً. جرب رابطاً آخر.')

def main():
    keep_alive()
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.add_handler(CallbackQueryHandler(button))
    bot_app.run_polling()

if __name__ == '__main__':
    main()
