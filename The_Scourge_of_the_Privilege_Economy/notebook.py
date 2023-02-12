"""Notebook to explore some data treated in the book."""

import pandas as pd
import altair as alt
from utils import chart_gdp_absolute

# GDP per capita (current US$)

# Absolute Stagnation (USD)
df_data = chart_gdp_absolute("Peru")
df_data.tail(7)


df_gdp_usd = pd.read_csv("data/wb_data1.csv")
df_gdp_usd.drop(["Unnamed: 66"], axis=1, inplace=True)
df_gdp_usd = df_gdp_usd.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="Value",
)

df_gdp_usd = df_gdp_usd.drop(["Indicator Code", "Country Code"], axis=1)

regions_list = ["Low & middle income", "World"]
country_list = ["Brazil", "World"]
chart_base = (
    alt.Chart(df_gdp_usd[df_gdp_usd["Country Name"].isin(country_list)])
    .mark_line()
    .encode(
        alt.X("Year:O"),
        alt.Y("Value:Q"),
        color="Country Name:N",
    )
    .properties(title="GDP per capita (current US$)", width=1600, height=800)
    .configure_axis(
        labelFontSize=20,
        titleFontSize=20,
    )
    .configure_title(fontSize=20)
    .configure_legend(labelFontSize=20, titleFontSize=20)
)
chart_base.save("charts/line_chart.html")

# GDP per capita (current US$) - Metadata

df_data_2 = pd.read_csv("data/wb_data2.csv")
df_data_2["SpecialNotes"].iloc[9]

# World Bank's remark about Argentina's exchange rate:
# 'The World Bank systematically assesses the appropriateness of official exchange rates as conversion factors. In this country, multiple or dual exchange rate activity exists and must be accounted for appropriately in underlying statistics. An alternative estimate (“alternative conversion factor” - PA.NUS.ATLS) is thus calculated as a weighted average of the different exchange rates in use in the country. Doing so better reflects economic reality and leads to more accurate cross-country comparisons and country classifications by income level. For this country, this applies to the period 1971-2018. Alternative conversion factors are used in the Atlas methodology and elsewhere in World Development Indicators as single-year conversion factors.'

# GDP per capita (current US$) - Metadata

df_data_3 = pd.read_csv("data/wb_data3.csv")

df_data_3.columns

# Index(['INDICATOR_CODE', 'INDICATOR_NAME', 'SOURCE_NOTE',
#        'SOURCE_ORGANIZATION', 'Unnamed: 4'],
df_data_3["SOURCE_NOTE"].unique()

# 'GDP per capita is gross domestic product divided by midyear population. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products. It is calculated without making deductions for depreciation of fabricated assets or for depletion and degradation of natural resources. Data are in current U.S. dollars.'

df_data_3["Unnamed: 4"].unique()

# GDP pe

df_gdp_ppp = pd.read_csv("data/gdp_ppp.csv")

df_gdp_ppp.drop(["Unnamed: 66"], axis=1, inplace=True)
df_gdp_ppp = df_gdp_ppp.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="Value",
)

df_gdp_ppp.drop(["Indicator Code", "Country Code"], axis=1, inplace=True)

regions_list = ["Low & middle income"]
country_list = ["Brazil", "World", "Argentina", "Korea, Rep."]
chart_base = (
    alt.Chart(df_gdp_ppp[df_gdp_ppp["Country Name"].isin(country_list)])
    .mark_line()
    .encode(
        alt.X("Year:O"),
        alt.Y("Value:Q"),
        color="Country Name:N",
    )
    .properties(title="GDP per capita (PPP)", width=1600, height=800)
    .configure_axis(
        labelFontSize=20,
        titleFontSize=20,
    )
    .configure_title(fontSize=20)
    .configure_legend(labelFontSize=20, titleFontSize=20)
)
chart_base.save("charts/chart_gdp_ppp.html")

df_gdp_ppp[df_gdp_ppp["Country Name"].str.contains("Korea")]["Country Name"].unique()
