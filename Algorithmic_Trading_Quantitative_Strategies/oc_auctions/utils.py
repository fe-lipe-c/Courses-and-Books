"""Some functions used in the project."""

import clickhouse_driver


def query(sql_command):

    client = clickhouse_driver.Client(
        host="localhost", database="aqdb", settings={"use_numpy": True}
    )

    df = client.query_dataframe(sql_command)
    return df


# SELECT * FROM (
#     SELECT
#         ticker,
#         trade_time,
#         toFloat64(price) AS price,
#         quantity,
#         ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time) AS rn
#     FROM tradeintraday
#     WHERE
#         ticker = 'PETR4'
# )
# WHERE rn = 1
# """
def auction(asset, open=True):
    """Return the open or close auction for a given asset."""
    if open:
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
    else:
        sql = f"""
        SELECT * FROM (
            SELECT
                ticker,
                trade_time,
                toFloat64(price) AS price,
                quantity,
                ROW_NUMBER() OVER (PARTITION BY DATE(trade_time) ORDER BY trade_time DESC) AS rn
            FROM tradeintraday
            WHERE 
                ticker = '{asset}'
        )
        WHERE rn = 1
        """
    df = query(sql)
    df.drop(columns=["rn"], inplace=True)
    # sort dataframe by date
    df.sort_values(by="trade_time", inplace=True)
    df["volume"] = df["quantity"] * df["price"]
    return df


# desc_tabela = client.execute("DESCRIBE tradeintraday")
# for col_tuple in desc_tabela:
#     print([t for t in col_tuple if t not in ""])
