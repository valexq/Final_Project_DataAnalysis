"""ETL pipeline for phase 1 of the climate analytics project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import (
    CLEANED_DATA_PATH,
    DATA_DICTIONARY_PATH,
    PROCESSED_DATA_PATH,
    QUALITY_REPORT_PATH,
    QUALITY_RULES_PATH,
    RAW_DATA_PATH,
)
from src.data_quality import assert_quality_rules, build_quality_report


COLUMN_MAPPING = {
    "Year": "year",
    "Country": "country",
    "Avg Temperature (°C)": "avg_temperature_c",
    "CO2 Emissions (Tons/Capita)": "co2_emissions_tons_capita",
    "Sea Level Rise (mm)": "sea_level_rise_mm",
    "Rainfall (mm)": "rainfall_mm",
    "Population": "population",
    "Renewable Energy (%)": "renewable_energy_pct",
    "Extreme Weather Events": "extreme_weather_events",
    "Forest Area (%)": "forest_area_pct",
}

FINAL_COLUMNS = [
    "year",
    "country",
    "avg_temperature_c",
    "co2_emissions_tons_capita",
    "sea_level_rise_mm",
    "rainfall_mm",
    "population",
    "renewable_energy_pct",
    "extreme_weather_events",
    "forest_area_pct",
]

INTEGER_COLUMNS = ["year", "rainfall_mm", "population", "extreme_weather_events"]
FLOAT_COLUMNS = [
    "avg_temperature_c",
    "co2_emissions_tons_capita",
    "sea_level_rise_mm",
    "renewable_energy_pct",
    "forest_area_pct",
]


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Read the raw CSV and return it unchanged."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Raw data file is empty: {path}")

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize structure, names, types, and ordering for the raw dataset."""

    missing_columns = sorted(set(COLUMN_MAPPING) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing raw columns: {missing_columns}")

    transformed = df.rename(columns=COLUMN_MAPPING).copy()
    transformed = transformed[FINAL_COLUMNS]

    transformed["country"] = transformed["country"].astype("string").str.strip()

    for column in INTEGER_COLUMNS:
        transformed[column] = pd.to_numeric(transformed[column], errors="raise").astype("int64")

    for column in FLOAT_COLUMNS:
        transformed[column] = pd.to_numeric(transformed[column], errors="raise").astype("float64")

    transformed = (
        transformed.drop_duplicates()
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )

    return transformed


def _classify_renewable_energy(value: float) -> str:
    if value < 20:
        return "baja"
    if value <= 35:
        return "media"
    return "alta"


def _temperature_thresholds(df: pd.DataFrame) -> tuple[float, float]:
    low = float(df["avg_temperature_c"].quantile(1 / 3))
    high = float(df["avg_temperature_c"].quantile(2 / 3))
    return low, high


def _classify_temperature(value: float, low: float, high: float) -> str:
    if value <= low:
        return "baja"
    if value <= high:
        return "media"
    return "alta"


def build_model_ready_data(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Create a conservative processed dataset for BI and later modeling."""

    processed = cleaned_df.copy()
    processed["emissions_total_estimated"] = (
        processed["co2_emissions_tons_capita"] * processed["population"]
    ).round(2)
    processed["renewable_energy_level"] = processed["renewable_energy_pct"].map(
        _classify_renewable_energy
    )

    low_temp, high_temp = _temperature_thresholds(processed)
    processed["temperature_category"] = processed["avg_temperature_c"].map(
        lambda value: _classify_temperature(value, low_temp, high_temp)
    )

    return processed


def build_data_dictionary() -> pd.DataFrame:
    """Return the data dictionary for cleaned and processed outputs."""

    rows = [
        {
            "column": "year",
            "source_column": "Year",
            "stage": "cleaned, processed",
            "dtype": "int64",
            "description": "Anio del registro climatico.",
        },
        {
            "column": "country",
            "source_column": "Country",
            "stage": "cleaned, processed",
            "dtype": "string",
            "description": "Pais analizado.",
        },
        {
            "column": "avg_temperature_c",
            "source_column": "Avg Temperature (°C)",
            "stage": "cleaned, processed",
            "dtype": "float64",
            "description": "Temperatura promedio anual en grados Celsius.",
        },
        {
            "column": "co2_emissions_tons_capita",
            "source_column": "CO2 Emissions (Tons/Capita)",
            "stage": "cleaned, processed",
            "dtype": "float64",
            "description": "Emisiones de CO2 en toneladas por habitante.",
        },
        {
            "column": "sea_level_rise_mm",
            "source_column": "Sea Level Rise (mm)",
            "stage": "cleaned, processed",
            "dtype": "float64",
            "description": "Aumento estimado del nivel del mar en milimetros.",
        },
        {
            "column": "rainfall_mm",
            "source_column": "Rainfall (mm)",
            "stage": "cleaned, processed",
            "dtype": "int64",
            "description": "Precipitacion anual en milimetros.",
        },
        {
            "column": "population",
            "source_column": "Population",
            "stage": "cleaned, processed",
            "dtype": "int64",
            "description": "Poblacion asociada al registro.",
        },
        {
            "column": "renewable_energy_pct",
            "source_column": "Renewable Energy (%)",
            "stage": "cleaned, processed",
            "dtype": "float64",
            "description": "Participacion de energia renovable en porcentaje.",
        },
        {
            "column": "extreme_weather_events",
            "source_column": "Extreme Weather Events",
            "stage": "cleaned, processed",
            "dtype": "int64",
            "description": "Cantidad de eventos climaticos extremos registrados.",
        },
        {
            "column": "forest_area_pct",
            "source_column": "Forest Area (%)",
            "stage": "cleaned, processed",
            "dtype": "float64",
            "description": "Porcentaje de area forestal.",
        },
        {
            "column": "emissions_total_estimated",
            "source_column": "derived",
            "stage": "processed",
            "dtype": "float64",
            "description": "Estimacion de emisiones totales: CO2 per capita por poblacion.",
        },
        {
            "column": "renewable_energy_level",
            "source_column": "derived",
            "stage": "processed",
            "dtype": "string",
            "description": "Nivel de energia renovable: baja (<20), media (20-35), alta (>35).",
        },
        {
            "column": "temperature_category",
            "source_column": "derived",
            "stage": "processed",
            "dtype": "string",
            "description": "Categoria de temperatura promedio basada en terciles del dataset.",
        },
    ]
    return pd.DataFrame(rows)


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_etl(
    raw_path: Path = RAW_DATA_PATH,
    cleaned_path: Path = CLEANED_DATA_PATH,
    processed_path: Path = PROCESSED_DATA_PATH,
    quality_report_path: Path = QUALITY_REPORT_PATH,
    quality_rules_path: Path = QUALITY_RULES_PATH,
    data_dictionary_path: Path = DATA_DICTIONARY_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run extraction, transformation, validation, and loading."""

    raw_df = load_raw_data(raw_path)
    cleaned_df = transform_data(raw_df)
    quality_rules = assert_quality_rules(cleaned_df)
    quality_report = build_quality_report(cleaned_df)
    processed_df = build_model_ready_data(cleaned_df)
    data_dictionary = build_data_dictionary()

    _write_csv(cleaned_df, cleaned_path)
    _write_csv(processed_df, processed_path)
    _write_csv(quality_report, quality_report_path)
    _write_csv(quality_rules, quality_rules_path)
    _write_csv(data_dictionary, data_dictionary_path)

    return cleaned_df, processed_df


def main() -> None:
    cleaned_df, processed_df = run_etl()
    print("ETL completed successfully.")
    print(f"Cleaned rows: {len(cleaned_df):,}")
    print(f"Processed rows: {len(processed_df):,}")
    print(f"Cleaned output: {CLEANED_DATA_PATH}")
    print(f"Processed output: {PROCESSED_DATA_PATH}")
    print(f"Quality report: {QUALITY_REPORT_PATH}")
    print(f"Quality rules: {QUALITY_RULES_PATH}")
    print(f"Data dictionary: {DATA_DICTIONARY_PATH}")


if __name__ == "__main__":
    main()
