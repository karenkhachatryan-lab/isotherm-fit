"""Sorption isotherm models, curve fitting, and goodness-of-fit metrics.

Model parameterizations follow the food-science convention where the GAB and
BET monolayer parameter is named ``m0`` directly (equilibrium moisture content
of the monomolecular layer, in the same units as the input moisture data).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import curve_fit

from isotherm_fit.data import IsothermData


def gab(aw: np.ndarray, m0: float, c: float, k: float) -> np.ndarray:
    """Guggenheim-Anderson-de Boer model."""
    return (m0 * c * k * aw) / ((1 - k * aw) * (1 - k * aw + c * k * aw))


def bet(aw: np.ndarray, m0: float, c: float) -> np.ndarray:
    """Brunauer-Emmett-Teller model (classically valid for aw < 0.5)."""
    return (m0 * c * aw) / ((1 - aw) * (1 - aw + c * aw))


def peleg(aw: np.ndarray, k1: float, n1: float, k2: float, n2: float) -> np.ndarray:
    """Peleg's empirical four-parameter model."""
    return k1 * np.power(aw, n1) + k2 * np.power(aw, n2)


@dataclass
class ModelSpec:
    name: str
    func: callable
    param_names: tuple[str, ...]
    p0: callable  # data -> initial guess list
    bounds: callable  # data -> (lower, upper)
    has_m0: bool


def _gab_p0(data: IsothermData) -> list[float]:
    return [float(data.moisture.max()) / 4.0, 2.0, 0.8]


def _gab_bounds(data: IsothermData):
    return ([1e-6, 1e-6, 1e-6], [np.inf, np.inf, 1.2])


def _bet_p0(data: IsothermData) -> list[float]:
    return [float(data.moisture.max()) / 4.0, 2.0]


def _bet_bounds(data: IsothermData):
    return ([1e-6, 1e-6], [np.inf, np.inf])


def _peleg_p0(data: IsothermData) -> list[float]:
    m_mean = float(data.moisture.mean())
    return [m_mean, 0.5, m_mean, 3.0]


def _peleg_bounds(data: IsothermData):
    return ([1e-6, 1e-6, 1e-6, 1e-6], [np.inf, 10.0, np.inf, 10.0])


MODEL_REGISTRY: dict[str, ModelSpec] = {
    "GAB": ModelSpec("GAB", gab, ("m0", "C", "K"), _gab_p0, _gab_bounds, has_m0=True),
    "BET": ModelSpec("BET", bet, ("m0", "C"), _bet_p0, _bet_bounds, has_m0=True),
    "Peleg": ModelSpec(
        "Peleg", peleg, ("k1", "n1", "k2", "n2"), _peleg_p0, _peleg_bounds, has_m0=False
    ),
}


@dataclass
class FitResult:
    model_name: str
    params: dict[str, float]
    param_errors: dict[str, float]
    r2: float
    rmse: float
    aic: float
    n_points: int
    m0: float | None = None
    predict: callable = field(repr=False, default=None)


def _compute_metrics(y: np.ndarray, y_pred: np.ndarray, n_params: int) -> tuple[float, float, float]:
    residuals = y - y_pred
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    n = y.size
    rmse = float(np.sqrt(ss_res / n))
    # Standard AIC (Akaike 1974) using RSS under Gaussian error assumption.
    aic = n * np.log(ss_res / n) + 2 * n_params
    return r2, rmse, aic


def fit_model(data: IsothermData, model_name: str) -> FitResult:
    """Fit a single named model (GAB, BET, or Peleg) to the isotherm data."""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model '{model_name}'. Available: {list(MODEL_REGISTRY)}"
        )
    spec = MODEL_REGISTRY[model_name]

    if model_name == "BET":
        mask = data.aw < 0.5
        if mask.sum() < len(spec.param_names) + 1:
            raise ValueError(
                "BET model requires at least "
                f"{len(spec.param_names) + 1} data points with aw < 0.5"
            )
        aw_fit, m_fit = data.aw[mask], data.moisture[mask]
    else:
        aw_fit, m_fit = data.aw, data.moisture

    p0 = spec.p0(data)
    bounds = spec.bounds(data)
    popt, pcov = curve_fit(
        spec.func, aw_fit, m_fit, p0=p0, bounds=bounds, maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))

    y_pred = spec.func(aw_fit, *popt)
    r2, rmse, aic = _compute_metrics(m_fit, y_pred, len(popt))

    params = dict(zip(spec.param_names, (float(v) for v in popt)))
    param_errors = dict(zip(spec.param_names, (float(v) for v in perr)))
    m0 = params.get("m0") if spec.has_m0 else None

    return FitResult(
        model_name=model_name,
        params=params,
        param_errors=param_errors,
        r2=r2,
        rmse=rmse,
        aic=aic,
        n_points=aw_fit.size,
        m0=m0,
        predict=lambda aw, _f=spec.func, _p=popt: _f(aw, *_p),
    )


def fit_all(data: IsothermData, model_names: tuple[str, ...] = ("GAB", "BET", "Peleg")) -> list[FitResult]:
    """Fit all requested models, skipping (with a warning) any that fail to converge."""
    results = []
    for name in model_names:
        try:
            results.append(fit_model(data, name))
        except RuntimeError as exc:
            import warnings

            warnings.warn(f"Model '{name}' failed to converge: {exc}")
    if not results:
        raise RuntimeError("No model converged on the given data")
    return results


def select_best_model(results: list[FitResult], n_total: int) -> FitResult:
    """Select the model with the lowest AIC among models fitted on the full
    dataset (n_points == n_total).

    AIC values are only comparable across models fitted on the *same* data.
    BET is classically restricted to aw < 0.5 and therefore fitted on a subset
    of the data (see `fit_model`); it is excluded from this comparison unless
    it is the only model that converged. Its own metrics are still reported.
    """
    comparable = [r for r in results if r.n_points == n_total]
    candidates = comparable if comparable else results
    return min(candidates, key=lambda r: r.aic)


def get_monolayer_reference(results: list[FitResult]) -> FitResult | None:
    """Return the fit result to use as the monolayer moisture content (m0)
    reference for stability assessment: GAB if available (the model
    recommended by the European COST 90 project for this purpose), otherwise
    BET, otherwise None. This is independent of `select_best_model`, since the
    overall best-fitting curve (e.g. Peleg) may not have an m0 parameter."""
    by_name = {r.model_name: r for r in results}
    return by_name.get("GAB") or by_name.get("BET")
