from pathlib import Path

import numpy as np
import pytest

from isotherm_fit.data import IsothermData
from isotherm_fit.models import (
    bet,
    fit_all,
    fit_model,
    gab,
    get_monolayer_reference,
    peleg,
    select_best_model,
)

RNG = np.random.default_rng(42)


def _synthetic_gab_data(m0=6.0, c=15.0, k=0.85, n=12, noise_sd=0.05) -> IsothermData:
    aw = np.linspace(0.05, 0.90, n)
    moisture = gab(aw, m0, c, k) + RNG.normal(0, noise_sd, size=n)
    return IsothermData(aw=aw, moisture=moisture, moisture_std=None, source=Path("synthetic"))


def test_gab_fit_recovers_known_parameters():
    true_m0, true_c, true_k = 6.0, 15.0, 0.85
    data = _synthetic_gab_data(m0=true_m0, c=true_c, k=true_k)
    result = fit_model(data, "GAB")

    assert result.r2 > 0.99
    assert result.params["m0"] == pytest.approx(true_m0, rel=0.1)
    assert result.params["C"] == pytest.approx(true_c, rel=0.3)
    assert result.params["K"] == pytest.approx(true_k, rel=0.1)
    assert result.m0 == result.params["m0"]


def test_bet_fit_uses_only_low_aw_subset():
    data = _synthetic_gab_data()
    result = fit_model(data, "BET")
    assert result.n_points == int(np.sum(data.aw < 0.5))
    assert result.n_points < len(data)


def test_peleg_fit_has_no_m0():
    data = _synthetic_gab_data()
    result = fit_model(data, "Peleg")
    assert result.m0 is None
    assert set(result.params) == {"k1", "n1", "k2", "n2"}


def test_bet_requires_enough_low_aw_points():
    aw = np.array([0.6, 0.7, 0.8, 0.9])
    moisture = np.array([8.0, 10.0, 13.0, 18.0])
    data = IsothermData(aw=aw, moisture=moisture, moisture_std=None, source=Path("synthetic"))
    with pytest.raises(ValueError, match="aw < 0.5"):
        fit_model(data, "BET")


def test_select_best_model_excludes_bet_subset_from_aic_race():
    data = _synthetic_gab_data(n=12)
    results = fit_all(data, ("GAB", "BET", "Peleg"))
    best = select_best_model(results, n_total=len(data))
    assert best.n_points == len(data)
    assert best.model_name != "BET"


def test_get_monolayer_reference_prefers_gab():
    data = _synthetic_gab_data()
    results = fit_all(data, ("GAB", "BET", "Peleg"))
    ref = get_monolayer_reference(results)
    assert ref.model_name == "GAB"


def test_get_monolayer_reference_falls_back_to_bet():
    data = _synthetic_gab_data()
    results = fit_all(data, ("BET", "Peleg"))
    ref = get_monolayer_reference(results)
    assert ref.model_name == "BET"


def test_get_monolayer_reference_none_when_unavailable():
    data = _synthetic_gab_data()
    results = fit_all(data, ("Peleg",))
    assert get_monolayer_reference(results) is None


def test_unknown_model_raises():
    data = _synthetic_gab_data()
    with pytest.raises(ValueError, match="Unknown model"):
        fit_model(data, "Oswin")
