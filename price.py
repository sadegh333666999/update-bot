import requests

def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if symbol in data:
            price = data[symbol]['usd']
            change = data[symbol]['usd_24h_change']
            return price, change
        else:
            return None, None
    else:
        return None, None
