#!/usr/bin/env python3
"""Dormancy check: for burst accounts, fetch global editcount via list=users.
Usage: dormancy_check.py <host> <accounts.txt> <out.tsv> <raw.jsonl>
accounts.txt: one "name<TAB>creation_ts" per line. Batched 50/query, paced >=5s.
curl only (VM Python HTTP stacks break on the egress proxy).
"""
import json, subprocess, sys, time, urllib.parse

host, acctf, outtsv, rawjl = sys.argv[1:5]
accts = []
for line in open(acctf):
    line = line.rstrip("\n")
    if line:
        parts = line.split("\t")
        accts.append((parts[0], parts[1] if len(parts) > 1 else ""))

def fetch(names):
    q = [("action", "query"), ("list", "users"),
         ("ususers", "|".join(names)), ("usprop", "editcount|registration"),
         ("format", "json")]
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(q)
    r = subprocess.run(["curl", "-s", "--max-time", "60", url], capture_output=True, text=True)
    return r.stdout

out = open(outtsv, "w")
raw = open(rawjl, "w")
cremap = dict(accts)
for i in range(0, len(accts), 50):
    batch = [a for a, _ in accts[i:i+50]]
    time.sleep(5)
    resp = fetch(batch)
    raw.write(resp + "\n")
    try:
        d = json.loads(resp)
        for u in d["query"]["users"]:
            name = u.get("name", "")
            out.write(f"{host}\t{name}\t{u.get('editcount', '?')}\t{cremap.get(name,'')}\n")
    except Exception as ex:
        print(f"  !! parse fail batch {i}: {ex}", flush=True)
        for name in batch:
            out.write(f"{host}\t{name}\tPARSE_FAIL\t{cremap.get(name,'')}\n")
out.close(); raw.close()
print(f"dormancy done {host}: {len(accts)} accounts", flush=True)
