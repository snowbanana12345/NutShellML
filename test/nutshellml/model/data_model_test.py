import unittest
import numpy as np
from src.nutshellml.model.data_model import TickData


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
