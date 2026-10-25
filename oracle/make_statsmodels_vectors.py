"""Scale oracle: 500+ vectors from statsmodels (NOT the ground truth).

statsmodels returns fractional N; G*Power rounds up. Differences are findings, not failures.
Run: python oracle/make_statsmodels_vectors.py
"""
import csv, itertools, math, pathlib, warnings
from statsmodels.stats.power import TTestIndPower

out = pathlib.Path(__file__).with_name("statsmodels_vectors.csv")
solver = TTestIndPower()
ds = [0.1, 0.2, 0.3, 0.5, 0.65, 0.8, 1.0, 1.2, 1.5, 2.0]
alphas = [0.001, 0.01, 0.05, 0.10]
powers = [0.5, 0.8, 0.9, 0.95]
ratios = [1.0, 0.5, 2.0, 3.0]
tails_l = [1, 2]

rows = []
skipped = 0
for d, a, p, r, t in itertools.product(ds, alphas, powers, ratios, tails_l):
    alt = "two-sided" if t == 2 else "larger"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        n1 = float(solver.solve_power(effect_size=d, alpha=a, power=p, ratio=r, alternative=alt))
    if math.isnan(n1):
        skipped += 1  # solver did not converge (very small N); covered by G*Power vectors instead
        continue
    rows.append(dict(d=d, alpha=a, power=p, ratio=r, tails=t,
                     n1_fractional=round(n1, 6), n1_ceil=math.ceil(n1 - 1e-9)))
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print(len(rows), "vectors ->", out, f"({skipped} skipped: solver NaN)")
