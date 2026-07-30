---
title: 'isotherm-fit: automated fitting of moisture sorption isotherm models for food stability assessment'
tags:
  - Python
  - food science
  - water activity
  - sorption isotherms
  - food stability
authors:
  - name: Karen Khachatryan
    orcid: 0000-0001-7823-5406
    affiliation: 1
affiliations:
  - name: Laboratory of Nanotechnology and Nanomaterials, Faculty of Food Technology, University of Agriculture in Krakow, Poland
    index: 1
date: 30 July 2026
bibliography: paper.bib
---

# Summary

Moisture sorption isotherms — the relationship between the equilibrium moisture content of a material and the surrounding water activity ($a_w$) — are a foundational measurement in food science, underpinning the design of drying processes, the prediction of storage stability, and the estimation of shelf life. Researchers typically obtain a handful of ($a_w$, moisture) pairs experimentally using the saturated salt solution method, then fit one or more mathematical models — GAB [@vandenberg1981], BET [@brunauer1938], or Peleg [@peleg1993], among others — to the data. `isotherm-fit` is a small, open-source Python command-line tool (with an optional desktop GUI) that automates this fitting process: it loads experimental data from CSV, fits multiple models via nonlinear least squares, computes standard goodness-of-fit metrics (R², RMSE, AIC) and parameter standard errors, selects the best-describing model objectively, extracts the monolayer moisture content ($m_0$) — a key food-stability parameter — and generates a publication-ready report.

# Statement of need

Sorption isotherm fitting is currently performed either manually in spreadsheets, in general-purpose statistical software without domain-specific conventions built in, or with commercial instrument-bundled software (e.g. LabSwift-a<sub>w</sub>) that is not freely available and not open to inspection or extension. Older dedicated tools, such as the DOS-era "ISOT" program, are no longer maintained and do not run on modern systems. To the authors' knowledge, no actively maintained, open-source tool exists that (1) fits the models most commonly used in the food science literature, (2) applies an objective, AIC-based model selection criterion, (3) correctly handles a well-known methodological pitfall — that BET is classically valid only for $a_w < 0.5$ and is therefore fitted on a different-sized data subset than full-range models, making its AIC not directly comparable — and (4) reports the monolayer moisture content independently of whichever model best describes the overall curve shape, since empirical models such as Peleg have no monolayer parameter at all. `isotherm-fit` addresses this gap with a compact, tested, MIT-licensed codebase intended for researchers who need consistent, reproducible isotherm analysis without adopting a full statistical modelling environment.

# Functionality

Given a CSV file of ($a_w$, moisture) pairs (with optional per-point standard deviations), `isotherm-fit`:

- fits the GAB (3-parameter), BET (2-parameter, restricted to $a_w < 0.5$), and Peleg (4-parameter) models using `scipy.optimize.curve_fit` [@virtanen2020scipy];
- reports R², RMSE, AIC, and parameter standard errors for each model;
- selects the best-fitting model by AIC among models fitted on the full dataset;
- reports the monolayer moisture content $m_0$ from GAB (preferred, following the COST 90 recommendation [@wolf1985]) or BET as a fallback, decoupled from the AIC-selected best model;
- generates a report (PDF and/or PNG) showing the experimental points, all fitted model curves, the shaded stability zone below $m_0$, and a residuals plot for the best model;
- exports all fitted parameters and metrics to a JSON file for use in downstream analyses, such as drying process simulations;
- provides an optional CustomTkinter desktop GUI (`isotherm-fit gui`) for interactive use without the command line.

The package is validated against a synthetic dataset with known ground-truth parameters and against a literature-referenced isotherm for microcrystalline cellulose (Avicel PH102) at 25°C [@sun2008], for which `isotherm-fit`'s GAB fit recovers the previously published parameters ($m_0 = 3.55$, $C = 14.42$, $K = 0.814$).

# Availability

`isotherm-fit` is available on GitHub at <https://github.com/karenkhachatryan/isotherm-fit> and on PyPI (`pip install isotherm-fit`), under the MIT license. Documentation, including installation instructions, a quick-start guide, and model descriptions, is available at <https://karenkhachatryan.github.io/isotherm-fit>.

# References
