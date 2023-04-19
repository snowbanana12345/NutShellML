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
    return BarData(timestamps = sampled_timestamps, close_price = close_prices.to_numpy(), volume = volume.to_numpy(), ticks = ticks.to_numpy())


def tick_sample_to_bar(tick_data : TickData, frequency : int) -> BarData:
    tmp_df = pd.DataFrame({
            "ts" : tick_data.timestamps,
            "p" : tick_data.trade_prices,
            "q" : tick_data.trade_sizes,
        }, index = pd.RangeIndex(len(tick_data))
    )
    tmp_df = tmp_df[tmp_df.p > 0]
    tmp_df = tmp_df[tmp_df.q > 0]
    ts_series = tmp_df.ts.groupby(tmp_df.index // frequency).first()
    close_series = tmp_df.p.groupby(tmp_df.index // frequency).last()
    volume_series = tmp_df.q.groupby(tmp_df.index // frequency).sum()
    tick_series = tmp_df.ts.groupby(tmp_df.index // frequency).count()
    return BarData(
        timestamps = ts_series.to_numpy(),
        close_price = close_series.to_numpy(),
        volume = volume_series.to_numpy(),
        ticks = tick_series.to_numpy()
    )




