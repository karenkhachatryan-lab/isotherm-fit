# Contributing to isotherm-fit

Thanks for your interest in improving `isotherm-fit`.

## Reporting bugs or requesting features

Please open an issue at [github.com/karenkhachatryan-lab/isotherm-fit/issues](https://github.com/karenkhachatryan-lab/isotherm-fit/issues). For bug reports, include:

- Your OS and Python version (`python --version`)
- The `isotherm-fit` version (`isotherm-fit cite` prints it)
- A minimal example CSV (or the one you used) and the exact command that failed
- The full error output

## Getting help

For usage questions, open a [GitHub issue](https://github.com/karenkhachatryan-lab/isotherm-fit/issues) — there is no separate mailing list or chat.

## Contributing code

1. Fork the repository and create a branch from `main`.
2. Install the development environment:
   ```bash
   python -m venv .venv
   .venv/Scripts/python.exe -m pip install -e ".[dev,gui]"
   ```
3. Make your change. Add or update tests in `tests/` for any behavior change.
4. Run the test suite:
   ```bash
   .venv/Scripts/python.exe -m pytest
   ```
5. Open a pull request describing the change and why it's needed.

## Adding a new isotherm model

New models belong in `src/isotherm_fit/models.py`, following the existing `ModelSpec` pattern (function, parameter names, initial guess, bounds). Add a corresponding entry to `MODEL_REGISTRY`, a unit test with synthetic data of known ground-truth parameters (see `tests/test_models.py`), and a short description in `docs/models.md`.

## Code style

Plain, typed Python (`from __future__ import annotations`, type hints on public functions). No enforced formatter/linter yet — match the surrounding code's style.
