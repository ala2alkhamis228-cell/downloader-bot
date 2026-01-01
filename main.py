import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k"

ydl_opts = {
    'outtmpl': '/app/downloads/%(title)s.%(ext)s',  # مجلد الحفظ داخل الحاوية
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'quiet': True,
}

os.makedirs("/app/downloads", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! أرسل لي أي رابط فيديو، صوت، أو صورة من أي منصة.")

async def download_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("جاري التحميل... ⏳")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # إرسال الملف إلى المستخدم
        if filename.endswith(('.mp4', '.mkv', '.webm')):
            await update.message.reply_video(video=open(filename, 'rb'))
        elif filename.endswith(('.mp3', '.m4a', '.wav')):
            await update.message.reply_audio(audio=open(filename, 'rb'))
        else:
            await update.message.reply_document(document=open(filename, 'rb'))

        await msg.edit_text("تم التحميل ✅")

    except Exception as e:
        await msg.edit_text(f"فشل التحميل ❌\n{str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_link))

print("بوت شغال...")
app.run_polling()
