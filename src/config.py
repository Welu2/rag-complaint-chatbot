from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

RAW_DATA_FILE = RAW_DATA_DIR / "complaints.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "filtered_complaints.csv"

TARGET_PRODUCTS = [
    "Credit card",
    "Personal loan",
    "Savings account",
    "Money transfer"
]