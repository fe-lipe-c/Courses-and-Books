import pandas as pd
import altair as alt
import get_dataframe as dfp
import plot_functions as pf
import config as cfg

# dft = cfg.df.query('auction_type == "Venda"')
# df_extra = cfg.df.query(
#     'auction_type == "Extra Compra" | auction_type == "Extra Venda"'
# )
# df_extra.query('auction_date >= "2018-05-01" & auction_date <= "2018-07-01"')[
#     "auction_date"
# ].unique()

df = cfg.df.copy()
df["total_amount_accepted"] = df["total_amount_accepted"].astype(int)
df["total_amount_accepted"] = df["total_amount_accepted"] / 1000000000
df["total_amount_accepted"] = df["total_amount_accepted"].round(2)
df_auction_date = df.query('auction_type == "Venda"')
df_extrav = df.query("auction_type == 'Extra Venda'")
df_extrac = df.query("auction_type == 'Extra Compra'")
df_auction_date.drop(
    [
        "auction_type",
        "round",
        "settlement_date",
        "quantity_tendered",
        "average_rate",
        "accepted_rate",
        "quantity_accepted",
        "quantity_to_central_bank",
        "total_amount_to_central_bank",
        "benchmark",
    ],
    axis=1,
    inplace=True,
)
year_ = "2018"
df_year = df_auction_date.query(
    f'auction_date >= "{year_}-01-01" & auction_date <= "{year_}-12-31"'
)
df_year_extrav = df_extrav.query(
    f'auction_date >= "{year_}-01-01" & auction_date <= "{year_}-12-31"'
)
df_year_extrac = df_extrac.query(
    f'auction_date >= "{year_}-01-01" & auction_date <= "{year_}-12-31"'
)
df_year_extrac.reset_index(inplace=True)
df_year_extrav.reset_index(inplace=True)
df_year_extrac
df_year_extrav

chart_rect = (
    alt.Chart(df_year)
    .mark_rect()
    .encode(
        alt.X("date(auction_date):O").title("Day").axis(format="%e", labelAngle=0),
        alt.Y("month(auction_date):O").title("Month"),
        alt.Color(
            "sum(total_amount_accepted)", scale=alt.Scale(scheme="yelloworangered")
        ),
    )
)
df_year_extrac

chart_extra = (
    alt.Chart(df_year_extrav)
    .mark_rect()
    .encode(
        alt.X("date(auction_date):O").title("Day").axis(format="%e", labelAngle=0),
        alt.Y("month(auction_date):O").title("Month"),
        alt.Color("sum(total_amount_accepted)", scale=alt.Scale(scheme="bluepurple")),
    )
)
chart_total = (
    (chart_extra)
    .configure_view(step=13, strokeWidth=0)
    .configure_axis(domain=False)
    .properties(
        height=400,
        width=800,
        title="Brazil National Treasury's Auctions: Volume per day",
    )
)
chart_total.save("charts/rect.html")


df_auction_date = df_auction_date.groupby("auction_date").sum()
df_auction_date.reset_index(inplace=True)
df_auction_date

df_auction_date["auction_date"] = pd.to_datetime(df_auction_date["auction_date"])
df_auction_date["year"] = df_auction_date["auction_date"].dt.year

df_auction_date["total_amount_accepted"]
df_auction_date.query("total_amount_accepted == 0")


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
# 2001-11-04
# 2002-02-27
# 2004-03-16
# 2004-05-04
# 2004-05-05
# 2004-08-04
# 2004-11-22
# 2004-12-06
# 2004-12-20
# 2005-01-24
# 2005-01-31
# 2005-02-21
# 2005-03-21
# 2005-05-02
# 2005-10-28
# 2008-10-23
# 2008-10-27
# 2008-10-29
# 2009-03-04
# 2009-03-10
# 2010-08-18
# 2010-11-17
# 2011-01-19
# 2012-05-22
cfg.df.query('auction_date == "2015-03-12" & round == 1')
