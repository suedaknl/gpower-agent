"""Command line layer. Thin: parse args -> engine -> one JSON line."""
from __future__ import annotations

import argparse
import json
import sys

from . import api, engine


class _Parser(argparse.ArgumentParser):
    def error(self, message):  # keep the {"error": ...} contract for bad args
        print(json.dumps({"error": message}))
        sys.exit(2)


def build_parser() -> argparse.ArgumentParser:
    p = _Parser(prog="gpower-clone", description="Sample-size / power calculator (t2-indep)")
    p.add_argument("--test", required=True)
    p.add_argument("--mode", required=True, choices=["a-priori", "post-hoc"])
    p.add_argument("--tails", type=int, default=2)
    p.add_argument("--d", type=float, required=True)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float)
    p.add_argument("--ratio", type=float, default=1.0)
    p.add_argument("--n1", type=int)
    p.add_argument("--n2", type=int)
    return p


def run(argv=None) -> dict:
    a = build_parser().parse_args(argv)
    return api.compute(a.test, a.mode, a.d, alpha=a.alpha, tails=a.tails,
                       power=a.power, ratio=a.ratio, n1=a.n1, n2=a.n2)


def main(argv=None) -> int:
    try:
        out = run(argv)
    except engine.InputError as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
