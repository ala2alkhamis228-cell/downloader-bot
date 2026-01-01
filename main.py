import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    status_msg = await update.message.reply_text('🌍 جاري جلب الفيديو عبر السيرفر الجديد...')
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            video_url = info.get('url')
            if video_url:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption="✅ تم التحميل بنجاح!")
                await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text("⚠️ الرابط محمي حالياً، سأحاول بطريقة أخرى.")

def main():
    Application.builder().token(TOKEN).build().run_polling()

if __name__ == '__main__': main()
