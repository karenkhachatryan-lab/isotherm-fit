# Installation

## From PyPI

```bash
pip install isotherm-fit
```

## From source

```bash
git clone https://github.com/karenkhachatryan-lab/isotherm-fit.git
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

## Standalone Windows executable (no Python needed)

For users who don't have Python installed, `isotherm-fit gui` can be packaged as a self-contained Windows executable with [PyInstaller](https://pyinstaller.org/):

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[gui,build]"
powershell -ExecutionPolicy Bypass -File packaging\build_exe.ps1
```

This produces `dist\isotherm-fit-gui\isotherm-fit-gui.exe` (~190 MB folder, including the Python runtime, numpy, scipy, pandas, and matplotlib) — copy the whole `dist\isotherm-fit-gui\` folder to distribute it; the app runs by double-clicking the `.exe` inside, no installation or Python required. This is intended as a convenience build for release assets (e.g. attached to a GitHub Release), not as the primary distribution method — `pip install isotherm-fit` remains the canonical way to install and cite the software.

## Verifying the installation

```bash
isotherm-fit cite
```

This should print the citation for the currently installed version.
