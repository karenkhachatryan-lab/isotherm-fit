"""Command-line interface for isotherm-fit."""

from __future__ import annotations

from pathlib import Path

import typer

from isotherm_fit import __version__
from isotherm_fit.data import load_isotherm_csv
from isotherm_fit.models import fit_all, get_monolayer_reference, select_best_model
from isotherm_fit.report import export_json, save_report

app = typer.Typer(
    name="isotherm-fit",
    help="Fit moisture sorption isotherm models and assess food stability.",
    add_completion=False,
)

CITATION_APA = (
    "Khachatryan, K. (2026). isotherm-fit: automated fitting of moisture sorption "
    "isotherm models for food stability assessment (Version "
    f"{__version__}) [Computer software]. "
    "University of Agriculture in Krakow. https://doi.org/10.5281/zenodo.PENDING"
)

CITATION_BIBTEX = f"""@software{{khachatryan_isotherm_fit_2026,
  author  = {{Khachatryan, Karen}},
  title   = {{isotherm-fit: automated fitting of moisture sorption isotherm models for food stability assessment}},
  year    = {{2026}},
  version = {{{__version__}}},
  doi     = {{10.5281/zenodo.PENDING}},
  url     = {{https://github.com/karenkhachatryan/isotherm-fit}}
}}"""


@app.command()
def fit(
    csv_path: Path = typer.Argument(..., help="Path to the input CSV (columns: aw, moisture[, moisture_std])."),
    output: Path = typer.Option(Path("report"), "--output", "-o", help="Output path stem (no extension)."),
    models: str = typer.Option("GAB,BET,Peleg", "--models", help="Comma-separated list of models to fit."),
    formats: str = typer.Option("pdf,png", "--formats", help="Comma-separated report formats to save."),
) -> None:
    """Fit sorption isotherm models to CSV data and generate a report."""
    data = load_isotherm_csv(csv_path)
    model_names = tuple(m.strip() for m in models.split(","))
    results = fit_all(data, model_names)
    best = select_best_model(results, n_total=len(data))
    m0_source = get_monolayer_reference(results)

    fmt_tuple = tuple(f.strip() for f in formats.split(","))
    saved_paths = save_report(data, results, best, output, fmt_tuple, m0_source=m0_source)
    json_path = export_json(data, results, best, output, m0_source=m0_source)

    typer.echo(f"Fitted {len(results)} model(s) on {len(data)} data points.")
    for r in results:
        if r.model_name == best.model_name:
            marker = " <- best (lowest AIC)"
        elif r.n_points != len(data):
            marker = f" (fit on aw<0.5 subset, n={r.n_points}; AIC not comparable to full-range models)"
        else:
            marker = ""
        typer.echo(f"  {r.model_name}: R2={r.r2:.4f}  RMSE={r.rmse:.4f}  AIC={r.aic:.2f}{marker}")
    if m0_source is not None:
        typer.echo(f"Monolayer moisture content (m0) from {m0_source.model_name}: {m0_source.m0:.4f}")
    typer.echo("Saved: " + ", ".join(str(p) for p in [*saved_paths, json_path]))


@app.command()
def cite() -> None:
    """Print citation information (APA + BibTeX)."""
    typer.echo(CITATION_APA)
    typer.echo("")
    typer.echo(CITATION_BIBTEX)


if __name__ == "__main__":
    app()
