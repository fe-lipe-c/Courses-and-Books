"""General tools and functions to be used in the project."""

import altair as alt
import clickhouse_driver
from scipy.stats import wasserstein_distance

# - [ ] Intraday volume distribution ------------------------------------------

client = clickhouse_driver.Client(
    host="localhost", database="aqdb", settings={"use_numpy": True}
)


def volume_distribution(asset, start_data, end_date, interval="1h", factor=1000000):
    """Volume distribution."""
    # Select intraday data for a given asset, exclude the first row and last
    # row for each day (open and close auction).

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
    elif factor == 100000:
        string_factor = "volume R$ hundreds of thousands"
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
    return new_df, df_data


def vol_distances(df, list_days):

    df_07 = df[
        (df["trade_time"] > f"{list_days[0]}") & (df["trade_time"] <= f"{list_days[1]}")
    ]
    df_08 = df[
        (df["trade_time"] > f"{list_days[1]}") & (df["trade_time"] <= f"{list_days[2]}")
    ]
    df_09 = df[
        (df["trade_time"] > f"{list_days[2]}") & (df["trade_time"] <= f"{list_days[3]}")
    ]
    df_10 = df[
        (df["trade_time"] > f"{list_days[3]}") & (df["trade_time"] <= f"{list_days[4]}")
    ]
    df_11 = df[
        (df["trade_time"] > f"{list_days[4]}") & (df["trade_time"] <= f"{list_days[5]}")
    ]

    lista = [df_07, df_08, df_09, df_10, df_11]
    dict_lista = {
        list_days[0]: [],
        list_days[1]: [],
        list_days[2]: [],
        list_days[3]: [],
        list_days[4]: [],
    }

    for i, tabela in enumerate(lista):
        for j, outra in enumerate(lista):
            dict_lista[list_days[i]].append(
                (wasserstein_distance(tabela["volume"], outra["volume"]))
            )

    return dict_lista


def trade_distribution(
    asset, start_data, end_date, max_domain=1000, opacity=0.5, steps=200
):
    """Trade distribution."""

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
    df_data["date"] = df_data["trade_time"].dt.date
    df_data["date"] = df_data["date"].astype("str")

    chart_data = (
        alt.Chart(df_data, title=f"{asset} - Trade Density")
        .transform_density(
            density="quantity",
            as_=["quantity", "density"],
            groupby=["date"],
            extent=[
                0,  # df_data["quantity"].min(),
                min(df_data["quantity"].max(), max_domain),
            ],
            counts=True,
            steps=steps,
        )
        .mark_area(opacity=opacity)
        .encode(
            alt.X("quantity:Q", title="trade size"),
            alt.Y("density:Q", stack=None),
            alt.Color("date:N", scale=alt.Scale(scheme="set1")),
        )
        .properties(width=600, height=400)
    )

    html_string = f"trade_density_{asset}.html"
    chart_data.save(html_string)
    return df_data


def trade_distances(df, list_days):

    df_07 = df[
        (df["trade_time"] > f"{list_days[0]}") & (df["trade_time"] <= f"{list_days[1]}")
    ]
    df_08 = df[
        (df["trade_time"] > f"{list_days[1]}") & (df["trade_time"] <= f"{list_days[2]}")
    ]
    df_09 = df[
        (df["trade_time"] > f"{list_days[2]}") & (df["trade_time"] <= f"{list_days[3]}")
    ]
    df_10 = df[
        (df["trade_time"] > f"{list_days[3]}") & (df["trade_time"] <= f"{list_days[4]}")
    ]
    df_11 = df[
        (df["trade_time"] > f"{list_days[4]}") & (df["trade_time"] <= f"{list_days[5]}")
    ]

    lista = [df_07, df_08, df_09, df_10, df_11]
    dict_lista = {
        list_days[0]: [],
        list_days[1]: [],
        list_days[2]: [],
        list_days[3]: [],
        list_days[4]: [],
    }

    for i, tabela in enumerate(lista):
        for j, outra in enumerate(lista):
            dict_lista[list_days[i]].append(
                (wasserstein_distance(tabela["quantity"], outra["quantity"]))
            )

    return dict_lista
