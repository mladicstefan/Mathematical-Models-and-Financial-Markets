# Mathematical Models and Financial Markets
---

## 📂 Repository Structure

```
/
├─ animations/           # C code for double‑pendulum chaos animations
├─ data.py               # DataFetcher: fetches OHLCV via YFData or BinanceData
├─ portfolio.py          # BacktestMaker: wraps vectorbtpro Portfolio.from_signals
├─ typing_.py            # @dataclass definitions for DataParameters & BacktestParameters
├─ main.py               # Orchestrates data fetch → signal gen → backtest → results
├─ README.md             # You are here
└─ RAD.pdf            # Full write‑up (in Serbian): “Matematički Modeli i Finansijska Tržišta”
└─ PAPER.pdf            # Full write‑up (in English): “Mathematical Models & Financial Markets”
```

---

## 🚀 Quickstart

1. **Install python dependencies**  
   ```bash
   pip install requirements.txt
   ```
#### Note! Vectorbtpro requires a purchased liscence
2. **Fetch & backtest**  
   ```bash
   python main.py
   ```
   This will:
   - Download OHLCV data for your chosen asset/timeframe. Editable in data.py
   - Generate simple long/short signals.
   - Run a portfolio backtest with stops, leverage, and fees.
   - Print portfolio statistics to console.

3. **View chaos animations**
   #### Install: GCC & Make
   In `animations/`, compile the Makefile:
   ```bash
   make
   ```
   ##### Note: tested on Ubuntu.
   These C simulations visualize the butterfly‑effect on three double pendulums, as featured in the PDF.
---

## 📄 About the Paper

The accompanying PDF (**`Paper.PDF`**)—*“Mathematical Models & Financial Markets”*—uses chaos theory to draw parallels between ecology (Yellowstone wolf reintroduction) and financial markets. It argues that markets behave like complex, sensitive systems, and demonstrates:

- **Butterfly Effect**: small changes → large divergences over time  
- **Mean‑Field Game Theory**: how individual decisions shape aggregate prices  
- **Limits of Classical Finance Theories**: EMH, Random Walk, Martingale vs. empirical anomalies  


## 📜 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
