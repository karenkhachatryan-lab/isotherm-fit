"""GUI smoke tests. Skipped automatically if customtkinter/a display is unavailable."""

from pathlib import Path

import pytest

ctk = pytest.importorskip("customtkinter")

from isotherm_fit.data import load_isotherm_csv
from isotherm_fit.gui import MODEL_NAMES, IsothermFitApp

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture(scope="module")
def app():
    # Module-scoped: Tkinter does not reliably support creating and tearing
    # down multiple Tk() root instances within one process (customtkinter's
    # internal DPI-scaling poll timer can outlive a destroyed instance and
    # interfere with the next one, causing intermittent "invalid command
    # name ... after script" errors). One shared instance, reset between
    # tests via clear_all(), avoids that entirely.
    try:
        instance = IsothermFitApp()
    except Exception as exc:
        pytest.skip(f"No display available for Tkinter: {exc}")
    yield instance
    instance.destroy()


@pytest.fixture(autouse=True)
def _reset_app_state(app):
    app.clear_all()
    app.update()
    yield


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


def test_menu_has_file_edit_help(app):
    menubar = app.nametowidget(app.cget("menu"))
    labels = [
        menubar.entrycget(i, "label")
        for i in range(menubar.index("end") + 1)
        if menubar.type(i) == "cascade"
    ]
    assert labels == ["File", "Edit", "Help"]


def test_save_project_disabled_until_data_loaded(app):
    app.update()
    assert app.file_menu.entrycget(app.file_menu.index("Save Project..."), "state") == "disabled"

    app.csv_path = EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv"
    app._load_data(load_isotherm_csv(app.csv_path), app.csv_path.name)
    app.update()
    assert app.file_menu.entrycget(app.file_menu.index("Save Project..."), "state") == "normal"


def test_project_round_trip(app, tmp_path):
    data = load_isotherm_csv(EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv")
    app.csv_path = EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv"
    app._load_data(data, app.csv_path.name)
    app.model_vars["BET"].set(False)
    app.update()

    project_path = tmp_path / "test.isofitproj"
    app.save_project_to(project_path)
    assert project_path.exists()

    app.clear_all()
    app.update()
    assert app.data is None

    app.load_project_from(project_path)
    app.update()

    assert app.data is not None
    assert len(app.data) == len(data)
    assert app.data.aw == pytest.approx(data.aw)
    assert app.data.moisture == pytest.approx(data.moisture)
    assert app.model_vars["GAB"].get() is True
    assert app.model_vars["BET"].get() is False
    assert app.model_vars["Peleg"].get() is True


def test_clear_all_resets_state(app):
    data = load_isotherm_csv(EXAMPLES_DIR / "mcc_avicel_ph102_25C.csv")
    app._load_data(data, "test.csv")
    app.run_fit()
    app.update()
    assert app.best is not None

    app.clear_all()
    app.update()

    assert app.data is None
    assert app.results is None
    assert app.best is None
    assert app.fit_button.cget("state") == "disabled"
    assert app.file_menu.entrycget(app.file_menu.index("Save Project..."), "state") == "disabled"
