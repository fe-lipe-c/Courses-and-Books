"""Notebook to explore future contracts."""


import altair as alt
import clickhouse_driver

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

# AND trade_time BETWEEN '{start_data}' AND '{end_date}'
# """

df_data = client.query_dataframe(sql)
df_data.sort_values("trade_time", inplace=True)
df_data["ticker"].unique()
df_data
