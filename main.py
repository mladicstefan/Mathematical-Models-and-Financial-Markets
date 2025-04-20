import logging
from data import DataFetcher
from portfolio import BacktestMaker
from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from indicators import IndicatorGenerator
import pandas as pd


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    fetcher = DataFetcher(is_stock=True)
    params = fetcher.input()
    logging.info(f"Fetching data for {params.asset}...")

    yfdata = fetcher.fetch_data(params)
    data = yfdata.data[params.asset]
    logging.info(f"Loading Strategy...")
    sg = IndicatorGenerator(data)

    signals = sg.run_indicators(
        {
            "SMA": {"timeperiod": 14},
            "RSI": {"timeperiod": 14},
        }
    )

    sma_series = signals["SMA"].sma
    long_entries = sma_series > sma_series.shift(1)
    long_exits = sma_series < sma_series.shift(1)
    short_entries = sma_series < sma_series.shift(1)
    short_exits = sma_series > sma_series.shift(1)
    logging.info(f"Loading Paramaters...")

    bt_params = BacktestParameters(
        data=data,
        longEntry=long_entries.values.tolist(),
        shortEntry=short_entries.values.tolist(),
        longExit=long_exits.values.tolist(),
        shortExit=short_exits.values.tolist(),
        orderType="limit",
        tpStop=1.0,
        slStop=1.0,
        tslStop=0.5,
        leverage=1,
        sizeType=SizeType.Percent100,
        size=10.0,
        startCash=10_000,
        fees=0.1,
    )
    logging.info(f"Running backtest")
    btm = BacktestMaker(bt_params, hasOptimizationsEnabled=False)
    result = btm.run()
    logging.info("Portfolio stats:\n%s", result.stats())
    logging.info(f"Plotting Reulsts")
    # btm.plot.show()


if __name__ == "__main__":
    main()
