import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 البوت شغال")

def main():
    if not TOKEN:
        raise ValueError("TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🚀 Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
