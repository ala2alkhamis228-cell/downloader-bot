import yt_dlp
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# توكن البوت الخاص بك
TOKEN = '8090192039:AAHYdpeZkKmrRv8hwBHZhqAwYwaqifVHI7k'

# تشغيل السيرفر لإبقاء البوت حياً على Render
app = Flask('')
@app.route('/')
def home(): return "All-in-One Downloader is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 مرحباً بك في بوت التحميل الشامل!\n\n"
        "يمكنني التحميل من: يوتيوب، تيك توك، إنستغرام، وتويتر.\n"
        "دعم كامل لـ: الفيديوهات، الصور، والمقاطع الصوتية MP3.\n"
        "فقط أرسل الرابط وابدأ التحميل!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith('http'): return

    # عرض أزرار الاختيار للمستخدم
    keyboard = [[
        InlineKeyboardButton("🎬 فيديو / صور", callback_data=f"vid|{url}"),
        InlineKeyboardButton("🎵 مقطع صوتي MP3", callback_data=f"aud|{url}")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('إختر ماذا تريد تحميله من الرابط:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('|')
    action, url = data[0], data[1]
    chat_id = query.message.chat_id
    msg = await query.edit_message_text('⏳ جاري استخراج المحتوى... يرجى الانتظار.')

    # إعدادات احترافية لفتح جميع المنصات وتجاوز الحظر
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 1. معالجة الصور (تيك توك Slideshow أو بوستات إنستغرام الصور)
            if action == "vid" and (not info.get('formats') or 'entries' in info):
                entries = info.get('entries', [info])
                media_group = []
                for entry in entries:
                    if entry.get('url'):
                        media_group.append(InputMediaPhoto(entry['url']))
                
                if media_group:
                    await context.bot.send_media_group(chat_id=chat_id, media=media_group[:10])
                    await msg.delete()
                    return

            # 2. إعدادات جودة الفيديو أو تحويل الصوت
            if action == "vid":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            else:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            # التحميل الفعلي للملف
            ydl_opts['outtmpl'] = f'file_{chat_id}.%(ext)s'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                down_info = ydl_down.extract_info(url, download=True)
                filename = ydl_down.prepare_filename(down_info)
                
                # تصحيح امتداد الملف في حال كان صوتاً
                if action == "aud" and not filename.endswith('.mp3'):
                    filename = os.path.splitext(filename)[0] + '.mp3'
                
                with open(filename, 'rb') as f:
                    if action == "vid":
                        await context.bot.send_video(chat_id=chat_id, video=f)
                    else:
                        await context.bot.send_audio(chat_id=chat_id, audio=f)
                
                os.remove(filename) # حذف الملف بعد الإرسال لتوفير المساحة
                await msg.delete()

    except Exception as e:
        # رسالة خطأ ذكية بدون تحديد اسم منصة معينة لتجنب الارتباك
        await msg.edit_text(f"❌ عذراً، تعذر تحميل هذا الرابط حالياً. قد يكون المحتوى خاصاً أو السيرفر مضغوط.")

def main():
    keep_alive()
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.add_handler(CallbackQueryHandler(button))
    bot_app.run_polling()

if __name__ == '__main__':
    main()
