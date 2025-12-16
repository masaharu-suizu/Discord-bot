import json
import os
import requests
from datetime import datetime
import yfinance as yf

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


def get_prices(symbol: str) -> tuple[float, float]:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")

    if len(hist) < 2:
        raise RuntimeError(f"価格データ不足: {symbol}")

    prev_close = hist.iloc[-2]["Close"]
    close = hist.iloc[-1]["Close"]

    return float(close), float(prev_close)


def send_discord(message: str):
    payload = {"content": message}
    r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    r.raise_for_status()


def main():
    with open("data.json", encoding="utf-8") as f:
        stocks = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 株価終値チェック ({today})\n"]

    total_assets = 0
    total_cost = 0
    total_prev_assets = 0

    for symbol, info in stocks.items():
        name = info["name"]
        buy_price = info["price"]
        units = info["unit"]

        close, prev_close = get_prices(symbol)

        asset = close * units
        prev_asset = prev_close * units
        cost = buy_price * units

        diff = close - buy_price
        prev_diff = close - prev_close

        profit_icon = "🟢" if diff >= 0 else "🔴"
        sign_diff = "+" if diff >= 0 else ""
        sign_prev = "+" if prev_diff >= 0 else ""

        lines.append(
            f"{symbol} ({name})\n"
            f"  購入価格: {buy_price:,.0f}円\n"
            f"  終値: {close:,.0f}円 "
            f"(購入比: {sign_diff}{diff:,.0f}円、"
            f"前日比: {sign_prev}{prev_diff:,.0f}円)\n"
            f"  資産額: {asset:,.0f}円 {profit_icon}\n"
        )

        total_assets += asset
        total_cost += cost
        total_prev_assets += prev_asset

    total_diff = total_assets - total_cost
    total_prev_diff = total_assets - total_prev_assets

    sign_total = "+" if total_diff >= 0 else ""
    sign_prev_total = "+" if total_prev_diff >= 0 else ""

    # 気分アイコン判定
    if total_diff >= 0 and total_prev_diff >= 0:
        mood = "😊"
    elif total_diff < 0 and total_prev_diff < 0:
        mood = "😱"
    else:
        mood = "😐"

    lines.append(
        "―――――――――――――\n"
        f"{mood} 総資産サマリー\n"
        f"📦 総資産額: {total_assets:,.0f}円 "
        f"(前日比: {sign_prev_total}{total_prev_diff:,.0f}円)\n"
        f"📈 評価損益: {sign_total}{total_diff:,.0f}円"
    )

    send_discord("\n".join(lines))


if __name__ == "__main__":
    main()

