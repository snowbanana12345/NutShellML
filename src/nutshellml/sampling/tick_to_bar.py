import numpy as np
from datetime import timedelta, datetime
from src.nutshellml.model.data_model import TickData, BarData
import pandas as pd


def time_sample_tick_to_bar(tick_data : TickData, frequency : timedelta = timedelta(seconds = 1)) -> BarData:
    pd_timestamps = [pd.Timestamp(ts) for ts in tick_data.timestamps]
    tmp_df = pd.DataFrame({
            "p" : tick_data.trade_prices,
            "q" : tick_data.trade_sizes,
        }, index = pd_timestamps
    )
    tmp_df = tmp_df[tmp_df.p > 0]
    tmp_df = tmp_df[tmp_df.q > 0]
    rule : str = str(frequency.total_seconds()) + "S"
    close_prices = tmp_df.p.resample(rule).last().fillna(0.0)
    volume = tmp_df.q.resample(rule).sum()
    ticks = tmp_df.q.resample(rule).count()
    sampled_timestamps = np.array([ts.value for ts in close_prices.index], np.int64)
    return BarData(timestamps = sampled_timestamps, close_price = close_prices, volume = volume, ticks = ticks)

