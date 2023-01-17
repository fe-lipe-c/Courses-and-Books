"""Notebook to LOB application."""

from LOB import LimitOrderBook, Order


trader_id = [2, 0, 4, 3, 1]
ord_id = [0, 1, 2, 3, 4]
order_type = ["bid", "ask", "bid", "ask", "bid"]
price = [100, 105, 102, 104, 104]
quantity = [1000, 500, 800, 1000, 500]

order_0 = Order(trader_id[0], ord_id[0], order_type[0], price[0], quantity[0])
order_1 = Order(trader_id[1], ord_id[1], order_type[1], price[1], quantity[1])
order_2 = Order(trader_id[2], ord_id[2], order_type[2], price[2], quantity[2])

order_1 < order_2

lob = LimitOrderBook()

lob.add_order(trader_id[0], order_type[0], price[0], quantity[0])
lob.add_order(trader_id[1], order_type[1], price[1], quantity[1])

lob.bid_history
lob.order_dict[2].price
