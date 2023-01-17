# Limit Order Book

A limit order book (LOB) is a mechanism that organizes buy and sell orders, sent to a exchange, by agents.
The Limit Order Book (LOB) supports three basic instructions: insert, cancel and modify. Insert initiate a new order, cancel remove an existing order and modify change some of the parameters of the existing order.

### LOB pipeline

- [ ] A trader sends an order to the exchange. Each trader has a unique identifier. The order must have the following fields:
		- [ ] trader id
		- [ ] order id
		- [ ] side (buy or sell)
		- [ ] order type
			- [ ] limit	
			- [ ] market
			- [ ] peg
			- [ ] iceberg
			- [ ] hidden
			- [ ] stop
			- [ ] trailing stop
		- [ ] price
		- [ ] quantity
		- [ ] life duration
		- [ ] time stamp.

- [ ] Once the order arrives at the exchange, it must be registered in the LOB. The LOB must be able to handle the following instructions:
		- [ ] insert
		- [ ] cancel
		- [ ] modify
