from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

RAW_DATA_FILE = RAW_DATA_DIR / "complaints.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "filtered_complaints.csv"

TARGET_PRODUCTS = [
    "Credit card",
    "Checking or savings account",
    "Money transfer, virtual currency, or money service",
    "Payday loan, title loan, or personal loan"
]