from vectorbtpro.data.custom import YFData, BinanceData
from typing import Union
from datetime import datetime
import pandas as pd
from dataclasses import dataclass
from yfinance.exceptions import YFRateLimitError
from time import sleep
import logging
from binance.exceptions import BinanceRequestException

DateLike = Union[str, datetime, pd.Timestamp]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@dataclass
class Parameters:
    asset: str
    timeframe: str
    start_date: pd.Timestamp
    end_date: pd.Timestamp


class DataFetcher:
    def __init__(self, is_stock: bool):
        self.is_stock = is_stock
        self.data = None

    def input(self) -> Parameters:

        asset = "SPY"
        timeframe = "1d"
        start_date = pd.to_datetime("2025-01-01")
        end_date = pd.to_datetime("2025-02-02")
        return Parameters(asset, timeframe, start_date, end_date)

    def fetch_data(self, params: Parameters):

        src = YFData if self.is_stock else BinanceData
        for attempt in range(1, 4):

            try:
                self.data = src.fetch(
                    params.asset,
                    start=params.start_date,
                    end=params.end_date,
                    timeframe=params.timeframe,
                )
                logging.info(f"Fetched {params.asset} data:\n{self.data}")
                return self.data

            except YFRateLimitError:
                wait = 30 * (attempt + 1)
                logging.INFO(f"Rate limited waiting {wait}")
                sleep(wait)

            except BinanceRequestException:
                wait = 30 * (attempt + 1)
                logging.INFO(f"Rate limited waiting {wait}")
                sleep(wait)

        raise RuntimeError(f"Failed to fetch data for {params.asset} after 3 attempts")
