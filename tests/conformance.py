"""Differential conformance report vs G*Power measurements. Run: python tests/conformance.py"""
import csv, math, pathlib, sys
from tpower import engine, config

ORACLE = pathlib.Path(__file__).resolve().parents[1] / "oracle" / "gpower_vectors.csv"
EXACT = ("n1", "n2", "n_total")
APPROX = ("actual_power", "critical", "df", "ncp")


def decimals(s: str) -> int:
    return len(s.split(".")[1]) if "." in s else 0


def engine_row(r):
    tails, d, alpha, ratio = int(r["tails"]), float(r["d"]), float(r["alpha"]), float(r["ratio"] or 1)
    if r["mode"] == "a-priori":
        res = engine.a_priori(d, alpha, float(r["power"]), tails, ratio)
        n1, n2 = res.n1, res.n2
    else:
        n1, n2 = int(r["n1_in"]), int(r["n2_in"])
    p, crit, df, ncp = engine.power_at(n1, n2, d, alpha, tails)
    return dict(n1=n1, n2=n2, n_total=n1 + n2, actual_power=p, critical=crit, df=df, ncp=ncp)


def load():
    with ORACLE.open() as f:
        return [r for r in csv.DictReader(f) if r["n1"] or r["note"]]


def compare(r):
    """Return (n_exact_match: bool|None, problems: list[str])."""
    probs = []
    if not r["n1"]:  # oracle rejected the input
        try:
            engine_row(r)
            probs.append("oracle rejected input but engine accepted it")
        except engine.InputError:
            return True, []
        return False, probs
    try:
        got = engine_row(r)
    except engine.InputError as e:
        return False, [f"engine rejected input: {e}"]
    n_ok = all(int(r[k]) == got[k] for k in EXACT)
    if not n_ok:
        probs.append("N mismatch: oracle " + "/".join(r[k] for k in EXACT) +
                     " engine " + "/".join(str(got[k]) for k in EXACT))
    for k in APPROX:
        if r[k] and round(got[k], decimals(r[k])) != float(r[k]):
            probs.append(f"{k}: oracle {r[k]} engine {got[k]:.{decimals(r[k])}f}")
    return n_ok, probs


def main():
    rows = load()
    if not rows:
        print("no G*Power measurements yet (fill oracle/gpower_vectors.csv)"); return 1
    ok = 0
    for r in rows:
        n_ok, probs = compare(r)
        ok += bool(n_ok)
        if probs:
            print(f"[{r['id']}] {r['category']}: " + "; ".join(probs))
    rate = ok / len(rows)
    print(f"\nN exact-match rate: {ok}/{len(rows)} = {rate:.1%}  (gate: >= 90%)")
    return 0 if rate >= 0.9 else 1


if __name__ == "__main__":
    sys.exit(main())
