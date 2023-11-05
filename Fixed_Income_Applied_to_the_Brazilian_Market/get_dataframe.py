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


_nr_auctions = get_df_nr_auctions()
