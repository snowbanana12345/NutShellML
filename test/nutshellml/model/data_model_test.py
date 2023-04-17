import unittest
import numpy as np
from src.nutshellml.model.data_model import TickData, BarData


class DataModelTest(unittest.TestCase):
    def test_tick_data(self):
        ts_col = np.array([1,2,3,4,5], dtype = np.int64)
        trade_prices = np.array([0.0, 7.0, 0.0, 0.0, 6.0], dtype = float)
        trade_sizes = np.array([0.0, 1.0, 0.0, 0.0, 5.0], dtype = float)
        ask_prices = np.array([[4.0, 5.0, 3.0, 2.0, 1.0], [5.0,6.0,4.0,3.0,2.0]], dtype = float)
        ask_sizes = np.array([[3.0, 1.5, 2.5, 2.0, 1.5], [2.0, 2.0, 1.5, 1.5, 1.25]], dtype = float)
        bid_prices = np.array([[2.0, 1.5, 1.0, 1.0, 0.5], [1.5, 1.5, 0.75, 0.75, 0.5]], dtype = float)
        bid_sizes = np.array([[1.5, 2.5, 2.75, 2.0, 1.75], [1.25, 1.0, 0.75, 0.8, 1.5]], dtype = float)
        dummy = TickData(timestamps = ts_col, trade_prices = trade_prices, trade_sizes = trade_sizes,
                         bid_prices = bid_prices, bid_sizes = bid_sizes, ask_prices = ask_prices, ask_sizes = ask_sizes)
        self.assertIsNotNone(dummy)

    def test_tick_data_fail_check(self):
        def try_create_tick_data_obj():
            ts_col = np.array([1, 2, 3, 4, 5], dtype=np.int64)
            trade_prices = np.array([0.0, 7.0, 0.0, 0.0, 6.0], dtype=float)
            trade_sizes = np.array([0.0, 1.0, 0.0, 0.0, 5.0], dtype=float)
            ask_prices = np.array([[4.0, 5.0, 3.0, 1.0], [5.0, 6.0, 3.0, 2.0]], dtype=float)
            ask_sizes = np.array([[3.0, 1.5, 2.5, 2.0, 1.5], [2.0, 2.0, 1.5, 1.5, 1.25]], dtype=float)
            bid_prices = np.array([[2.0, 1.5, 1.0, 1.0, 0.5]], dtype=float)
            bid_sizes = np.array([[1.5, 2.5, 2.75, 2.0, 1.75], [1.25, 1.0, 0.75, 0.8, 1.5]], dtype=float)
            dummy = TickData(timestamps=ts_col, trade_prices=trade_prices, trade_sizes=trade_sizes,
                             bid_prices=bid_prices, bid_sizes=bid_sizes, ask_prices=ask_prices, ask_sizes=ask_sizes)
        self.assertRaises(ValueError, try_create_tick_data_obj)

    def test_bar_data(self):
        ts_col = np.array([1, 2, 3, 4, 5], dtype = np.int64)
        close = np.array([3.0, 1.0, 5.0, 6.0, 5.0], dtype = float)
        volume = np.array([5.0, 5.0, 4.0, 3.0, 2.0], dtype = float)
        ticks = np.array([1,5,4,3,6], dtype = np.int64)
        bar_data = BarData(timestamps = ts_col, close_price=  close, volume = volume, ticks = ticks)
        self.assertIsNotNone(bar_data)

