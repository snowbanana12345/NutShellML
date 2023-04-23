import unittest
import numpy as np
import random
from src.nutshellml.model.data_model import TickData
import src.nutshellml.sampling.tick_to_bar as sampler
from datetime import timedelta
import timeit

"""
Single threaded performance testing, very computationally expensive and results in console
DO NOT run in pipeline
"""

class SamplingTest(unittest.TestCase):
    def test_time_sampling_performance(self):
        number_trials : int  = 10
        results : list = []
        bar_sizes : list = []

        for i in range(number_trials):
            tick_data = self.generate_random_ticks(sample_size=int(1E6))
            start_time = timeit.default_timer()
            bar_data = sampler.time_sample_tick_to_bar(tick_data, time_per_bar=timedelta(seconds = 10))
            end_time = timeit.default_timer()
            results.append(end_time - start_time)
            bar_sizes.append(len(bar_data))
            print(f"Completed trial : {i + 1} - {end_time - start_time}, bar size : {len(bar_data)}")

        print(f"{np.mean(results)} ± {np.std(results)}, bar_sizes : {np.mean(results)} ± {np.std(results)}")

    def test_volume_sampling_performance(self):
        number_trials: int = 10
        results: list = []
        bar_sizes: list = []

        for i in range(number_trials):
            tick_data = self.generate_random_ticks(sample_size=int(1E6))
            start_time = timeit.default_timer()
            bar_data = sampler.volume_sample_to_bar(tick_data, volume_per_bar = 60)
            end_time = timeit.default_timer()
            results.append(end_time - start_time)
            bar_sizes.append(len(bar_data))
            print(f"Completed trial : {i + 1} - {end_time - start_time}, bar size : {len(bar_data)}")

        print(f"{np.mean(results)} ± {np.std(results)}, bar sizes : {np.mean(bar_sizes)} ± {np.std(bar_sizes)}")

    def test_tick_sampling_performance(self):
        number_trials: int = 10
        results: list = []
        bar_sizes: list = []

        for i in range(number_trials):
            tick_data = self.generate_random_ticks(sample_size=int(1E6))
            start_time = timeit.default_timer()
            bar_data = sampler.tick_sample_to_bar(tick_data, ticks_per_bar = 3000)
            end_time = timeit.default_timer()
            results.append(end_time - start_time)
            bar_sizes.append(len(bar_data))
            print(f"Completed trial : {i + 1} - {end_time - start_time}, bar size : {len(bar_data)}")

        print(f"{np.mean(results)} ± {np.std(results)}, bar sizes : {np.mean(bar_sizes)} ± {np.std(bar_sizes)}")

    def test_dollar_sampling_performance(self):
        number_trials: int = 10
        results: list = []
        bar_sizes: list = []

        for i in range(number_trials):
            tick_data = self.generate_random_ticks(sample_size=int(1E6))
            start_time = timeit.default_timer()
            bar_data = sampler.tick_sample_to_bar(tick_data, ticks_per_bar=10)
            end_time = timeit.default_timer()
            results.append(end_time - start_time)
            bar_sizes.append(len(bar_data))
            print(f"Completed trial : {i + 1} - {end_time - start_time}, bar size : {len(bar_data)}")

        print(f"{np.mean(results)} ± {np.std(results)}, bar sizes : {np.mean(bar_sizes)} ± {np.std(bar_sizes)}")


    def generate_random_ticks(self, sample_size : int) -> TickData:
        ts_deltas = [random.random() * 1E9]
        ts_arr = np.array([sum(ts_deltas[:i + 1]) for i in range(sample_size)])
        trade_prices = np.array([random.random() for _ in range(sample_size)])
        trade_sizes = np.array([random.random() for _ in range(sample_size)])
        bid_prices = np.array([[0 for _ in range(sample_size)]])
        bid_sizes = np.array([[0 for _ in range(sample_size)]])
        ask_prices = np.array([[0 for _ in range(sample_size)]])
        ask_sizes = np.array([[0 for _ in range(sample_size)]])
        return TickData(ts_arr, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)
