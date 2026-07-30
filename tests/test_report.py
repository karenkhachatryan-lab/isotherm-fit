import json
from pathlib import Path

import numpy as np

from isotherm_fit.data import IsothermData
from isotherm_fit.models import fit_all, get_monolayer_reference, select_best_model
from isotherm_fit.report import export_json, save_report

RNG = np.random.default_rng(7)


def _sample_data():
    aw = np.linspace(0.05, 0.9, 10)
    from isotherm_fit.models import gab

    moisture = gab(aw, 6.0, 15.0, 0.85) + RNG.normal(0, 0.05, size=10)
    return IsothermData(aw=aw, moisture=moisture, moisture_std=None, source=Path("synthetic"))


def test_save_report_creates_expected_files(tmp_path):
    data = _sample_data()
    results = fit_all(data, ("GAB", "BET", "Peleg"))
    best = select_best_model(results, n_total=len(data))
    m0_source = get_monolayer_reference(results)

    output = tmp_path / "report"
    paths = save_report(data, results, best, output, formats=("png",), m0_source=m0_source)

    assert len(paths) == 1
    assert paths[0].exists()
    assert paths[0].stat().st_size > 0


def test_export_json_contains_expected_fields(tmp_path):
    data = _sample_data()
    results = fit_all(data, ("GAB", "BET", "Peleg"))
    best = select_best_model(results, n_total=len(data))
    m0_source = get_monolayer_reference(results)

    output = tmp_path / "report"
    json_path = export_json(data, results, best, output, m0_source=m0_source)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["best_model"] == best.model_name
    assert payload["monolayer_moisture_content"]["source_model"] == "GAB"
    assert len(payload["models"]) == 3
    assert payload["n_data_points"] == len(data)
