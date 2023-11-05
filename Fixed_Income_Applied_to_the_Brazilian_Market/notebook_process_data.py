import pandas as pd

df = pd.DataFrame()
years = [i for i in range(2000, 2024)]

for year in years:
    df_temp = pd.read_excel(
        open("data/brl_tsy_auctions.xlsx", "rb"), sheet_name=f"Ano {year}"
    )
    df = pd.concat([df, df_temp])
    df.reset_index(drop=True, inplace=True)

# Replace the values in 'Round' for '1' and '2'
round_dict = {df["Round"].unique()[0]: 1, df["Round"].unique()[1]: 2}
df["Round"].replace(round_dict, inplace=True)

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

df.to_csv("data/brl_tsy_auctions.csv", index=False)
