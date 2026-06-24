from telegram.ext import ApplicationBuilder,ContextTypes, MessageHandler, filters
from telegram import Update
from transcriber import transcribe 
from extractor import extract
import os
from dotenv import load_dotenv
from database import init_db, save_call

load_dotenv()
init_db()
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice=update.message.voice
    file = await context.bot.get_file(voice.file_id)

    file_path = f"voice_{update.message.message_id}.ogg"
    await file.download_to_drive(file_path)
    await update.message.reply_text(
        f"Voice message saved as {file_path}. In progressing...") 
    transcript = transcribe(file_path)
    os.remove(file_path)

    data = extract (transcript)
    save_call(data)
    await update.message.reply_text(
        f"Transcript: {transcript}\n\n"
        f"📋 Extracted:\n"
        f"📅 Date: {data['date']}\n"
        f"👤 Customer: {data['customer_id']}\n"
        f"👤 Customer Phone: {data['customer_phone']}\n"
        f"📊 Status: {data['status']}\n"
        f"📝 Note: {data['note']}"
    )
    await update.message.reply_text(
        f"✅ Đã lưu cuộc gọi:\n"
        f"📅 Date: {data['date']}\n"
        f"👤 Customer: {data['customer_id']}\n"
        f"👤 Customer Phone: {data['customer_phone']}\n"
        f"📊 Status: {data['status']}\n"
        f"📝 Note: {data['note']}"
    )


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    file = await context.bot.get_file(audio.file_id)

    file_path = f"audio_{update.message.message_id}.ogg"
    await file.download_to_drive(file_path)
    await update.message.reply_text(
        f"Voice message saved as {file_path}. In progressing...") 
    transcript = transcribe(file_path)
    os.remove(file_path)

    data = extract (transcript)
    save_call(data)
    await update.message.reply_text(
        f"Transcript: {transcript}\n\n"
        f"📋 Extracted:\n"
        f"📅 Date: {data['date']}\n"
        f"👤 Customer: {data['customer_id']}\n"
        f"👤 Customer Phone: {data['customer_phone']}\n"
        f"📊 Status: {data['status']}\n"
        f"📝 Note: {data['note']}"
    )
    await update.message.reply_text(
        f"✅ Đã lưu cuộc gọi:\n"
        f"📅 Date: {data['date']}\n"
        f"👤 Customer: {data['customer_id']}\n"
        f"👤 Customer Phone: {data['customer_phone']}\n"
        f"📊 Status: {data['status']}\n"
        f"📝 Note: {data['note']}"
    )

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.AUDIO | filters.Document.MP3, handle_audio))
print("Bot started OK")
app.run_polling()

