import os
from telegram.ext import Updater, CommandHandler
from price import get_price

TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("سلام! برای گرفتن قیمت، بنویس: /price btc")

def price(update, context):
    if context.args:
        symbol = context.args[0].lower()
        price, change = get_price(symbol)
        if price:
            update.message.reply_text(f"💰 قیمت {symbol.upper()}: ${price}\n📉 تغییرات ۲۴ساعته: {change}%")
        else:
            update.message.reply_text("ارز پیدا نشد یا مشکلی در دریافت اطلاعات بود.")
    else:
        update.message.reply_text("مثال: /price btc")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", price))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
