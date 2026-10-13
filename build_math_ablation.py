"""Math ablation: keep each problem's wording in its register, but replace the register's own format line
with one fixed line shared by all three registers. Separates 'harder to read' from 'format line obeyed
more strictly'.
  A: "Answer with the number only."  (bare answer, same for all registers)
  B: "Work it out step by step, then write the final number on the last line."  (reasoning allowed)"""
import json
from pathlib import Path
HERE = Path(__file__).parent
ENDS = {"plain": " Give only the number.", "normal": " Answer with the number only.",
        "ornate": " Furnish solely the numerical figure, without accompanying exposition."}
FIXED = {"A": " Answer with the number only.",
         "B": " Work it out step by step, then write the final number on the last line."}
items = [i for i in json.loads((HERE / "prompts.json").read_text(encoding="utf-8")) if i["family"] == "math"]
for k, line in FIXED.items():
    out = []
    for it in items:
        v = {}
        for reg, text in it["variants"].items():
            assert text.endswith(ENDS[reg]), (it["task"], reg)
            v[reg] = text[: -len(ENDS[reg])] + line
        out.append({**it, "variants": v})
    (HERE / f"prompts_math_{k}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"prompts_math_{k}.json: {len(out)} tasks")
