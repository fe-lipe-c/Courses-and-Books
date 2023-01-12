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
    df_open["vol_pct_change"] = df_open["volume"].pct_change()
    df_open["price_pct_change"] = df_open["price"].pct_change()

    sql = sql.replace("BY trade_time)", "BY trade_time DESC)")

    df_close = client.query_dataframe(sql)
    df_close.drop(columns=["rn"], inplace=True)
    # sort dataframe by date
    df_close.sort_values(by="trade_time", inplace=True)
    df_close["volume"] = df_close["quantity"] * df_close["price"]
    df_close["vol_pct_change"] = df_open["volume"].pct_change()
    df_close["price_pct_change"] = df_open["price"].pct_change()

    sql_interval = f"""
    SELECT
        ticker,
        trade_time,
        toFloat64(price) AS price,
        quantity
    FROM tradeintraday
    WHERE
        ticker = '{asset}'
    AND DATE_TRUNC(trade_time) <= (SELECT DATE_ADD(MIN(trade_time), INTERVAL 1 HOUR) FROM tradeintraday WHERE DATE(trade_time) = DATE(trade_time))
    """

    # [Error] ServerException: Code: 46.
    # DB::Exception: Unknown function TIME. Maybe you meant: ['tid','like']: While processing SELECT ticker, trade_time, toFloat64(price) AS price, quantity FROM tradeintraday WHERE (ticker = 'PETR4') AND (TIME(trade_time) <= (_CAST('1581328800.023', 'Nullable(DateTime64(3, \'UTC\'))') AS _subquery2)). Stack trace:
    #

    df_interval = client.query_dataframe(sql_interval)
    # SELECT *
    # FROM stocks
    # WHERE TIME(datetime) <= (SELECT DATE_ADD(MIN(TIME(datetime)), INTERVAL 1 HOUR) FROM stocks WHERE DATE(datetime) = DATE(datetime))
    # GROUP BY DATE(datetime);

    return df_open, df_close, df_interval
