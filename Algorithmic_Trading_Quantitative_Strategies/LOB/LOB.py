"""Script that implements the Limit Order Book (LOB) class.

The LOB class is used to store the order book of a financial instrument.
It supports the following operations: insert, modify and cancel.
"""

import numpy as np
import heapq
from collections import defaultdict
from decimal import Decimal, getcontext
import datetime
from order import Order

getcontext().prec = 6

class LimitOrderBook:
    """Class representing a limit order book."""

    def __init__(self):
        """Initialize the limit order book.

        Set the following attributes: order_id_counter, bids, asks, order_dict.
        """

        self.order_id_counter = 0
        self.bids = defaultdict(list)  # price as key and quantity as value
        self.asks = defaultdict(list)  # price as key and quantity as value
        self.order_dict = {}
        self.bid_history = []  # list to store the history of bids
        self.ask_history = []  # list to store the history of asks
        self.outstanding_bid = 0
        self.outstanding_ask = np.inf

    def add_order(self, trader_id, order_side, price, quantity):
        """Add an order to the limit order book."""
        self.order_id_counter += 1
        order = Order(
            trader_id,
            self.order_id_counter,
            order_side,
            price,
            quantity,
        )
        self.order_dict[self.order_id_counter] = order
        if order_side == "bid":
            if order.price > self.outstanding_bid:
                m

            heapq.heappush(self.bids[price], order)
        elif order_side == "ask":
            heapq.heappush(self.asks[price], order)
        else:
            raise ValueError("Invalid order side")

    #   return order.order_id

    def remove_order(self, order_id):
        """Remove an order from the limit order book."""
        order = self.order_dict[order_id]
        if order.order_side == "bid":
            self.bids[order.price].remove(
                order
            )  # (order.quantity, trader_id, order_id))
            if not self.bids[order.price]:
                del self.bids[order.price]
        elif order.order_side == "ask":
            self.asks[order.price].remove(
                order
            )  # (order.quantity, trader_id, order_id))
            if not self.asks[order.price]:
                del self.asks[order.price]
        else:
            raise ValueError("Invalid order side")
        del self.order_dict[order_id]

    def modify_order(self, order_id, new_price, new_quantity):
        """Modify an order in the limit order book."""
        order = self.order_dict[order_id]
        if order.order_side == "bid":
            self.bids[order.price].remove(
                order
            )  # (order.quantity, trader_id, order_id))
            self.add_order(
                order.trader_id,
                order.order_side,
                new_price,
                new_quantity,
            )

    def match_orders(self,order):
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
