from vectorbtpro.data.custom import YFData, BinanceData
from typing import Union
import pandas as pd
from typing_ import DataParameters
from yfinance.exceptions import YFRateLimitError
from time import sleep
import logging
from binance.exceptions import BinanceRequestException
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
DATA_DIR = Path("data")


class DataFetcher:
    def __init__(self, is_stock: bool):
        self.is_stock = is_stock
        self.data = None

    def input(self) -> DataParameters:

        assets = ["^VIX", "^GSPC", "GC=F"]
        timeframe = "1d"
        start_date = pd.to_datetime("2024-01-01")
        end_date = pd.to_datetime("2025-02-02")
        return DataParameters(assets, timeframe, start_date, end_date)

    def cache_data(
        self, data: Union[pd.Series, pd.DataFrame], ticker: str, pkl_path: Path
    ):
        series = data.copy()
        series.name = ticker
        series.to_pickle(pkl_path)

    def fetch_data(self, params: DataParameters) -> dict[str, pd.DataFrame]:
        DATA_DIR.mkdir(exist_ok=True)
        src = YFData if self.is_stock else BinanceData
        dfs = {}
        for asset in params.assets:
            symbol = asset.lstrip("^").replace("=", "_")
            pkl_path = DATA_DIR / f"{symbol}.pkl"
            if pkl_path.is_file():
                df = pd.read_pickle(pkl_path)
            else:
                for attempt in range(1, 4):
                    try:
                        df = src.fetch(
                            asset,
                            start=params.start_date,
                            end=params.end_date,
                            timeframe=params.timeframe,
                        )
                        df.to_pickle(pkl_path)
                        break
                    except (YFRateLimitError, BinanceRequestException):
                        sleep(30 * attempt)
                else:
                    raise RuntimeError(f"Failed to fetch {asset}")

            if isinstance(df, pd.Series):
                df = df.to_frame(asset)
            elif "Close" in df.columns:
                df = df["Close"].to_frame(asset)
            else:
                df.columns = [asset]
            dfs[asset] = df
        return dfs
