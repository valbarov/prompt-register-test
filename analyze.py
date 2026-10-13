"""Report. Usage: python analyze.py [results.jsonl ...] > report.md

Accuracy per model x register, per family, and the paired difference ornate-normal and plain-normal with
a 95% bootstrap interval. The bootstrap resamples tasks (50 clusters), not single calls, because the
3 trials and 3 registers of one task are not independent."""
import json, random, sys
from collections import defaultdict
from pathlib import Path
from grade import grade

HERE = Path(__file__).parent
items = {i["task"]: i for i in json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))}
srcs = [Path(s) for s in sys.argv[1:]] or [HERE / "results.jsonl"]
rows = [json.loads(l) for s in srcs if s.exists() for l in s.read_text(encoding="utf-8").splitlines() if l.strip()]
errors = [r for r in rows if r.get("is_error")]
rows = [r for r in rows if not r.get("is_error")]
for r in rows:
    r["correct"], r["exact"] = grade(items[r["task"]], r["result"])

ORDER = ["qwen3:0.6b", "qwen3:1.7b", "qwen3:4b-instruct", "qwen3:8b", "qwen3:14b", "gemma3:1b", "gemma3:4b", "gemma3:12b", "qwen3:4b"]  # qwen3:4b = Thinking-2507, always reasons; side result
def short(m): return m.split(":", 1)[1] if m.startswith("ollama:") else m
models = sorted({short(r["model"]) for r in rows}, key=lambda m: (ORDER.index(m) if m in ORDER else 99, m))
REGS = ["plain", "normal", "ornate"]; FAMS = ["math", "extract", "classify", "filter", "format"]

# per (model, task, register): mean over trials
cell = defaultdict(list)
for r in rows: cell[(short(r["model"]), r["task"], r["register"], "c")].append(r["correct"]); cell[(short(r["model"]), r["task"], r["register"], "e")].append(r["exact"])
def mean(xs): return sum(xs) / len(xs) if xs else float("nan")
def acc(m, reg, tasks, k="c"): return mean([mean(cell[(m, t, reg, k)]) for t in tasks if cell[(m, t, reg, k)]])

def boot_diff(m, a, b, tasks, k="c", n=5000, seed=0):
    rnd = random.Random(seed)
    d = [mean(cell[(m, t, a, k)]) - mean(cell[(m, t, b, k)]) for t in tasks if cell[(m, t, a, k)] and cell[(m, t, b, k)]]
    if not d: return float("nan"), float("nan"), float("nan")
    bs = sorted(mean([d[rnd.randrange(len(d))] for _ in d]) for _ in range(n))
    return mean(d), bs[int(0.025 * n)], bs[int(0.975 * n)]

ALL = list(items)
def pct(x): return "-" if x != x else f"{100*x:.0f}"
def ci(t): return "-" if t[0] != t[0] else f"{100*t[0]:+.0f} [{100*t[1]:+.0f}, {100*t[2]:+.0f}]"

out = [f"# Prompt register test ({len(rows)} graded calls, {len(errors)} errors)\n",
       "Each cell: percent correct over 50 tasks x trials. Difference columns: percentage points, 95% bootstrap interval over tasks.\n",
       "## Correct (answer right, extra words tolerated)\n",
       "| model | plain | normal | ornate | plain - normal | ornate - normal |", "|---|---|---|---|---|---|"]
for m in models:
    out.append(f"| {m} | " + " | ".join(pct(acc(m, r, ALL)) for r in REGS) +
               f" | {ci(boot_diff(m, 'plain', 'normal', ALL))} | {ci(boot_diff(m, 'ornate', 'normal', ALL))} |")
out += ["\n## Exact (answer right AND output format followed strictly)\n",
        "| model | plain | normal | ornate | plain - normal | ornate - normal |", "|---|---|---|---|---|---|"]
for m in models:
    out.append(f"| {m} | " + " | ".join(pct(acc(m, r, ALL, 'e')) for r in REGS) +
               f" | {ci(boot_diff(m, 'plain', 'normal', ALL, 'e'))} | {ci(boot_diff(m, 'ornate', 'normal', ALL, 'e'))} |")
NOMATH = [t for t in ALL if items[t]["family"] != "math"]
out += ["\n## Without math (40 tasks; math is explained by the format line, see analyze_math.py)\n",
        "| model | plain | normal | ornate | plain - normal | ornate - normal |", "|---|---|---|---|---|---|"]
for m in models:
    out.append(f"| {m} | " + " | ".join(pct(acc(m, r, NOMATH)) for r in REGS) +
               f" | {ci(boot_diff(m, 'plain', 'normal', NOMATH))} | {ci(boot_diff(m, 'ornate', 'normal', NOMATH))} |")
for fam in FAMS:
    ts = [t for t in ALL if items[t]["family"] == fam]
    out += [f"\n## Family: {fam} (correct)\n", "| model | plain | normal | ornate |", "|---|---|---|---|"]
    for m in models:
        out.append(f"| {m} | " + " | ".join(pct(acc(m, r, ts)) for r in REGS) + " |")

# cost side: tokens and time
tok = defaultdict(list)
for r in rows:
    tok[(short(r["model"]), r["register"], "in")].append(r.get("input_tokens") or 0)
    tok[(short(r["model"]), r["register"], "out")].append(r.get("output_tokens") or 0)
    tok[(short(r["model"]), r["register"], "s")].append((r.get("duration_ms") or 0) / 1000)
out += ["\n## Cost: mean input tokens / output tokens / seconds per call\n",
        "| model | plain | normal | ornate |", "|---|---|---|---|"]
for m in models:
    out.append(f"| {m} | " + " | ".join(f"{mean(tok[(m, r, 'in')]):.0f} / {mean(tok[(m, r, 'out')]):.0f} / {mean(tok[(m, r, 's')]):.1f}" for r in REGS) + " |")

# tasks that flip most between registers (pooled over models)
flip = []
for t in ALL:
    a = {r: mean([mean(cell[(m, t, r, 'c')]) for m in models if cell[(m, t, r, 'c')]]) for r in REGS}
    flip.append((a["ornate"] - a["normal"], a["plain"] - a["normal"], t))
flip.sort()
out += ["\n## Tasks with the biggest register effect (mean over models, points)\n",
        "| task | family | plain | normal | ornate |", "|---|---|---|---|---|"]
for d_o, d_p, t in flip[:6] + flip[-4:]:
    out.append(f"| {t} | {items[t]['family']} | " + " | ".join(
        pct(mean([mean(cell[(m, t, r, 'c')]) for m in models if cell[(m, t, r, 'c')]])) for r in REGS) + " |")
print("\n".join(out))
