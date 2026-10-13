# Math ablation

| setup | plain | normal | ornate |
|---|---|---|---|
| own | 28% correct, 27% shown | 34% correct, 37% shown | 18% correct, 8% shown |
| A | 37% correct, 39% shown | 35% correct, 37% shown | 40% correct, 43% shown |
| B | 84% correct, 100% shown | 83% correct, 100% shown | 79% correct, 100% shown |

## Setup own: correct % (working shown %)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 33 (77) | 37 (77) | 7 (13) |
| qwen3:1.7b | 17 (17) | 50 (63) | 10 (0) |
| qwen3:4b-instruct | 97 (100) | 93 (100) | 43 (43) |
| qwen3:8b | 17 (10) | 47 (47) | 13 (3) |
| qwen3:14b | 30 (10) | 13 (3) | 37 (0) |
| gemma3:1b | 0 (0) | 0 (3) | 7 (0) |
| gemma3:4b | 7 (0) | 10 (0) | 13 (0) |
| gemma3:12b | 23 (0) | 23 (0) | 17 (0) |
| ALL | 28 (27) | 34 (37) | 18 (8) |

## Setup A: correct % (working shown %)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 50 (83) | 37 (77) | 50 (93) |
| qwen3:1.7b | 53 (80) | 57 (67) | 60 (87) |
| qwen3:4b-instruct | 93 (100) | 93 (100) | 97 (100) |
| qwen3:8b | 40 (40) | 47 (47) | 67 (60) |
| qwen3:14b | 27 (10) | 13 (3) | 30 (7) |
| gemma3:1b | 0 (0) | 0 (3) | 0 (0) |
| gemma3:4b | 10 (0) | 10 (0) | 7 (0) |
| gemma3:12b | 20 (0) | 20 (0) | 13 (0) |
| ALL | 37 (39) | 35 (37) | 40 (43) |

## Setup B: correct % (working shown %)

| model | plain | normal | ornate |
|---|---|---|---|
| qwen3:0.6b | 60 (100) | 53 (100) | 57 (100) |
| qwen3:1.7b | 40 (100) | 57 (100) | 43 (100) |
| qwen3:4b-instruct | 100 (100) | 90 (100) | 97 (100) |
| qwen3:8b | 90 (100) | 93 (100) | 70 (100) |
| qwen3:14b | 100 (100) | 100 (100) | 100 (100) |
| gemma3:1b | 87 (100) | 73 (100) | 67 (100) |
| gemma3:4b | 97 (100) | 100 (100) | 100 (100) |
| gemma3:12b | 100 (100) | 100 (100) | 100 (100) |
| ALL | 84 (100) | 83 (100) | 79 (100) |
