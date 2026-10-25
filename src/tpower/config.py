"""Behavioural constants that are NOT derivable from textbook math.

Each constant is a HYPOTHESIS until LEDGER.md has an [REA] row for it.
Change the value here only after the evidence says so; never in the CLI/MCP layer.
"""
# H-ROUND-N2: how n2 is derived from n1 and the allocation ratio (n2 = ratio * n1).
N2_ROUNDING = "floor"

# H-SEARCH-START: smallest n1 tried by the a priori search.
N1_MIN = 2

# H-SEARCH-MAX: upper bound on n1; beyond this the search gives up.
N1_MAX = 1_000_000

# H-DIGITS: decimals in the JSON output.
DIGITS = 4

# H-ONETAIL-SIGN: how one-tailed power treats negative d.
ONE_TAIL_NEGATIVE_D = "abs"