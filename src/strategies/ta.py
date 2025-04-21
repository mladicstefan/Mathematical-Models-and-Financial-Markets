from route.indicators import IndicatorGenerator
from pandas import Series


class StrategyTA:
    def __init__(self, sg: IndicatorGenerator):
        signals = sg.run_indicators(
            {
                "SMA": {"timeperiod": 14},
                "RSI": {"timeperiod": 14},
            }
        )
        sma_series = signals["SMA"].sma
        self.long_entries = sma_series > sma_series.shift(1)
        self.long_exits = sma_series < sma_series.shift(1)
        self.short_entries = sma_series < sma_series.shift(1)
        self.short_exits = sma_series > sma_series.shift(1)

    def generate_signals(self) -> tuple[Series, Series, Series, Series]:

        return (
            self.long_entries,
            self.short_entries,
            self.long_exits,
            self.short_exits,
        )
