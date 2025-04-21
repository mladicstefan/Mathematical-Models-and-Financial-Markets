from pandas import Series, DataFrame
from typing import Tuple


class StrategyDCA:
    """
    Dollar‑Cost‑Averaging: buy on the first trading day of each month,
    hold indefinitely (no exits), no shorts.
    """

    def __init__(self, price: DataFrame):
        price = price["Close"]
        idx = price.index

        # Mark True whenever the day-of-month == 1
        long_entries = []
        for ts in idx:
            long_entries.append(ts.day == 1)

        self.long_entries = Series(long_entries, index=idx)
        self.long_exits = Series(False, index=price.index)
        self.short_entries = Series(False, index=price.index)
        self.short_exits = Series(False, index=price.index)

    def generate_signals(self) -> Tuple[Series, Series, Series, Series]:
        """
        Returns signals in the order:
        (long_entries, short_entries, long_exits, short_exits)
        """
        return (
            self.long_entries,
            self.short_entries,
            self.long_exits,
            self.short_exits,
        )
