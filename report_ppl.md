# Perplexity of the instruction wording

Perplexity = exp(mean NLL per token). Lower = more familiar to the model.

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 15.6 | 16.7 | 37.2 |
| qwen3:1.7b | 15.9 | 16.3 | 31.2 |
| qwen3:4b-instruct | 17.4 | 17.4 | 31.9 |

## By family (mean over the 3 models)

| family | plain | normal | ornate |
|---|---|---|---|
| math | 8.5 | 7.3 | 31.6 |
| extract | 17.2 | 15.4 | 28.1 |
| classify | 28.0 | 30.9 | 25.3 |
| filter | 12.7 | 15.3 | 36.8 |
| format | 22.0 | 24.8 | 49.9 |

## Within-task link: familiarity vs accuracy (r, 95% CI)

| model | all 50 tasks | without math |
|---|---|---|
| qwen3:0.6b | -0.17 [-0.36, +0.03] | +0.08 [-0.10, +0.25] |
| qwen3:1.7b | -0.21 [-0.43, +0.01] | -0.15 [-0.39, +0.13] |
| qwen3:4b-instruct | -0.41 [-0.61, -0.15] | -0.15 [-0.38, +0.13] |

## Most familiar register, counted over tasks

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 31 | 18 | 1 |
| qwen3:1.7b | 15 | 25 | 10 |
| qwen3:4b-instruct | 15 | 24 | 11 |
