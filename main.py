from fastapi import FastAPI, Request
import asyncio
from llm_client import generate_reply
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = '2917659389355495111:rTYTMWCClErpHsAvrIruegPVJkPKTgXTlZnzIuZAkwZUNqoYkJqoNXewDgNkETiw'
bot = Bot(token=TOKEN)

app = FastAPI()

# Cấu hình webhook 1 lần khi chạy lần đầu
@app.on_event("startup")
async def setup_webhook():
    webhook_url = 'https://tombui-agent.ngrok.app/webhook'
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: bot.set_webhook(url=webhook_url, secret_token="ZTEGC8941D33"))

# Hàm xử lý /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Xin chào {update.effective_user.first_name}!")

# Hàm xử lý tin nhắn thường
async def echo(update: Update, context: CallbackContext):
    user_text = update.message.text or ""
    user_locale = getattr(update.effective_user, "language_code", None)
    print("user text:", user_text)
    reply = await generate_reply(user_text=user_text, user_locale=user_locale)
    print("bot reply:", reply)
    await update.message.reply_text(reply)

# Gắn dispatcher và handler
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook endpoint
@app.post('/webhook')
async def webhook(request: Request):
    payload = await request.json()
    update = Update.de_json(payload, bot)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: dispatcher.process_update(update))
    return 'ok'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8443)

