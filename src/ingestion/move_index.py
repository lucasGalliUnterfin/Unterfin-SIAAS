import yfinance as yf
import pandas as pd

# -------------------------
# MOVE Index (Yahoo Finance)
# --------------------------
def get_move_index(period="1y", interval="1d"):
    move = yf.download("^MOVE", period=period, interval=interval)

    if isinstance(move.columns, pd.MultiIndex):
        move.columns = ['_'.join(col).strip() for col in move.columns.values]

    if "Close_^MOVE" in move.columns:
        move = move[["Close_^MOVE"]].rename(columns={"Close_^MOVE": "move_index"})
    else:
        move = move[["Close"]].rename(columns={"Close": "move_index"})

    move.index = pd.to_datetime(move.index)
    return move
