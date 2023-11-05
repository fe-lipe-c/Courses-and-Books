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
