import logging
import pandas as pd
from data import DataFetcher
from portfolio import BacktestMaker
from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType


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
    # placeholder
    long_entry = pd.Series([False] * len(data), index=data.index)
    long_exit = pd.Series([False] * len(data), index=data.index)
    short_entry = pd.Series([False] * len(data), index=data.index)
    short_exit = pd.Series([False] * len(data), index=data.index)
    logging.info(f"Loading Paramaters...")
    bt_params = BacktestParameters(
        data=data,
        longEntry=long_entry.values.tolist(),
        shortEntry=short_entry.values.tolist(),
        longExit=long_exit.values.tolist(),
        shortExit=short_exit.values.tolist(),
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
