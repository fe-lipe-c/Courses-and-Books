import pandas as pd
import altair as alt
import get_dataframe as dfp
import plot_functions as pf
import config as cfg

cfg.df["total_amount_accepted"] = cfg.df["total_amount_accepted"].astype(int)
cfg.df["total_amount_accepted"] = cfg.df["total_amount_accepted"] / 1000000000
cfg.df["total_amount_accepted"] = cfg.df["total_amount_accepted"].round(2)
df_auction_date = cfg.df.groupby("auction_date").sum()
df_auction_date.reset_index(inplace=True)
df_auction_date["auction_date"] = pd.to_datetime(df_auction_date["auction_date"])
df_auction_date["year"] = df_auction_date["auction_date"].dt.year

df_auction_date["year"] % 2

chart_volume = pf.plot_volume(dfp._volume)
chart_points = (
    alt.Chart(df_auction_date)
    .mark_circle(size=10)
    .encode(
        alt.X("auction_date:T"),
        alt.Y(
            "total_amount_accepted:Q",
            scale=alt.Scale(domain=[0, cfg.df["total_amount_accepted"].max() + 1]),
            axis=alt.Axis(
                title="Volume",
                titleColor="white",
                labelColor="white",
            ),
        ),
        color=alt.condition(
            alt.datum.year % 2 == 0, alt.value("yellow"), alt.value("#6fa8dc")
        ),
    )
)
chart_total = (
    (chart_points + chart_volume)
    .properties(
        width=1000,
        height=800,
        title="Brazil National Treasury's Auctions: Volume per day | Mean volume per auction per year (R$ bi)",
        background="#202025",
    )
    .configure_axis(grid=False)
    .configure_title(color="white")
)

chart_total.save("charts/points.html")
chart_points.save("charts/points.html")

# .configure_axis(grid=False)
# .configure_title(color="white")
# .properties(background="#202025")
