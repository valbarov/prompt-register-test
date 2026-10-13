"""Shows that the three registers really differ in language, and by how much they differ in length.
Flesch-Kincaid grade uses a simple vowel-group syllable count (standard library only).
Only the instruction text is measured: pasted data blocks (order notes, tickets, record lists) are the
same across registers and are removed first."""
import json, re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
items = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))

def syllables(w):
    w = w.lower().strip("'")
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1: n -= 1
    return max(n, 1)

def instruction_only(item, text):
    t = text
    if item["family"] in ("extract", "classify"):
        t = re.split(r"\n\n(?:Order note|Order correspondence|Message|Communication):\n", t)[0]
    if item["family"] == "filter":
        lines = t.split("\n"); t = " ".join([lines[0], lines[-1]])
    return t

def stats(t):
    ws = re.findall(r"[A-Za-z']+", t)
    sents = max(len(re.findall(r"[.!?](?:\s|$)", t)), 1)
    syl = sum(syllables(w) for w in ws)
    return dict(words=len(ws), sents=sents, syl=syl, long=sum(len(w) >= 9 for w in ws), chars=len(t))

agg = defaultdict(lambda: defaultdict(float))
for it in items:
    for reg, text in it["variants"].items():
        s = stats(instruction_only(it, text))
        for k, v in s.items(): agg[reg][k] += v
        agg[reg]["n"] += 1
        agg[(it["family"], reg)]["words"] += s["words"]; agg[(it["family"], reg)]["n"] += 1

def fk(d): return 0.39 * d["words"] / d["sents"] + 11.8 * d["syl"] / d["words"] - 15.59
print("| register | FK grade | words/sentence | syllables/word | words with 9+ letters | avg instruction words |")
print("|---|---|---|---|---|---|")
for reg in ("plain", "normal", "ornate"):
    d = agg[reg]
    print(f"| {reg} | {fk(d):.1f} | {d['words']/d['sents']:.1f} | {d['syl']/d['words']:.2f} | "
          f"{100*d['long']/d['words']:.0f}% | {d['words']/d['n']:.0f} |")
print("\n| family | plain words | normal words | ornate words |\n|---|---|---|---|")
for fam in ("math", "extract", "classify", "filter", "format"):
    print(f"| {fam} | " + " | ".join(f"{agg[(fam, r)]['words']/agg[(fam, r)]['n']:.0f}" for r in ("plain", "normal", "ornate")) + " |")
