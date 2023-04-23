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

        actual_bar = sampler.time_sample_tick_to_bar(tick_data, time_per_bar= timedelta(seconds = 15))
        self.assertTrue(all(expected_bar.timestamps == actual_bar.timestamps))
        self.assertTrue(all(expected_bar.close_price == actual_bar.close_price))
        self.assertTrue(all(expected_bar.volume == actual_bar.volume))
        self.assertTrue(all(expected_bar.ticks == actual_bar.ticks))

    def test_tick_sampling(self):
        timestamps = np.arange(1E9, 12 * 1E9, 1E9)
        trade_prices = np.array([1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,10.0,1.0,10.0])
        trade_sizes = np.array([2.0,3.0,1.0,4.0,5.0,6.0,8.0,2.0,2.5,2.5,2.5])
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

        actual_bar = sampler.tick_sample_to_bar(tick_data, ticks_per_bar= 4)
        self.assertTrue((expected_bar.timestamps == actual_bar.timestamps).all())
        self.assertTrue((expected_bar.close_price == actual_bar.close_price).all())
        self.assertTrue((expected_bar.volume == actual_bar.volume).all())
        self.assertTrue((expected_bar.ticks == actual_bar.ticks).all())

    def test_volume_sampling(self):
        timestamps = np.arange(1E9, 15 * 1E9, 1E9)
        trade_prices = np.array([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0, 11.0, 12.0, 5.0, 7.0], dtype = float)
        trade_sizes = np.array([4.0,7.0,3.0,6.0, 5.0,3.0,8.0,6.0, 18.0, 6.0, 36.0, 18.0, 6.0, 4.0], dtype = float)
        bid_prices = np.array([[0 for _ in range(14)]], dtype=float)
        ask_prices = np.array([[0 for _ in range(14)]], dtype=float)
        bid_sizes = np.array([[0 for _ in range(14)]], dtype=float)
        ask_sizes = np.array([[0 for _ in range(14)]], dtype=float)
        tick_data = TickData(timestamps, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)

        expec_bar_ts = np.array([1E9, 5E9, 8E9, 10E9, 11E9, 11E9, 13E9], dtype=float)
        expec_close = np.array([4.0, 8.0, 9.0, 11.0, 11.0, 12.0, 7.0], dtype=float)
        expec_vol = np.array([20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 10.0], dtype=float)
        expec_ticks = np.array([4, 4, 2, 2, 1, 2, 2], dtype=np.int64)
        expected_bar = BarData(timestamps=expec_bar_ts, close_price=expec_close, volume=expec_vol, ticks=expec_ticks)

        actual_bar = sampler.volume_sample_to_bar(tick_data, volume_per_bar = 20)
        self.assertTrue((expected_bar.timestamps == actual_bar.timestamps).all())
        self.assertTrue((expected_bar.close_price == actual_bar.close_price).all())
        self.assertTrue((expected_bar.volume == actual_bar.volume).all())
        self.assertTrue((expected_bar.ticks == actual_bar.ticks).all())

    def test_dollar_sampling(self):
        timestamps = np.arange(1E9, 8 * 1E9, 1E9)
        trade_prices = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 1.0], dtype=float)
        trade_sizes = np.array([12.0, 5.0, 4.0, 4.0, 4.0, 6.0, 42.0], dtype=float)
        bid_prices = np.array([[0 for _ in range(7)]], dtype=float)
        ask_prices = np.array([[0 for _ in range(7)]], dtype=float)
        bid_sizes = np.array([[0 for _ in range(7)]], dtype=float)
        ask_sizes = np.array([[0 for _ in range(7)]], dtype=float)
        tick_data = TickData(timestamps, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)

        expec_bar_ts = np.array([1E9, 5E9, 6E9], dtype=float)
        expec_close = np.array([4.0, 6.0, 1.0], dtype=float)
        expec_vol = np.array([25.0, 9.0, 43.0], dtype=float)
        expec_ticks = np.array([4,2,2], dtype=np.int64)
        expected_bar = BarData(timestamps=expec_bar_ts, close_price=expec_close, volume=expec_vol, ticks=expec_ticks)

        actual_bar = sampler.dollar_sample_to_bar(tick_data, dollar_per_bar = 50.0)
        self.assertTrue((expected_bar.timestamps == actual_bar.timestamps).all())
        self.assertTrue((expected_bar.close_price == actual_bar.close_price).all())
        self.assertTrue((expected_bar.volume == actual_bar.volume).all())
        self.assertTrue((expected_bar.ticks == actual_bar.ticks).all())
