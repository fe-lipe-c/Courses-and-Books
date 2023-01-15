"""Some functions used in the project."""

import clickhouse_driver
import pandas as pd
import numpy as np


def auction(asset, delta=10):
    """Return the open or close auction for a given asset."""

    client = clickhouse_driver.Client(
        host="localhost", database="aqdb", settings={"use_numpy": True}
    )

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
            ticker = '{asset}'
    )
    WHERE rn = 1
    """

    df_open = client.query_dataframe(sql)
    df_open.drop(columns=["rn"], inplace=True)
    # sort dataframe by date
    df_open.sort_values(by="trade_time", inplace=True)
    df_open["volume"] = df_open["quantity"] * df_open["price"]
    df_open["vol_pct_change"] = df_open["volume"].pct_change()
    df_open["price_pct_change"] = df_open["price"].pct_change()

    sql = sql.replace("BY trade_time)", "BY trade_time DESC)")

    df_close = client.query_dataframe(sql)
    df_close.drop(columns=["rn"], inplace=True)
    # sort dataframe by date
    df_close.sort_values(by="trade_time", inplace=True)
    df_close["volume"] = df_close["quantity"] * df_close["price"]
    df_close["vol_pct_change"] = df_close["volume"].pct_change()
    df_close["price_pct_change"] = df_close["price"].pct_change()

    # Add a column with the price change in the following delta time

    sql_new = f"""
    SELECT
        ticker,
        trade_time,
        toFloat64(price) AS price,
        quantity
    FROM tradeintraday
    WHERE ticker = '{asset}'
    AND EXTRACT(HOUR FROM trade_time) <= {delta}
    """

    df_new = client.query_dataframe(sql_new)

    df_new.sort_values(by="trade_time", inplace=True)
    df_new.reset_index(drop=True, inplace=True)

    df_new["date"] = df_new["trade_time"].dt.date
    first_prices = df_new.groupby(by="date")["price"].first()
    last_prices = df_new.groupby(by="date")["price"].last()

    df_prices = pd.DataFrame()
    df_prices["date"] = last_prices.index
    df_prices["first_price"] = first_prices.values
    df_prices["last_price"] = last_prices.values
    df_prices["return"] = df_prices["last_price"] / df_prices["first_price"] - 1
    df_open_geq = df_open[df_open["trade_time"].dt.hour > 11].reset_index(drop=True)
    df_open_leq = df_open[df_open["trade_time"].dt.hour <= 11].reset_index(drop=True)
    df_open_geq["return_delta"] = np.nan
    df_open_leq["return_delta"] = df_prices["return"]
    df_open_new = pd.concat([df_open_geq, df_open_leq])
    df_open_new.sort_values(by="trade_time", inplace=True)
    df_open_new.reset_index(drop=True, inplace=True)

    return df_open_new, df_close
