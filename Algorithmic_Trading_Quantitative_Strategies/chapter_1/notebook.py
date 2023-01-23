"""Notebook to explore  B3 data."""

from utils import volume_distribution, vol_distances
import pandas as pd

# - [ ] Intraday volume distribution ------------------------------------------

asset = "PRIO3"
month = "08"
day_start = "22"
day_end = "27"
start_data = f"2022-{month}-{day_start}"
end_date = f"2022-{month}-{day_end}"

list_days = (
    pd.date_range(start=start_data, end=end_date, freq="D")
    .strftime("%Y-%m-%d")
    .tolist()
)

df, df_data = volume_distribution(
    asset,
    start_data,
    end_date,
    interval="30min",
    factor=1,
)

dist_list = vol_distances(df_data, list_days)
