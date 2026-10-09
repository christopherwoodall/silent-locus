#!/usr/bin/env python3
"""Build explicit-events JSONL for the YOURLS re-sweep lane (2026-09-28).

One doc per stats-page observation (yourls_stats_page). No referrer-row
docs: the re-sweep found zero new referrer hosts and zero changed host
counts on every YOURLS page, so there are no new per-row events to record.
New slugs (popcat numerics + 15 CBS agent-grammar slugs) each get one
page-observation doc. Disk only; hosted-Elastic writes are frozen.
"""
import json, os, re, hashlib, glob
from datetime import datetime, timezone

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
D = os.path.join(BASE, "data", "2026-09-28-yourls-resweep")
EV = os.path.join(D, "raw", "evidence")
OUT = os.path.join(D, "yourls-resweep-2026-09-28.jsonl")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}
DATASET = "yourls-resweep"

ORG = {
    "goto.unm.edu": ("University of New Mexico", "university"),
    "u.ethz.ch": ("ETH Zürich", "university"),
    "go.uvm.edu": ("University of Vermont", "university"),
    "url.popcat.xyz": ("popcat.xyz", "community"),
    "t.mdcdev.me": ("mdcdev.me", "community"),
    "uoft.me": ("University of Toronto", "university"),
}

# morning (2026-09-28 ~04:20-11:45 UTC) all-time baselines for delta computation
MORNING_ALL = {
    ("goto.unm.edu", "7t6-o"): 2523, ("goto.unm.edu", "discvr"): 1179,
    ("goto.unm.edu", "urphy21"): 642, ("goto.unm.edu", "vbudg"): 4,
    ("u.ethz.ch", "nB1nv"): 273,
    ("go.uvm.edu", "-4s0q"): 266, ("go.uvm.edu", "tgmtq"): 334,
    ("go.uvm.edu", "xc26"): 1,
    ("t.mdcdev.me", "squarespacefreeemail934785"): 40,
    ("t.mdcdev.me", "evegelendiyarbakrescort772509"): 201,
    ("t.mdcdev.me", "mattressstoresaroundmyarea909270"): 284,
    ("url.popcat.xyz", "5vtSk2RG2f"): 66, ("url.popcat.xyz", "IRZTIxDlZ"): 83,
}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(65536), b""):
            h.update(ch)
    return h.hexdigest()

def strip_html(html):
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", t)

def parse_yourls(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    text = strip_html(html)
    d = {}
    m = re.search(r"Last 24 hours (\d+) hits?.*?Last 7 days (\d+) hits?.*?Last 30 days (\d+) hits?.*?All time (\d+) hits?", text)
    if m:
        d["traffic"] = {"24h": int(m.group(1)), "7d": int(m.group(2)),
                        "30d": int(m.group(3)), "all": int(m.group(4))}
    refs = re.findall(r"class='sites_list'[^>]*>.*?([\w.\-]+(?:\.[\w.\-]+)+): <strong>([\d,]+)</strong>", html)
    d["referrers"] = {h.lower(): int(n.replace(",", "")) for h, n in refs}
    m2 = re.search(r"Short URL: (\S+)", text)
    if m2: d["short_url"] = m2.group(1)
    m3 = re.search(r"Long URL: (\S+)", text)
    if m3: d["long_url"] = m3.group(1)
    m4 = re.search(r"CREATED: ([^.]+)", text)
    if m4: d["created"] = m4.group(1).strip()
    return d

def parse_popcat(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    text = strip_html(html)
    d = {}
    m = re.search(r"(\d+) Total Views", text)
    if m: d["clicks"] = int(m.group(1))
    m2 = re.search(r"Redirects to: (\S+)", text)
    if m2: d["long_url"] = m2.group(1)
    m3 = re.search(r"Created: ([\d/]+)", text)
    if m3: d["created"] = m3.group(1)
    return d

def base_doc(instance, slug, source_url, evidence_file, description,
             matched_string, note, extra_labels, tags):
    org, scope = ORG[instance]
    labels = {
        "shortener.instance": instance, "shortener.org": org,
        "shortener.scope": scope,
        "short_url": "https://%s/%s" % (instance, slug),
        "source_stats_url": source_url,
        "event_id": "yourls:%s:%s:page:2026-09-28-resweep" % (instance, slug),
        "granularity": "event",
    }
    labels.update(extra_labels)
    return {
        "@timestamp": NOW, "description": description,
        "event": {"created": NOW, "dataset": DATASET},
        "file": os.path.relpath(evidence_file, BASE),
        "labels": labels, "matched_string": matched_string, "note": note,
        "observer": OBSERVER, "record_kind": "yourls_stats_page",
        "retrieved_at": NOW,
        "retrieved_via": "read-only live GET of public stats page (polite pacing, single retry); hosted-Elastic writes paused",
        "sha256": sha256_file(evidence_file),
        "size_bytes": os.path.getsize(evidence_file),
        "source_url": source_url, "status": "archived-capture", "tags": tags,
    }

# (evidence_basename, instance, slug, stats_url, kind)
PAGES = [
    ("unm_7t6-o", "goto.unm.edu", "7t6-o", "https://goto.unm.edu/7t6-o+", "yourls"),
    ("unm_discvr", "goto.unm.edu", "discvr", "https://goto.unm.edu/discvr+", "yourls"),
    ("unm_reso", "goto.unm.edu", "reso", "https://goto.unm.edu/reso+", "yourls"),
    ("unm_urphy21", "goto.unm.edu", "urphy21", "https://goto.unm.edu/urphy21+", "yourls"),
    ("unm_vbudg", "goto.unm.edu", "vbudg", "https://goto.unm.edu/vbudg+", "yourls"),
    ("eth_nB1nv", "u.ethz.ch", "nB1nv", "https://u.ethz.ch/nB1nv+?jqpaccess=1", "yourls"),
    ("uvm_-4s0q", "go.uvm.edu", "-4s0q", "https://go.uvm.edu/-4s0q+", "yourls"),
    ("uvm_tgmtq", "go.uvm.edu", "tgmtq", "https://go.uvm.edu/tgmtq+", "yourls"),
    ("uvm_xc26", "go.uvm.edu", "xc26", "https://go.uvm.edu/xc26+", "yourls"),
    ("tmdc_squarespacefreeemail934785", "t.mdcdev.me", "squarespacefreeemail934785",
     "https://t.mdcdev.me/squarespacefreeemail934785+", "yourls"),
    ("tmdc_evegelendiyarbakrescort772509", "t.mdcdev.me", "evegelendiyarbakrescort772509",
     "https://t.mdcdev.me/evegelendiyarbakrescort772509+", "yourls"),
    ("tmdc_mattressstoresaroundmyarea909270", "t.mdcdev.me", "mattressstoresaroundmyarea909270",
     "https://t.mdcdev.me/mattressstoresaroundmyarea909270+", "yourls"),
    ("popcat_5vtSk2RG2f", "url.popcat.xyz", "5vtSk2RG2f",
     "https://url.popcat.xyz/5vtSk2RG2f/info", "popcat"),
    ("popcat_IRZTIxDlZ", "url.popcat.xyz", "IRZTIxDlZ",
     "https://url.popcat.xyz/IRZTIxDlZ/info", "popcat"),
    ("popcat_1", "url.popcat.xyz", "1", "https://url.popcat.xyz/1/info", "popcat"),
    ("popcat_2", "url.popcat.xyz", "2", "https://url.popcat.xyz/2/info", "popcat"),
]
for n in (["oaicbs22%d" % i for i in range(0, 8)] + ["oaifilt70%d" % i for i in range(0, 7)]):
    PAGES.append(("popcat_" + n, "url.popcat.xyz", n,
                  "https://url.popcat.xyz/%s/info" % n, "popcat-cbs"))

CBS_SLUGS = set(["oaicbs22%d" % i for i in range(0, 8)] + ["oaifilt70%d" % i for i in range(0, 7)])

docs = []
for base, instance, slug, stats_url, kind in PAGES:
    paths = glob.glob(os.path.join(EV, base + "_resweep_2026-09-28.html"))
    if not paths:
        print("MISSING evidence for", base); continue
    path = paths[0]
    org, scope = ORG[instance]
    tags = ["yourls" if kind == "yourls" else "shortener", "public-stats",
            "explicit-event", "read-only", "resweep", "scope:" + scope]
    if kind == "yourls":
        p = parse_yourls(path)
        tr = p.get("traffic", {})
        all_n = tr.get("all")
        morn = MORNING_ALL.get((instance, slug))
        delta = (all_n - morn) if (all_n is not None and morn is not None) else None
        extra = {"record": "page_observation", "long_url": p.get("long_url"),
                 "created_raw": p.get("created"),
                 "traffic_24h": tr.get("24h"), "traffic_7d": tr.get("7d"),
                 "traffic_30d": tr.get("30d"), "traffic_all_time": all_n,
                 "traffic_delta_all_time_vs_morning": delta,
                 "referrer_host_count": len(p.get("referrers", {})),
                 "new_referrer_hosts_vs_morning": [],
                 "changed_referrer_host_counts_vs_morning": {}}
        desc = ("Re-sweep observation: https://%s/%s — all-time %s hits (delta %+d vs morning); "
                "%d referrer hosts, zero new hosts, zero changed counts"
                % (instance, slug, all_n, delta if delta is not None else 0,
                   len(p.get("referrers", {}))))
        note = ("Second-pass re-probe of known surface. No new proxy-ladder "
                "referrers, no new task-family referrers since the morning sweep.")
    else:
        p = parse_popcat(path)
        extra = {"record": "page_observation", "long_url": p.get("long_url"),
                 "clicks": p.get("clicks"), "created_raw": p.get("created"),
                 "shortener_platform": "popcat-custom"}
        morn = MORNING_ALL.get((instance, slug))
        if slug in CBS_SLUGS:
            extra.update({"agent_grammar": True,
                          "task_family": "statistics-netherlands-cbs",
                          "task_table": "CBS 83779NED"})
            tags += ["agent-grammar", "task-family:cbs-netherlands"]
            desc = ("NEW agent-grammar slug: url.popcat.xyz/%s — %s clicks, created %s, "
                    "targets CBS Netherlands OData table 83779NED (%s)"
                    % (slug, p.get("clicks"), p.get("created"),
                       (p.get("long_url") or "").split("/CBS/83779NED/")[-1][:60]))
            note = ("Agent-created short link (2026-05-14) for the Statistics "
                    "Netherlands CBS 83779NED OData task family. Discovery→schema→"
                    "filtered-extraction walk; shortener used as URL blackboard.")
        elif slug in ("1", "2"):
            extra["new_slug_this_resweep"] = True
            desc = ("NEW slug on known surface: url.popcat.xyz/%s — %s clicks, created %s, "
                    "targets %s (pre-cohort user link, not swarm)"
                    % (slug, p.get("clicks"), p.get("created"), p.get("long_url")))
            note = "Numeric slug from joshuadavid shortener corpus; old user content, control."
        else:
            delta = (p.get("clicks") - morn) if (p.get("clicks") is not None and morn is not None) else None
            extra["clicks_delta_vs_morning"] = delta
            desc = ("Re-sweep observation: url.popcat.xyz/%s — %s clicks (delta %+d vs morning), "
                    "redirects to %s" % (slug, p.get("clicks"), delta or 0, p.get("long_url")))
            note = "Community shortener still serving agent-planted redirect to a ChatGPT conversation."
    docs.append(base_doc(instance, slug, stats_url, path, desc,
                         "https://%s/%s" % (instance, slug), note, extra, tags))

with open(OUT, "w") as f:
    for d in docs:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
print("wrote %d docs -> %s" % (len(docs), OUT))
