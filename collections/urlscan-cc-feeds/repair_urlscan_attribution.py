#!/usr/bin/env python3
"""One-time repair (2026-10-03): correct over-attribution in urlscan.jsonl.

The initial mapping set labels.attribution.provider=openai on every record
whose scan URL merely contained the substring "oai" (query classes
page.url:oai* / task.url:oai* / filename:oai*). Audit showed these are
unrelated recent scans (OpenAI-brand phishing infra, "occupyai", "oai-pmh",
etc.) — NOT oai* tag matches, and zero records carry the corroborated
tag form zz=oai<digits>. Per the lane rule (provider=openai ONLY on direct
evidence), this repair removes the provider attribution and the
oai-fingerprint tag from all oai-fingerprint-class records, keeping
fingerprints (uuid-derived) and everything else identical so the file stays
ES-append-safe and idempotent.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PATH = os.path.join(ROOT, "openai-agent-traces", "data", "urlscan.jsonl")

fixed = 0
out = []
with open(PATH) as f:
    for line in f:
        rec = json.loads(line)
        if rec["labels"].get("query.class") == "oai-fingerprint":
            rec["labels"].pop("attribution.provider", None)
            rec["tags"] = [t for t in rec["tags"] if t != "oai-fingerprint"]
            rec["matched_string"] = None
            rec.pop("matched_string", None)
            rec["note"] = ("2026-10-03 repair: initial mapping set "
                           "attribution.provider=openai on substring 'oai' matches; "
                           "audit found zero records carrying the corroborated tag form "
                           "(zz=oai<digits>). These are unrelated recent scans (OpenAI-brand "
                           "phishing infra, 'occupyai', 'oai-pmh', etc.) — provider attribution "
                           "withheld; no eval-agent evidence. Record kept as a logged "
                           "query hit only.")
            fixed += 1
        out.append(rec)

with open(PATH, "w") as f:
    for rec in out:
        f.write(json.dumps(rec) + "\n")
print(f"repaired {fixed} records; fingerprints unchanged")
