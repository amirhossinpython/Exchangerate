from flask import Flask, render_template, jsonify
import aiohttp
import asyncio
import re
from datetime import datetime
from pytz import timezone
import jdatetime

app = Flask(__name__)

async def convert_to_jalali():
    tehran_tz = timezone('Asia/Tehran')
    tehran_time = datetime.now(tehran_tz)
    jalali_datetime = jdatetime.datetime.fromgregorian(datetime=tehran_time)
    return jalali_datetime.strftime("%Y/%m/%d %H:%M:%S")

async def fetch_currency_data():
    url = 'https://www.iranjib.ir/showgroup/23/realtime_price/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    persian_date = await convert_to_jalali()
    price_matches = re.findall(r'<span class="lastprice">(.*?)<\/span>', html)
    prices = price_matches if price_matches else []

    selected_indices = [4, 8, 12, 20, 25, 30, 49, 57, 67, 81, 85]
    selected_prices = [prices[idx] if idx < len(prices) else 'ندارد' for idx in selected_indices]

    data = {
        "date": persian_date,
        "gold_mesghal": selected_prices[0],
        "gold_18": selected_prices[1],
        "gold_24": selected_prices[2],
        "new_coin": selected_prices[3],
        "old_coin": selected_prices[4],
        "half_coin": selected_prices[5],
        "tether": selected_prices[6],
        "dollar": selected_prices[7],
        "euro": selected_prices[8],
        "btc": selected_prices[9],
        "eth": selected_prices[10]
    }
    return data

@app.route("/")
def index():
    data = asyncio.run(fetch_currency_data())
    return render_template("index.html", data=data)

@app.route("/update")
def update_data():
    data = asyncio.run(fetch_currency_data())
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
