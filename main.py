import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ البوت محدث بأقوى كسر حماية! أرسل الرابط الآن.')

async def download_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text('⏳ أحاول كسر حماية يوتيوب الآن...')
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file_%(id)s.%(ext)s',
        'nocheckcertificate': True,
        'geo_bypass': True,
        'quiet': True,
        # هذه الإضافة تجبر يوتيوب على التعامل مع السيرفر كمتصفح أندرويد قديم (غالباً لا يتم حجبه)
        'user_agent': 'Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/9.2 Chrome/67.0.3396.87 Mobile Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                await update.message.reply_photo(photo=open(filename, 'rb'))
            else:
                await update.message.reply_video(video=open(filename, 'rb'))
        
        if os.path.exists(filename): os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ يوتيوب يقاوم بشدة. جرب رابطاً آخر أو انتظر قليلاً.\n{str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_content))
    application.run_polling()

if __name__ == '__main__': main()
