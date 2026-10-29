#!/usr/bin/env python3
"""Targeted temporal check: version dates on July-7 family + distinctive May names.
Appends one JSON line per name to data/2026-09-29-gem-temporal-pivot/gem-temporal-pivot-diffend-targeted-check.jsonl.
Skips names already present. Read-only, ~3s spacing + retry.
"""
import sys, time, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diffend_temporal_sweep import gem_versions

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))),
                   "data", "2026-09-29-gem-temporal-pivot", "gem-temporal-pivot-diffend-targeted-check.jsonl")
NAMES = ["attacker-xss-admin-1", "xssname-1783397821", "test-apex-gem", "test-ssti-0",
         "test-ssti-1", "test-ssti-4", "zz-oai-test12", "zzfadgivar00", "zzdelay2119",
         "southwarkssrfhack", "tryf3zz", "xss-test-gem", "southpxdatapp6pi"]

done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        try: done.add(json.loads(line)["name"])
        except Exception: pass

out = open(OUT, "a")
for n in NAMES:
    if n in done:
        continue
    vers, st = gem_versions(n)
    if vers is None:
        time.sleep(8)
        vers, st = gem_versions(n)
    if vers is None:
        rec = {"name": n, "ok": False, "status": str(st)}
    else:
        oow = [v[0] for v in vers if v[3]]
        rec = {"name": n, "ok": True,
               "versions": [{"version": v[0], "ts": v[1], "ts_iso": v[2]} for v in vers],
               "out_of_window": oow}
    out.write(json.dumps(rec) + "\n"); out.flush()
    print("%s -> %s" % (n, "OOW=%s" % rec.get("out_of_window") if rec.get("ok") else "FAIL %s" % rec.get("status")), flush=True)
    time.sleep(3)
out.close()
print("DONE", flush=True)
