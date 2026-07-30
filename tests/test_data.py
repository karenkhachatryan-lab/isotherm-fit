from pathlib import Path

import pytest

from isotherm_fit.data import load_isotherm_csv


def _write_csv(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "data.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_valid_csv(tmp_path):
    path = _write_csv(
        tmp_path,
        "aw,moisture\n0.1,3.0\n0.3,5.0\n0.5,7.0\n0.7,10.0\n",
    )
    data = load_isotherm_csv(path)
    assert len(data) == 4
    assert data.moisture_std is None


def test_load_csv_with_std(tmp_path):
    path = _write_csv(
        tmp_path,
        "aw,moisture,moisture_std\n0.1,3.0,0.1\n0.3,5.0,0.2\n0.5,7.0,0.1\n0.7,10.0,0.3\n",
    )
    data = load_isotherm_csv(path)
    assert data.moisture_std is not None
    assert data.moisture_std.shape == data.aw.shape


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_isotherm_csv(tmp_path / "nope.csv")


def test_missing_required_column_raises(tmp_path):
    path = _write_csv(tmp_path, "aw,humidity\n0.1,3.0\n0.3,5.0\n0.5,7.0\n0.7,10.0\n")
    with pytest.raises(ValueError, match="missing required column"):
        load_isotherm_csv(path)


def test_too_few_points_raises(tmp_path):
    path = _write_csv(tmp_path, "aw,moisture\n0.1,3.0\n0.3,5.0\n")
    with pytest.raises(ValueError, match="At least 4"):
        load_isotherm_csv(path)


def test_aw_out_of_range_raises(tmp_path):
    path = _write_csv(
        tmp_path, "aw,moisture\n0.1,3.0\n0.3,5.0\n0.5,7.0\n1.2,10.0\n"
    )
    with pytest.raises(ValueError, match=r"\[0, 1\)"):
        load_isotherm_csv(path)


def test_non_positive_moisture_raises(tmp_path):
    path = _write_csv(
        tmp_path, "aw,moisture\n0.1,3.0\n0.3,5.0\n0.5,-1.0\n0.7,10.0\n"
    )
    with pytest.raises(ValueError, match="strictly positive"):
        load_isotherm_csv(path)
