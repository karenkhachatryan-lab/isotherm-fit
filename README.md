# isotherm-fit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-orange.svg)](#project-status)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21710137.svg)](https://doi.org/10.5281/zenodo.21710137)

Automated fitting of moisture sorption isotherm models (GAB, BET, Peleg) to experimental water activity data, with objective model selection and food-stability assessment via the monolayer moisture content (m₀).

## Problem

Moisture sorption isotherms — the relationship between equilibrium moisture content and water activity (a_w) — underpin drying process design, storage stability prediction, and shelf-life estimation in food science. Researchers typically measure a handful of (a_w, moisture) points with the saturated salt solution method and then fit models (GAB, BET, Oswin, Henderson, Peleg) by hand in spreadsheets or proprietary software — a slow, inconsistent process. `isotherm-fit` automates model fitting, objective model selection (AIC), and stability-relevant parameter extraction, producing a publication-ready report.

## Installation

```bash
pip install isotherm-fit
```

Or from source:

```bash
git clone https://github.com/karenkhachatryan-lab/isotherm-fit.git
cd isotherm-fit
pip install -e ".[dev]"
```

## Usage

Input CSV with columns `aw`, `moisture` (g water / 100 g dry solid or kg/kg), and optionally `moisture_std`:

```csv
aw,moisture,moisture_std
0.113,3.21,0.08
0.225,4.85,0.10
0.328,6.02,0.09
...
```

Fit models and generate a report:

```bash
isotherm-fit fit data.csv --output report
```

This produces:
- `report.pdf` — isotherm plot with all fitted model curves, parameter/metrics table, stability zone, residuals plot for the best model,
- `report.json` — fitted parameters, metrics (R², RMSE, AIC), and m₀ for downstream use (e.g. drying simulations).

Print citation information:

```bash
isotherm-fit cite
```

### Desktop GUI (optional)

```bash
pip install "isotherm-fit[gui]"
isotherm-fit gui
```

Opens a desktop window (CustomTkinter) to load a CSV, pick models, view the report plot and metrics live, and save the PDF/PNG/JSON outputs — no command-line arguments needed.

For users without Python, a prebuilt standalone Windows GUI is attached as a `.zip` to each [GitHub Release](https://github.com/karenkhachatryan-lab/isotherm-fit/releases/latest) — download, extract, and run `isotherm-fit-gui.exe`, no installation needed. To build it yourself instead, see `packaging/build_exe.ps1` (PyInstaller) in [docs/installation.md](https://karenkhachatryan-lab.github.io/isotherm-fit/installation/#standalone-windows-executable-no-python-needed).

## Project status

Early development (v0.2.0) — MVP scope: GAB, BET, Peleg models; CSV loader; AIC-based model selection; PDF/PNG + JSON report generation; CLI via Typer; optional CustomTkinter desktop GUI. See [CHANGELOG](#) once released.

## Citing this software

If you use `isotherm-fit` in your research, please cite it — see [`CITATION.cff`](CITATION.cff) or run `isotherm-fit cite` for the formatted citation and BibTeX entry. DOI: [10.5281/zenodo.21710137](https://doi.org/10.5281/zenodo.21710137).

## License

MIT — see [LICENSE](LICENSE).
