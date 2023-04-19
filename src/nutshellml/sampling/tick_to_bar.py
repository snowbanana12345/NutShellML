import numpy as np
from datetime import timedelta
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


def volume_sample_to_bar(tick_data : TickData, volume_per_bar : int) -> BarData:
    # TODO : replace this portion with native C code
    vol_counter = 0
    resampled_ts = []
    resampled_prices = []
    resampled_quantities = []
    for ts, p, q in zip(tick_data.timestamps, tick_data.trade_prices, tick_data.trade_sizes):
        if vol_counter + q <= volume_per_bar:
            vol_counter += q
            resampled_ts.append(ts)
            resampled_prices.append(p)
            resampled_quantities.append(q)
            if vol_counter == volume_per_bar:
                vol_counter = 0
        else :
            resampled_ts.append(ts)
            resampled_prices.append(p)
            resampled_quantities.append(volume_per_bar - vol_counter)
            remaining_quantity = q - volume_per_bar + vol_counter
            while remaining_quantity >= volume_per_bar:
                remaining_quantity -= volume_per_bar
                resampled_ts.append(ts)
                resampled_prices.append(p)
                resampled_quantities.append(volume_per_bar)
            if remaining_quantity > 0:
                resampled_ts.append(ts)
                resampled_prices.append(p)
                resampled_quantities.append(remaining_quantity)
            vol_counter = remaining_quantity

    tmp_df = pd.DataFrame({
        "ts" : resampled_ts,
        "p" : resampled_prices,
        "q" : resampled_quantities
    })
    vol_time_series = tmp_df.q.cumsum()
    tmp_df.index = [pd.Timestamp(v * 1E9 - 1) for v in vol_time_series.values]
    rule = str(volume_per_bar) + "S"
    ts_series = tmp_df.ts.resample(rule).first()
    close_series = tmp_df.p.resample(rule).last()
    vol_series = tmp_df.q.resample(rule).sum()
    tick_series = tmp_df.q.resample(rule).count()
    return BarData(timestamps = ts_series.to_numpy(), close_price = close_series.to_numpy(),volume = vol_series.to_numpy(), ticks = tick_series.to_numpy())
