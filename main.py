import logging
from route.data import DataFetcher
from route.portfolio import BacktestMaker
from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from route.indicators import IndicatorGenerator
import pandas as pd
from route.plotting import plot_results
from strategies.ToU import StrategyToU
import numpy as np
import vectorbtpro as vbt


def main():
    fetcher = DataFetcher(is_stock=False)
    params = fetcher.input()
    logging.info(f"Fetching data for {params.assets}...")
    data_dict = fetcher.fetch_data(params)
    print(params.assets)
    print(data_dict)
    strat = StrategyToU(params.assets, data_dict)
    long_entries, long_exits = strat.generate_signals()

    from vectorbtpro.portfolio.enums import SizeType

    pf_spx = vbt.Portfolio.from_holding(
        close=data_dict["^GSPC"],
        size=100.0,  # 100 %
        size_type=SizeType.ValuePercent,
        init_cash=10_000,
        close_at_end=True,
    )

    # pf_gold = vbt.Portfolio.from_holding(
    #     close=data_dict["GC=F"],
    #     size=100.0,  # 100 %
    #     size_type=SizeType.ValuePercent,
    #     init_cash=10_000,
    #     close_at_end=True,
    # )

    pf_vix = vbt.Portfolio.from_signals(
        close=data_dict["^VIX"],
        entries=long_entries["^VIX"],
        exits=long_exits["^VIX"],
        direction="longonly",
        size=100.0,
        size_type=SizeType.ValuePercent,
        init_cash=10_000,
        fees=0.04,
    )
    # pf_vix = vbt.Portfolio.from_holding(
    #     close=data_dict["^VIX"],
    #     size=100.0,  # 100 %
    #     size_type=SizeType.ValuePercent,
    #     init_cash=10_000,
    #     close_at_end=True,
    # )
    print(pf_vix.stats())
    pf_vix.plot().show()
    pf_vix.plots(subplots=["value", "cumulative_returns"], per_column=False).show()
    # combined_pf = vbt.Portfolio.column_stack(pf_spx, pf_gold, pf_vix, group_by=True)
    # print(combined_pf.stats())
    # combined_pf.plots(subplots=["value", "cumulative_returns"], per_column=False).show()


if __name__ == "__main__":
    main()
