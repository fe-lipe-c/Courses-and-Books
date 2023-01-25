"""Notebook to explore  B3 data."""

from utils import (
    volume_distribution,
    vol_distances,
    trade_distribution,
    trade_distances,
)
import clickhouse_driver
import pandas as pd

# - [ ] Intraday volume distribution ------------------------------------------

asset = "PRIO3"
month = "12"
day_start = "23"
day_end = "24"
start_data = f"2022-{month}-{day_start}"
end_date = f"2022-{month}-{day_end}"

list_days = (
    pd.date_range(start=start_data, end=end_date, freq="D")
    .strftime("%Y-%m-%d")
    .tolist()
)

df_vol, df_data = volume_distribution(
    asset,
    start_data,
    end_date,
    interval="30min",
    factor=1,
)

dist_list = vol_distances(df_data, list_days)

# - [ ] Disbribution of trade size

asset = "PRIO3"
month = "05"
day_start = "23"
day_end = "28"
start_data = f"2022-{month}-{day_start}"
end_date = f"2022-{month}-{day_end}"

list_days = (
    pd.date_range(start=start_data, end=end_date, freq="D")
    .strftime("%Y-%m-%d")
    .tolist()
)

df_trades = trade_distribution(
    asset,
    start_data,
    end_date,
    max_domain=1000,
    opacity=0.7,
)

dist_list = trade_distances(df_trades, list_days)

df_distance_ = pd.DataFrame()

for i in dist_list.keys():
    df_distance_[i] = dist_list[i]

df_distance_.index = df_distance_.columns


# - [ ] Intraday spread distribution

# SPREAD ------

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

# The first thing to do is to exclude the spreads associated  with the opening
# and closing auctions. This information is available in the intraday table.

sql = f"""
SELECT 
    ticker,
    spread_time,
    toFloat64(bid) AS bid,
    toFloat64(ask) AS ask
FROM spread
WHERE
    ticker = '{asset}'
AND spread_time BETWEEN '{start_data}' AND '{end_date}'
"""

df_spread = client.query_dataframe(sql)
df_spread.sort_values(by=["spread_time"], inplace=True)
df_spread.reset_index(drop=True, inplace=True)
df_spread.head(150)
df_spread


sql_open_auction = f"""
SELECT *
FROM (
    SELECT
        ticker,
        trade_time,
        toFloat64(price) AS price,
        quantity,
        ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time) AS rn
    FROM tradeintraday
    WHERE
        ticker = '{asset}'
    AND trade_time BETWEEN '{start_data}' AND '{end_date}'
)
WHERE rn = 1
"""

sql_close_auction = f"""
SELECT *
FROM (
    SELECT
        ticker,
        trade_time,
        toFloat64(price) AS price,
        quantity,
        ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time DESC) AS rn
    FROM tradeintraday
    WHERE
        ticker = '{asset}'
    AND trade_time BETWEEN '{start_data}' AND '{end_date}'
)
WHERE rn = 1
"""

df_open = client.query_dataframe(sql_open_auction)
df_open.drop(columns=["rn"], inplace=True)
df_close = client.query_dataframe(sql_close_auction)
df_close.drop(columns=["rn"], inplace=True)

df_open
df_close

list_open = df_open["trade_time"].tolist()
list_close = df_close["trade_time"].tolist()


# df[(df["spread_time"] <= list_open[0]) | (df["spread_time"] >= list_close[0])]
# df.tail(30)

# df_spread_trades = df_spread[
#     (df_spread["spread_time"] > list_open[0]) & (df_spread["spread_time"] < list_close[0])
#     | (df_spread["spread_time"] > list_open[1]) & (df_spread["spread_time"] < list_close[1])
#     | (df_spread["spread_time"] > list_open[2]) & (df_spread["spread_time"] < list_close[2])
#     | (df_spread["spread_time"] > list_open[3]) & (df_spread["spread_time"] < list_close[3])
#     | (df_spread["spread_time"] > list_open[4]) & (df_spread["spread_time"] < list_close[4])
# ]


df_spread_trades = df_spread[
    (df_spread["spread_time"] > list_open[0])
    & (df_spread["spread_time"] < list_close[0])
]
df_spread_trades

df_spread_trades["spread_size"] = df_spread_trades["ask"] - df_spread_trades["bid"]

df_spread_trades[df_spread_trades["spread_size"] < 0].head(100)

# Trading hours
#   	                                    Início 	Fim
# Cancelamento de Ofertas 	                09:30 	09:45
# Pré-Abertura                              09:45 	10:00
# Negociação                                10:00 	17:55
# Call de Fechamento                        17:55 	18:00
# Cancelamento de Ofertas(After Market)     18:25 	18:45

# Data

# Open Auction

df_open

#   ticker              trade_time  price  quantity
# 0  PRIO3 2022-12-23 10:08:20.283  35.95     57400

# First trades

df_data.head(10)

#   ticker              trade_time  price  quantity    volume        date
# 0  PRIO3 2022-12-23 10:08:20.287  35.92      1000   35920.0  2022-12-23
# 1  PRIO3 2022-12-23 10:08:20.297  35.90       200    7180.0  2022-12-23
# 2  PRIO3 2022-12-23 10:08:20.360  35.75      6000  214500.0  2022-12-23
# 3  PRIO3 2022-12-23 10:08:20.457  35.85       100    3585.0  2022-12-23
# 4  PRIO3 2022-12-23 10:08:20.837  35.85       300   10755.0  2022-12-23
# 5  PRIO3 2022-12-23 10:08:21.287  35.85       600   21510.0  2022-12-23
# 6  PRIO3 2022-12-23 10:08:23.033  35.89       800   28712.0  2022-12-23
# 7  PRIO3 2022-12-23 10:08:24.397  35.95      9000  323550.0  2022-12-23
# 8  PRIO3 2022-12-23 10:08:24.580  35.96      3000  107880.0  2022-12-23
# 9  PRIO3 2022-12-23 10:08:25.307  35.86      6200  222332.0  2022-12-23

# Auction Spreads
df_spread[df_spread["spread_time"] <= "2022-12-23 10:00"]

#       ticker             spread_time    bid    ask
# 0      PRIO3 2022-12-23 09:45:03.224   0.00   0.00
# 1      PRIO3 2022-12-23 09:45:03.225   0.00  35.26
# 2      PRIO3 2022-12-23 09:45:03.227  35.11  35.26
# 3      PRIO3 2022-12-23 09:45:03.232  35.05  35.26
# 4      PRIO3 2022-12-23 09:45:03.238  35.11  35.26
# ...      ...                     ...    ...    ...
# 12029  PRIO3 2022-12-23 09:58:07.715  35.42  29.98
# 12030  PRIO3 2022-12-23 09:58:44.633   0.00  29.98
# 12031  PRIO3 2022-12-23 09:59:05.226   0.00  29.98
# 12032  PRIO3 2022-12-23 09:59:43.391  35.26  29.98
# 12033  PRIO3 2022-12-23 09:59:58.159   0.00  29.98

# Trading hours spreads (Negative spreads)

df_spread[
    (df_spread["spread_time"] >= "2022-12-23 10:00")
    & (df_spread["spread_time"] <= "2022-12-23 10:08:20.350")
]

#       ticker             spread_time    bid    ask
# 64     PRIO3 2022-12-23 10:00:02.488   0.00  29.98
# 65     PRIO3 2022-12-23 10:00:49.616  35.55  29.98
# 66     PRIO3 2022-12-23 10:00:57.987   0.00  29.98
# 67     PRIO3 2022-12-23 10:01:00.585   0.00  29.98
# 68     PRIO3 2022-12-23 10:01:05.007  40.88  29.98
# ...      ...                     ...    ...    ...
# 12119  PRIO3 2022-12-23 10:08:07.657  36.00  29.98
# 12120  PRIO3 2022-12-23 10:08:20.324  36.00  29.98
# 12121  PRIO3 2022-12-23 10:08:20.326  36.00  33.00
# 12122  PRIO3 2022-12-23 10:08:20.334  35.83  35.95
# 12123  PRIO3 2022-12-23 10:08:20.349  35.78  35.90
