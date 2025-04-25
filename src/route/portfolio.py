from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from vectorbtpro.portfolio.base import PortfolioResultT, Portfolio
import pandas as pd
from typing import Optional


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
            close=self.data,
            order_type=int(self.params.orderType == "limit"),
            fees=self.params.fees / 100,
            init_cash=self.params.startCash,
            tp_stop=self.params.tpStop / 100 if not None else None,
            sl_stop=self.params.slStop / 100 if not None else None,
            tsl_stop=self.params.tslStop / 100 if not None else None,
            leverage=self.params.leverage,
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
