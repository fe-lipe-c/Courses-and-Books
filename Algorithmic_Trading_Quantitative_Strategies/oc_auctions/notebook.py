"""Notebook to explore the open and close B3 auctions."""

import pandas as pd
import altair as alt
from utils import auction
import clickhouse_driver

#
df_open, df_close = auction("TRAD3")

# add colum with change relative to previous value
df_close

df_open["vol_pct_change"] = df_open["volume"].pct_change()
df_open["price_pct_change"] = df_open["price"].pct_change()

df_open[df_open["price_pct_change"] <= 0]
# concat the two dataframes

df_total = pd.concat([df_open, df_close])
df_total.sort_values(by="trade_time", inplace=True)
df_total

df_auction
df_total
df_open
df_close
# df_auction = pd.DataFrame()
# df_auction["trade_day"] = df_open["trade_time"].dt.date
# df_auction["open_vol"] = df_open["volume"]
# df_auction["close_vol"] = df_close["volume"]
#
# df_auction

chart_auction = (
    alt.Chart(df_auction)
    .mark_circle()
    .encode(
        alt.X("open_vol:Q"),
        alt.Y("close_vol:Q"),
    )
)

chart_auction.save("chart_auction.html")


# sql = """
# SELECT
#     ticker,
#     trade_time,
#     toFloat64(price) AS price,
#     quantity
# FROM tradeintraday
# WHERE
#     ticker = 'PETR4'
# LIMIT 37000
# """

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

desc_tabela = client.execute("DESCRIBE spread")

for col_tuple in desc_tabela:
    if "Decimal" in col_tuple[1]:
        print("ok")
    print([t for t in col_tuple if t not in ""])

sql = """
SELECT 
    ticker,
    spread_time,
    toFloat64(bid) AS bid,
    toFloat64(ask) AS ask
FROM spread
WHERE
    ticker = 'VALE3'
LIMIT 100
"""

df = client.query_dataframe(sql)
df.head(20)

#    ticker             spread_time     bid     ask
# 0   VALE3 2022-03-03 09:30:28.936   99.26   99.66
# 1   VALE3 2022-03-03 09:31:30.098   99.26   99.66
# 2   VALE3 2022-03-03 09:37:17.740   99.26   99.66
# 3   VALE3 2022-03-03 09:44:19.243   99.26   99.72
# 4   VALE3 2022-03-03 09:45:00.414   99.72   99.72
# 5   VALE3 2022-03-03 09:45:00.765   99.72   99.65
# 6   VALE3 2022-03-03 09:45:01.248   99.72   98.00
# 7   VALE3 2022-03-03 09:45:02.816   99.72   92.28
# 8   VALE3 2022-03-03 09:45:03.347   99.80   92.28
# 9   VALE3 2022-03-03 09:45:06.489  100.00   92.28
# 10  VALE3 2022-03-03 10:03:40.668  100.20  100.23
# 11  VALE3 2022-03-03 10:03:40.917  100.20  100.25

#       ticker              trade_time   price  quantity
# 0      VALE3 2022-03-03 10:03:40.603  100.20    278300
# 1      VALE3 2022-03-03 10:03:40.610  100.21       900
# 2      VALE3 2022-03-03 10:03:40.613  100.26       200
# 3      VALE3 2022-03-03 10:03:40.617  100.22      1600
# 4      VALE3 2022-03-03 10:03:40.623  100.22       500
#

sql = """
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity
FROM tradeintraday
WHERE
    ticker = 'VALE3'
AND trade_time BETWEEN '2022-03-03' AND '2022-03-04'
"""

df_alt = client.query_dataframe(sql)
df_alt

sql = f"""
SELECT * FROM (
    SELECT
        ticker,
        trade_time,
        toFloat64(price) AS price,
        quantity,
        ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time) AS rn
    FROM tradeintraday
    WHERE
        ticker = 'PETR4'
)
WHERE rn = 1
"""

print(sql.replace("trade_time", "trade_time DESC"))
print(sql)


asset = "TRAD3"
sql = f"""
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity
FROM tradeintraday
WHERE
    ticker = '{asset}'
"""
# AND EXTRACT(hour from trade_time) < (SELECT DATE_ADD(MIN(trade_time), INTERVAL 1 HOUR) FROM tradeintraday WHERE DATE(trade_time) = DATE(trade_time))
# """
#
client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

df = client.query_dataframe(sql)
df.sort_values(by="trade_time", inplace=True)
df[df["trade_time"] <= "2021-07-29"]


# SELECT
#     ticker,
#     trade_time,
#     toFloat64(price) AS price,
#     quantity
# FROM tradeintraday
# WHERE ticker = 'TRAD3'
# AND EXTRACT(HOUR FROM trade_time) <= (SELECT MIN(EXTRACT(HOUR FROM trade_time)) FROM tradeintraday WHERE ticker = 'TRAD3')
sql_teste = """
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity
FROM tradeintraday
WHERE ticker = 'TRAD3'
AND EXTRACT(HOUR FROM trade_time) <= (SELECT MIN(EXTRACT(HOUR FROM trade_time)) FROM tradeintraday WHERE ticker = 'TRAD3') 
"""
# AND EXTRACT(HOUR FROM trade_time) <= (SELECT MIN(EXTRACT(HOUR FROM trade_time)) FROM tradeintraday WHERE DATE_TRUNC('day', trade_time) = DATE_TRUNC('day', trade_time))
# """

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

df = client.query_dataframe(sql_teste)

df.sort_values(by="trade_time", inplace=True)
df
df[df["trade_time"] <= "2021-07-29"]

sql_new = """
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity
FROM tradeintraday
WHERE ticker = 'TRAD3'
AND EXTRACT(HOUR FROM trade_time) <= 10
"""

df_new = client.query_dataframe(sql_new)

df_new.sort_values(by="trade_time", inplace=True)
df_new.reset_index(drop=True, inplace=True)
df_new[(df_new["trade_time"] <= "2023-01-05") & (df_new["trade_time"] >= "2023-01-04")]
df_new


df = df_new.copy()
df = df.set_index("trade_time")
df["date"] = df.index.date
first_prices = df.groupby(by="date")["price"].first()
last_prices = df.groupby(by="date")["price"].last()
df_prices = pd.DataFrame()
df_prices["date"] = last_prices.index
df_prices["first_price"] = first_prices.values
df_prices["last_price"] = last_prices.values
df_prices["return"] = df_prices["last_price"] / df_prices["first_price"] - 1
df_prices
df_open = df_open[df_open["trade_time"].dt.hour <= 11]
df_open.reset_index(drop=True, inplace=True)
df_open["return"] = df_prices["return"]
df_open

df["price_pct_change"] = (last_prices - first_prices) / first_prices
df.dropna(inplace=True)
df
