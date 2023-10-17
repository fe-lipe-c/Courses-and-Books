from pathlib import Path

DATA_PATH = Path("__file__").parent / "data"
REFERENCE_PATH = DATA_PATH / "reference"

# Create folders if they don't exist.
Path.mkdir(REFERENCE_PATH, parents=True, exist_ok=True)

URL_ANBIMA = "https://www.anbima.com.br/informacoes/merc-sec/arqs/"
# Load DI data.
# DI_DATA = pd.read_csv(DATA_PATH / "df_DI_20230907.csv")

# Load reference data.
# HOLIDAYS = pd.read_csv(REFERENCE_PATH / "holidays.csv", sep=";")
