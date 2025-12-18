from datetime import datetime, timedelta
from common import load_prices, get_prices, send_discord


def main():
    today = datetime.now()

    stocks = load_prices()
    week_start = today - timedelta(days=4)

    total_now = 0
    total_week_start = 0

    lines = [f"📅 週間レポート ({week_start:%m/%d} → {today:%m/%d})\n"]

    for symbol, info in stocks.items():
        hist = get_prices(symbol, period="7d")
        week_open = float(hist.iloc[0]["Close"])
        close = float(hist.iloc[-1]["Close"])

        units = info["unit"]

        total_week_start += week_open * units
        total_now += close * units

    diff = total_now - total_week_start
    icon = "🚀" if diff >= 0 else "📉"

    lines.append(
        "―――――――――――――\n"
        f"{icon} 週間収支\n"
        f"📊 週初比: {diff:+,.0f}円"
    )

    send_discord("\n".join(lines))


if __name__ == "__main__":
    main()

