"""Score logs/tool_calls.jsonl against eval/questions.json: tool-choice rate + N exact match."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
qs = {q["id"]: q for q in json.loads((R / "eval/questions.json").read_text())}
logs = [json.loads(l) for l in (R / "agent/logs/tool_calls.jsonl").read_text().splitlines()]
ok_route = ok_n = n_calls = 0
for l in logs:
    q = qs[l["id"]]; called = bool(l["calls"])
    want_call = q["expected_action"] == "call_tool"
    ok_route += (called == want_call)
    if want_call and called:
        n_calls += 1
        got = json.loads(l["calls"][-1]["result"]); exp = q["expected_result_provisional"]
        ok_n += all(got.get(k) == exp[k] for k in ("n1", "n2", "n_total", "actual_power"))
print(f"routing correct: {ok_route}/{len(logs)}   numbers exact: {ok_n}/{n_calls}")
