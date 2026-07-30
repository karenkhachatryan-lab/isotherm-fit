"""Loading and validation of experimental sorption isotherm data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("aw", "moisture")
STD_COLUMN = "moisture_std"


@dataclass
class IsothermData:
    """Experimental water activity / equilibrium moisture content pairs."""

    aw: np.ndarray
    moisture: np.ndarray
    moisture_std: np.ndarray | None
    source: Path

    def __post_init__(self) -> None:
        if self.aw.shape != self.moisture.shape:
            raise ValueError("aw and moisture arrays must have the same shape")
        if self.moisture_std is not None and self.moisture_std.shape != self.aw.shape:
            raise ValueError("moisture_std must have the same shape as aw")

    def __len__(self) -> int:
        return self.aw.size


def load_isotherm_csv(path: str | Path) -> IsothermData:
    """Load a CSV file with columns `aw`, `moisture`, and optional `moisture_std`.

    Parameters
    ----------
    path : str | Path
        Path to a CSV file. `aw` must be in [0, 1); `moisture` in g water / 100 g
        dry solid or kg/kg (any consistent unit is fine, it only affects m0's units).

    Returns
    -------
    IsothermData
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {missing}. "
            f"Expected at least: {REQUIRED_COLUMNS}"
        )

    df = df.dropna(subset=list(REQUIRED_COLUMNS))
    if len(df) < 4:
        raise ValueError(
            f"At least 4 valid (aw, moisture) data points are required for fitting "
            f"a 3-parameter model; got {len(df)}"
        )

    aw = df["aw"].to_numpy(dtype=float)
    moisture = df["moisture"].to_numpy(dtype=float)

    if np.any((aw < 0) | (aw >= 1)):
        raise ValueError("aw values must lie in [0, 1)")
    if np.any(moisture <= 0):
        raise ValueError("moisture values must be strictly positive")

    moisture_std = None
    if STD_COLUMN in df.columns:
        moisture_std = df[STD_COLUMN].to_numpy(dtype=float)

    return IsothermData(aw=aw, moisture=moisture, moisture_std=moisture_std, source=path)
