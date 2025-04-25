import pandas as pd
import logging
from typing import List, Dict, Tuple

# configure module-level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class StrategyToU:
    """
    Enhanced VIX strategy with noise reduction and diagnostics:
    - Long VIX on significant volatility shocks filtered by dynamic thresholds.
    - Exit when VIX mean-reverts, via trailing stop, or max hold.
    - SPX and Gold remain buy-and-hold.
    Provides signal summaries for analysis.
    """

    def __init__(
        self,
        tickers: List[str],
        data_dict: Dict[str, pd.DataFrame],
        vix_jump_thresh: float = 0.25,
        spx_drop_thresh: float = -0.015,
        dynamic_quantile: float = 0.75,
        vix_entry_cap: float = 50.0,
        max_hold_days: int = 200,
        trailing_stop_pct: float = 0.10,
        mean_window: int = 10,
    ):
        df = pd.DataFrame(
            {t: data_dict[t].iloc[:, 0] for t in tickers},
            index=next(iter(data_dict.values())).index,
        )
        self.data = df.dropna()
        logger.debug(
            f"Initialized with {len(self.data)} rows, cols: {self.data.columns.tolist()}"
        )

        self.vix_jump_thresh = vix_jump_thresh
        self.spx_drop_thresh = spx_drop_thresh
        self.dynamic_quantile = dynamic_quantile
        self.vix_entry_cap = vix_entry_cap
        self.max_hold_days = max_hold_days
        self.trailing_stop_pct = trailing_stop_pct
        self.mean_window = mean_window

    def generate_signals(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        idx = self.close.index
        cols = self.tickers
        long_entries = pd.DataFrame(False, index=idx, columns=cols)
        long_exits = pd.DataFrame(False, index=idx, columns=cols)

        # SPX и Gold — стално улажење
        for ticker in cols:
            if ticker in ("^GSPC", "GC=F"):
                long_entries[ticker] = True

        vix = self.close["^VIX"]
        spx = self.close["^GSPC"]

        vix_ret = vix.pct_change()
        spx_ret = spx.pct_change()

        # Статус држања позиције
        open_trade = False
        entry_day_counter = 0
        highest_vix = None

        for i in range(1, len(idx)):
            date = idx[i]

            if not open_trade:
                if (
                    vix_ret.iloc[i] >= self.vix_jump_thresh
                    and spx_ret.iloc[i] <= self.spx_drop_thresh
                    and vix.iloc[i] < self.vix_entry_cap
                ):
                    long_entries.loc[date, "^VIX"] = True
                    open_trade = True
                    entry_day_counter = 0
                    highest_vix = vix.iloc[i]
            else:
                # Пратимо колико дана смо у трговини
                entry_day_counter += 1
                highest_vix = max(highest_vix, vix.iloc[i])
                drawdown_from_high = (highest_vix - vix.iloc[i]) / highest_vix

                exit_due_to_trailing = drawdown_from_high >= self.trailing_stop_pct
                exit_due_to_timeout = entry_day_counter >= self.max_hold_days

                if exit_due_to_trailing or exit_due_to_timeout:
                    long_exits.loc[date, "^VIX"] = True
                    open_trade = False
                    entry_day_counter = 0
                    highest_vix = None

        return long_entries, long_exits
