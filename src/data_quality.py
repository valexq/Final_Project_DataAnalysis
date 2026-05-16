"""Data quality reporting and validation rules for the climate dataset."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


class DataQualityError(ValueError):
    """Raised when a data quality rule fails."""


@dataclass(frozen=True)
class QualityRule:
    """Simple row-level validation rule."""

    name: str
    column: str
    valid_mask: pd.Series


def build_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Build a compact column-level data quality report."""

    total_rows = len(df)
    total_columns = len(df.columns)
    duplicate_exact_rows = int(df.duplicated().sum())

    report = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(df[column].dtype) for column in df.columns],
            "missing_values": [int(df[column].isna().sum()) for column in df.columns],
            "missing_pct": [
                round(float(df[column].isna().mean() * 100), 2) for column in df.columns
            ],
            "unique_values": [int(df[column].nunique(dropna=False)) for column in df.columns],
        }
    )
    report.insert(0, "total_rows", total_rows)
    report.insert(1, "total_columns", total_columns)
    report.insert(2, "duplicate_exact_rows", duplicate_exact_rows)
    return report


def build_quality_rules_report(df: pd.DataFrame) -> pd.DataFrame:
    """Evaluate business and quality rules for the transformed dataset."""

    rules = [
        QualityRule("year_between_2000_and_2023", "year", df["year"].between(2000, 2023)),
        QualityRule("population_positive", "population", df["population"] > 0),
        QualityRule(
            "renewable_energy_pct_between_0_and_100",
            "renewable_energy_pct",
            df["renewable_energy_pct"].between(0, 100),
        ),
        QualityRule(
            "forest_area_pct_between_0_and_100",
            "forest_area_pct",
            df["forest_area_pct"].between(0, 100),
        ),
        QualityRule(
            "co2_emissions_tons_capita_non_negative",
            "co2_emissions_tons_capita",
            df["co2_emissions_tons_capita"] >= 0,
        ),
        QualityRule(
            "sea_level_rise_mm_non_negative",
            "sea_level_rise_mm",
            df["sea_level_rise_mm"] >= 0,
        ),
        QualityRule("rainfall_mm_non_negative", "rainfall_mm", df["rainfall_mm"] >= 0),
        QualityRule(
            "extreme_weather_events_non_negative",
            "extreme_weather_events",
            df["extreme_weather_events"] >= 0,
        ),
    ]

    rows = []
    for rule in rules:
        valid_mask = rule.valid_mask.fillna(False)
        violation_count = int((~valid_mask).sum())
        rows.append(
            {
                "rule": rule.name,
                "column": rule.column,
                "passed": violation_count == 0,
                "violation_count": violation_count,
                "min_value": df[rule.column].min(),
                "max_value": df[rule.column].max(),
            }
        )

    return pd.DataFrame(rows)


def assert_quality_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Validate quality rules and raise a clear error if any rule fails."""

    rules_report = build_quality_rules_report(df)
    failed_rules = rules_report.loc[~rules_report["passed"], "rule"].tolist()
    if failed_rules:
        joined_rules = ", ".join(failed_rules)
        raise DataQualityError(f"Data quality rules failed: {joined_rules}")
    return rules_report

