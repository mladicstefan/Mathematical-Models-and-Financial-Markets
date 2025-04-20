from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from vectorbtpro.portfolio.base import PortfolioResultT, Portfolio
import pandas as pd


class BacktestMaker:

    def __init__(self, params: BacktestParameters, hasOptimizationsEnabled) -> None:
        self.params = params
        self.data = params.data
        self.hasOptimizationsEnabled = hasOptimizationsEnabled
        self.longEntries = params.longEntry
        self.longExits = params.longExit
        self.shortEntries = params.shortEntry
        self.shortExits = params.shortExit

        self.pf_config = dict(
            open=self.data.get("Open"),
            high=self.data.get("High"),
            low=self.data.get("Low"),
            close=self.data.get("Close"),
            order_type=int(self.params.orderType == "limit"),
            fees=float(self.params.fees) / 100,
            init_cash=float(self.params.startCash),
            tp_stop=float(self.params.tpStop) / 100,
            sl_stop=float(self.params.slStop) / 100,
            tsl_stop=float(self.params.tslStop) / 100,
            leverage=float(self.params.leverage),
            size_type=SizeType.Percent100,
            size=10.0,
        )

    def run(self) -> PortfolioResultT | pd.DataFrame:

        if not self.hasOptimizationsEnabled:
            pf = Portfolio.from_signals(
                long_entries=self.longEntries,
                short_entries=self.shortEntries,
                long_exits=self.longExits,
                short_exits=self.shortExits,
                **self.pf_config,
            )

            return pf
