from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import subprocess

# ضع هنا التوكن مباشرة (فقط للتجربة المحلية)
BOT_TOKEN = "8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 البوت شغّال!\nابعث رابط فيديو أو صوت، وسأقوم بتحميله لك."
    )

# وظيفة تحميل الفيديو/الصوت باستخدام yt-dlp
async def download_media(url: str, media_type: str = "video"):
    output_format = "%(title)s.%(ext)s"
    command = ["yt-dlp", "-o", output_format, url]

    if media_type == "audio":
        command = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_format, url]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

# معالجة أي رسالة تحتوي على رابط
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("http"):
        await update.message.reply_text("⏳ جاري التحميل...")
        # تحميل الفيديو
        stdout, stderr = await download_media(text, media_type="video")
        if stderr:
            await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل:\n{stderr}")
        else:
            await update.message.reply_text("✅ تم التحميل بنجاح! الملف محفوظ على جهازك.")
    else:
        await update.message.reply_text("⚠️ هذا ليس رابطًا صالحًا.")

# إعداد التطبيق
app = ApplicationBuilder().token(BOT_TOKEN).build()

# إضافة Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# تشغيل البوت
if __name__ == "__main__":
    app.run_polling()
