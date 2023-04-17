import numpy as np
from dataclasses import dataclass


@dataclass
class TickData:
    timestamps : np.array
    trade_prices : np.array
    trade_sizes : np.array
    bid_prices : np.array
    bid_sizes : np.array
    ask_prices : np.array
    ask_sizes : np.array
