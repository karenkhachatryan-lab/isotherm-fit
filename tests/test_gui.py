"""GUI smoke tests. Skipped automatically if customtkinter/a display is unavailable."""

from pathlib import Path

import pytest

ctk = pytest.importorskip("customtkinter")

from isotherm_fit.data import load_isotherm_csv
from isotherm_fit.gui import MODEL_NAMES, IsothermFitApp

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture
def app():
    try:
        instance = IsothermFitApp()
    except Exception as exc:
        pytest.skip(f"No display available for Tkinter: {exc}")
    yield instance
    instance.destroy()


def test_app_builds_with_expected_widgets(app):
    app.update()
    assert set(app.model_vars) == set(MODEL_NAMES)
    assert app.fit_button.cget("state") == "disabled"


def test_fit_workflow_populates_results(app):
    app.data = load_isotherm_csv(EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv")
    app.fit_button.configure(state="normal")
    app.update()

    app.run_fit()
    app.update()

    assert app.best is not None
    assert app.best.model_name == "GAB"
    assert app.m0_source.model_name == "GAB"
    assert app.m0_source.m0 == pytest.approx(3.55, abs=0.01)
