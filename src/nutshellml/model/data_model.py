import numpy as np
from dataclasses import dataclass
import pandas as pd

@dataclass
class TickData:
    timestamps : np.array
    trade_prices : np.array
    trade_sizes : np.array
    bid_prices : np.array
    bid_sizes : np.array
    ask_prices : np.array
    ask_sizes : np.array

    def __post_init__(self):
        if len(self.timestamps.shape) != 1:
            raise ValueError("timestamp array should be 1d")
        if len(self.trade_prices.shape) != 1:
            raise ValueError("trade prices array should be 1d")
        if len(self.trade_sizes.shape) != 1:
            raise ValueError("trade sizes array should be 1d")
        if len(self.bid_prices.shape) != 2:
            raise ValueError("bid prices should be a 2d array")
        if len(self.bid_sizes.shape) != 2:
            raise ValueError("bid sizes should be a 2d array")
        if len(self.ask_prices.shape) != 2:
            raise ValueError("ask prices should be a 2d array")
        if len(self.ask_sizes.shape) != 2:
            raise ValueError("ask sizes should be a 2d array")
        length = self.timestamps.shape[0]
        if self.trade_prices.shape[0] != length:
            raise ValueError(f"trade sizes array should be the same length as timestamp : {length}")
        if self.trade_sizes.shape[0] != length:
            raise ValueError(f"trade sizes array should be the same length as timestamp : {length}")
        if self.bid_prices.shape[1] != length:
            raise ValueError(f"bid prices array should be the same length as timestamp : {length}")
        if self.ask_prices.shape[1] != length:
            raise ValueError(f"ask prices array should be the same length as timestamp : {length}")
        if self.bid_sizes.shape[1] != length:
            raise ValueError(f"bid sizes array should be the same length as timestamp : {length}")
        if self.ask_sizes.shape[1] != length:
            raise ValueError(f"ask sizes array should be the same length as timestamp : {length}")

    def to_dataframe(self):
        df = pd.DataFrame({
            "ts" : self.timestamps,
            "p" : self.trade_prices,
            "q" : self.trade_sizes,
        })

        for i,bid_px in enumerate(self.bid_prices):
            df["bp" + str(i + 1)] = bid_px
        for i,bid_sz in enumerate(self.bid_sizes):
            df["bs" + str(i + 1)] = bid_sz
        for i,ask_px in enumerate(self.ask_prices):
            df["ap" + str(i + 1)] = ask_px
        for i,ask_sz in enumerate(self.ask_sizes):
            df["as" + str(i + 1)] = ask_sz

        return df


@dataclass
class BarData:
    timestamps : np.array
    close_price : np.array
    volume : np.array
    ticks : np.array

    def __post_init__(self):
        if len(self.timestamps.shape) != 1:
            raise ValueError("timestamps array must be 1d")
        if len(self.close_price.shape) != 1:
            raise ValueError("close price array must be 1d")
        if len(self.volume.shape) != 1:
            raise ValueError("volume must be 1d")
        if len(self.ticks.shape) != 1:
            raise ValueError("ticks array must be 1d")
        length = self.timestamps.shape[0]
        if self.close_price.shape[0] != length:
            raise ValueError(f"close price array should be the same length as timestamp : {length}")
        if self.volume.shape[0] != length:
            raise ValueError(f"volume array should be the same length as timestamp : {length}")
        if self.ticks.shape[0] != length:
            raise ValueError(f"ticks array should be the same length as timestamp : {length}")

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "ts" : self.timestamps,
            "p" : self.close_price,
            "q" : self.volume,
            "ti" : self.ticks
        })