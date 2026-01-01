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
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    status_msg = await update.message.reply_text('🕵️ جاري محاولة كسر الحماية...')

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # استخدام هوية متصفح أندرويد حقيقية لتجنب رسالة "Confirm you are not a bot"
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as f:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=f)
            os.remove(filename)
            await status_msg.delete()
    except Exception as e:
        # إذا استمر الحظر، سنخبر المستخدم أن السيرفر يحتاج "استراحة"
        await status_msg.edit_text("⚠️ المنصة لا تزال تحظر السيرفر. سأحاول تغيير الهوية، جرب رابطاً آخر بعد قليل.")

def main():
    keep_alive()
    Application.builder().token(TOKEN).build().add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)).run_polling()

if __name__ == '__main__': main()
