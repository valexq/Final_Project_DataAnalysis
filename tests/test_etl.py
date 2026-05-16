from pathlib import Path

from src.config import RAW_DATA_PATH
from src.etl import FINAL_COLUMNS, load_raw_data, run_etl


def test_raw_file_exists():
    assert RAW_DATA_PATH.exists()


def test_load_raw_data_returns_non_empty_dataframe():
    raw_df = load_raw_data(RAW_DATA_PATH)

    assert not raw_df.empty
    assert raw_df.shape == (1000, 10)


def test_run_etl_generates_valid_outputs(tmp_path: Path):
    cleaned_path = tmp_path / "cleaned" / "climate_change_cleaned.csv"
    processed_path = tmp_path / "processed" / "climate_change_model_ready.csv"
    quality_report_path = tmp_path / "reports" / "data_quality_report.csv"
    quality_rules_path = tmp_path / "reports" / "data_quality_rules.csv"
    data_dictionary_path = tmp_path / "reports" / "data_dictionary.csv"

    cleaned_df, processed_df = run_etl(
        cleaned_path=cleaned_path,
        processed_path=processed_path,
        quality_report_path=quality_report_path,
        quality_rules_path=quality_rules_path,
        data_dictionary_path=data_dictionary_path,
    )

    assert not cleaned_df.empty
    assert len(cleaned_df) == 1000
    assert list(cleaned_df.columns) == FINAL_COLUMNS
    assert int(cleaned_df.isna().sum().sum()) == 0
    assert int(cleaned_df.duplicated().sum()) == 0
    assert cleaned_df["year"].between(2000, 2023).all()
    assert cleaned_df["renewable_energy_pct"].between(0, 100).all()
    assert cleaned_df["forest_area_pct"].between(0, 100).all()
    assert "emissions_total_estimated" in processed_df.columns
    assert "renewable_energy_level" in processed_df.columns
    assert "temperature_category" in processed_df.columns
    assert cleaned_path.exists()
    assert processed_path.exists()
    assert quality_report_path.exists()
    assert quality_rules_path.exists()
    assert data_dictionary_path.exists()

