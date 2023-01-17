"""Notebook to LOB application."""

from LOB import LimitOrderBook
from order import Order

# trader_id, order_id, side, order_type, price, quantity, life_duration

trader_id = [2, 0, 4, 3, 1]
order_side = ["buy", "sell", "buy", "sell", "buy"]
order_type = ["limit", "limit", "limit", "market", "limit"]
price = [100, 105, 102, 104, 104]
quantity = [1000, 500, 800, 1000, 500]
order_lifetime = [10, 10, 20, 30, 10]
# order_id = [0, 1, 2, 3, 4]

order_0 = Order(
    trader_id[0], order_side[0], order_type[0], price[0], quantity[0], order_lifetime[0]
)
order_1 = Order(
    trader_id[1], order_side[1], order_type[1], price[1], quantity[1], order_lifetime[1]
)
order_2 = Order(
    trader_id[2], order_side[2], order_type[2], price[2], quantity[2], order_lifetime[2]
)

order_0 < order_2
print(order_0)

lob = LimitOrderBook()

lob.add_order(trader_id[0], order_type[0], price[0], quantity[0])
lob.add_order(trader_id[1], order_type[1], price[1], quantity[1])

lob.bid_history
lob.order_dict[2].price
