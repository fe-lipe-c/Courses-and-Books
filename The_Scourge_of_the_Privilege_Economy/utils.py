"""General functions for the project."""

import pandas as pd
import altair as alt


def chart_gdp_absolute(
    country, type="usd", opacity=1, line_color="white", color_1="red", color_2="#2D9EB3"
):
    """Return a chart of GDP per capita."""
    df_gdp = pd.read_csv(f"data/gdp_{type}.csv")
    df_gdp.drop(["Unnamed: 66"], axis=1, inplace=True)
    df_gdp = df_gdp.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
        var_name="Year",
        value_name="Value",
    )

    df_gdp = df_gdp.drop(["Indicator Code", "Country Code"], axis=1)

    country_list = [country]

    df_gdp_list = df_gdp[df_gdp["Country Name"].isin(country_list)].reset_index(
        drop=True
    )
    df_gdp_list["Growth"] = [
        "Absolute Stagnation" if x <= 0 else "Absolute Growth"
        for x in df_gdp_list["Value"].pct_change()
    ]

    start = []
    end = []
    event = []

    for i, evento in enumerate(df_gdp_list["Growth"]):
        if i == 0:
            start.append(df_gdp_list["Year"].iloc[i])
            event.append(evento)
        else:
            if evento == event[-1]:
                if i == len(df_gdp_list["Growth"]) - 1:
                    end.append(df_gdp_list["Year"].iloc[i])
                pass
            elif i == len(df_gdp_list["Growth"]) - 1:
                end.append(df_gdp_list["Year"].iloc[-2])
                start.append(df_gdp_list["Year"].iloc[-2])
                end.append(df_gdp_list["Year"].iloc[-1])
                event.append(evento)
            else:
                end.append(df_gdp_list["Year"].iloc[i - 1])
                start.append(df_gdp_list["Year"].iloc[i - 1])
                event.append(evento)
                # if i == len(df_gdp_list["Growth"]) - 1:
                #     end.append(df_gdp_list["Year"].iloc[-1])

    df_event = pd.DataFrame()
    df_event["start"] = start
    df_event["end"] = end
    df_event["condition"] = event

    chart_base = (
        alt.Chart(df_gdp_list)
        .mark_line(color=line_color, strokeWidth=5)
        .encode(
            alt.X("Year:T", title="Year"),
            alt.Y("Value:Q"),
        )
    )
    chart_rect = (
        alt.Chart(df_event)
        .mark_rect(opacity=opacity)
        .encode(
            alt.X("start:T"),
            alt.X2("end:T"),
            color=alt.Color(
                "condition:N",
                scale=alt.Scale(
                    domain=["Absolute Stagnation", "Absolute Growth"],
                    range=[color_1, color_2],
                ),
                legend=None,
            ),
        )
    )
    chart_total = chart_rect + chart_base
    chart_total = (
        chart_total.resolve_scale(color="independent").properties(
            # title=f"GDP per capita (current US$) - {country_list[0]}",
            title=f"{country_list[0]}",
            width=800,
            height=400,
        )
        # .configure_legend(labelFontSize=20, titleFontSize=20, labelLimit=300)
        # .configure_title(fontSize=20)
        # .configure_axis(
        #     # labelFontSize=8,
        #     titleFontSize=20,
        # )
    )
    chart_total.save(f"charts/gdp_usd_absolute_{country}.html")
    return df_gdp_list, chart_total
