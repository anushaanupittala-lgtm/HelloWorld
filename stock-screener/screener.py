import pandas as pd
import yfinance as yf

from indicators import add_indicators

def check_stock(symbol):

    df = yf.download(
        symbol,
        period="6mo",
        interval="1d",
        auto_adjust=True
    )

    if len(df) < 60:
        return None

    df = add_indicators(df)

    latest = df.iloc[-1]

    avg_volume = (
        df["Volume"]
        .tail(20)
        .mean()
    )

    buy_signal = (
        latest["Close"] > latest["EMA20"]
        and latest["EMA20"] > latest["EMA50"]
        and 55 < latest["RSI"] < 70
        and latest["MACD"] > latest["MACD_SIGNAL"]
        and latest["Volume"] > avg_volume * 1.5
    )

    if not buy_signal:
        return None

    entry = round(float(latest["Close"]), 2)

    stop_loss = round(
        entry - (latest["ATR"] * 1.5),
        2
    )

    risk = entry - stop_loss

    target = round(
        entry + (risk * 2),
        2
    )

    return {
        "symbol": symbol,
        "entry": entry,
        "stop_loss": stop_loss,
        "target": target,
        "rsi": round(float(latest["RSI"]), 2),
        "atr": round(float(latest["ATR"]), 2),
    }
