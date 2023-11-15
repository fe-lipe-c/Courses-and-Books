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


def update_auction_data(update_all=False):
    current_year = datetime.today().year
    df_total = pd.read_csv("data/brl_tsy_auctions.csv")

    if update_all is not True:
        xls_url = f"https://sisweb.tesouro.gov.br/apex/cosis/rleiloes/arquivos/todos/desc/historico-leiloes-{current_year}.xlsx"
        years = [current_year]
    else:
        xls_url = "https://sisweb.tesouro.gov.br/apex/cosis/rleiloes/arquivos/todos/desc/historico-leiloes-todos.xls"
        years = [i for i in range(2000, current_year + 1)]

    df = pd.DataFrame()
    for year in years:
        df_temp = pd.read_excel(
            xls_url,
            sheet_name=f"Ano {year}",
            header=6
            # open("data/brl_tsy_auctions.xlsx", "rb"), sheet_name=f"Ano {year}"
        ).iloc[:, 1:]
        df = pd.concat([df, df_temp])
        df.reset_index(drop=True, inplace=True)

    # Replace the values in 'Round' for '1' and '2'
    round_dict = {df["Round"].unique()[0]: 1, df["Round"].unique()[1]: 2}
    df["Round"].replace(round_dict, inplace=True)
    df["Benchmark"] = df["Benchmark"].str.replace(" ", "_")

    # Change columns names
    col_names = {
        "Auction Date": "auction_date",
        "Bond Type": "bond_type",
        "Auction Type*": "auction_type",
        "Round": "round",
        "Settlement Date": "settlement_date",
        "Maturity Date": "maturity_date",
        "Quantity Tendered": "quantity_tendered",
        "Average Rate": "average_rate",
        "Accepted Rate": "accepted_rate",
        "Quantity Accepted": "quantity_accepted",
        "Total Amount Accepted (R$)": "total_amount_accepted",
        "Quantity to Central Bank": "quantity_to_central_bank",
        "Total Amount to Central Bank (R$)": "total_amount_to_central_bank",
        "Benchmark": "benchmark",
    }

    df.rename(columns=col_names, inplace=True)
    df["auction_date"] = df["auction_date"].str.replace(" 00:00:00", "")
    df["maturity_date"] = df["maturity_date"].str.replace(" 00:00:00", "")
    df["settlement_date"] = df["settlement_date"].str.replace(" 00:00:00", "")

    df_total = pd.concat([df_total, df])
    df_total.drop_duplicates(inplace=True)
    df_total.reset_index(drop=True, inplace=True)

    df_total.to_csv("data/brl_tsy_auctions.csv", index=False)


update_auction_data()
_nr_auctions = get_df_nr_auctions()
_volume = get_df_mean_volume()
