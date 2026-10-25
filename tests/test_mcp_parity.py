"""CLI and MCP must return identical output for identical input."""
import pytest
from tpower import cli, mcp_server

CASES = [
    ("--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1",
     lambda: mcp_server.t2_indep_sample_size(d=0.5, alpha=0.05, power=0.95, tails=2, ratio=1.0)),
    ("--test t2-indep --mode a-priori --tails 1 --d 0.3 --alpha 0.05 --power 0.9 --ratio 2",
     lambda: mcp_server.t2_indep_sample_size(d=0.3, alpha=0.05, power=0.9, tails=1, ratio=2.0)),
    ("--test t2-indep --mode post-hoc --tails 2 --d 0.8 --alpha 0.05 --n1 20 --n2 40",
     lambda: mcp_server.t2_indep_power(d=0.8, n1=20, n2=40, alpha=0.05, tails=2)),
]


@pytest.mark.parametrize("argv,call", CASES)
def test_same_output(argv, call):
    assert cli.run(argv.split()) == call()


def test_error_is_reported_not_raised():
    assert "error" in mcp_server.t2_indep_sample_size(d=0.0, power=0.8)
