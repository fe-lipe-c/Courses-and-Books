"""Notebook to explore some data treated in the book."""

import numpy as np
import pandas as pd
import altair as alt

df_data = pd.read_csv("data/wb_data1.csv")
df_data.drop(["Unnamed: 66"], axis=1, inplace=True)
df_data = df_data.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="Value",
)

df_data

#                       Country Name Country Code                Indicator Name  \
# 0                            Aruba          ABW  GDP per capita (current US$)
# 1      Africa Eastern and Southern          AFE  GDP per capita (current US$)
# 2                      Afghanistan          AFG  GDP per capita (current US$)
# 3       Africa Western and Central          AFW  GDP per capita (current US$)

#        Indicator Code  Year        Value
# 0      NY.GDP.PCAP.CD  1960          NaN
# 1      NY.GDP.PCAP.CD  1960   162.907576
# 2      NY.GDP.PCAP.CD  1960    62.369375
# 3      NY.GDP.PCAP.CD  1960   106.976475
df_data[df_data["Country Name"] == "Brazil"]
