from dataclasses import dataclass
import pandas as pd
from vectorbtpro import YFData, BinanceData
from vectorbtpro.portfolio.enums import SizeTypeT
from typing import Union, List, Optional


@dataclass
class IndicatorData:
    data: Union[YFData, BinanceData]


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
    tpStop: float
    slStop: float
    tslStop: float
    leverage: int
    sizeType: SizeTypeT
    size: float
    startCash: float
    fees: float
    orderType: str = "limit"
