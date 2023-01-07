"""Script that implements the Limit Order Book (LOB) class.

The LOB class is used to store the order book of a financial instrument.
It supports the following operations: insert, modify and cancel.
"""

import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 6

class LOB:
    """Implements the LOB."""
    def __init__(self, asset,max_size=1000):
        """Initializes the LOB."""
        self.asset = asset
        self.max_size = max_size
        self.bids = np.zeros((max_size, 2))
        self.asks = np.zeros((max_size, 2))
        self.bid_size = 0
        self.ask_size = 0
    
    def insert(price, quantity):

1.1 + 2.2
one = Decimal(1.1)
two = Decimal(2.2)
one
two
one + two 
