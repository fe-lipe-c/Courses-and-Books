"""Notebook to explore  B3 data."""

from utils import volume_distribution, vol_distances
from sklearn.neighbors import KernelDensity
import pandas as pd
from scipy.stats import iqr, wasserstein_distance


# - [ ] Intraday volume distribution ------------------------------------------

asset = "PETR4"
month = "12"
day_start = "05"
day_end = "10"
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
