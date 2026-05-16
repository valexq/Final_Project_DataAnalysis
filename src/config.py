"""Project paths used by the ETL pipeline."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANED_DIR = DATA_DIR / "cleaned"
PROCESSED_DIR = DATA_DIR / "processed"

REPORTS_DIR = ROOT_DIR / "reports"
TABLES_DIR = REPORTS_DIR / "tables"

RAW_DATA_PATH = RAW_DIR / "climate_change_dataset.csv"
CLEANED_DATA_PATH = CLEANED_DIR / "climate_change_cleaned.csv"
PROCESSED_DATA_PATH = PROCESSED_DIR / "climate_change_model_ready.csv"

QUALITY_REPORT_PATH = TABLES_DIR / "data_quality_report.csv"
QUALITY_RULES_PATH = TABLES_DIR / "data_quality_rules.csv"
DATA_DICTIONARY_PATH = TABLES_DIR / "data_dictionary.csv"
