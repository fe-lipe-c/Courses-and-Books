import pandas as pd
import altair as alt
import get_dataframe as dfp
import config as cfg

cfg.df.columns
# Index(['auction_date', 'bond_type', 'auction_type', 'round', 'settlement_date',
#        'maturity_date', 'quantity_tendered', 'average_rate', 'accepted_rate',
#        'quantity_accepted', 'total_amount_accepted',
#        'quantity_to_central_bank', 'total_amount_to_central_bank',
#        'benchmark'],
#       dtype='object')

# Group by auction date
cfg.df["total_amount_accepted"] = cfg.df["total_amount_accepted"].astype(int)
df_auction_date = pd.DataFrame()
df_auction_date = cfg.df.groupby("auction_date").sum()
df_auction_date.reset_index(inplace=True)
df_auction_date = df_auction_date[["auction_date", "total_amount_accepted"]]

# New column year
df_auction_date["auction_date"] = pd.to_datetime(df_auction_date["auction_date"])
df_auction_date["year"] = df_auction_date["auction_date"].dt.year
df_auction_date.drop(columns=["auction_date"], inplace=True)
df_volume = df_auction_date.groupby("year").mean()
df_volume.reset_index(inplace=True)
df_volume["total_amount_accepted"] = df_volume["total_amount_accepted"].astype(int)
df_volume["total_amount_accepted"] = df_volume["total_amount_accepted"] / 1000000000
df_volume["total_amount_accepted"] = df_volume["total_amount_accepted"].round(2)
df_volume["year"] = pd.to_datetime(df_volume["year"], format="%Y")
df_volume.info()


chart_volume = (
    (
        alt.Chart(df_volume)
        .mark_line(color="lightblue")
        .encode(
            alt.X(
                "year:T",
                axis=alt.Axis(title="Year", titleColor="white", labelColor="white"),
            ),
            alt.Y(
                "total_amount_accepted",
                # scale=alt.Scale(domain=[40, 150]),
                axis=alt.Axis(
                    title="Volume per auction (R$ bi)",
                    titleColor="white",
                    labelColor="white",
                ),
            ),
        )
        .properties(width=300, height=200, title="Volume per auction (R$ bi)")
    )
    .configure_axis(grid=False)
    .configure_title(color="white")
    .properties(background="#202025")
)
chart_volume.save("charts/vol_auctions.html")
