import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! أرسل لي رابط الفيديو أو الصوت وسأقوم بتحميله لك فوراً. 🚀')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    msg = await update.message.reply_text('⏳ جاري التحميل والمعالجة... انتظر قليلاً.')

    # إعدادات التحميل
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{chat_id}.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # إرسال الفيديو
            await context.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
            
            # حذف الملف بعد الإرسال
            os.remove(filename)
            await msg.delete()

    except Exception as e:
        await msg.edit_text(f'❌ حدث خطأ: {str(e)}')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
