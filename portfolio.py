from typing_ import BacktestParameters
from vectorbtpro.portfolio.enums import SizeType
from vectorbtpro.portfolio.base import PortfolioResultT, Portfolio
import pandas as pd


class BacktestMaker:
    has_optimizations_enabled: bool

    def __init__(self, config: BacktestParameters) -> None:
        self.config = config
        self.has_optimizations_enabled = False
        pf_config = dict(
            order_type=int(self.config.orderType == "limit"),
            fees=float(self.config.exchangeFeesPercent) / 100,
            init_cash=float(self.config.startingCash),
            tp_stop=float(self.config.tp) / 100,
            sl_stop=float(self.config.sl) / 100,
            tsl_stop=float(self.config.tsl) / 100,
            leverage=float(self.config.leverage),
            size_type=SizeType.Percent100,
            size=10.0,
        )

    def run(self) -> PortfolioResultT | pd.DataFrame:
        pass
