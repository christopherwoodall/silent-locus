#!/usr/bin/env python3
"""Heuristic outcome classification over the sampled shards (read-only).

Classes (proxies, NOT ground-truth resolved/unresolved labels):
  C1 clean_finish  - last environment message returncode == 0
  C2 error_finish  - last environment message returncode != 0
  C3 giveup_lang   - final assistant message contains give-up language
  C4 length_q      - trajectory length quartile (1=short .. 4=long)
A trajectory can carry C1/C2 plus C3 and a C4 quartile.
Writes OUTCOME-MIX.md and outcome_mix.json.
"""
import re, json, glob, os
from collections import Counter
import pyarrow.parquet as pq
import pandas as pd

RAW = os.path.dirname(os.path.abspath(__file__))
rc_re = re.compile(r"<returncode>(-?\d+)</returncode>")
marker_re = re.compile(r"MINI_SWE_AGENT_FINAL_OUTPUT")
stuck_re = re.compile(r"(?i)\b(unable to|cannot|could not|failed to|give up|giving up|stuck|exhausted|out of (steps|time|ideas)|no (further |more )?progress|limit reached|max\w* steps)\b")

files = sorted(glob.glob(os.path.join(RAW, "train-*-of-00047.parquet")))
assert files, "no shards found"
print(f"{len(files)} shards")

lens_all, rows = [], []
for f in files:
    tbl = pq.read_table(f, columns=["instance_id", "messages"]).to_pandas()
    for _, r in tbl.iterrows():
        m = r.messages
        lastA = m[-1]["content"] if m[-1]["role"] == "assistant" else ""
        lastU = ""
        for x in reversed(m):
            if x["role"] == "user":
                lastU = x["content"]; break
        rcs = rc_re.findall(" ".join(x["content"] for x in m if x["role"] == "user"))
        rows.append({
            "shard": os.path.basename(f),
            "id": r.instance_id,
            "n_msgs": len(m),
            "final_marker": bool(marker_re.search(lastA)),
            "stuck_kw": bool(stuck_re.search(lastA)),
            "last_rc": rcs[-1] if rcs else None,
            "n_nonzero": sum(1 for x in rcs if x != "0"),
        })
        lens_all.append(len(m))

q1, q2, q3 = pd.Series(lens_all).quantile([0.25, 0.5, 0.75])
def quart(n):
    return 1 if n <= q1 else 2 if n <= q2 else 3 if n <= q3 else 4

c1 = c2 = c3 = 0
q = Counter(); no_marker = 0; norc = 0
for r in rows:
    r["q"] = quart(r["n_msgs"]); q[r["q"]] += 1
    if r["last_rc"] == "0": c1 += 1
    elif r["last_rc"] is None: norc += 1
    else: c2 += 1
    if r["stuck_kw"]: c3 += 1
    if not r["final_marker"]: no_marker += 1

n = len(rows)
mix = {
    "n_trajectories": n, "n_shards": len(files),
    "length_quartiles": {"q1_max": int(q1), "median": int(q2), "q3_max": int(q3)},
    "C1_clean_finish_last_rc0": c1, "C1_pct": round(100*c1/n, 2),
    "C2_error_finish_last_rc_nonzero": c2, "C2_pct": round(100*c2/n, 2),
    "C2_no_returncode_found": norc,
    "C3_giveup_language": c3, "C3_pct": round(100*c3/n, 2),
    "C4_length_quartile_counts": {str(k): q[k] for k in sorted(q)},
    "no_final_marker": no_marker,
}
json.dump(mix, open(os.path.join(RAW, "outcome_mix.json"), "w"), indent=2)
with open(os.path.join(RAW, "OUTCOME-MIX.md"), "w") as fh:
    fh.write("# Outcome mix (heuristic, from trajectory text)\n\n")
    fh.write("Date: 2026-10-17 (UTC). These are proxies, not ground-truth labels.\n")
    fh.write("The dataset has no resolved/unresolved column.\n\n")
    fh.write(f"- Trajectories scored: {n} in {len(files)} shards\n")
    fh.write(f"- Length quartiles (messages): Q1<={int(q1)}, median={int(q2)}, Q3<={int(q3)}\n")
    fh.write(f"- C1 clean finish (last tool call rc=0): {c1} ({100*c1/n:.2f}%)\n")
    fh.write(f"- C2 error finish (last tool call rc!=0): {c2} ({100*c2/n:.2f}%)\n")
    fh.write(f"- no returncode found: {norc}\n")
    fh.write(f"- C3 give-up language in final message: {c3} ({100*c3/n:.2f}%)\n")
    fh.write(f"- C4 length quartiles: {dict(sorted(q.items()))}\n")
    fh.write(f"- missing final-output marker: {no_marker}\n")
print(json.dumps(mix, indent=2))
