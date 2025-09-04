from zalo_bot import Update
from zalo_bot.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from llm_client import generate_reply

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Chào {update.effective_user.display_name}! Tôi là TomBui AI!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    user_locale = getattr(update.effective_user, "language_code", None)
    reply = await generate_reply(user_text=user_text, user_locale=user_locale)
    print("user text:", user_text)
    print("bot reply:", reply)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token("2917659389355495111:rTYTMWCClErpHsAvrIruegPVJkPKTgXTlZnzIuZAkwZUNqoYkJqoNXewDgNkETiw").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot đang chạy...")
    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("Bot đã dừng lại.")