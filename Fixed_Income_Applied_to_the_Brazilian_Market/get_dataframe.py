import pandas as pd
import config as cfg


def get_df_nr_auctions():
    years = [i for i in range(2000, 2024)]
    list_nr_auctions = []
    for year in years:
        df_year = cfg.df.query(
            f'auction_date >= "{year}-01-01" & auction_date<= "{year}-12-31"'
        ).reset_index(drop=True)
        df_year = df_year.query("round == 1").reset_index(drop=True)

        nr_auctions = len(df_year.auction_date.unique())
        list_nr_auctions.append(nr_auctions)

    df_nr_auctions = pd.DataFrame({"year": years, "nr_auctions": list_nr_auctions})
    df_nr_auctions["year"] = pd.to_datetime(df_nr_auctions["year"], format="%Y")

    return df_nr_auctions


def get_df_mean_volume():
    # Group by auction date
    cfg.df["total_amount_accepted"] = cfg.df["total_amount_accepted"].astype(int)
    df_auction_date = cfg.df.query('auction_type == "Venda"').copy()
    df_auction_date = df_auction_date.groupby("auction_date").sum()
    df_auction_date.reset_index(inplace=True)
    df_auction_date = df_auction_date[["auction_date", "total_amount_accepted"]]

    # New column year
    df_auction_date["auction_date"] = pd.to_datetime(df_auction_date["auction_date"])
    df_auction_date["year"] = df_auction_date["auction_date"].dt.year
    df_auction_date.drop(columns=["auction_date"], inplace=True)
    df_volume = df_auction_date.groupby("year").agg(
        {"total_amount_accepted": ["sum", "count", "mean", "std"]}
    )
    df_volume = df_volume["total_amount_accepted"]
    df_volume.reset_index(inplace=True)
    for col_label in ["mean", "std"]:
        df_volume[f"{col_label}"] = df_volume[f"{col_label}"].astype(int)
        df_volume[f"{col_label}"] = df_volume[f"{col_label}"] / 1000000000
        df_volume[f"{col_label}"] = df_volume[f"{col_label}"].round(2)
    df_volume["year"] = pd.to_datetime(df_volume["year"], format="%Y")
    return df_volume


_nr_auctions = get_df_nr_auctions()
_volume = get_df_mean_volume()
