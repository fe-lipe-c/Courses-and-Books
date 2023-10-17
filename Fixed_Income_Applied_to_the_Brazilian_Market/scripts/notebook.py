import pandas as pd
import config as cfg

date = "231013"
url = cfg.URL_ANBIMA + f"ms{date}.txt"

df = pd.read_csv(url, sep="@", encoding="latin1", skiprows=2)
df
