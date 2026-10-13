"""Grading. grade(item, reply) -> (correct, exact).

correct = the task was done right (an explanation around the answer is tolerated where the answer can be
          found without guessing).
exact   = correct AND the reply follows the requested output format strictly (number only, JSON only,
          label only, list only). For the format family the constraints are the format, so exact == correct.
"""
import json, re

def strip_think(s):
    return re.sub(r"<think>.*?</think>", "", s or "", flags=re.S).strip()

def clean(s):
    s = strip_think(s)
    s = re.sub(r"^```[a-zA-Z]*\s*\n?|\n?```\s*$", "", s.strip())
    return s.strip()

def lenient(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())

NUM = r"-?\$?€?\d[\d,]*(?:\.\d+)?"
def to_num(tok):
    try: return float(tok.replace("$", "").replace("€", "").replace(",", ""))
    except ValueError: return None

def g_number(item, reply):
    exp = float(item["expected"]); s = clean(reply).replace("**", "")
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    if not lines: return False, False
    def line_ok(l):
        nums = re.findall(NUM, l)
        return bool(nums) and abs((to_num(nums[-1]) or 1e18) - exp) < 1e-6
    exact = len(lines) == 1 and re.fullmatch(r"[\s$€]*" + NUM + r"[\s.]*(dollars|euros)?\.?", lines[0], re.I) is not None and line_ok(lines[0])
    # correct: final line holds the answer, or a line marked as the answer does
    correct = exact or line_ok(lines[-1]) or any(re.search(r"answer|total|=|result", l, re.I) and line_ok(l) for l in lines[-3:])
    return correct, exact

def find_json(s):
    m = re.search(r"\{.*\}", s, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def field_eq(k, got, exp):
    if isinstance(exp, (int, float)):
        if isinstance(got, str): got = to_num(re.sub(r"[^\d.,-]", "", got) or "x")
        return isinstance(got, (int, float)) and abs(got - exp) < 1e-6
    g, e = lenient(str(got)), lenient(str(exp))
    if k == "delivery_date": return str(got).strip() == exp
    # product: accept plural or a longer name that contains the expected one ("Desk Lamps")
    return bool(g) and (e in g or g.rstrip("s") == e or g == e + "es")

def g_json(item, reply):
    s = clean(reply); obj = find_json(s)
    fields = item["check"]["fields"]
    if not isinstance(obj, dict): return False, False
    correct = all(k in obj and field_eq(k, obj[k], v) for k, v in fields.items())
    exact = correct and s.startswith("{") and s.endswith("}") and set(obj) == set(fields)
    return correct, exact

def g_label(item, reply):
    s = clean(reply).replace("*", "").strip(); labels = item["check"]["labels"]; exp = item["expected"]
    found = {l for l in labels if re.search(rf"\b{l}\b", s, re.I)}
    exact = lenient(s) == exp
    correct = exact or found == {exp} or lenient(s.splitlines()[0] if s else "") == exp
    return correct, exact

def g_list(item, reply):
    exp = [lenient(x) for x in item["expected"].split(",")]
    s = clean(reply).replace("**", "")
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    def parse(l):
        l = l.split(":", 1)[1] if ":" in l and not re.match(r"^[A-Za-z]+-\d", l) and len(l.split(":", 1)[0].split()) <= 4 else l
        return [lenient(x) for x in re.split(r",|\band\b", l) if lenient(x)]
    exact = len(lines) == 1 and [lenient(x) for x in lines[0].rstrip(".").split(",")] == exp
    correct = exact or any(parse(l) == exp for l in lines)
    if not correct:  # one item per line
        items = [lenient(re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", l)) for l in lines]
        correct = items == exp
    return correct, exact

WORD = re.compile(r"[A-Za-z0-9'’-]+")
def words(s): return WORD.findall(s)
def nonempty(s): return [l.rstrip() for l in s.splitlines() if l.strip()]

def g_format(item, reply):
    c = item["check"]; s = clean(reply); t = c["type"]; low = s.lower()
    if t == "bullets":
        ls = nonempty(s)
        ok = len(ls) == c["n"] and all(l.lstrip().startswith("- ") for l in ls) and not any(re.search(rf"\b{w}\b", low) for w in c["forbid"])
    elif t == "one_sentence":
        ls = nonempty(s); body = s.strip()
        ok = len(ls) == 1 and body.endswith(c["end"]) and len(words(body)) <= c["max_words"] and len(re.findall(r"[.!?](\s|$)", body)) == 1
    elif t == "upper_lines":
        ls = [l.strip() for l in nonempty(s)]
        ok = (len(ls) == c["n"] and all(l == l.upper() and not re.match(r"^[\d\-*•]", l) for l in ls)
              and all(l.lower().strip(" .") in c["allowed"] for l in ls) and len({l for l in ls}) == c["n"])
    elif t == "paragraphs":
        paras = [p for p in re.split(r"\n\s*\n", s.strip()) if p.strip()]
        ok = (len(paras) == c["n"] and all(re.search(rf"\b{w}\b", low) for w in c["require"])
              and not any(re.search(rf"\b{w}\b", low) for w in c["forbid"]))
    elif t == "lines_start":
        ls = [l.strip().lstrip("*_\"'") for l in nonempty(s)]
        ok = len(ls) == c["n"] and all(l[:1].lower() == c["letter"] for l in ls)
    elif t == "title":
        ls = nonempty(s); body = s.strip().strip("\"'*#").strip()
        ws = words(body)
        ok = len(ls) == 1 and 0 < len(ws) <= c["max_words"] and c["forbid_chars"] not in body and all(w[0].isupper() or w[0].isdigit() for w in ws)
    elif t == "json_fields":
        return g_json(item, reply)
    elif t == "rhymes":
        parts = [p.strip().rstrip(".") for p in s.split(",")]
        ok = (len(nonempty(s)) == 1 and len(parts) == c["n"] and all(re.fullmatch(r"[a-z]+", p) and p.endswith(c["suffix"]) for p in parts)
              and c["exclude"] not in parts and len(set(parts)) == c["n"])
    elif t == "two_sentences_q":
        ends = re.findall(r"[.!?](?=\s|$)", s.strip())
        ok = len(ends) == 2 and ends[0] == "?" and len(re.findall(rf"\b{c['word']}\b", low)) == c["count"]
    elif t == "repeat":
        ok = s.strip().rstrip(".!").lower() == " ".join([c["word"]] * c["n"])
    else:
        raise ValueError(t)
    return ok, ok

def grade(item, reply):
    if not reply: return False, False
    t = item["check"]["type"]
    if item["family"] == "math": return g_number(item, reply)
    if item["family"] == "extract": return g_json(item, reply)
    if item["family"] == "classify": return g_label(item, reply)
    if item["family"] == "filter": return g_list(item, reply)
    return g_format(item, reply)
