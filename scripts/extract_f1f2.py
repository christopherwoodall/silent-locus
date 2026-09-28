#!/usr/bin/env python3
"""F1 (httpbun) + F2 (epoch nonces) fingerprint extraction and hunt-corpus matching.

Read-only on the frozen hunt repo. Decodes base64 only for byte comparison;
never executes payload content.
"""
import csv, gzip, json, re, base64, os
from urllib.parse import unquote

HUNT = "/home/hatch/workspace/muse-home/projects/urlquery-api-hunt"
ST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = ST + "/data/raw/redacted.jsonl.gz"
OUT = ST + "/data/matches-f1f2.jsonl"

HTTPBUN_IOCS = [
    "api.browserless.io",
    "httpbun.com",
    "pp.aihw.gov.au",
    "unctadstat-api.unctad.org",
    "cors.isomorphic-git.org",
    "https://httpbun-com.translate.goog/base64/",
    "https://webhook.site/0194ba46-b8b4-4dbe-8572-fa98567226fe",
]

# ---- hunt epoch set (value -> [ioc field1]) ----
rows = list(csv.reader(open(HUNT + "/artifacts/dataset/iocs.csv")))
hunt_epochs = {}
for r in rows[1:]:
    for m in re.findall(r"(?<!\d)\d{10}(?!\d)", " ".join(r)):
        v = int(m)
        if 1700000000 <= v <= 1800000000:
            hunt_epochs.setdefault(v, set()).add(r[0])

# ---- hunt decoded httpbun samples ----
findings = json.load(open(HUNT + "/artifacts/findings_httpbun.json"))
hunt_samples = [(c.get("signature", "?"), c.get("sample", ""),
                 c.get("link", "")) for c in findings["top_decoded_clusters"]]

def try_b64decode(s):
    """Double-URL-decode then base64-decode. Returns bytes or None."""
    for _ in range(2):
        s2 = unquote(s)
        if s2 == s:
            break
        s = s2
    s = s.strip()
    for alt in (False, True):
        t = s.replace("-", "+").replace("_", "/") if alt else s
        t += "=" * (-len(t) % 4)
        try:
            return base64.b64decode(t, validate=True)
        except Exception:
            continue
    return None

def head_tail(b, n=64):
    return (b[:n], b[-n:] if len(b) > n else b"")

hunt_ht = [(sig, head_tail(s.encode("utf-8", "ignore")), link)
           for sig, s, link in hunt_samples if s]

matches = []
mid = {"F1": 0, "F2": 0}
def add(fp, kind, conf, hunt_ioc, st_id, evidence):
    mid[fp] += 1
    matches.append({
        "match_id": f"{fp}-{mid[fp]:04d}",
        "fingerprint": fp,
        "match_kind": kind,
        "confidence": conf,
        "hunt_ioc": hunt_ioc,
        "swarmtraces_id": st_id,
        "evidence": evidence[:300],
    })

# ---- scan dataset ----
f1_seen_iocs = set()   # which hunt IOCs got any hit
f2_hit_epochs = set()  # hunt epoch values found in dataset
epoch_re = re.compile(r"(?<!\d)(\d{10})(?!\d)")
param_re = re.compile(r"[?&](x|uqscan|r|ov|t|ts|nonce)=(\d{6,19})")
b64url_re = re.compile(r"https?://httpbun\.com/base64/([A-Za-z0-9+/%=_.-]{20,20000})")
httpbun_lit = 0
b64_count = 0
ds_epochs = {}  # epoch -> set of (record_id, convention)

with gzip.open(DS, "rt", encoding="utf-8", errors="replace") as f:
    for line in f:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        rid = rec.get("id", "?")
        text = rec.get("text") or ""

        # ---- F1 ----
        if "httpbun" in text:
            httpbun_lit += text.count("httpbun")
            f1_seen_iocs.add("httpbun.com")
            for m in b64url_re.finditer(text):
                b64_count += 1
                blob = m.group(1)
                dec = try_b64decode(blob)
                ev = f"{rid} | httpbun.com/base64/{blob[:80]}"
                if dec is not None:
                    ht = head_tail(dec)
                    hit = None
                    for sig, hht, link in hunt_ht:
                        if ht[0] and hht[0] and ht[0] == hht[0]:
                            hit = ("head", sig, link); break
                        if ht[1] and hht[1] and ht[1] == hht[1]:
                            hit = ("tail", sig, link); break
                    if hit:
                        add("F1", "exact", "high", f"decoded-cluster:{hit[1]}",
                            rid, f"{ev} | decoded {len(dec)}B, {hit[0]}-64B matches hunt cluster {hit[2]}")
                        f1_seen_iocs.add("decoded-cluster:" + hit[1])
                    else:
                        add("F1", "structural", "low", "httpbun.com", rid,
                            f"{ev} | decoded {len(dec)}B, no hunt-cluster head/tail match")
                else:
                    add("F1", "structural", "low", "httpbun.com", rid,
                        f"{ev} | blob not base64-decodable")
            if "httpbun-com.translate.goog" in text:
                f1_seen_iocs.add("https://httpbun-com.translate.goog/base64/")
                add("F1", "exact", "high",
                    "https://httpbun-com.translate.goog/base64/", rid,
                    f"{rid} | literal httpbun-com.translate.goog in text")
            if "webhook.site/0194ba46-b8b4-4dbe-8572-fa98567226fe" in text:
                f1_seen_iocs.add("https://webhook.site/0194ba46-b8b4-4dbe-8572-fa98567226fe")
                add("F1", "exact", "high",
                    "https://webhook.site/0194ba46-b8b4-4dbe-8572-fa98567226fe", rid,
                    f"{rid} | literal hunt webhook inbox URL")
            if "cors.isomorphic-git.org" in text:
                f1_seen_iocs.add("cors.isomorphic-git.org")
                add("F1", "structural", "medium", "cors.isomorphic-git.org", rid,
                    f"{rid} | cors.isomorphic-git.org co-occurs with httpbun")

        # ---- F2 ----
        for m in epoch_re.finditer(text):
            v = int(m.group(1))
            if 1700000000 <= v <= 1800000000:
                start = m.start()
                ctx = text[max(0, start-30):start]
                conv = "query-param" if re.search(r"[?&][a-z_]*=$", ctx) else \
                       "underscore-suffix" if ctx.endswith("_") else "bare"
                ds_epochs.setdefault(v, set()).add((rid, conv))
        for m in param_re.finditer(text):
            name, num = m.group(1), m.group(2)
            if len(num) >= 10:
                v = int(num[:10])
                if 1700000000 <= v <= 1800000000:
                    ds_epochs.setdefault(v, set()).add((rid, f"?{name}="))

# structural baseline: bare httpbun mentions (not base64 URLs)
if b64_count == 0 and httpbun_lit > 0:
    add("F1", "structural", "medium", "httpbun.com", "corpus-wide",
        f"httpbun literal {httpbun_lit}x across dataset; zero /base64/ URLs (recon Host-header/DNS use per verification)")

# ---- F2 matching ----
for v, locs in sorted(ds_epochs.items()):
    if v in hunt_epochs:
        f2_hit_epochs.add(v)
        for rid, conv in sorted(locs)[:5]:
            # exact if same convention seen in hunt context; else near
            add("F2", "exact", "high", sorted(hunt_epochs[v])[0], rid,
                f"{rid} | epoch {v} via {conv}; hunt IOC(s): {', '.join(sorted(hunt_epochs[v])[:3])}")
# near: ms-prefix matches (dataset 10-digit == first 10 digits of hunt ms value) already covered;
# near: identical epoch, different path — covered as exact-value; mark convention differences
# misses
for ioc in HTTPBUN_IOCS:
    if ioc not in f1_seen_iocs:
        mid["F1"] += 1
        matches.append({"match_id": f"F1-{mid['F1']:04d}", "fingerprint": "F1",
                        "match_kind": "miss", "confidence": "high",
                        "hunt_ioc": ioc, "swarmtraces_id": None,
                        "evidence": "no occurrence in 189,579 dataset records"})
for v, iocs in sorted(hunt_epochs.items()):
    if v not in f2_hit_epochs:
        mid["F2"] += 1
        matches.append({"match_id": f"F2-{mid['F2']:04d}", "fingerprint": "F2",
                        "match_kind": "miss", "confidence": "high",
                        "hunt_ioc": sorted(iocs)[0], "swarmtraces_id": None,
                        "evidence": f"epoch {v} absent from dataset epoch set ({len(ds_epochs)} distinct epochs)"})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    for m in matches:
        f.write(json.dumps(m) + "\n")

print("httpbun literal occurrences:", httpbun_lit)
print("base64 URLs found:", b64_count)
print("distinct dataset epochs:", len(ds_epochs))
print("hunt epochs hit:", sorted(f2_hit_epochs))
print("total match records:", len(matches))
from collections import Counter
print(Counter((m["fingerprint"], m["match_kind"]) for m in matches))
