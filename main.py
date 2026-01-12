import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k"

# الخيارات الجديدة لحل مشكلة يوتيوب
ydl_opts = {
    'outtmpl': '/app/downloads/%(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'quiet': False,  # خليناه False عشان نشوف الخطأ بوضوح لو صار شي
    'cookiefile': 'cookies.txt',  # السطر اللي طلبه يوتيوب في صورتك (0b4f)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

os.makedirs("/app/downloads", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! أنا شغال الآن.. أرسل لي أي رابط.")

async def download_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("جاري التحميل... ⏳")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # إرسال الملف
        with open(filename, 'rb') as f:
            if filename.endswith(('.mp4', '.mkv', '.webm')):
                await update.message.reply_video(video=f)
            elif filename.endswith(('.mp3', '.m4a', '.wav')):
                await update.message.reply_audio(audio=f)
            else:
                await update.message.reply_document(document=f)

        await msg.edit_text("تم التحميل ✅")
        os.remove(filename) # مسح الملف بعد الإرسال لتوفير مساحة السيرفر

    except Exception as e:
        await msg.edit_text(f"فشل التحميل ❌\n تأكد من رفع ملف cookies.txt في GitHub")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_link))

print("بوت شغال...")
app.run_polling()
