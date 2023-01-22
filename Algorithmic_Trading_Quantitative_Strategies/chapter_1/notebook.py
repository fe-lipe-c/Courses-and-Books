"""Notebook to explore  B3 data."""

import pandas as pd
import altair as alt
import clickhouse_driver


# - [ ] Intraday volume distribution ------------------------------------------

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)

asset = "PETR4"
start_data = "2022-01-03"
end_date = "2022-01-04"

# Select intraday data for a given asset, exlude the first row and last row for
# each day (open and close auction)

sql = f"""
SELECT * FROM (
SELECT
    ticker,
    trade_time,
    toFloat64(price) AS price,
    quantity,
    ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time) AS rn_
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
WHERE rn >= 2)
WHERE rn_ >= 2
"""

df_data = client.query_dataframe(sql)
df_data.sort_values(by=["trade_time"], inplace=True)
df_data.drop(columns=["rn_"], inplace=True)
df_data["volume"] = df_data["quantity"] * df_data["price"]
dates = df_data["trade_time"].dt.date.unique()
df_data
dates
dates = [str(i) for i in dates]
dates

chart_data = (
    alt.Chart(df_data)
    .transform_fold(dates, as_=["date", "volume"])
    .transform_density(
        density="volume",
        bandwidth=0.3,
        groupby=["date"],
        extent=[0, 1000000],
        counts=True,
        steps=10,
    )
    .mark_area()
    .encode(
        alt.X("volume:Q"),
        alt.Y("density:Q", stack="zero"),
        alt.Color("date:N"),
    )
    .properties(width=600, height=400)
)

chart_data.save("volume_density.html")

df_data

# from vega_datasets import data
#
# source = data.iris()
