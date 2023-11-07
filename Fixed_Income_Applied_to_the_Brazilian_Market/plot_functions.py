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


def plot_volume(df_volume, line_color="lightgreen"):
    chart_volume = (
        alt.Chart(df_volume)
        .mark_line(color=line_color)
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
                "mean",
                # scale=alt.Scale(domain=[40, 150]),
                axis=alt.Axis(
                    title="Mean volume (R$ bi)",
                    titleColor="white",
                    labelColor="white",
                ),
            ),
        )
    )

    return chart_volume


def error_band(df_error, df_volume):
    chart_vol = plot_volume(df_volume)

    chart_area = (
        alt.Chart(df_error)
        .mark_area(opacity=0.3, color="yellow", interpolate="step-after")
        .encode(
            alt.X(
                "year:T",
                axis=alt.Axis(
                    title="Year",
                    titleColor="white",
                    labelColor="white",
                ),
            ),
            alt.Y("min"),
            alt.Y2("max"),
        )
    )
    chart_total = (
        (chart_area + chart_vol)
        .configure_axis(grid=False)
        .configure_title(color="white")
        .properties(background="#202025")
    )
    chart_total.save("charts/vol_auctions.html")
