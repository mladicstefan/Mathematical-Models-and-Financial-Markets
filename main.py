import logging
from route.data import DataFetcher
from route.portfolio import BacktestMaker
from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from route.indicators import IndicatorGenerator
import pandas as pd
from route.plotting import plot_results
from strategies.ta import StrategyTA
from strategies.dca import StrategyDCA
import numpy as np
import vectorbtpro as vbt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def main():

    fetcher = DataFetcher(is_stock=False)
    params = fetcher.input()
    logging.info(f"Fetching data for {params.assets}...")

    data = fetcher.fetch_data(params)
    logging.info(f"Loading Strategy...")
    data_dict = fetcher.fetch_data(params)
    logging.info(data_dict)
    for asset, data in data_dict.items():
        long_entries, short_entries, long_exits, short_exits = StrategyDCA(
            data
        ).generate_signals()

        logging.info(f"Loading Paramaters...")
        bt_params = BacktestParameters(
            data=data,
            longEntry=long_entries,
            shortEntry=short_entries,
            longExit=long_exits,
            shortExit=short_exits,
            orderType="limit",
            tpStop=5,
            slStop=5,
            tslStop=5,
            leverage=1,
            sizeType=SizeType.Percent100,
            size=10.0,
            startCash=10_000,
            fees=0.04,
        )

        logging.info(f"Running backtest")
        btm = BacktestMaker(bt_params, hasOptimizationsEnabled=False)
        result = btm.run()

        logging.info("Portfolio stats:\n%s", result.stats())
        logging.info(f"Plotting Reulsts")
        plot_results(result)


if __name__ == "__main__":
    main()
