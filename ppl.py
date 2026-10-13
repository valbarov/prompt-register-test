"""Perplexity test: how familiar does each prompt look to the model?

For each model and each of the 150 prompts, the prompt is placed in the model's chat template (same system
prompt as the runs) and scored as a user turn. We record the mean negative log-likelihood (NLL, nats per
token) of the user-message tokens, leaving out the pasted data block that is identical across registers
(order note, ticket, record list), so only the instruction wording is scored.

Usage: .venv/Scripts/python.exe ppl.py  -> ppl.jsonl"""
import json, difflib, sys
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

HERE = Path(__file__).parent
SYSTEM = "You are a helpful assistant. Follow the user's instructions exactly."
MODELS = {"qwen3:0.6b": "Qwen/Qwen3-0.6B", "qwen3:1.7b": "Qwen/Qwen3-1.7B", "qwen3:4b-instruct": "Qwen/Qwen3-4B-Instruct-2507"}
items = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))

def shared_block(item):
    """Character span of the data block shared by all three variants, or None."""
    a, b = item["variants"]["plain"], item["variants"]["normal"]
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    block = a[m.a: m.a + m.size]
    return block if m.size >= 60 and block in item["variants"]["ornate"] else None

out = open(HERE / "ppl.jsonl", "w", encoding="utf-8")
for short, hf in MODELS.items():
    tok = AutoTokenizer.from_pretrained(hf)
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.bfloat16).cuda().eval()
    for it in items:
        block = shared_block(it)
        for reg, prompt in it["variants"].items():
            msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False, enable_thinking=False)
            start = text.index(prompt); end = start + len(prompt)
            skip = None
            if block:
                bs = start + prompt.index(block); skip = (bs, bs + len(block))
            enc = tok(text, return_offsets_mapping=True, return_tensors="pt")
            ids = enc["input_ids"].cuda(); offs = enc["offset_mapping"][0].tolist()
            with torch.no_grad():
                logits = model(ids).logits[0, :-1].float()
            nll = torch.nn.functional.cross_entropy(logits, ids[0, 1:], reduction="none").tolist()
            keep = []
            for i, (s, e) in enumerate(offs[1:]):      # token i+1 is predicted by position i
                if s >= start and e <= end and e > s and not (skip and s < skip[1] and e > skip[0]):
                    keep.append(nll[i])
            rec = {"model": short, "task": it["task"], "family": it["family"], "register": reg,
                   "tokens": len(keep), "nll": sum(keep) / len(keep)}
            out.write(json.dumps(rec) + "\n")
    print(f"{short}: done", flush=True)
    del model; torch.cuda.empty_cache()
out.close()
