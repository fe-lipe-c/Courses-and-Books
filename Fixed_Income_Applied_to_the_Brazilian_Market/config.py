import pandas as pd
from pathlib import Path

DATA_PATH = Path("__file__").parent / "data"

# upload data
df = pd.read_csv(DATA_PATH / "brl_auctions.csv")
