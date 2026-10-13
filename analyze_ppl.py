"""Perplexity report.
1. Mean perplexity of the instruction wording per model x register.
2. Within-task link between familiarity and accuracy: for each task, NLL and accuracy are centred on the
   task's own mean over its 3 registers, so task difficulty drops out. r < 0 means: the less familiar
   wording of a task (higher NLL) is the one the model gets wrong more often. 95% bootstrap over tasks.
Accuracy comes from the Ollama runs (Q4 quantized); perplexity from the bf16 Hugging Face weights."""
import json, math, random
from collections import defaultdict
from pathlib import Path
from grade import grade

HERE = Path(__file__).parent
items = {i["task"]: i for i in json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))}
ppl = [json.loads(l) for l in (HERE / "ppl.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
REGS = ["plain", "normal", "ornate"]; FAMS = ["math", "extract", "classify", "filter", "format"]
models = list(dict.fromkeys(r["model"] for r in ppl))

acc = defaultdict(list)
for l in (HERE / "results.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l); m = r["model"].split(":", 1)[1]
    if m in models and not r.get("is_error"):
        acc[(m, r["task"], r["register"])].append(grade(items[r["task"]], r["result"])[0])
nll = {(r["model"], r["task"], r["register"]): r["nll"] for r in ppl}
def mean(xs): return sum(xs) / len(xs)

out = ["# Perplexity of the instruction wording\n", "Perplexity = exp(mean NLL per token). Lower = more familiar to the model.\n",
       "| model | plain | normal | ornate |", "|---|---|---|---|"]
for m in models:
    out.append(f"| {m} | " + " | ".join(f"{math.exp(mean([nll[(m, t, r)] for t in items])):.1f}" for r in REGS) + " |")
out += ["\n## By family (mean over the 3 models)\n", "| family | plain | normal | ornate |", "|---|---|---|---|"]
for f in FAMS:
    ts = [t for t in items if items[t]["family"] == f]
    out.append(f"| {f} | " + " | ".join(f"{math.exp(mean([nll[(m, t, r)] for m in models for t in ts])):.1f}" for r in REGS) + " |")

def within(m, tasks):
    pairs = defaultdict(list)
    for t in tasks:
        n = [nll[(m, t, r)] for r in REGS]; a = [mean(acc[(m, t, r)]) for r in REGS]
        pairs[t] = [(n[i] - mean(n), a[i] - mean(a)) for i in range(3)]
    return pairs
def corr(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = mean(xs), mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in pts); sx = sum((x - mx) ** 2 for x in xs); sy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sx * sy) if sx and sy else float("nan")
def boot(pairs, n=5000, seed=0):
    rnd = random.Random(seed); ts = list(pairs)
    vals = sorted(v for v in (corr([p for _ in ts for p in pairs[rnd.choice(ts)]]) for _ in range(n)) if v == v)
    return corr([p for t in ts for p in pairs[t]]), vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]

out += ["\n## Within-task link: familiarity vs accuracy (r, 95% CI)\n",
        "| model | all 50 tasks | without math |", "|---|---|---|"]
for m in models:
    a = boot(within(m, list(items))); b = boot(within(m, [t for t in items if items[t]["family"] != "math"]))
    out.append(f"| {m} | {a[0]:+.2f} [{a[1]:+.2f}, {a[2]:+.2f}] | {b[0]:+.2f} [{b[1]:+.2f}, {b[2]:+.2f}] |")

# which register is the most familiar, task by task
out += ["\n## Most familiar register, counted over tasks\n", "| model | plain | normal | ornate |", "|---|---|---|---|"]
for m in models:
    cnt = defaultdict(int)
    for t in items: cnt[min(REGS, key=lambda r: nll[(m, t, r)])] += 1
    out.append(f"| {m} | " + " | ".join(str(cnt[r]) for r in REGS) + " |")
print("\n".join(out))
