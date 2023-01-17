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


import heapq
from collections import defaultdict

class Order:
    def __init__(self, trader_id, order_id, order_type, price, quantity):
        self.trader_id = trader_id
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.timestamp = datetime.datetime.now()

    def __lt__(self, other):
        if self.price != other.price:
            return self.price < other.price
        return self.order_id < other.order_id

class LimitOrderBook:
    def __init__(self):
        self.order_id_counter = 0
        self.bids = defaultdict(list) # bids are stored in a dictionary with the price as the key and the quantity as the value
        self.asks = defaultdict(list) # asks are stored in a dictionary with the price as the key and the quantity as the value
        self.order_dict = {}
        self.bid_history = [] # list to store the history of bids
        self.ask_history = [] # list to store the history of asks

    def add_order(self, trader_id, order_type, price, quantity):
        self.order_id_counter += 1
        order = Order(trader_id,self.order_id_counter, order_type, price, quantity)
        self.order_dict[self.order_id_counter] = order
        if order_type == "bid":
            heapq.heappush(self.bids[price], order) #(quantity, trader_id, self.order_id_counter))
        elif order_type == "ask":
            heapq.heappush(self.asks[price], order) #(quantity, trader_id, self.order_id_counter))
        else:
            raise ValueError("Invalid order type")
    #   return order.order_id

    def remove_order(self, order_id):
        order = self.order_dict[order_id]
        if order.order_type == "bid":
            self.bids[order.price].remove(order) # (order.quantity, trader_id, order_id))
            if not self.bids[order.price]:
                del self.bids[order.price]
        elif order.order_type == "ask":
            self.asks[order.price].remove(order) # (order.quantity, trader_id, order_id))
            if not self.asks[order.price]:
                del self.asks[order.price]
        else:
            raise ValueError("Invalid order type")
        del self.order_dict[order_id]

    def modify_order(self, order_id, new_price, new_quantity):
        order = self.order_dict[order_id]
        if order.order_type == "bid":
            self.bids[order.price].remove(order) # (order.quantity, trader_id, order_id))
            self.add_order(order.trader_id, order.order_type, new_price, new_quantity)

    # def match_orders(self):
    #     best_bid = self.get_best_bid()
    #     best_ask = self.get_best_ask()
    #     while best_bid[0] >= best_ask[0]:
    #         bid_order = self.order_dict[best_bid[1]]
    #         ask_order = self.order_dict[best_ask[1]]
    #         trade_qty = min(bid_order.quantity, ask_order.quantity)
    #         bid_order.quantity -= trade_qty
    #         ask_order.quantity -= trade_qty
    #         print(f"Trade executed: {trade_qty} shares at {best_ask[0]}")
    #         if bid_order.quantity == 0:
    #             self.remove_order(best_bid[1])
    #         if ask_order.quantity == 0:
    #             self.remove_order(best_ask[1])
    #         best_bid = self.get_best_bid()
    #         best_ask = self.get_best_ask()
