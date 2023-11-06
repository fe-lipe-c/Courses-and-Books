import pandas as pd
import altair as alt
import get_dataframe as dfp
import config as cfg


chart_volume = (
    alt.Chart(dfp._volume)
    .mark_line(color="blue")
    .encode(
        alt.X(
            "year:T",
            axis=alt.Axis(title="Year", titleColor="white", labelColor="white"),
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
    .properties(width=300, height=200, title="Mean volume per auction per year (R$ bi)")
)

chart_area = (
    alt.Chart(dfp._volume)
    .mark_area(opacity=0.3, color="yellow", interpolate="step-after")
    .encode(
        alt.X(
            "year:T",
            axis=alt.Axis(title="Year", titleColor="white", labelColor="white"),
        ),
        alt.Y("min"),
        alt.Y2("max"),
    )
)
chart_total = (
    (chart_area + chart_volume)
    .configure_axis(grid=False)
    .configure_title(color="white")
    .properties(background="#202025")
)
chart_total.save("charts/vol_auctions.html")
