import src.nutshellml.sampling.tick_to_bar as sampler
from src.nutshellml.model.data_model import TickData, BarData
import unittest
import numpy as np
from datetime import timedelta


class SamplingTest(unittest.TestCase):
    def test_time_sampling(self):
        timestamps = np.array([int(ts * 1E9) for ts in [0,2,7,14,35,35.01, 35.02, 35.03, 45, 74.99, 75.01, 90.02, 90.06, 90.11]], dtype = np.int64)
        trade_prices = np.array([10.0, 20.0, 30.0, 40.0, 5.0, 4.0, 3.0, 2.0, 19.0, 81.0, 109.0, 205.0, 210.0, 215.0], dtype = float)
        trade_sizes = np.array([1.0, 1.0, 1.0, 1.0, 5.0, 7.0, 2.0, 2.0, 15.0, 25.0, 79.0, 40.0, 30.0, 30.0], dtype = float)
        bid_prices = np.array([[0 for _ in range(14)]], dtype = float)
        ask_prices = np.array([[0 for _ in range(14)]], dtype = float)
        bid_sizes = np.array([[0 for _ in range(14)]], dtype = float)
        ask_sizes = np.array([[0 for _ in range(14)]], dtype = float)
        tick_data = TickData(timestamps, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)

        expec_bar_ts = np.array([int(ts * 1E9) for ts in [0, 15, 30, 45, 60, 75, 90]], dtype = float)
        expec_close = np.array([40.0, 0.0, 2.0, 19.0, 81.0, 109.0, 215.0], dtype = float)
        expec_vol = np.array([4, 0, 16,15,25,79,100], dtype = float)
        expec_ticks = np.array([4, 0, 4, 1, 1, 1, 3], dtype = np.int64)
        expected_bar = BarData(timestamps = expec_bar_ts, close_price = expec_close, volume = expec_vol, ticks = expec_ticks)

        actual_bar = sampler.time_sample_tick_to_bar(tick_data, frequency = timedelta(seconds = 15))
        self.assertTrue(all(expected_bar.timestamps == actual_bar.timestamps))
        self.assertTrue(all(expected_bar.close_price == actual_bar.close_price))
        self.assertTrue(all(expected_bar.volume == actual_bar.volume))
        self.assertTrue(all(expected_bar.ticks == actual_bar.ticks))

    def test_tick_sampling(self):
        timestamps = np.arange(1E9, 11 * 1E9, 1E9)
        trade_prices = np.arange([1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,10.0,1.0,10.0])
        trade_sizes = np.arange([2.0,3.0,1.0,4.0,5.0,6.0,8.0,2.0,2.5,2.5,2.5])
        bid_prices = np.array([[0 for _ in range(11)]], dtype=float)
        ask_prices = np.array([[0 for _ in range(11)]], dtype=float)
        bid_sizes = np.array([[0 for _ in range(11)]], dtype=float)
        ask_sizes = np.array([[0 for _ in range(11)]], dtype=float)
        tick_data = TickData(timestamps, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)

        expec_bar_ts = np.array([1E9, 5*1E9, 9*1E9], dtype=float)
        expec_close = np.array([4.0, 2.0, 10.0], dtype=float)
        expec_vol = np.array([10.0, 21.0, 7.5], dtype=float)
        expec_ticks = np.array([4, 4, 3], dtype=np.int64)
        expected_bar = BarData(timestamps=expec_bar_ts, close_price=expec_close, volume=expec_vol, ticks=expec_ticks)

        actual_bar = sampler.tick_sample_to_bar(tick_data, frequency = 4)
        print(actual_bar.to_dataframe())

