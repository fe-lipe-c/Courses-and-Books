"""Some functions used in the project."""

import clickhouse_driver


def auction(asset):
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

    sql = sql.replace("BY trade_time)", "BY trade_time DESC)")

    df_close = client.query_dataframe(sql)
    df_close.drop(columns=["rn"], inplace=True)
    # sort dataframe by date
    df_close.sort_values(by="trade_time", inplace=True)
    df_close["volume"] = df_close["quantity"] * df_close["price"]

    return df_open, df_close
