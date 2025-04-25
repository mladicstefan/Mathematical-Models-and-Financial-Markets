import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from pathlib import Path

TICKERS = ["^VIX", "^GSPC", "GC=F"]
START_DATE = "2006-01-01"
DATA_DIR = Path("data")
COLORS = {"^VIX": "purple", "^GSPC": "green", "GC=F": "gold"}


def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def download_and_cache(ticker: str) -> pd.Series:
    symbol = ticker.lstrip("^").replace("=", "_")
    pkl_path = DATA_DIR / f"{symbol}.pkl"
    if pkl_path.is_file():
        return pd.read_pickle(pkl_path)
    df = yf.download(ticker, start=START_DATE, auto_adjust=False, progress=False)[
        ["Close"]
    ]
    series = df["Close"].copy()
    series.name = ticker
    series.to_pickle(pkl_path)
    return series


def load_cached(symbol: str) -> pd.Series:
    return pd.read_pickle(DATA_DIR / f"{symbol}.pkl")


def build_indexed_df(series_list: list[pd.Series]) -> pd.DataFrame:
    df = pd.concat(series_list, axis=1)
    return df.div(df.iloc[0]) * 100


def plot_indexed(df: pd.DataFrame):
    fig = go.Figure()
    for t in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[t],
                mode="lines",
                name=t,
                line=dict(color=COLORS.get(t)),
            )
        )
    fig.update_layout(
        title="VIX, S&P 500 & Gold During Financial Crises",
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(title="Indexed Price (Base = 100)"),
        template="plotly_white",
    )
    fig.show()


def main():
    ensure_data_dir()
    series = [download_and_cache(t) for t in TICKERS]
    df_indexed = build_indexed_df(series)
    plot_indexed(df_indexed)
    prices = pd.concat(series, axis=1)
    returns = prices.pct_change().dropna()
    print(returns.corr())


if __name__ == "__main__":
    main()
