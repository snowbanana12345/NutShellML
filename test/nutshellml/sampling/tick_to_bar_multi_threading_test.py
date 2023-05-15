import unittest
import numpy as np
import random
from src.nutshellml.model.data_model import TickData, BarData
import src.nutshellml.sampling.tick_to_bar as sampler
from datetime import timedelta
import threading
from typing import List


def generate_random_ticks(sample_size : int) -> TickData:
    ts_arr = np.array([(i + random.random()) * 1E9 for i in range(sample_size)])
    trade_prices = np.array([random.random() for _ in range(sample_size)])
    trade_sizes = np.array([random.random() for _ in range(sample_size)])
    bid_prices = np.array([[0 for _ in range(sample_size)]])
    bid_sizes = np.array([[0 for _ in range(sample_size)]])
    ask_prices = np.array([[0 for _ in range(sample_size)]])
    ask_sizes = np.array([[0 for _ in range(sample_size)]])
    return TickData(ts_arr, trade_prices, trade_sizes, bid_prices, bid_sizes, ask_prices, ask_sizes)


class ResultHolder:
    def __init__(self):
        self.value = None

    def set(self, value : BarData):
        self.value = value


class MultiThreadCorrectnessTest(unittest.TestCase):
    def setUp(self):
        self.raw_data = generate_random_ticks(1000)

    def test_time_sampling_correctness(self):
        intervals = [timedelta(seconds = s) for s in [1, 7, 13, 17, 21, 119]]
        seq_results = [sampler.time_sample_tick_to_bar(self.raw_data, interval) for interval in intervals]

        def sample_into_holder(raw_data : TickData, t : timedelta, holder : ResultHolder):
            result = sampler.time_sample_tick_to_bar(raw_data, t)
            holder.set(result)

        holders = [ResultHolder() for _ in range(len(intervals))]
        workers: List[threading.Thread] = [threading.Thread(target = sample_into_holder, args = (self.raw_data, interval, holder))
                                           for interval, holder in zip(intervals, holders)]
        _ = [worker.start() for worker in workers]
        _ = [worker.join() for worker in workers]
        par_results: List[BarData] = [holder.value for holder in holders]

        for seq_result, par_result in zip(seq_results, par_results):
            self.assertTrue(all(seq_result.timestamps == par_result.timestamps))
            self.assertTrue(all(seq_result.close_price == par_result.close_price))
            self.assertTrue(all(seq_result.volume == par_result.volume))
            self.assertTrue(all(seq_result.ticks == par_result.ticks))

    def test_volume_sampling_correctness(self):
        volumes = [1,7, 11, 13,19, 127]
        seq_results = [sampler.volume_sample_to_bar(self.raw_data, vol) for vol in volumes]

        def sample_into_holder(raw_data : TickData, v : int, holder : ResultHolder):
            result = sampler.volume_sample_to_bar(raw_data, v)
            holder.set(result)

        holders = [ResultHolder() for _ in range(len(volumes))]
        workers: List[threading.Thread] = [
            threading.Thread(target=sample_into_holder, args=(self.raw_data, interval, holder))
            for interval, holder in zip(volumes, holders)]
        _ = [worker.start() for worker in workers]
        _ = [worker.join() for worker in workers]
        par_results: List[BarData] = [holder.value for holder in holders]

        for seq_result, par_result in zip(seq_results, par_results):
            self.assertTrue(all(seq_result.timestamps == par_result.timestamps))
            self.assertTrue(all(seq_result.close_price == par_result.close_price))
            self.assertTrue(all(seq_result.volume == par_result.volume))
            self.assertTrue(all(seq_result.ticks == par_result.ticks))

    def test_tick_sampling_correctness(self):
        ticks = [1, 7, 11, 13,19, 127]
        seq_results = [sampler.tick_sample_to_bar(self.raw_data, tick) for tick in ticks]

        def sample_into_holder(raw_data : TickData, v : int, holder : ResultHolder):
            result = sampler.tick_sample_to_bar(raw_data, v)
            holder.set(result)

        holders = [ResultHolder() for _ in range(len(ticks))]
        workers: List[threading.Thread] = [
            threading.Thread(target=sample_into_holder, args=(self.raw_data, interval, holder))
            for interval, holder in zip(ticks, holders)]
        _ = [worker.start() for worker in workers]
        _ = [worker.join() for worker in workers]
        par_results: List[BarData] = [holder.value for holder in holders]

        for seq_result, par_result in zip(seq_results, par_results):
            self.assertTrue(all(seq_result.timestamps == par_result.timestamps))
            self.assertTrue(all(seq_result.close_price == par_result.close_price))
            self.assertTrue(all(seq_result.volume == par_result.volume))
            self.assertTrue(all(seq_result.ticks == par_result.ticks))