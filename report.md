# Prompt register test (4050 graded calls, 0 errors)

Each cell: percent correct over 50 tasks x trials. Difference columns: percentage points, 95% bootstrap interval over tasks.

## Correct (answer right, extra words tolerated)

| model | plain | normal | ornate | plain - normal | ornate - normal |
|---|---|---|---|---|---|
| qwen3:0.6b | 31 | 41 | 33 | -9 [-20, +1] | -8 [-18, +2] |
| qwen3:1.7b | 58 | 65 | 50 | -7 [-17, +3] | -15 [-25, -5] |
| qwen3:4b-instruct | 85 | 90 | 72 | -5 [-14, +3] | -18 [-31, -5] |
| qwen3:8b | 62 | 69 | 62 | -7 [-16, +1] | -7 [-18, +3] |
| qwen3:14b | 69 | 63 | 69 | +5 [-3, +14] | +5 [-4, +15] |
| gemma3:1b | 41 | 49 | 44 | -7 [-16, +1] | -5 [-14, +5] |
| gemma3:4b | 57 | 58 | 57 | -1 [-7, +5] | -1 [-9, +7] |
| gemma3:12b | 67 | 64 | 65 | +3 [-4, +11] | +1 [-3, +6] |
| qwen3:4b | 35 | 32 | 37 | +3 [-2, +9] | +5 [+0, +11] |

## Exact (answer right AND output format followed strictly)

| model | plain | normal | ornate | plain - normal | ornate - normal |
|---|---|---|---|---|---|
| qwen3:0.6b | 25 | 31 | 31 | -7 [-17, +3] | -1 [-8, +7] |
| qwen3:1.7b | 55 | 54 | 50 | +1 [-7, +7] | -4 [-13, +5] |
| qwen3:4b-instruct | 63 | 59 | 57 | +3 [-2, +9] | -2 [-9, +5] |
| qwen3:8b | 60 | 60 | 61 | -0 [-6, +6] | +1 [-6, +9] |
| qwen3:14b | 67 | 63 | 69 | +4 [-3, +12] | +6 [-3, +15] |
| gemma3:1b | 41 | 43 | 44 | -1 [-11, +9] | +1 [-10, +13] |
| gemma3:4b | 57 | 58 | 57 | -1 [-7, +5] | -1 [-9, +7] |
| gemma3:12b | 67 | 64 | 65 | +3 [-4, +11] | +1 [-3, +6] |
| qwen3:4b | 0 | 0 | 0 | +0 [+0, +0] | +0 [+0, +0] |

## Without math (40 tasks; math is explained by the format line, see analyze_math.py)

| model | plain | normal | ornate | plain - normal | ornate - normal |
|---|---|---|---|---|---|
| qwen3:0.6b | 31 | 39 | 39 | -8 [-21, +3] | +0 [-9, +9] |
| qwen3:1.7b | 68 | 68 | 60 | +1 [-8, +9] | -8 [-17, +2] |
| qwen3:4b-instruct | 82 | 89 | 79 | -8 [-18, +2] | -10 [-22, +1] |
| qwen3:8b | 73 | 75 | 74 | -2 [-9, +6] | -1 [-9, +7] |
| qwen3:14b | 78 | 76 | 77 | +3 [-5, +10] | +1 [-8, +9] |
| gemma3:1b | 52 | 61 | 53 | -9 [-19, +1] | -8 [-19, +4] |
| gemma3:4b | 69 | 70 | 68 | -1 [-8, +7] | -2 [-12, +8] |
| gemma3:12b | 78 | 74 | 78 | +4 [-4, +13] | +3 [+0, +9] |
| qwen3:4b | 21 | 16 | 22 | +5 [-1, +11] | +7 [+1, +12] |

## Family: math (correct)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 33 | 47 | 7 |
| qwen3:1.7b | 17 | 53 | 10 |
| qwen3:4b-instruct | 97 | 93 | 43 |
| qwen3:8b | 17 | 47 | 13 |
| qwen3:14b | 30 | 13 | 37 |
| gemma3:1b | 0 | 0 | 7 |
| gemma3:4b | 7 | 10 | 13 |
| gemma3:12b | 23 | 23 | 17 |
| qwen3:4b | 93 | 97 | 97 |

## Family: extract (correct)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 47 | 73 | 87 |
| qwen3:1.7b | 100 | 100 | 90 |
| qwen3:4b-instruct | 100 | 100 | 90 |
| qwen3:8b | 100 | 100 | 90 |
| qwen3:14b | 100 | 100 | 90 |
| gemma3:1b | 80 | 80 | 90 |
| gemma3:4b | 100 | 97 | 90 |
| gemma3:12b | 100 | 90 | 100 |
| qwen3:4b | 30 | 7 | 27 |

## Family: classify (correct)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 37 | 40 | 33 |
| qwen3:1.7b | 90 | 100 | 83 |
| qwen3:4b-instruct | 100 | 100 | 100 |
| qwen3:8b | 97 | 100 | 100 |
| qwen3:14b | 100 | 100 | 100 |
| gemma3:1b | 73 | 100 | 93 |
| gemma3:4b | 100 | 100 | 100 |
| gemma3:12b | 100 | 100 | 100 |
| qwen3:4b | 0 | 0 | 0 |

## Family: filter (correct)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 0 | 3 | 0 |
| qwen3:1.7b | 0 | 0 | 10 |
| qwen3:4b-instruct | 37 | 60 | 40 |
| qwen3:8b | 0 | 10 | 10 |
| qwen3:14b | 30 | 17 | 20 |
| gemma3:1b | 0 | 0 | 0 |
| gemma3:4b | 0 | 0 | 0 |
| gemma3:12b | 23 | 7 | 10 |
| qwen3:4b | 53 | 57 | 60 |

## Family: format (correct)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 40 | 40 | 37 |
| qwen3:1.7b | 83 | 70 | 57 |
| qwen3:4b-instruct | 90 | 97 | 87 |
| qwen3:8b | 97 | 90 | 97 |
| qwen3:14b | 83 | 87 | 97 |
| gemma3:1b | 53 | 63 | 30 |
| gemma3:4b | 77 | 83 | 80 |
| gemma3:12b | 90 | 100 | 100 |
| qwen3:4b | 0 | 0 | 3 |

## Cost: mean input tokens / output tokens / seconds per call

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 139 / 36 / 0.3 | 126 / 42 / 0.3 | 162 / 32 / 0.2 |
| qwen3:1.7b | 139 / 23 / 0.2 | 126 / 35 / 0.2 | 162 / 20 / 0.1 |
| qwen3:4b-instruct | 131 / 59 / 0.6 | 118 / 92 / 0.8 | 154 / 54 / 0.5 |
| qwen3:8b | 139 / 21 / 0.3 | 126 / 30 / 0.4 | 162 / 22 / 0.3 |
| qwen3:14b | 139 / 22 / 4.0 | 126 / 22 / 3.9 | 162 / 22 / 4.0 |
| gemma3:1b | 134 / 24 / 0.4 | 122 / 31 / 0.3 | 153 / 25 / 0.3 |
| gemma3:4b | 136 / 23 / 0.3 | 124 / 23 / 0.2 | 155 / 23 / 0.2 |
| gemma3:12b | 136 / 22 / 0.6 | 124 / 22 / 0.5 | 155 / 22 / 0.5 |
| qwen3:4b | 133 / 778 / 8.6 | 120 / 749 / 8.2 | 156 / 795 / 8.4 |

## Tasks with the biggest register effect (mean over models, points)

| task | family | plain | normal | ornate |
|---|---|---|---|---|
| e01 | extract | 78 | 85 | 22 |
| m08 | math | 37 | 59 | 26 |
| m04 | math | 26 | 41 | 11 |
| m01 | math | 37 | 52 | 30 |
| c04 | format | 78 | 74 | 52 |
| f01 | filter | 33 | 52 | 33 |
| f08 | filter | 11 | 0 | 15 |
| e03 | extract | 81 | 70 | 89 |
| e07 | extract | 93 | 78 | 96 |
| f03 | filter | 15 | 19 | 37 |
