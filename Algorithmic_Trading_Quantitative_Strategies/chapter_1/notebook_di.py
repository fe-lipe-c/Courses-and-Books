"""Notebook to explore B3 tickers."""


import altair as alt
import pandas as pd
import numpy as np
import clickhouse_driver
import datetime

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

# 5GTK11
ticks_b3 = {}
asset_search = [
    "^DI1",
    "^IND",
    "WIN___",
    "DOL___",
    "DOL___P%",
    "DOL___C%",
    "WDO___",
    "WDO___P%",
    "WDO___C%",
    "^.{4}[0-9]$",  # 4 letters + 1 number
    "^.{4}[0-9]T$",  # 4 letters + 1 number + T
    "^.{4}[0-9]F$",  # 4 letters + 1 number + F
    "^.{4}11$",  # Unit, ETF, FII
    "^[A-Z]{5}[0-9]",  # Options
]
list_asset_search = "|".join(asset_search)
list_asset_search

# asset = "^[^IND|WIN___|^DI1|WDO___]"
asset = "^[^.{4}11$]"
month = "12"
day_start = "23"
day_end = "24"
start_data = f"2022-{month}-{day_start}"
end_date = f"2022-{month}-{day_end}"

sql = f"""
SELECT DISTINCT
    ticker,
    trade_time
FROM tradeintraday
WHERE match(ticker,'{asset}')
AND trade_time Between '{start_data}' AND '{end_date}'
"""

df_data = client.query_dataframe(sql)
# df_data.sort_values("trade_time", inplace=True)
df_data.reset_index(drop=True, inplace=True)
contracts = df_data["ticker"].unique()

# len(df_data[df_data["ticker"].str.startswith("PETR")]["ticker"].unique())
df_data
"5GTK11" in contracts
len(contracts)

df_data.sort_values("ticker", inplace=True)
df_data[df_data["ticker"] == "PETR3"]

ticks_b3["DOL"] = contracts
ticks_b3


asset = "DOLH20"

sql = f"""
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity
FROM tradeintraday
WHERE
    ticker LIKE '{asset}'
"""

df_data = client.query_dataframe(sql)

df_data

#         ticker              trade_time   price  quantity
# 0       DOLH20 2020-02-10 09:00:39.783  4315.5       290
# 1       DOLH20 2020-02-10 09:00:39.877  4313.5        10
# 2       DOLH20 2020-02-10 09:00:42.277  4313.5         5
# 3       DOLH20 2020-02-10 09:00:42.280  4313.5         5
# 4       DOLH20 2020-02-10 09:00:42.557  4313.5         5
# ...        ...                     ...     ...       ...
# 173163  DOLH20 2020-02-28 17:54:28.923  4499.0        10
# 173164  DOLH20 2020-02-28 17:55:33.317  4499.0       875
# 173165  DOLH20 2020-02-28 18:16:27.343  4498.5        20
# 173166  DOLH20 2020-02-28 18:17:31.313  4498.5       105
# 173167  DOLH20 2020-02-28 18:25:00.363  4499.0        20

#            ticker              trade_time   price  quantity
# 0   DOLH20C004300 2020-02-10 09:44:08.353   62.00         5
# 1   DOLH20C004300 2020-02-10 10:20:28.187   52.29       140
# 2   DOLH20C004300 2020-02-10 12:47:37.497   56.60       415
# 3   DOLH20C004300 2020-02-10 15:06:03.290   53.50        10
# 4   DOLH20C004300 2020-02-10 15:06:28.780   53.50        10
# 5   DOLH20C004300 2020-02-10 15:08:07.457   53.50         5
# 6   DOLH20C004300 2020-02-10 15:09:13.950   53.50         5
# 7   DOLH20C004300 2020-02-10 15:15:24.730   53.50         5
# 8   DOLH20C004300 2020-02-10 15:15:43.723   54.00        10
# 9   DOLH20C004300 2020-02-10 15:15:59.237   55.00         5
# 10  DOLH20C004300 2020-02-10 15:18:53.260   55.00         5
# 11  DOLH20C004300 2020-02-10 15:25:42.573   56.00        10
# 12  DOLH20C004300 2020-02-10 15:32:32.223   54.90       100
# 13  DOLH20C004300 2020-02-11 16:21:49.173   58.00       550
# 14  DOLH20C004300 2020-02-13 14:03:10.927   61.00        10
# 15  DOLH20C004300 2020-02-14 13:07:42.337   42.00        10
# 16  DOLH20C004300 2020-02-14 16:23:50.320   35.00       100
# 17  DOLH20C004300 2020-02-17 10:34:31.853   41.00        15
# 18  DOLH20C004300 2020-02-18 10:45:09.167   60.20        10
# 19  DOLH20C004300 2020-02-19 17:58:52.213   69.80        50
# 20  DOLH20C004300 2020-02-21 11:06:04.897  100.00       300
# 21  DOLH20C004300 2020-02-21 11:21:32.587  101.50       150
# 22  DOLH20C004300 2020-02-21 11:31:03.137  100.00       150
# 23  DOLH20C004300 2020-02-26 16:17:17.283  140.00        10
# 24  DOLH20C004300 2020-02-26 16:25:20.343  145.00         5
# 25  DOLH20C004300 2020-02-26 16:26:06.810  143.00         5
# 26  DOLH20C004300 2020-02-26 16:27:10.433  142.00        15
# 27  DOLH20C004300 2020-02-27 09:07:10.537  148.44        15
# 28  DOLH20C004300 2020-02-27 15:07:43.580  155.00         5
