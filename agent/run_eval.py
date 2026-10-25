"""Agent layer (UNTESTED against a live API in this scaffold -- run it once and fix what breaks).

Turkish question -> LLM picks a tool -> tool runs over MCP (stdio) -> engine computes.
The LLM never calculates: every number in the answer must come from a tool result.
Logs every call to agent/logs/tool_calls.jsonl and token usage to agent/logs/usage.jsonl.

Usage:  ANTHROPIC_API_KEY=... python agent/run_eval.py [--model claude-sonnet-5-5]
Only fictional research scenarios may be sent to an external API (no real patient data).
"""
import argparse, asyncio, json, pathlib, sys, time

import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOGS = ROOT / "agent" / "logs"
SYSTEM = (
    "You help clinical researchers with sample-size and power questions. You do NOT calculate. "
    "Choose the right test family from the question. This server supports only: t test for two "
    "independent means (e.g. drug vs placebo). If the question is about another design (paired, "
    "ANOVA, chi-square, regression), say it is unsupported here and do not call a tool. If key "
    "parameters are missing or the design is unclear, ask the researcher one short question. "
    "Otherwise call the tool and report n1, n2, n_total or power exactly as returned. "
    "Reply in Turkish. ratio means n2/n1; the drug group is group 1."
)


async def main(model: str):
    LOGS.mkdir(parents=True, exist_ok=True)
    client = anthropic.AsyncAnthropic()
    params = StdioServerParameters(command=sys.executable, args=["-m", "tpower.mcp_server"])
    questions = json.loads((ROOT / "eval" / "questions.json").read_text())
    async with stdio_client(params) as (r, w), ClientSession(r, w) as sess:
        await sess.initialize()
        tools = [{"name": t.name, "description": t.description, "input_schema": t.inputSchema}
                 for t in (await sess.list_tools()).tools]
        for q in questions:
            msgs = [{"role": "user", "content": q["question_tr"]}]
            t0, tin, tout, called = time.time(), 0, 0, []
            for _ in range(4):
                resp = await client.messages.create(model=model, max_tokens=800, system=SYSTEM,
                                                    tools=tools, messages=msgs)
                tin += resp.usage.input_tokens; tout += resp.usage.output_tokens
                msgs.append({"role": "assistant", "content": resp.content})
                uses = [b for b in resp.content if b.type == "tool_use"]
                if not uses:
                    break
                results = []
                for u in uses:
                    res = await sess.call_tool(u.name, u.input)
                    text = res.content[0].text if res.content else ""
                    called.append({"tool": u.name, "args": u.input, "result": text})
                    results.append({"type": "tool_result", "tool_use_id": u.id, "content": text})
                msgs.append({"role": "user", "content": results})
            final = "".join(b.text for b in resp.content if b.type == "text")
            with (LOGS / "tool_calls.jsonl").open("a") as f:
                f.write(json.dumps({"id": q["id"], "calls": called, "answer": final}, ensure_ascii=False) + "\n")
            with (LOGS / "usage.jsonl").open("a") as f:
                f.write(json.dumps({"id": q["id"], "model": model, "input_tokens": tin,
                                    "output_tokens": tout, "seconds": round(time.time() - t0, 2)}) + "\n")
            print(q["id"], "tools:", [c["tool"] for c in called], f"{tin}+{tout} tok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", default="claude-sonnet-5-5")
    asyncio.run(main(ap.parse_args().model))
