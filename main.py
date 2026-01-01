import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# توكن البوت الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ البوت جاهز للعمل!\nأرسل لي أي رابط (فيديو أو صورة) وسأقوم بتحميله فوراً.')

async def download_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text('⏳ جاري التحميل... انتظر لحظة.')
    
    # أقوى إعدادات لكسر حظر يوتيوب وتيك توك ودعم الصور
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file_%(id)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'writethumbnail': True, # يدعم سحب الصور
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # إرسال المحتوى حسب نوعه (صورة أو فيديو)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                await update.message.reply_photo(photo=open(filename, 'rb'), caption='📸 تم تحميل الصورة!')
            else:
                await update.message.reply_video(video=open(filename, 'rb'), caption='🎬 تم تحميل الفيديو!')
        
        if os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f'❌ فشل التحميل. تأكد أن الرابط عام.\nالخطأ: {str(e)}')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_content))
    application.run_polling()

if __name__ == '__main__':
    main()
