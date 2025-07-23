import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def get_price(symbol):
    symbol = symbol.lower()

    # بررسی دستی ECG
    if symbol == "ecg":
        coin_id = "ecg-token"
    else:
        try:
            coins = requests.get("https://api.coingecko.com/api/v3/coins/list").json()
            match = next((c for c in coins if c["symbol"] == symbol), None)
            if not match:
                return "❌ نماد ارز یافت نشد. لطفاً با دقت وارد کنید. مثال: btc, eth, sol"
            coin_id = match["id"]
        except:
            return "⚠️ خطا در اتصال به سرور CoinGecko. لطفاً دوباره تلاش کنید."

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        res = requests.get(url).json()
        name = res["name"]
        price = res["market_data"]["current_price"]["usd"]
        change = res["market_data"]["price_change_percentage_24h"]
        high = res["market_data"]["high_24h"]["usd"]
        low = res["market_data"]["low_24h"]["usd"]
        chart = f"https://www.coingecko.com/en/coins/{coin_id}"

        return f"""💰 {name} ({symbol.upper()})
🔹 قیمت: ${price:,.2f}
📈 ۲۴ساعته: {change:.2f}%
🔺 بیشترین: ${high:,.2f}
🔻 کمترین: ${low:,.2f}
📊 چارت: {chart}"""
    except:
        return "❌ دریافت اطلاعات با خطا مواجه شد."

def price_command(update: Update, context: CallbackContext):
    if context.args:
        symbol = context.args[0]
        update.message.reply_text(get_price(symbol))
    else:
        update.message.reply_text("❗️ لطفاً نماد ارز را وارد کنید. مثال: /price btc")

def handle_message(update: Update, context: CallbackContext):
    symbol = update.message.text.strip()
    if len(symbol) > 6 or not symbol.isalpha():
        update.message.reply_text("❗️ لطفاً فقط نماد ارز را وارد کنید. مثال: btc")
        return
    update.message.reply_text(get_price(symbol))

def main():
    token = os.getenv("BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("price", price_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
