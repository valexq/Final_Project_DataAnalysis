from pathlib import Path

from src.eda import build_eda_tables, run_eda
from src.etl import load_raw_data, transform_data


def test_build_eda_tables_returns_expected_outputs():
    cleaned_df = transform_data(load_raw_data())

    tables = build_eda_tables(cleaned_df)

    assert set(tables) == {
        "preliminary_summary",
        "numeric_summary",
        "country_summary",
        "yearly_summary",
        "correlation_matrix",
        "top_correlations",
    }
    assert tables["preliminary_summary"].loc[0, "rows"] == 1000
    assert tables["preliminary_summary"].loc[0, "missing_total"] == 0
    assert tables["country_summary"].shape[0] == 15
    assert tables["yearly_summary"]["year"].min() == 2000
    assert tables["yearly_summary"]["year"].max() == 2023
    assert tables["correlation_matrix"].shape == (9, 9)
    assert not tables["top_correlations"].empty


def test_run_eda_saves_tables_and_figures(tmp_path: Path):
    table_paths = {
        "preliminary_summary": tmp_path / "tables" / "eda_preliminary_summary.csv",
        "numeric_summary": tmp_path / "tables" / "eda_numeric_summary.csv",
        "country_summary": tmp_path / "tables" / "eda_country_summary.csv",
        "yearly_summary": tmp_path / "tables" / "eda_yearly_summary.csv",
        "correlation_matrix": tmp_path / "tables" / "eda_correlation_matrix.csv",
        "top_correlations": tmp_path / "tables" / "eda_top_correlations.csv",
    }

    tables, figure_paths = run_eda(
        table_paths=table_paths,
        figures_dir=tmp_path / "figures",
    )

    assert tables["numeric_summary"].shape[0] == 9
    assert all(path.exists() for path in table_paths.values())
    assert set(figure_paths) == {
        "distributions",
        "yearly_trends",
        "correlation_heatmap",
        "country_temperature_co2",
    }
    assert all(path.exists() and path.stat().st_size > 0 for path in figure_paths.values())

