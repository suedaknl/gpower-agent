"""Differential tests. statsmodels = scale check (fractional N); G*Power CSV = ground truth."""
import csv, pathlib
import pytest
from tpower import engine
import conformance  # noqa: E402

ORA = pathlib.Path(__file__).resolve().parents[1] / "oracle"


def _sm_rows():
    p = ORA / "statsmodels_vectors.csv"
    return list(csv.DictReader(p.open())) if p.exists() else []


@pytest.mark.skipif(not _sm_rows(), reason="run oracle/make_statsmodels_vectors.py")
def test_statsmodels_equal_ratio_exact_ceil():
    bad = []
    rows = [r for r in _sm_rows() if float(r["ratio"]) == 1.0]
    for r in rows:
        got = engine.a_priori(float(r["d"]), float(r["alpha"]), float(r["power"]), int(r["tails"]), 1.0)
        if got.n1 != int(r["n1_ceil"]):
            bad.append((r, got.n1))
    assert len(bad) / len(rows) < 0.02, bad[:5]


@pytest.mark.skipif(not _sm_rows(), reason="run oracle/make_statsmodels_vectors.py")
def test_statsmodels_unequal_ratio_within_one():
    """Unequal ratios: n2 rounding is a hypothesis; allow +-1 here, G*Power rows decide."""
    rows = [r for r in _sm_rows() if float(r["ratio"]) != 1.0]
    off = 0
    for r in rows:
        got = engine.a_priori(float(r["d"]), float(r["alpha"]), float(r["power"]), int(r["tails"]), float(r["ratio"]))
        if abs(got.n1 - int(r["n1_ceil"])) > 1:
            off += 1
    assert off / len(rows) < 0.02


def test_gpower_conformance_gate():
    rows = conformance.load()
    if not rows:
        pytest.skip("no G*Power measurements in oracle/gpower_vectors.csv yet")
    ok = sum(bool(conformance.compare(r)[0]) for r in rows)
    assert ok / len(rows) >= 0.90
