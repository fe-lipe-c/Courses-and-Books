"""Notebook to explore the open and close B3 auctions."""

import pandas as pd
import altair as alt
from utils import query, auction


df_open = auction("PETR4", open=True)
df_open
df_close = auction("PETR4", open=False)
df_close

df_auction = pd.DataFrame()
# df_auction["trade_day"] = df_open["trade_time"].dt.date
df_auction["open_vol"] = df_open["volume"]
df_auction["close_vol"] = df_close["volume"]

df_auction

chart_auction = (
    alt.Chart(df_auction)
    .mark_circle()
    .encode(
        alt.X("open_vol:Q"),
        alt.Y("close_vol:Q"),
    )
)

chart_auction.save("chart_auction.html")


# 0    PETR4 2020-02-10 18:13:07.237  29.13   6486400  188948832.0
# 1    PETR4 2020-02-11 18:07:17.863  29.48   4147800  122277144.0
# 2    PETR4 2020-02-12 18:50:04.477  30.13      8300     250079.0
# 3    PETR4 2020-02-13 18:08:18.907  29.72   4260700  126628004.0
# 4    PETR4 2020-02-14 18:11:04.903  29.42   2778300   81737586.0

# 0    PETR4 2020-02-10 10:12:04.693  28.89    143500   4145715.0
# 1    PETR4 2020-02-11 10:10:15.463  29.40    557700  16396380.0
# 2    PETR4 2020-02-12 10:09:57.047  29.64    245700   7282548.0
# 3    PETR4 2020-02-13 10:09:37.957  29.77    161000   4792970.0
# 4    PETR4 2020-02-14 10:07:15.307  29.86    236700   7067862.0

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
