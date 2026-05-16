"""Exploratory data analysis outputs for phase 2."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import (
    CLEANED_DATA_PATH,
    REPORTS_DIR,
    TABLES_DIR,
)


FIGURES_DIR = REPORTS_DIR / "figures"
EDA_PRELIMINARY_SUMMARY_PATH = TABLES_DIR / "eda_preliminary_summary.csv"
EDA_NUMERIC_SUMMARY_PATH = TABLES_DIR / "eda_numeric_summary.csv"
EDA_COUNTRY_SUMMARY_PATH = TABLES_DIR / "eda_country_summary.csv"
EDA_YEARLY_SUMMARY_PATH = TABLES_DIR / "eda_yearly_summary.csv"
EDA_CORRELATION_MATRIX_PATH = TABLES_DIR / "eda_correlation_matrix.csv"
EDA_TOP_CORRELATIONS_PATH = TABLES_DIR / "eda_top_correlations.csv"


NUMERIC_COLUMNS = [
    "year",
    "avg_temperature_c",
    "co2_emissions_tons_capita",
    "sea_level_rise_mm",
    "rainfall_mm",
    "population",
    "renewable_energy_pct",
    "extreme_weather_events",
    "forest_area_pct",
]

EDA_TABLE_PATHS = {
    "preliminary_summary": EDA_PRELIMINARY_SUMMARY_PATH,
    "numeric_summary": EDA_NUMERIC_SUMMARY_PATH,
    "country_summary": EDA_COUNTRY_SUMMARY_PATH,
    "yearly_summary": EDA_YEARLY_SUMMARY_PATH,
    "correlation_matrix": EDA_CORRELATION_MATRIX_PATH,
    "top_correlations": EDA_TOP_CORRELATIONS_PATH,
}


def load_cleaned_data(path: Path = CLEANED_DATA_PATH) -> pd.DataFrame:
    """Load the cleaned dataset produced by phase 1."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Cleaned dataset is empty: {path}")

    return df


def build_preliminary_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize the initial EDA checks over the cleaned dataset."""

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "countries": df["country"].nunique(),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "missing_total": int(df.isna().sum().sum()),
        "duplicate_exact_rows": int(df.duplicated().sum()),
        "numeric_columns": len(df.select_dtypes(include="number").columns),
        "categorical_columns": len(df.select_dtypes(exclude="number").columns),
    }
    return pd.DataFrame([summary])


def build_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Build descriptive statistics for numeric variables."""

    summary = df[NUMERIC_COLUMNS].describe().T.round(2)
    summary["missing_values"] = df[NUMERIC_COLUMNS].isna().sum()
    summary["unique_values"] = df[NUMERIC_COLUMNS].nunique(dropna=False)
    return summary.reset_index(names="variable")


def build_country_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate climate indicators by country."""

    summary = (
        df.groupby("country", as_index=False)
        .agg(
            records=("country", "size"),
            avg_temperature_c=("avg_temperature_c", "mean"),
            avg_co2_emissions_tons_capita=("co2_emissions_tons_capita", "mean"),
            avg_sea_level_rise_mm=("sea_level_rise_mm", "mean"),
            avg_rainfall_mm=("rainfall_mm", "mean"),
            avg_population=("population", "mean"),
            avg_renewable_energy_pct=("renewable_energy_pct", "mean"),
            avg_extreme_weather_events=("extreme_weather_events", "mean"),
            avg_forest_area_pct=("forest_area_pct", "mean"),
        )
        .round(2)
        .sort_values("country")
        .reset_index(drop=True)
    )
    return summary


def build_yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate climate indicators by year to support trend analysis."""

    summary = (
        df.groupby("year", as_index=False)
        .agg(
            records=("year", "size"),
            avg_temperature_c=("avg_temperature_c", "mean"),
            avg_co2_emissions_tons_capita=("co2_emissions_tons_capita", "mean"),
            avg_sea_level_rise_mm=("sea_level_rise_mm", "mean"),
            avg_rainfall_mm=("rainfall_mm", "mean"),
            avg_renewable_energy_pct=("renewable_energy_pct", "mean"),
            avg_extreme_weather_events=("extreme_weather_events", "mean"),
            avg_forest_area_pct=("forest_area_pct", "mean"),
        )
        .round(2)
        .sort_values("year")
        .reset_index(drop=True)
    )
    return summary


def build_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Pearson correlations among numeric variables."""

    return df[NUMERIC_COLUMNS].corr().round(3)


def build_top_correlations(correlation_matrix: pd.DataFrame) -> pd.DataFrame:
    """Return the strongest non-duplicate correlations by absolute value."""

    rows = []
    columns = list(correlation_matrix.columns)
    for index, left in enumerate(columns):
        for right in columns[index + 1 :]:
            value = float(correlation_matrix.loc[left, right])
            rows.append(
                {
                    "variable_1": left,
                    "variable_2": right,
                    "correlation": round(value, 3),
                    "absolute_correlation": round(abs(value), 3),
                }
            )

    return (
        pd.DataFrame(rows)
        .sort_values("absolute_correlation", ascending=False)
        .reset_index(drop=True)
    )


def build_eda_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build all EDA tables used by the notebook and reports."""

    correlation_matrix = build_correlation_matrix(df)
    return {
        "preliminary_summary": build_preliminary_summary(df),
        "numeric_summary": build_numeric_summary(df),
        "country_summary": build_country_summary(df),
        "yearly_summary": build_yearly_summary(df),
        "correlation_matrix": correlation_matrix,
        "top_correlations": build_top_correlations(correlation_matrix),
    }


def save_eda_tables(
    tables: dict[str, pd.DataFrame],
    table_paths: dict[str, Path] = EDA_TABLE_PATHS,
) -> dict[str, Path]:
    """Save EDA tables as CSV files."""

    saved_paths: dict[str, Path] = {}
    for name, table in tables.items():
        path = Path(table_paths[name])
        path.parent.mkdir(parents=True, exist_ok=True)
        if name == "correlation_matrix":
            table.to_csv(path, index_label="variable")
        else:
            table.to_csv(path, index=False)
        saved_paths[name] = path
    return saved_paths


def _save_current_figure(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def save_distribution_figure(df: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> Path:
    """Save histograms for key numeric variables."""

    variables = [
        "avg_temperature_c",
        "co2_emissions_tons_capita",
        "sea_level_rise_mm",
        "rainfall_mm",
        "renewable_energy_pct",
        "forest_area_pct",
    ]
    titles = [
        "Temperatura promedio",
        "Emisiones de CO2 per capita",
        "Aumento del nivel del mar",
        "Precipitacion",
        "Energia renovable",
        "Area forestal",
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for ax, variable, title in zip(axes.ravel(), variables, titles):
        sns.histplot(df[variable], bins=20, kde=True, ax=ax, color="#2f6f73")
        ax.set_title(title)
        ax.set_xlabel(variable)
        ax.set_ylabel("Frecuencia")

    return _save_current_figure(Path(figures_dir) / "eda_distributions.png")


def save_yearly_trends_figure(df: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> Path:
    """Save line charts for yearly climate trends."""

    yearly = build_yearly_summary(df)
    variables = [
        ("avg_temperature_c", "Temperatura promedio"),
        ("avg_co2_emissions_tons_capita", "CO2 per capita"),
        ("avg_sea_level_rise_mm", "Nivel del mar"),
        ("avg_renewable_energy_pct", "Energia renovable"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharex=True)
    for ax, (variable, title) in zip(axes.ravel(), variables):
        sns.lineplot(data=yearly, x="year", y=variable, marker="o", ax=ax, color="#7b4f9d")
        ax.set_title(title)
        ax.set_xlabel("Anio")
        ax.set_ylabel(variable)

    return _save_current_figure(Path(figures_dir) / "eda_yearly_trends.png")


def save_correlation_heatmap(df: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> Path:
    """Save a correlation heatmap for numeric variables."""

    corr = build_correlation_matrix(df)
    plt.figure(figsize=(11, 8))
    sns.heatmap(corr, annot=True, cmap="vlag", fmt=".2f", center=0, linewidths=0.5)
    plt.title("Matriz de correlacion de variables numericas")
    return _save_current_figure(Path(figures_dir) / "eda_correlation_heatmap.png")


def save_country_scatter_figure(df: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> Path:
    """Save a country-level scatter plot for temperature and CO2."""

    country = build_country_summary(df)
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=country,
        x="avg_co2_emissions_tons_capita",
        y="avg_temperature_c",
        size="avg_extreme_weather_events",
        hue="avg_renewable_energy_pct",
        palette="viridis",
        sizes=(60, 260),
    )
    plt.title("Relacion promedio por pais: temperatura, CO2 y energia renovable")
    plt.xlabel("CO2 per capita promedio")
    plt.ylabel("Temperatura promedio")
    return _save_current_figure(Path(figures_dir) / "eda_country_temperature_co2.png")


def save_eda_figures(df: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> dict[str, Path]:
    """Generate all EDA figures."""

    figures_dir = Path(figures_dir)
    return {
        "distributions": save_distribution_figure(df, figures_dir),
        "yearly_trends": save_yearly_trends_figure(df, figures_dir),
        "correlation_heatmap": save_correlation_heatmap(df, figures_dir),
        "country_temperature_co2": save_country_scatter_figure(df, figures_dir),
    }


def run_eda(
    cleaned_path: Path = CLEANED_DATA_PATH,
    table_paths: dict[str, Path] = EDA_TABLE_PATHS,
    figures_dir: Path = FIGURES_DIR,
) -> tuple[dict[str, pd.DataFrame], dict[str, Path]]:
    """Run EDA and save tables plus figures."""

    df = load_cleaned_data(cleaned_path)
    tables = build_eda_tables(df)
    save_eda_tables(tables, table_paths)
    figure_paths = save_eda_figures(df, figures_dir)
    return tables, figure_paths


def main() -> None:
    tables, figure_paths = run_eda()
    print("EDA completed successfully.")
    for name, table in tables.items():
        print(f"Table {name}: {table.shape}")
    for name, path in figure_paths.items():
        print(f"Figure {name}: {path}")


if __name__ == "__main__":
    main()
