"""Class of the order object."""

from decimal import Decimal, getcontext
import datetime

getcontext().prec = 6


class Order:
    """Class representing an order in the limit order book."""

    def __init__(
        self, trader_id, order_id, side, order_type, price, quantity, life_duration
    ):
        """Initialize an order."""
        self.valid_order_types = {
            "limit": "An order to buy or sell a security at a specific price or better.",
            "market": "An order to buy or sell a security at the best available current market price.",
            "peg": "An order that is pegged to the market and adjusts automatically with the market.",
            "iceberg": "An order that hides a portion of the order quantity and only displays a portion of it.",
            "hidden": "An order that is not visible to other traders.",
            "stop": "An order that becomes a market order when the specified stop price is reached.",
            "trailing stop": "An order that becomes a market order when the specified trailing amount or percentage is reached.",
        }
        self.valid_sides = ["buy", "sell"]

        if order_type not in self.valid_order_types:
            raise ValueError(
                f"Invalid order type {order_type}. Must be one of {self.valid_order_types.keys()}"
            )
        if side not in self.valid_sides:
            raise ValueError(f"Invalid side {side}. Must be one of {self.valid_sides}")

        self.trader_id = trader_id
        self.order_id = order_id
        self.side = side
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.life_duration = life_duration
        self.timestamp = datetime.datetime.now()

    def __lt__(self, other):
        """Compare two orders first by price and then by order id."""
        if self.price != other.price:
            return self.price < other.price
        return self.order_id < other.order_id
