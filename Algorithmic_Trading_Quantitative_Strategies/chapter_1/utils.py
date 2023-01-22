"""General tools and functions to be used in the project."""

import altair as alt
import clickhouse_driver

# - [ ] Intraday volume distribution ------------------------------------------

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)


def volume_distribution(asset, start_data, end_date, interval="1h", factor=1000000):

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
    df_data["date"] = df_data["trade_time"].dt.date
    df_data["date"] = df_data["date"].astype("str")

    new_df = df_data.resample(f"{interval}", on="trade_time", origin="end").agg(
        {"volume": "sum"}
    )
    new_df.reset_index(inplace=True)
    new_df["date"] = new_df["trade_time"].dt.date
    new_df["date"] = new_df["date"].astype("str")
    new_df["volume"] = new_df["volume"] / factor
    new_df["volume"] = new_df["volume"].round(0)
    new_df = new_df[new_df["volume"] > 0]

    if factor == 1000000:
        string_factor = "volume R$ millions"
    elif factor == 1000:
        string_factor = "volume R$ thousands"
    elif factor == 1:
        string_factor = "volume R$"

    chart_data = (
        alt.Chart(new_df, title=f"{asset} - Volume Density ({interval} interval)")
        .transform_density(
            density="volume",
            as_=["volume", "density"],
            groupby=["date"],
            extent=[new_df["volume"].min(), new_df["volume"].max()],
            counts=False,
            steps=200,
        )
        .mark_area(opacity=0.8)
        .encode(
            alt.X("volume:Q", title=string_factor),
            alt.Y("density:Q", stack=None),
            alt.Color("date:N", scale=alt.Scale(scheme="set1")),
        )
        .properties(width=600, height=400)
    )

    html_string = f"volume_density_{asset}.html"
    chart_data.save(html_string)
    return new_df
