"""Core calculation: independent-samples t test, noncentral t distribution.

Textbook definitions (Cohen; Faul et al. 2007) -- no decompiled material is used here.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from scipy import stats

from . import config


class InputError(ValueError):
    """Invalid user input. Message goes to the {"error": ...} JSON."""


@dataclass(frozen=True)
class Result:
    n1: int
    n2: int
    n_total: int
    actual_power: float
    critical: float
    df: int
    ncp: float

    def as_dict(self) -> dict:
        d = config.DIGITS
        return {
            "n1": self.n1,
            "n2": self.n2,
            "n_total": self.n_total,
            "actual_power": round(self.actual_power, d),
            "critical": round(self.critical, d),
            "df": self.df,
            "ncp": round(self.ncp, d),
        }


def _n2_from(n1: int, ratio: float) -> int:
    x = round(n1 * ratio, 9)  # strip float noise such as 105.00000000000001
    mode = config.N2_ROUNDING
    if mode == "ceil":
        return int(math.ceil(x))
    if mode == "floor":
        return int(math.floor(x))
    return int(round(x))


def validate(d: float, alpha: float, tails: int, ratio: float) -> None:
    if tails not in (1, 2):
        raise InputError("tails must be 1 or 2")
    if not (0.0 < alpha < 1.0):
        raise InputError("alpha must be in (0, 1)")
    if not math.isfinite(d):
        raise InputError("d must be a finite number")
    if not (ratio > 0 and math.isfinite(ratio)):
        raise InputError("ratio must be > 0")


def ncp_of(n1: int, n2: int, d: float) -> float:
    return d * math.sqrt(n1 * n2 / (n1 + n2))


def power_at(n1: int, n2: int, d: float, alpha: float, tails: int):
    """Return (power, critical, df, ncp) for given group sizes."""
    if n1 < 2 or n2 < 2:
        raise InputError("each group needs at least 2 observations")
    df = n1 + n2 - 2
    ncp = ncp_of(n1, n2, d)
    if tails == 2:
        crit = float(stats.t.ppf(1 - alpha / 2, df))
        upper = float(stats.nct.sf(crit, df, ncp))
        lower = float(stats.nct.sf(crit, df, -ncp))  # == cdf(-crit, df, ncp); avoids scipy nan in far tail
        if not math.isfinite(lower):
            lower = 0.0  # far-tail mass is < 1e-15 when scipy cannot evaluate it
        if not math.isfinite(upper):
            raise InputError("numerical failure computing power")
        power = upper + lower
    else:
        crit = float(stats.t.ppf(1 - alpha, df))
        eff = abs(ncp) if config.ONE_TAIL_NEGATIVE_D == "abs" else ncp
        power = float(stats.nct.sf(crit, df, eff))
    return power, crit, df, ncp


def post_hoc(n1: int, n2: int, d: float, alpha: float, tails: int) -> dict:
    validate(d, alpha, tails, 1.0)
    power, crit, df, ncp = power_at(n1, n2, d, alpha, tails)
    dg = config.DIGITS
    return {
        "n1": n1, "n2": n2, "n_total": n1 + n2,
        "actual_power": round(power, dg),
        "critical": round(crit, dg), "df": df, "ncp": round(ncp, dg),
    }


def a_priori(d: float, alpha: float, power: float, tails: int, ratio: float) -> Result:
    validate(d, alpha, tails, ratio)
    if not (0.0 < power < 1.0):
        raise InputError("power must be in (0, 1)")
    if d == 0:
        raise InputError("d must be non-zero for an a priori analysis")

    def ok(n1: int) -> bool:
        n2 = _n2_from(n1, ratio)
        if n2 < 2:
            return False
        return power_at(n1, n2, d, alpha, tails)[0] >= power

    lo = config.N1_MIN
    if ok(lo):
        best = lo
    else:
        hi = lo
        while not ok(hi):
            lo, hi = hi, hi * 2
            if hi > config.N1_MAX:
                raise InputError("required sample size exceeds the supported maximum")
        while hi - lo > 1:  # power is monotone in n
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid
        best = hi
    n1 = best
    n2 = _n2_from(n1, ratio)
    p, crit, df, ncp = power_at(n1, n2, d, alpha, tails)
    return Result(n1, n2, n1 + n2, p, crit, df, ncp)
