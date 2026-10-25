"""Single entry point used by every layer (CLI, MCP, agent). No logic lives above this."""
from __future__ import annotations

from . import engine

SUPPORTED = {"t2-indep"}


def compute(test, mode, d, alpha=0.05, tails=2, power=None, ratio=1.0, n1=None, n2=None) -> dict:
    if test not in SUPPORTED:
        raise engine.InputError(f"unsupported test '{test}'; supported: {sorted(SUPPORTED)}")
    if mode == "a-priori":
        if power is None:
            raise engine.InputError("power is required for a-priori mode")
        return engine.a_priori(d, alpha, power, tails, ratio).as_dict()
    if mode == "post-hoc":
        if n1 is None or n2 is None:
            raise engine.InputError("n1 and n2 are required for post-hoc mode")
        return engine.post_hoc(n1, n2, d, alpha, tails)
    raise engine.InputError("mode must be 'a-priori' or 'post-hoc'")
