import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# ضع توكن البوت الخاص بك هنا
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! أرسل لي أي رابط من يوتيوب، تيك توك، فيسبوك، أو إنستغرام وسأقوم بتحميله لك فوراً.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text('جاري المعالجة وتحميل الفيديو... انتظر لحظة.')
    
    # إعدادات متقدمة لتجاوز حظر يوتيوب وتيك توك
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            await update.message.reply_video(video=video, caption='تم التحميل بنجاح بواسطة بوتك الخاص!')
        
        os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f'عذراً، حدث خطأ أثناء التحميل. تأكد من أن الرابط عام وليس خاص.\nالخطأ: {str(e)}')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling()

if __name__ == '__main__':
    main()
