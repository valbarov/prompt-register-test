# prompt-register-test

Does the language of a prompt change how well local LLMs answer? This repo holds 50 tasks written in three registers (plain, normal, ornate), the runner, the grader, every raw reply from 8 local models, a math follow-up that isolates the format line, and a perplexity check.

Short answer: the register barely matters. From 8B up, plain, normal, and ornate land within 4 points of each other. At 4B and below, normal does slightly best (about 8 points, intervals touch zero). The big swings come from the format line: "number only" stops a model with thinking off from writing out its working, and then it guesses. Same problems, same models: 37% with "number only", 82% with "work it out step by step".

Article: *link coming*

## Layout

| file | what it is |
|---|---|
| `build_prompts.py` | The 50 tasks in three registers. Writes `prompts.json`. Pasted data (order notes, tickets, record lists) is identical across registers; only the wording around it changes. Math problems are rewritten as a whole. |
| `prompts.json` | 50 tasks x 3 registers. Families: `math` (number), `extract` (JSON with fixed keys), `classify` (one of 4 labels), `filter` (filtered and sorted list, with edge-case traps), `format` (IFEval-style checkable constraints). |
| `judge_input.txt` | The input given to a Claude subagent that checked every triple for equal meaning and solved every task. Three small fixes were applied after its review. |
| `readability.py` | Flesch-Kincaid grade and length per register (instruction text only). |
| `grade.py`, `test_grade.py` | Automatic grading. `correct` = the answer is right (extra words tolerated). `exact` = right and the format was followed strictly. `test_grade.py` has 51 hand-made cases. |
| `run.py` | Runner. Ollama HTTP API (and optionally Claude via `claude -p`). One fresh session per call, resumable. Seed = trial number, thinking off, `num_ctx` 4096, `num_predict` 1024, Ollama default temperature. |
| `run_local.sh` | The main run: 8 models x 50 tasks x 3 registers x 3 trials. |
| `build_math_ablation.py`, `run_math_ablation.sh` | Math follow-up. Each problem keeps its register, but all three end with the same line: A = "Answer with the number only.", B = "Work it out step by step, then write the final number on the last line." |
| `ppl.py`, `analyze_ppl.py` | Perplexity of the instruction wording (pasted data excluded) under Qwen3 0.6B, 1.7B, and 4B-Instruct-2507 (Hugging Face, bf16), and its within-task link to accuracy. |
| `analyze.py`, `analyze_math.py` | Reports with 95% bootstrap intervals that resample tasks. |
| `report.md`, `report_math.md`, `report_ppl.md` | Generated reports. |
| `results.jsonl`, `results_math_A.jsonl`, `results_math_B.jsonl`, `ppl.jsonl` | Every call: model, task, register, trial, prompt length, reply, tokens, latency. |

## Models

Through Ollama, Q4 builds: `qwen3:0.6b`, `qwen3:1.7b`, `qwen3:4b-instruct`, `qwen3:8b`, `qwen3:14b`, `gemma3:1b`, `gemma3:4b`, `gemma3:12b`.

`results.jsonl` also contains `qwen3:4b`. That tag is now the Thinking-2507 build: it ignores `think: false`, reasons for about 800 tokens before every answer, and 44% of its replies hit the 1,024-token limit before the answer. It is left out of the conclusions and kept only for transparency.

## Reproduce

Requirements: Python 3.10+ (standard library only for the runs and reports), Ollama running locally. The perplexity check needs `torch` and `transformers`.

```bash
python build_prompts.py
python build_math_ablation.py
python test_grade.py

bash run_local.sh              # main run, writes results.jsonl and report.md
bash run_math_ablation.sh      # math follow-up
python run.py --models ollama:qwen3:4b-instruct --trials 3 --out results.jsonl

python analyze.py results.jsonl > report.md
python analyze_math.py > report_math.md
python readability.py

# perplexity (GPU)
python ppl.py
python analyze_ppl.py > report_ppl.md
```

Runs are resumable: a rerun skips every (model, task, register, trial) already in the output file.

Windows note: call Ollama at `127.0.0.1`, not `localhost`. On Windows, `localhost` may try IPv6 first and add about 2 seconds to every request.
