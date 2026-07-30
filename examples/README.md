# Examples

## `mcc_avicel_ph102_25C.csv` — literature-referenced validation case

Moisture content values (g water / 100 g dry solid) for microcrystalline
cellulose (Avicel PH102) at 25 °C, at water activities corresponding to the
saturated salt solutions LiCl, potassium acetate, NaI, Mg(NO₃)₂, NaBr, NaCl,
and KCl (a_w = 0.113, 0.216, 0.382, 0.520, 0.575, 0.750, 0.843).

**Provenance:** the original raw data table from the source publication was
not accessible to us. The values in this CSV were instead computed from the
GAB model equation using the fitted parameters reported in that publication
(Wm = 3.55 g/100 g, C = 14.42, K = 0.814, R² = 0.9998), evaluated at the a_w
values listed above. They are therefore **literature-parameter-derived
reference points, not digitized raw experimental data**.

Source: Sun, C.C. (2008). Mechanism of moisture induced variations in true
density and compaction properties of microcrystalline cellulose.
*International Journal of Pharmaceutics*, 346, 93–101.
https://doi.org/10.1016/j.ijpharm.2007.06.017

**Expected validation outcome:** fitting `isotherm-fit` to this CSV with the
GAB model should recover parameters close to the published values
(m0 ≈ 3.55, C ≈ 14.42, K ≈ 0.814), since the points were generated from that
exact model. This is a useful smoke test that the GAB implementation is
numerically correct and reproduces a well-known literature isotherm — it is
*not* a test of fit quality against experimental noise (see
`synthetic_noisy_isotherm.csv` for that).

```bash
isotherm-fit fit examples/mcc_avicel_ph102_25C.csv --output examples/mcc_report
```

## `synthetic_noisy_isotherm.csv` — illustrative noisy dataset

Synthetic (aw, moisture) data generated from a GAB curve (m0=6.0, C=15.0,
K=0.85) with added Gaussian noise, to illustrate a typical noisy experimental
dataset where GAB, BET, and Peleg give visibly different fits and AIC-based
model selection matters. Not tied to any real material.
