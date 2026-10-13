"""Math ablation report. Compares three setups on the same 10 problems:
  own  = each register's own format line (main run, results.jsonl)
  A    = same line for all registers: "Answer with the number only."
  B    = same line for all registers: "Work it out step by step, then write the final number on the last line."
Cells: percent correct. 'shown' = share of replies longer than 8 words (the model wrote out its working)."""
import json
from collections import defaultdict
from pathlib import Path
from grade import grade

HERE = Path(__file__).parent
items = {i["task"]: i for i in json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))}
ORDER = ["qwen3:0.6b", "qwen3:1.7b", "qwen3:4b-instruct", "qwen3:8b", "qwen3:14b", "gemma3:1b", "gemma3:4b", "gemma3:12b"]
REGS = ["plain", "normal", "ornate"]

def load(name):
    p = HERE / name
    rs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []
    return [r for r in rs if not r.get("is_error") and r["family"] == "math" and r["model"] != "ollama:qwen3:4b"]

def mean(xs): return sum(xs) / len(xs) if xs else float("nan")
def pct(x): return "-" if x != x else f"{100*x:.0f}"

out = []
pooled = {}
for setup, f in [("own", "results.jsonl"), ("A", "results_math_A.jsonl"), ("B", "results_math_B.jsonl")]:
    c = defaultdict(list); w = defaultdict(list)
    for r in load(f):
        m = r["model"].split(":", 1)[1]
        c[(m, r["register"])].append(grade(items[r["task"]], r["result"])[0])
        w[(m, r["register"])].append(len((r["result"] or "").split()) > 8)
        c[("ALL", r["register"])].append(c[(m, r["register"])][-1]); w[("ALL", r["register"])].append(w[(m, r["register"])][-1])
    pooled[setup] = {reg: (mean(c[("ALL", reg)]), mean(w[("ALL", reg)])) for reg in REGS}
    out += [f"\n## Setup {setup}: correct % (working shown %)\n", "| model | plain | normal | ornate |", "|---|---|---|---|"]
    for m in ORDER + ["ALL"]:
        if any(c[(m, r)] for r in REGS):
            out.append(f"| {m} | " + " | ".join(f"{pct(mean(c[(m, r)]))} ({pct(mean(w[(m, r)]))})" for r in REGS) + " |")
out.insert(0, "# Math ablation\n\n| setup | plain | normal | ornate |\n|---|---|---|---|\n" + "\n".join(
    f"| {s} | " + " | ".join(f"{pct(v[r][0])}% correct, {pct(v[r][1])}% shown" for r in REGS) + " |" for s, v in pooled.items()))
print("\n".join(out))
