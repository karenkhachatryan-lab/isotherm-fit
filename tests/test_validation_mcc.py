"""Validation against a literature-referenced isotherm (see examples/README.md).

These points were computed from the GAB parameters reported for Avicel PH102
microcrystalline cellulose at 25 degC by Sun (2008), Int. J. Pharm. 346:93-101
(doi: 10.1016/j.ijpharm.2007.06.017): m0=3.55, C=14.42, K=0.814.
"""

from pathlib import Path

import pytest

from isotherm_fit.data import load_isotherm_csv
from isotherm_fit.models import fit_model

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

PUBLISHED_M0 = 3.55
PUBLISHED_C = 14.42
PUBLISHED_K = 0.814


def test_gab_recovers_published_avicel_ph102_parameters():
    data = load_isotherm_csv(EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv")
    result = fit_model(data, "GAB")

    assert result.r2 > 0.9999
    assert result.params["m0"] == pytest.approx(PUBLISHED_M0, abs=0.01)
    assert result.params["C"] == pytest.approx(PUBLISHED_C, rel=0.01)
    assert result.params["K"] == pytest.approx(PUBLISHED_K, abs=0.005)
