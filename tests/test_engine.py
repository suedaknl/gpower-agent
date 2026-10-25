import json, math, subprocess, sys
import pytest
from tpower import api, cli, engine


def test_contract_example_exact():
    out = cli.run("--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1".split())
    assert out == {"n1": 105, "n2": 105, "n_total": 210, "actual_power": 0.9501,
                   "critical": 1.9714, "df": 208, "ncp": 3.6228}


def test_ncp_formula():
    assert engine.ncp_of(105, 105, 0.5) == pytest.approx(3.6228, abs=1e-4)


@pytest.mark.parametrize("kw", [
    dict(d=0.5, alpha=0.0, power=0.8, tails=2, ratio=1),
    dict(d=0.5, alpha=1.0, power=0.8, tails=2, ratio=1),
    dict(d=0.5, alpha=0.05, power=1.0, tails=2, ratio=1),
    dict(d=0.5, alpha=0.05, power=0.0, tails=2, ratio=1),
    dict(d=0.5, alpha=0.05, power=0.8, tails=3, ratio=1),
    dict(d=0.5, alpha=0.05, power=0.8, tails=2, ratio=0),
    dict(d=0.0, alpha=0.05, power=0.8, tails=2, ratio=1),
    dict(d=float("nan"), alpha=0.05, power=0.8, tails=2, ratio=1),
])
def test_invalid_inputs_raise(kw):
    with pytest.raises(engine.InputError):
        engine.a_priori(**kw)


def test_invalid_cli_json_and_exit_code(capsys):
    code = cli.main("--test t2-indep --mode a-priori --d 0 --power 0.9".split())
    assert code != 0
    assert "error" in json.loads(capsys.readouterr().out)


def test_unknown_test_is_error(capsys):
    assert cli.main("--test anova-oneway --mode a-priori --d 0.5 --power 0.8".split()) != 0


def test_power_monotone_in_n():
    ps = [engine.power_at(n, n, 0.5, 0.05, 2)[0] for n in range(5, 200, 5)]
    assert ps == sorted(ps)


def test_search_returns_minimal_n():
    r = engine.a_priori(0.5, 0.05, 0.8, 2, 1.0)
    assert engine.power_at(r.n1, r.n2, 0.5, 0.05, 2)[0] >= 0.8
    assert engine.power_at(r.n1 - 1, r.n2 - 1, 0.5, 0.05, 2)[0] < 0.8


def test_post_hoc_roundtrip():
    r = engine.a_priori(0.5, 0.05, 0.9, 2, 1.0)
    ph = engine.post_hoc(r.n1, r.n2, 0.5, 0.05, 2)
    assert ph["actual_power"] == r.as_dict()["actual_power"]


def test_cli_entrypoint_subprocess():
    p = subprocess.run([sys.executable, "-m", "tpower.cli", "--test", "t2-indep", "--mode", "a-priori",
                        "--d", "0.5", "--power", "0.95"], capture_output=True, text=True)
    assert p.returncode == 0 and json.loads(p.stdout)["n_total"] == 210
