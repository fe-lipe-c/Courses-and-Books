"""Notebook to explore  B3 data."""

from utils import volume_distribution


# - [ ] Intraday volume distribution ------------------------------------------

asset = "PRIO3"
start_data = "2022-11-07"
end_date = "2022-11-09"

df = volume_distribution(asset, start_data, end_date, interval="30min", factor=1000000)
