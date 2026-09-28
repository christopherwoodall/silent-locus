#!/usr/bin/env python3
"""Export all Kibana dashboards (+ deep references) to versioned NDJSON files.
Read-only against Kibana. Run: python3 export_dashboards.py
Outputs to this directory with fresh timestamps (never overwrites)."""
import sys, json, urllib.request, datetime, os
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

KB = "https://agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud"
HOSTS = ["agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
OUT = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def req(method, path, body=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(KB + path, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    r.add_header("kbn-xsrf", "true")
    r.add_header("x-elastic-internal-origin", "kibana")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return resp.read() if raw else read_json_response(resp)

def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")[:60]

# 1. list dashboards
found = req("GET", "/api/saved_objects/_find?type=dashboard&per_page=1000&fields=title")
dashboards = found.get("saved_objects", [])
print("dashboards found:", len(dashboards))
for d in dashboards:
    print(" -", d["id"], "|", d["attributes"].get("title"))

# 2. per-dashboard deep export
all_refs = {}
for d in dashboards:
    body = {"objects": [{"type": "dashboard", "id": d["id"]}], "includeReferencesDeep": True}
    nd = req("POST", "/api/saved_objects/_export", body, raw=True)
    fn = f"dashboard-{slug(d['attributes'].get('title','untitled'))}-{TS}.ndjson"
    open(os.path.join(OUT, fn), "wb").write(nd)
    objs = [json.loads(l) for l in nd.decode().splitlines() if l.strip()]
    types = {}
    for o in objs:
        types[o.get("type")] = types.get(o.get("type"), 0) + 1
    print(fn, types)
    all_refs[d["id"]] = types

# 3. full export (all dashboards in one file, deep)
body = {"objects": [{"type": "dashboard", "id": d["id"]} for d in dashboards],
        "includeReferencesDeep": True}
nd = req("POST", "/api/saved_objects/_export", body, raw=True)
fn = f"all-dashboards-{TS}.ndjson"
open(os.path.join(OUT, fn), "wb").write(nd)
print(fn, "bytes:", len(nd))
json.dump({"exported_at": TS, "dashboards": all_refs},
          open(os.path.join(OUT, f"export-summary-{TS}.json"), "w"), indent=1)
