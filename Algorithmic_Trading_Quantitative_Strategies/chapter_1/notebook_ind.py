"""Notebook to explore future contracts."""


import altair as alt
import pandas as pd
import numpy as np
import clickhouse_driver
import datetime

# - [ ] Figure 1.4: Futures Rolling

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

asset = "IND%"
month = "12"
day_start = "23"
day_end = "24"
start_data = f"2022-{month}-{day_start}"
end_date = f"2022-{month}-{day_end}"

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
df_data.sort_values("trade_time", inplace=True)
df_data.reset_index(drop=True, inplace=True)
contracts = df_data["ticker"].unique()
df_data["volume"] = df_data["price"] * df_data["quantity"]

list_df_ind = []

for i, future_contract in enumerate(contracts):
    print(i)
    df_temp = df_data[df_data["ticker"] == future_contract]
    ano = int(str(df_temp[-1:]["trade_time"].values[0])[:4])
    mes = int(str(df_temp[-1:]["trade_time"].values[0])[5:7])
    dia = int(str(df_temp[-1:]["trade_time"].values[0])[8:10])

    df_temp = df_temp.append(
        {
            "ticker": "----",
            "trade_time": datetime.datetime(ano, mes, dia, 19, 0),
            "price": 0,
            "quantity": 0,
            "volume": 0,
        },
        ignore_index=True,
    )
    df_temp = df_temp.resample("1D", on="trade_time").sum()
    df_temp = df_temp[df_temp["price"] > 0.1]
    df_temp["ticker"] = future_contract
    df_temp["trade_time"] = df_temp.index
    df_temp["moving_average"] = df_temp["volume"].rolling(5).mean()
    df_temp.reset_index(inplace=True, drop=True)
    list_df_ind.append(df_temp)

df_temp
df_ind = pd.concat(list_df_ind, axis=0).reset_index(drop=True)
df_sample = df_ind[
    (df_ind["trade_time"] > "2022-01-01") & (df_ind["trade_time"] < "2023-01-25")
]

chart_ind = (
    alt.Chart(df_sample, title="IND 5 day Volume Moving Average")
    .mark_area(opacity=0.8, interpolate="monotone")
    .encode(
        alt.X("trade_time:T"), alt.Y("moving_average:Q", stack=None), color="ticker:N"
    )
    .properties(width=800, height=400)
)
chart_ind.save("chart_ind.html")
