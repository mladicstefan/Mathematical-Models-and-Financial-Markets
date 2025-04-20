from dataclasses import dataclass
import pandas as pd
from vectorbtpro import YFData, BinanceData
from vectorbtpro.portfolio.enums import SizeTypeT
from typing import Union, List, Optional


@dataclass
class DataParameters:
    asset: str
    timeframe: str
    start_date: pd.Timestamp
    end_date: pd.Timestamp


@dataclass
class BacktestParameters:
    data: Union[YFData, BinanceData]
    longEntry: List[bool]
    shortEntry: Optional[List[bool]]
    longExit: Optional[List[bool]]
    shortExit: Optional[List[bool]]
    orderType: str = "limit"
    tpStop: float
    slStop: float
    tslStop: float
    leverage: int
    size_type: SizeTypeT
    size: float
