"""MCP adapter. Thin layer: schema + call into api.compute. No calculation here."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import api, engine

mcp = FastMCP("tpower")


def _call(**kw) -> dict:
    try:
        return api.compute(**kw)
    except engine.InputError as e:
        return {"error": str(e)}


@mcp.tool()
def t2_indep_sample_size(d: float, alpha: float = 0.05, power: float = 0.8,
                         tails: int = 2, ratio: float = 1.0) -> dict:
    """A priori sample size for a t test comparing two independent means
    (e.g. drug vs placebo). d = standardized effect size (Cohen's d),
    ratio = n2/n1. Returns n1, n2, n_total, actual_power, critical, df, ncp."""
    return _call(test="t2-indep", mode="a-priori", d=d, alpha=alpha,
                 power=power, tails=tails, ratio=ratio)


@mcp.tool()
def t2_indep_power(d: float, n1: int, n2: int, alpha: float = 0.05, tails: int = 2) -> dict:
    """Post hoc power for a t test comparing two independent means with
    group sizes n1 and n2. Returns actual_power, critical, df, ncp."""
    return _call(test="t2-indep", mode="post-hoc", d=d, alpha=alpha,
                 tails=tails, n1=n1, n2=n2)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
