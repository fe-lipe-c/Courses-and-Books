The Brazilian stock exchange (B3) has the following [trading hours](https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/) in the spot market:

|                                           | Início      | Fim         |
| -----------                               | ----------- | ----------- |
| **Cancelamento de Ofertas**               | 09:30       | 09:45       |
| **Pré-Abertura**                          | 09:45       | 10:00       |
| **Negociação**                            | 10:00       | 17:55       |
| **Call de Fechamento**                    | 17:55       | 18:00       |
| **Cancelamento de Ofertas(After Market)** | 18:25       | 18:45       |

We have to types of financial data: (i) intraday quotes and (ii) intraday best bid and best ask.

When you look at, for example, for PRIO3 we get the following data:

Open Auction final price and volume
| ticker      | trade_time  | price  | quantity | 
| ----------- | ----------- | ----------- | ----------- |
 PRIO3 |2022-12-23 10:08:20.283 | 35.95  |   57400

Normal trading hours
| ticker      | trade_time              | price       | quantity    |
| ----------- | -----------             | ----------- | ----------- |
| PRIO3       | 2022-12-23 10:08:20.287 | 35.92       | 1000        |
| PRIO3       | 2022-12-23 10:08:20.297 | 35.90       | 200         |
| PRIO3       | 2022-12-23 10:08:20.360 | 35.75       | 6000        |
| PRIO3       | 2022-12-23 10:08:20.457 | 35.85       | 100         |
| PRIO3       | 2022-12-23 10:08:20.837 | 35.85       | 300         |
| PRIO3       | 2022-12-23 10:08:21.287 | 35.85       | 600         |
| PRIO3       | 2022-12-23 10:08:23.033 | 35.89       | 800         |
| PRIO3       | 2022-12-23 10:08:24.397 | 35.95       | 9000        |
| PRIO3       | 2022-12-23 10:08:24.580 | 35.96       | 3000        |
| PRIO3       | 2022-12-23 10:08:25.307 | 35.86       | 6200        |


Auction bids and asks
| spread_time             | bid         | ask         |
| -----------             | ----------- | ----------- |
| 2022-12-23 09:45:03.224 | 0.00        | 0.00        |
| 2022-12-23 09:45:03.225 | 0.00        | 35.26       |
| 2022-12-23 09:45:03.227 | 35.11       | 35.26       |
| 2022-12-23 09:45:03.232 | 35.05       | 35.26       |
| 2022-12-23 09:45:03.238 | 35.11       | 35.26       |
| ...                     | ...         | ...         |
| 2022-12-23 09:58:07.715 | 35.42       | 29.98       |
| 2022-12-23 09:58:44.633 | 0.00        | 29.98       |
| 2022-12-23 09:59:05.226 | 0.00        | 29.98       |
| 2022-12-23 09:59:43.391 | 35.26       | 29.98       |
| 2022-12-23 09:59:58.159 | 0.00        | 29.98       |

Trading hours (Negative Spreads)
| spread_time             | bid         | ask         |
| -----------             | ----------- | ----------- |
| 2022-12-23 10:00:02.488 | 0.00        | 29.98       |
| 2022-12-23 10:00:49.616 | 35.55       | 29.98       |
| 2022-12-23 10:00:57.987 | 0.00        | 29.98       |
| 2022-12-23 10:01:00.585 | 0.00        | 29.98       |
| 2022-12-23 10:01:05.007 | 40.88       | 29.98       |
| ...                     | ...         | ...         |
| 2022-12-23 10:08:07.657 | 36.00       | 29.98       |
| 2022-12-23 10:08:20.324 | 36.00       | 29.98       |
| 2022-12-23 10:08:20.326 | 36.00       | 33.00       |
| 2022-12-23 10:08:20.334 | 35.83       | 35.95       |
| 2022-12-23 10:08:20.349 | 35.78       | 35.90       |

As you can see, the spread in **2022-12-23 10:08:20.326** is negative, just like the previous ones, turning positive soon after. At this moment we already have normal trades, as can be seen at **2022-12-23 10:08:20.297**. 

