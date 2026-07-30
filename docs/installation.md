# Installation

## From PyPI

```bash
pip install isotherm-fit
```

## From source

```bash
git clone https://github.com/karenkhachatryan/isotherm-fit.git
cd isotherm-fit
pip install -e ".[dev]"
```

## Optional: desktop GUI

```bash
pip install "isotherm-fit[gui]"
```

Adds [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (CC0-licensed) and enables `isotherm-fit gui`, a desktop window for loading data, fitting models, and viewing/saving reports without the command line.

## Requirements

- Python ≥ 3.10
- `numpy`, `scipy`, `pandas`, `matplotlib`, `typer` (installed automatically as dependencies)
- `customtkinter` (optional, only for the `[gui]` extra)

## Verifying the installation

```bash
isotherm-fit cite
```

This should print the citation for the currently installed version.
