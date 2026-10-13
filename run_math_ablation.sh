#!/usr/bin/env bash
# Math ablation: 8 models x 10 problems x 3 registers x 3 trials, for each fixed format line (A, B).
# One model at a time, with all models unloaded in between, so the 14B does not spill out of VRAM.
cd "$(dirname "$0")"
for m in qwen3:0.6b gemma3:1b qwen3:1.7b qwen3:4b-instruct gemma3:4b qwen3:8b gemma3:12b qwen3:14b; do
  for loaded in $(ollama ps | awk 'NR>1{print $1}'); do ollama stop "$loaded"; done
  for k in A B; do
    python run.py --prompts prompts_math_$k.json --models ollama:$m --trials 3 --out results_math_$k.jsonl
  done
done
echo MATH_DONE
