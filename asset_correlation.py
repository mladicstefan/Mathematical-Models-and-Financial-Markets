import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

tickers = ["^VIX", "^GSPC", "GC=F"]
df = yf.download(tickers, start="2006-01-01", progress=False)["Close"]

df_indexed = df / df.iloc[0] * 100

fig = go.Figure()
colors = {"^VIX": "purple", "^GSPC": "green", "GC=F": "gold"}

for t in tickers:
    s = df_indexed[t].dropna()

    fig.add_trace(
        go.Scatter(
            x=s.index, y=s.values, mode="lines", name=t, line=dict(color=colors[t])
        )
    )

fig.update_layout(
    title="VIX S&P500 i Zlato u Finansijskim Krizama",
    xaxis=dict(rangeslider=dict(visible=True)),
    yaxis=dict(title="Indeksirana Cena", type="linear"),
    template="plotly_white",
)
fig.show()

returns = df.pct_change().dropna()
print("Correlation of daily returns:\n", returns.corr())
