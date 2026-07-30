# Quick Start

## 1. Prepare a CSV

Columns: `aw` (water activity, 0–1), `moisture` (equilibrium moisture content, e.g. g water / 100 g dry solid), optional `moisture_std` (standard deviation across replicates).

```csv
aw,moisture
0.113,3.21
0.225,4.85
0.328,6.02
0.432,7.15
0.529,8.40
0.643,10.10
0.753,12.85
```

At least 4 points are required (5+ recommended, so GAB's 3 parameters are not underdetermined).

## 2. Fit models and generate a report

```bash
isotherm-fit fit data.csv --output report
```

This fits GAB, BET, and Peleg (by default), selects the best model by AIC, and writes:

- `report.pdf` / `report.png` — isotherm plot with all model curves, the stability zone (shaded, based on m₀ from GAB), and a residuals plot for the best model,
- `report.json` — all fitted parameters, metrics, and m₀ for downstream use.

## 3. Choose specific models or formats

```bash
isotherm-fit fit data.csv --models GAB,BET --formats png
```

## 4. Get the citation

```bash
isotherm-fit cite
```

Prints the APA-style citation and BibTeX entry for the installed version — see also [Cite](cite.md).

## Try it on the bundled examples

```bash
isotherm-fit fit examples/mcc_avicel_ph102_25C.csv --output mcc_report
isotherm-fit fit examples/synthetic_noisy_isotherm.csv --output synthetic_report
```

See `examples/README.md` in the repository for details on both datasets.
