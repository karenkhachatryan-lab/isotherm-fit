# Changelog

All notable changes to this project are documented here. Versioning follows [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-07-30

### Added
- Optional CustomTkinter desktop GUI (`isotherm-fit gui`): File/Edit/Help menu bar, project save/load (`.isofitproj`), Cite and About dialogs, live plot/metrics view.
- PyInstaller build script (`packaging/build_exe.ps1`) for a standalone Windows executable, distributed as a `.zip` on GitHub Releases.
- Zenodo archival and DOI: [10.5281/zenodo.21710137](https://doi.org/10.5281/zenodo.21710137).
- Published to PyPI (`pip install isotherm-fit`).

## [0.1.0] - 2026-07-30

### Added
- Initial release: GAB, BET, and Peleg isotherm model fitting via `scipy.optimize.curve_fit`.
- AIC-based best-model selection, correctly excluding BET (fitted on a restricted a_w < 0.5 subset) from the comparison against full-range models.
- Monolayer moisture content (m0) reporting from GAB (preferred) or BET, independent of the AIC-selected best model.
- CLI (`isotherm-fit fit`, `isotherm-fit cite`) built with Typer.
- PDF/PNG report generation (isotherm plot, model curves, stability zone, residuals) and JSON parameter export.
- MkDocs Material documentation site with a Cite page.
- Literature-validated example (Avicel PH102 microcrystalline cellulose, Sun 2008).
- 25 passing pytest tests.
