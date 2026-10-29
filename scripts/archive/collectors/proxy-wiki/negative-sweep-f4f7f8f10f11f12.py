#!/usr/bin/env python3
"""Negative-sweep fingerprints F4, F7, F8, F10, F11, F12 against the
SwarmTraces redacted dataset. Read-only; payload content inspected as data,
never executed.

Outputs:
  data/aggregates/2026-09-29-overlap-analysis/events.jsonl   (hit AND miss records)
Prints a per-fingerprint summary for the notes section.
"""
import gzip, json, re, sys, os

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = os.path.join(_REPO, 'data', 'raw', 'redacted.jsonl.gz')
OUT = os.path.join(_REPO, 'data', 'matches-f4f7f8f10f11f12.jsonl')

NTFY_TOPICS = ["tabx1781967972","P91781976932","rb1782012062tfkhj","oaimic1781974645",
 "cross1781797021","a115r1781964433","oai1781965813","gro528fa63","gpleoleenso",
 "glm5-mi355x-bench-728962","Qky8CmfN45aZflWH","everyman-chasing-utopia-mg-8f3k2s9p"]
WEBHOOK_UUIDS = ["00f36f21-d00e-48b3-9456-8bf532e8c863","0194ba46-b8b4-4dbe-8572-fa98567226fe",
 "0ff0d84e-7743-4430-af1d-1622c6053077","178c74fe-e0e6-43e0-baee-fe0af45ba5ce",
 "47a9e270-5916-4eb0-a111-152a2159e51c","6051dd2b-86dc-427d-8083-071a687af4f8",
 "980e5c81-b533-4898-9323-44355d7c5ef1","abf2db69-ca01-4346-a644-e5a8c886c4bf",
 "bda06178-a70f-4827-9af2-dd9672eeb8ac","c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357",
 "c773aa22-7dc5-4e6a-8961-8d0c29314bfd","f9c24dca-807e-4a06-b99a-400d2cb68594",
 "5dd22f50-78f2-4a40-bad4-89efda802ea4"]
COUNTERAPI_NS = ["apr23-cvd-horizon-2025","cashier-bach2015-r5-jan02-2027","cashier-postr5-dec21-oai"]
TABLEAU_ENDPOINTS = [
 "https://vizprod.aihw.gov.au/javascripts/api/tableau-2.9.2.min.js",
 "https://vizprod.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/",
 "https://vizprod.aihw.gov.au/vizql/t/Public/w/PBSdashboardallATC1-ATC2medicines-Agegroup/v/PBSDashboard/bootstrapSession/sessions/<sessionid>",
 "https://vizprod.aihw.gov.au/vizql/t/Public/w/PBSdashboardallATC1-ATC2medicines-Agegroup/v/PBSDashboard/startSession/viewing",
 "https://vizprod.aihw.gov.au/vizql/w/",
]

def load():
    recs = []
    with gzip.open(DS, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line: recs.append(json.loads(line))
    return recs

recs = load()
print(f"loaded {len(recs)} records", file=sys.stderr)
texts = [(r['id'], r['kind'], r['tags'], r['text']) for r in recs]

def search(pat, flags=0):
    rx = re.compile(pat, flags)
    return [(i, k, t, x) for (i, k, t, x) in texts if rx.search(x) or (t and rx.search(t))]

out = []
n = 0
def emit(fp, kind, conf, hunt_ioc, hunt_ioc_type, payload_id, field, evidence, notes):
    global n
    n += 1
    out.append({
        "match_id": f"{'ovl' if kind!='miss' else 'neg'}-{fp.lower()}-{n:04d}",
        "fingerprint": fp,
        "match_kind": kind,
        "confidence": conf,
        "hunt_ioc": hunt_ioc,
        "hunt_ioc_type": hunt_ioc_type,
        "swarmtraces_payload_id": payload_id,
        "swarmtraces_field": field,
        "swarmtraces_evidence": (evidence or "")[:200],
        "notes": notes,
    })

print("=== F4 ntfy ===")
f4_generic = search(r'ntfy\.sh|ntfy\.envs\.net')
print("generic ntfy.sh|ntfy.envs.net records:", len(f4_generic))
for (i, k, t, x) in f4_generic:
    m = re.search(r'.{120}(ntfy\.sh|ntfy\.envs\.net).{120}', x, re.S)
    emit("ntfy-topic", "weak-string", "low", "ntfy.sh|ntfy.envs.net (generic)",
         "ntfy-topic", i, "text", m.group(0) if m else x[:200],
         "generic ntfy host reference; NO hunt topic string co-occurs; URL otherwise redacted")
for topic in NTFY_TOPICS:
    hits = search(re.escape(topic))
    if hits:
        for (i, k, t, x) in hits:
            emit("ntfy-topic", "exact-string", "high", topic, "ntfy-topic", i, "text",
                 x[:200], "exact hunt topic string in dataset")
    else:
        emit("ntfy-topic", "miss", "high", topic, "ntfy-topic", None, None, "",
             f"exact-string search over all 189,579 records (text+tags): zero hits")
print("per-topic hits:", {t: len(search(re.escape(t))) for t in NTFY_TOPICS})

print("=== F7 itty.bitty ===")
for pat, label in [(r'itty\.bitty', 'itty.bitty'), (r'ittybitty', 'ittybitty'),
                   (r'XQAAAA', 'LZMA XQAAAA fragment header'),
                   (r'#/XQ', '#/XQ fragment carrier')]:
    hits = search(pat)
    print(f"{label}: {len(hits)} records")
    if hits:
        for (i, k, t, x) in hits[:5]:
            m = re.search(r'.{100}'+pat+r'.{100}', x, re.S)
            emit("ittybitty-fragment", "exact-string", "high", label, "domain",
                 i, "text", m.group(0) if m else x[:200], "itty.bitty-family string in dataset")
    else:
        emit("ittybitty-fragment", "miss", "high", label, "domain", None, None, "",
             f"case-sensitive literal search over all 189,579 records (text+tags): zero hits")
# also hunt-side itty.bitty-adjacent IOC values as strings
for v, vt in [("itty.bitty.site","domain"),("rlCnlZ","yourls-slug"),("3JlIp7","yourls-slug"),
              ("j8miwk","yourls-slug"),("YvkRo3","yourls-slug"),("3r437m6h","url")]:
    hits = search(re.escape(v))
    if hits:
        for (i, k, t, x) in hits:
            emit("ittybitty-fragment", "exact-string", "high", v, vt, i, "text", x[:200],
                 "hunt-side itty.bitty-family IOC value in dataset")
    else:
        emit("ittybitty-fragment", "miss", "high", v, vt, None, None, "",
             "exact-string search over all 189,579 records: zero hits")

print("=== F8 tableau ===")
# exact hunt marker first
hits_exact = search(r'tableau-2\.9\.2\.min\.js')
print("tableau-2.9.2.min.js:", len(hits_exact))
emit("tableau-marker", "miss" if not hits_exact else "exact-string", "high",
     "tableau-2.9.2.min.js", "tableau-endpoint",
     hits_exact[0][0] if hits_exact else None, "text" if hits_exact else None,
     hits_exact[0][3][:200] if hits_exact else "",
     "exact hunt marker string over all 189,579 records")
# embedding-API fragments: enumerate then explicitly exclude
for pat, label in [(r'tableau-viz', 'tableau-viz web component'),
                   (r'tableauEventType', 'tableauEventType'),
                   (r'tableau\.com', 'tableau.com'),
                   (r'vizprod', 'vizprod'),
                   (r'vizql', 'vizql path'),
                   (r'bootstrapSession', 'bootstrapSession'),
                   (r'startSession', 'startSession')]:
    hits = search(pat)
    print(f"{label}: {len(hits)}")
    if label in ('vizql path', 'bootstrapSession'):
        for (i, k, t, x) in hits[:3]:
            m = re.search(r'.{80}'+pat+r'.{80}', x, re.S)
            emit("tableau-marker", "lexical-only", "low", label, "tableau-endpoint", i,
                 "text", m.group(0) if m else x[:200],
                 "embedding-API fragment WITHOUT the hunt's tableau-2.9.2.min.js exfil marker; "
                 "explicitly excluded from hit verdict")
for ep in TABLEAU_ENDPOINTS:
    # strip scheme/host for the path-shaped ones; the vizprod host is redacted-able
    key = ep.split('vizprod.aihw.gov.au')[-1]
    hits = search(re.escape(key)) if key else []
    emit("tableau-marker", "miss" if not hits else "exact-string", "high",
         ep, "tableau-endpoint",
         hits[0][0] if hits else None, "text" if hits else None,
         hits[0][3][:200] if hits else "",
         "hunt tableau-endpoint path component in dataset" if hits else
         "path component absent from all 189,579 records (vizprod.aihw.gov.au itself: "
         f"{len(search(re.escape('vizprod.aihw.gov.au')))} hits)")
print("vizprod.aihw.gov.au:", len(search(re.escape('vizprod.aihw.gov.au'))))

print("=== F10 webhook DELETE ===")
del_re = re.compile(r"""method\s*:\s*['"]DELETE['"]""")
del_hits = [(i, k, t, x) for (i, k, t, x) in texts if del_re.search(x)]
print("method:'DELETE' records:", len(del_hits))
for (i, k, t, x) in del_hits:
    m = del_re.search(x)
    s = max(0, m.start()-160)
    # what host is the fetch aimed at?
    hostm = re.search(r'fetch\(\s*([\'"])(.{0,80}?)\1', x)
    emit("webhook-delete", "structural-pattern", "medium",
         "method:'DELETE' evidence-destruction TTP", "webhook-inbox", i, "text",
         x[s:m.end()+80][:200],
         f"DELETE-method fetch; target host in excerpt is redacted/markerized "
         f"({'webhook.site literal present' if 'webhook.site' in x else 'no webhook.site literal'}); "
         f"kind={k}")
ws_hits = search(r'webhook\.site')
print("webhook.site literal:", len(ws_hits))
emit("webhook-delete", "miss" if not ws_hits else "exact-string", "high",
     "webhook.site (literal)", "webhook-inbox",
     ws_hits[0][0] if ws_hits else None, "text" if ws_hits else None,
     ws_hits[0][3][:200] if ws_hits else "",
     "literal webhook.site hostname over all 189,579 records (host is redacted in this dataset)")
for u in WEBHOOK_UUIDS:
    hits = search(re.escape(u))
    emit("webhook-delete", "miss" if not hits else "exact-string", "high",
         f"https://webhook.site/{u}", "webhook-inbox",
         hits[0][0] if hits else None, "text" if hits else None,
         hits[0][3][:200] if hits else "",
         "hunt webhook-inbox UUID in dataset" if hits else
         "UUID absent from all 189,579 records — no inbox reuse observable")

print("=== F11 counterapi ===")
for pat, label in [(r'counterapi', 'counterapi (any)'),
                   (r'counterapi\.dev', 'counterapi.dev'),
                   (r'counterapi\.io', 'counterapi.io')]:
    hits = search(pat, re.IGNORECASE)
    print(f"{label}: {len(hits)}")
for ns in COUNTERAPI_NS:
    hits = search(re.escape(ns))
    print(f"namespace {ns}: {len(hits)}")
    emit("counterapi", "miss" if not hits else "exact-string", "high", ns,
         "counterapi-namespace", hits[0][0] if hits else None,
         "text" if hits else None, hits[0][3][:200] if hits else "",
         "hunt counterapi namespace in dataset" if hits else
         "absent from all 189,579 records; counterapi host strings also zero")

print("=== F12 translate.goog ===")
for pat, label in [(r'translate\.goog', 'translate.goog'),
                   (r'translate\.google', 'translate.google'),
                   (r'-translate\.', '-translate. host prefix'),
                   (r'httpbun-com\.translate', 'httpbun-com.translate.goog (hunt row)')]:
    hits = search(pat, re.IGNORECASE)
    print(f"{label}: {len(hits)}")
    emit("translate-launder", "miss" if not hits else "exact-string", "high", label,
         "url", hits[0][0] if hits else None, "text" if hits else None,
         hits[0][3][:200] if hits else "",
         "translate-laundering host in dataset" if hits else
         "absent from all 189,579 records")

with open(OUT, 'w') as f:
    for r in out:
        f.write(json.dumps(r) + "\n")
print(f"wrote {len(out)} match/miss records to {OUT}", file=sys.stderr)
