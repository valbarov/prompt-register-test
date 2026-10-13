#!/usr/bin/env bash
# Full local run: 8 models x 50 tasks x 3 registers x 3 trials = 3,600 calls, smallest models first.
cd "$(dirname "$0")"
M=ollama:qwen3:0.6b,ollama:gemma3:1b,ollama:qwen3:1.7b,ollama:qwen3:4b,ollama:gemma3:4b,ollama:qwen3:8b,ollama:gemma3:12b,ollama:qwen3:14b
python run.py --models $M --trials 3 --workers 1 --out results.jsonl
python analyze.py results.jsonl > report.md
echo LOCAL_DONE
