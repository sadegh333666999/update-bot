import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from price import get_price

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.lower()
    price, change = get_price(symbol)
    if price:
        await update.message.reply_text(f"💰 {symbol.upper()}\nPrice: ${price}\n24h Change: {change}%")
    else:
        await update.message.reply_text("❌ ارز مورد نظر یافت نشد.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
