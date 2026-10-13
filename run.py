"""Runner. Local models via the Ollama HTTP API, optional Claude models via `claude -p`.
One fresh session per call. Resumable: skips (model, task, register, trial) already in --out.

Local calls use Ollama defaults for temperature, with seed = trial number so every run is repeatable,
thinking off, num_ctx 4096, num_predict 1024."""
import json, subprocess, shutil, sys, time, itertools, argparse, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # log lines may hold any character
ap = argparse.ArgumentParser()
ap.add_argument("--prompts", default=str(HERE / "prompts.json"))
ap.add_argument("--models", required=True, help="ollama:<model> for local, or a claude alias")
ap.add_argument("--registers", default="plain,normal,ornate")
ap.add_argument("--tasks", default="")
ap.add_argument("--trials", type=int, default=3)
ap.add_argument("--workers", type=int, default=1)
ap.add_argument("--out", default=str(HERE / "results.jsonl"))
ap.add_argument("--timeout", type=int, default=300)
a = ap.parse_args()

CLAUDE = shutil.which("claude") or "claude"
SYSTEM = "You are a helpful assistant. Follow the user's instructions exactly."
prompts = json.loads(Path(a.prompts).read_text(encoding="utf-8"))
if a.tasks:
    keep = set(a.tasks.split(",")); prompts = [p for p in prompts if p["task"] in keep]
regs = a.registers.split(",")

out = Path(a.out); done = set()
if out.exists():
    for line in out.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if not r.get("is_error"):
                done.add((r["model"], r["task"], r["register"], r["trial"]))

# model-major order so Ollama loads each model once
jobs = [((m, p["task"], reg, tr), p) for m, tr, p, reg in itertools.product(a.models.split(","), range(a.trials), prompts, regs)
        if (m, p["task"], reg, tr) not in done]
print(f"{len(jobs)} jobs to run ({len(done)} already done) -> {out.name}", flush=True)

def call_ollama(model, prompt, seed):
    name = model.split(":", 1)[1]
    body = {"model": name, "stream": False, "keep_alive": "30m",
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            "options": {"num_ctx": 4096, "num_predict": 1024, "seed": seed}}
    for think in (False, None):            # some models reject the think flag
        b = dict(body)
        if think is not None: b["think"] = think
        req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=json.dumps(b).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=a.timeout) as resp:
                d = json.loads(resp.read())
            break
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")
            if think is None or "think" not in err: raise RuntimeError(err)
    return dict(result=d["message"]["content"], is_error=False,
                duration_ms=(d.get("total_duration") or 0) // 1_000_000,
                input_tokens=d.get("prompt_eval_count"), output_tokens=d.get("eval_count"),
                model_used=d.get("model"), thinking=d["message"].get("thinking"))

def call_claude(model, prompt):
    cmd = [CLAUDE, "-p", "--model", model, "--effort", "low", "--output-format", "json", "--max-turns", "1",
           "--tools", "", "--no-session-persistence", "--system-prompt", SYSTEM, prompt]
    cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=a.timeout)
    d = json.loads(cp.stdout); u = d.get("usage") or {}
    return dict(result=d.get("result"), is_error=d.get("is_error"), duration_ms=d.get("duration_ms"),
                input_tokens=u.get("input_tokens"), output_tokens=u.get("output_tokens"),
                model_used=",".join((d.get("modelUsage") or {}).keys()))

def run(job):
    (model, task, reg, trial), p = job
    prompt = p["variants"][reg]
    rec = {"model": model, "task": task, "family": p["family"], "register": reg, "trial": trial,
           "prompt_chars": len(prompt)}
    t0 = time.time()
    try:
        rec.update(call_ollama(model, prompt, trial) if model.startswith("ollama:") else call_claude(model, prompt))
    except subprocess.TimeoutExpired:
        rec.update(result=None, is_error=True, error="timeout")
    except Exception as e:
        rec.update(result=None, is_error=True, error=f"{type(e).__name__}: {str(e)[:500]}")
    rec["wall_s"] = round(time.time() - t0, 1)
    return rec

lock = threading.Lock()
with ThreadPoolExecutor(max_workers=a.workers) as ex, open(out, "a", encoding="utf-8") as f:
    futs = [ex.submit(run, j) for j in jobs]
    for i, fut in enumerate(as_completed(futs), 1):
        rec = fut.result()
        with lock:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        flag = "ERR" if rec.get("is_error") else "ok "
        print(f"[{i}/{len(jobs)}] {flag} {rec['model']:<18} {rec['task']} {rec['register']:<6} t{rec['trial']} "
              f"-> {str(rec.get('result') or rec.get('error'))[:50]!r}  ({rec['wall_s']}s)", flush=True)
