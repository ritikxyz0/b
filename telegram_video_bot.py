from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os


def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = ydl.prepare_filename(info_dict)
    return video_title


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me any YouTube, Instagram, or Facebook Link and I'll send you the video! 📥\n\n"
        "👨‍💻 Developer: ritikxyz\n"
        "📲 Telegram: @RitikXyz099"
    )


async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("👨‍💻 Developer: @RitikXyz099")
    await update.message.reply_text("Downloading... ⏳")

    try:
        file_path = download_video(url)
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")


TOKEN = "7647515503:AAGS7t15F-BC-JewX6EcnpuBK2z-YOYGwP8"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links))

print("Bot is running... ✅")
app.run_polling()
