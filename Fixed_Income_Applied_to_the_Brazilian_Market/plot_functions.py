import pandas as pd
import altair as alt


def plot_nr_auctions(df_nr_auctions):
    chart_nr_auctions = (
        (
            alt.Chart(df_nr_auctions)
            .mark_line(color="red")
            .encode(
                alt.X(
                    "year:T",
                    axis=alt.Axis(
                        title="Year",
                        titleColor="white",
                        labelColor="white",
                    ),
                ),
                alt.Y(
                    "nr_auctions",
                    scale=alt.Scale(domain=[40, 150]),
                    axis=alt.Axis(
                        title="Number of Auctions",
                        titleColor="white",
                        labelColor="white",
                    ),
                ),
            )
            .properties(
                width=300,
                height=200,
                title="Number of auctions per year",
            )
        )
        .configure_axis(grid=False)
        .configure_title(color="white")
        .properties(background="#202025")
    )
    chart_nr_auctions.save("charts/nr_auctions.html")


def plot_nr_auctions(df_volume):
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
                        title="Mean volume (R$ bi)",
                        titleColor="white",
                        labelColor="white",
                    ),
                ),
            )
            .properties(
                width=300, height=200, title="Mean volume per auction per year (R$ bi)"
            )
        )
        .configure_axis(grid=False)
        .configure_title(color="white")
        .properties(background="#202025")
    )
    chart_volume.save("charts/vol_auctions.html")
