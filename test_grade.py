"""Sanity tests for grade.py with hand-made replies. Run: python test_grade.py"""
import json
from grade import grade
P = {i["task"]: i for i in json.load(open("prompts.json", encoding="utf-8"))}
cases = [
 ("m01", "30", (True, True)), ("m01", "30.", (True, True)), ("m01", "60 left, then half sold.\nAnswer: 30", (True, False)),
 ("m01", "60", (False, False)), ("m10", "$36.80", (True, True)), ("m10", "36.8", (True, True)), ("m10", "110.40", (False, False)),
 ("m02", "1,300", (True, True)), ("m02", "$1300 dollars", (True, True)), ("m05", "4.56", (False, False)),
 ("e02", '{"customer":"Tomas Novak","product":"office chairs","quantity":5,"delivery_date":"2026-05-20","total_eur":1495}', (True, True)),
 ("e02", '```json\n{"customer":"Tomas Novak","product":"Office Chair","quantity":"5","delivery_date":"2026-05-20","total_eur":"1,495"}\n```', (True, True)),
 ("e02", '{"customer":"Tomas Novak","product":"office chair","quantity":4,"delivery_date":"2026-05-20","total_eur":1196}', (False, False)),
 ("e02", 'Here is the JSON:\n{"customer":"Tomas Novak","product":"office chair","quantity":5,"delivery_date":"2026-05-20","total_eur":1495}', (True, False)),
 ("e09", '{"customer":"Paul","product":"ergonomic keyboard","quantity":8,"delivery_date":"2026-10-05","total_eur":720}', (False, False)),
 ("k01", "shipping", (True, True)), ("k01", "**Shipping**", (True, True)), ("k01", "Category: shipping", (True, False)),
 ("k01", "billing", (False, False)), ("k05", "billing or shipping", (False, False)),
 ("f01", "Anna, David, Greta", (True, True)), ("f01", "Anna, Clara, David, Greta", (False, False)),
 ("f01", "The employees are: Anna, David, Greta.", (True, False)), ("f01", "- Anna\n- David\n- Greta", (True, False)),
 ("f03", "T-3, T-4, T-6", (True, True)), ("f08", "web-1, db-1, api-1, api-2", (True, True)),
 ("f08", "web-1, db-1, cache-1, api-1, api-2", (False, False)), ("f06", "AZ102, AZ103, FR300", (True, True)),
 ("c01", "- Sleep restores energy.\n- It improves memory.\n- It lifts mood.", (True, True)),
 ("c01", "- Good for health.\n- b\n- c", (False, False)), ("c01", "Here:\n- a\n- b\n- c", (False, False)),
 ("c02", "The ocean hums with ancient, endless life!", (True, True)), ("c02", "The ocean is vast. It is blue!", (False, False)),
 ("c03", "PARIS\nBERLIN\nROME\nMADRID\nVIENNA", (True, True)), ("c03", "1. PARIS\nBERLIN\nROME\nMADRID\nVIENNA", (False, False)),
 ("c03", "Paris\nBerlin\nRome\nMadrid\nVienna", (False, False)),
 ("c04", "This steel bottle keeps drinks cold.\n\nIt lasts for years.", (True, True)), ("c04", "Steel bottle, no plastic.\n\nNice.", (False, False)),
 ("c05", "Soft leaves fall\nSilent winds blow\nSummer is gone", (True, True)), ("c05", "Soft leaves\nWinds blow\nSummer", (False, False)),
 ("c06", "Simple Ways To Save Money", (True, True)), ("c06", "Saving Money: A Guide", (False, False)), ("c06", "Simple ways to save money", (False, False)),
 ("c07", '{"city": "Paris", "country": "France"}', (True, True)),
 ("c08", "bat, hat, mat, rat", (True, True)), ("c08", "bat, hat, cat, rat", (False, False)), ("c08", "Bat, hat, mat, rat", (False, False)),
 ("c09", "Don't forget our team meeting? It is on Friday at 3 pm.", (True, True)),
 ("c09", "Are you ready for Friday? The meeting is Friday at 3 pm.", (False, False)),
 ("c10", "yes yes yes yes yes yes yes", (True, True)), ("c10", "yes yes yes yes yes yes", (False, False)),
]
bad = 0
for t, reply, want in cases:
    got = grade(P[t], reply)
    if got != want:
        bad += 1; print(f"FAIL {t} {reply!r}: got {got}, want {want}")
print(f"{len(cases)-bad}/{len(cases)} passed")
