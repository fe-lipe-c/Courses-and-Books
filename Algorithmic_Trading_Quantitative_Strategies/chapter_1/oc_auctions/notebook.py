"""Notebook to explore the open and close B3 auctions."""

import pandas as pd
import altair as alt
from utils import auction
import clickhouse_driver

#
df_open, df_close = auction("PRIO3")

# add colum with change relative to previous value
df_close
df_open[1:]

# Plot price change between open auctions and delta time price variation

chart_open = (
    alt.Chart(df_open[1:])
    .mark_point(size=60, color="red")
    .encode(
        alt.X("price_pct_change"),
        alt.Y("return_delta"),
    )
    .properties(width=800, height=800)
)

chart_open.save("chart_open.html")

# Plot delta time change versus open auction volume

df_open_posive = df_open[df_open["price_pct_change"] >= 0]

chart_open_positive = (
    alt.Chart(df_open_posive)
    .mark_circle(size=60)
    .encode(
        alt.X("vol_pct_change", title="Volume Change (%)"),
        alt.Y("return_delta", title="Delta Change (%)"),
    )
    .properties(width=800, height=800)
)

chart_open_positive.save("chart_open_positive.html")


df_open_negative = df_open[df_open["price_pct_change"] < 0]

chart_open_negative = (
    alt.Chart(df_open_negative)
    .mark_circle(size=60)
    .encode(
        alt.X("price_pct_change", title="Price Change (%)"),
        alt.Y("vol_pct_change", title="Volume Change (%)"),
    )
    .properties(width=800, height=800)
)

chart_open_negative.save("chart_open_negative.html")

# concat the two dataframes

df_total = pd.concat([df_open, df_close])
df_total.sort_values(by="trade_time", inplace=True)
df_total

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

# SPREAD ------

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

# ---------------
