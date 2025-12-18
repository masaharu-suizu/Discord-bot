from datetime import datetime
from common import load_prices, get_prices, send_discord


def main():
    stocks = load_prices()
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [f"📊 株価終値チェック ({today})\n"]

    total_assets = 0
    total_prev_assets = 0
    total_cost = 0

    for symbol, info in stocks.items():
        hist = get_prices(symbol)
        prev_close = float(hist.iloc[-2]["Close"])
        close = float(hist.iloc[-1]["Close"])

        name = info["name"]
        buy_price = info["price"]
        units = info["unit"]

        asset = close * units
        prev_asset = prev_close * units
        cost = buy_price * units

        diff_buy = close - buy_price
        diff_prev = close - prev_close

        icon = "🟢" if diff_buy >= 0 else "🔴"
        sb = "+" if diff_buy >= 0 else ""
        sp = "+" if diff_prev >= 0 else ""

        lines.append(
            f"{symbol} ({name})\n"
            f"  購入価格: {buy_price:,.0f}円\n"
            f"  終値: {close:,.0f}円 "
            f"(購入比: {sb}{diff_buy:,.0f}円、前日比: {sp}{diff_prev:,.0f}円)\n"
            f"  資産額: {asset:,.0f}円 {icon}\n"
        )

        total_assets += asset
        total_prev_assets += prev_asset
        total_cost += cost

    total_profit = total_assets - total_cost
    total_prev_diff = total_assets - total_prev_assets

    mood = "😊" if total_profit >= 0 and total_prev_diff >= 0 else \
           "😱" if total_profit < 0 and total_prev_diff < 0 else "😐"

    lines.append(
        "―――――――――――――\n"
        f"{mood} 総資産サマリー\n"
        f"📦 総資産額: {total_assets:,.0f}円 "
        f"(前日比: {total_prev_diff:+,.0f}円)\n"
        f"📈 評価損益: {total_profit:+,.0f}円"
    )

    send_discord("\n".join(lines))


if __name__ == "__main__":
    main()

