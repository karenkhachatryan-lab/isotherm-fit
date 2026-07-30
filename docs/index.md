# isotherm-fit

Automated fitting of moisture sorption isotherm models (GAB, BET, Peleg) to experimental water activity data, with objective model selection and food-stability assessment via the monolayer moisture content (m₀).

## About

Moisture sorption isotherms — the relationship between equilibrium moisture content and water activity (a<sub>w</sub>) — are fundamental to drying process design, storage stability prediction, and shelf-life estimation in food science. Researchers typically measure a handful of (a<sub>w</sub>, moisture) points using the saturated salt solution method, then fit models by hand in spreadsheets or proprietary software — a slow, inconsistent process, and one with no modern open-source equivalent.

`isotherm-fit` is a lightweight command-line tool that:

1. Loads experimental data from CSV (`aw`, `moisture`, optional `moisture_std`).
2. Fits GAB, BET, and Peleg models via nonlinear least squares.
3. Computes R², RMSE, AIC, and parameter standard errors for each model.
4. Selects the best-fitting model by AIC (compared only among models fitted on the same data — see [Models](models.md) for why BET is treated separately).
5. Reports the monolayer moisture content m₀ from GAB (or BET as fallback) — the key stability-assessment parameter, independent of which model best describes the overall curve shape.
6. Generates a publication-ready report (PDF/PNG) with the isotherm plot, model curves, stability zone, and residuals, plus a JSON file with all fitted parameters for downstream use (e.g. drying simulations).

## Why it matters

Moisture sorption isotherms are a standard measurement in food technology research. Existing tools are either bundled into expensive commercial packages or long unmaintained. `isotherm-fit` fills that gap with a small (MIT-licensed), tested, documented, open-source alternative.

## Status

Early development (v0.2.0). See the [GitHub repository](https://github.com/karenkhachatryan-lab/isotherm-fit) for the latest release.
