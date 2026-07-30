"""Report generation: isotherm plot, metrics table, residuals, and JSON export."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

from isotherm_fit import __version__
from isotherm_fit.data import IsothermData
from isotherm_fit.models import FitResult

_MODEL_COLORS = {"GAB": "#1b9e77", "BET": "#d95f02", "Peleg": "#7570b3"}


def _monolayer_aw(m0_source: FitResult) -> float | None:
    """Solve for the water activity at which the m0-reference model's predicted
    moisture equals its monolayer value m0 (upper edge of the stability zone).
    Returns None if the model has no m0 or no root is found in (0, 1)."""
    if m0_source is None or m0_source.m0 is None:
        return None
    try:
        f = lambda aw: m0_source.predict(np.array([aw]))[0] - m0_source.m0
        return float(brentq(f, 1e-6, 0.999))
    except (ValueError, RuntimeError):
        return None


def build_figure(
    data: IsothermData,
    results: list[FitResult],
    best: FitResult,
    m0_source: FitResult | None = None,
) -> plt.Figure:
    fig, (ax_main, ax_res) = plt.subplots(
        2, 1, figsize=(8, 9), gridspec_kw={"height_ratios": [2.5, 1]}
    )

    aw_smooth = np.linspace(max(data.aw.min() - 0.02, 1e-4), min(data.aw.max() + 0.02, 0.999), 300)
    for r in results:
        aw_curve = aw_smooth if r.model_name != "BET" else aw_smooth[aw_smooth < 0.5]
        if aw_curve.size == 0:
            continue
        style = "-" if r.model_name == best.model_name else "--"
        lw = 2.5 if r.model_name == best.model_name else 1.3
        label = f"{r.model_name} (R²={r.r2:.4f})" + (" — best" if r.model_name == best.model_name else "")
        ax_main.plot(
            aw_curve, r.predict(aw_curve), style, lw=lw,
            color=_MODEL_COLORS.get(r.model_name, "gray"), label=label,
        )

    if data.moisture_std is not None:
        ax_main.errorbar(
            data.aw, data.moisture, yerr=data.moisture_std, fmt="o",
            color="black", ecolor="gray", capsize=3, label="Experimental data", zorder=5,
        )
    else:
        ax_main.scatter(data.aw, data.moisture, color="black", zorder=5, label="Experimental data")

    aw_star = _monolayer_aw(m0_source)
    if aw_star is not None:
        ax_main.axvspan(
            0, aw_star, color="gold", alpha=0.15,
            label=f"Stability zone (a_w < {aw_star:.3f}, m0 from {m0_source.model_name})",
        )
        ax_main.axhline(m0_source.m0, color="gray", linestyle=":", lw=1)

    ax_main.set_xlabel("Water activity, $a_w$")
    ax_main.set_ylabel("Equilibrium moisture content")
    ax_main.set_title("Moisture sorption isotherm — model comparison")
    ax_main.legend(loc="upper left", fontsize=8)
    ax_main.grid(alpha=0.3)

    residuals = data.moisture - best.predict(data.aw)
    ax_res.axhline(0, color="black", lw=1)
    ax_res.scatter(data.aw, residuals, color=_MODEL_COLORS.get(best.model_name, "gray"))
    ax_res.set_xlabel("Water activity, $a_w$")
    ax_res.set_ylabel("Residual")
    ax_res.set_title(f"Residuals — best model ({best.model_name})")
    ax_res.grid(alpha=0.3)

    fig.suptitle(f"isotherm-fit v{__version__}", fontsize=9, x=0.99, y=0.995, ha="right", color="gray")
    fig.tight_layout()
    return fig


def save_report(
    data: IsothermData,
    results: list[FitResult],
    best: FitResult,
    output: str | Path,
    formats: tuple[str, ...] = ("pdf", "png"),
    m0_source: FitResult | None = None,
) -> list[Path]:
    """Render and save the report figure in the requested formats."""
    output = Path(output)
    fig = build_figure(data, results, best, m0_source=m0_source)
    saved = []
    for fmt in formats:
        path = output.with_suffix(f".{fmt}")
        fig.savefig(path, dpi=200, bbox_inches="tight")
        saved.append(path)
    plt.close(fig)
    return saved


def export_json(
    data: IsothermData,
    results: list[FitResult],
    best: FitResult,
    output: str | Path,
    m0_source: FitResult | None = None,
) -> Path:
    """Write fitted parameters and metrics to a JSON file for downstream use."""
    output = Path(output).with_suffix(".json")
    payload = {
        "isotherm_fit_version": __version__,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(data.source),
        "n_data_points": len(data),
        "best_model": best.model_name,
        "monolayer_moisture_content": {
            "value": m0_source.m0 if m0_source else None,
            "source_model": m0_source.model_name if m0_source else None,
        },
        "models": [
            {
                "name": r.model_name,
                "params": r.params,
                "param_errors": r.param_errors,
                "r2": r.r2,
                "rmse": r.rmse,
                "aic": r.aic,
                "n_points_used": r.n_points,
                "m0": r.m0,
            }
            for r in results
        ],
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output
