#!/usr/bin/env python3
"""Wayback CDX sweep, May-Jul 2026 retrospective. Sequential, paced, no bursts.
One range query per target; flake policy: retry 45-90s spacing, max 3 attempts.
Writes raw JSON per target + .PROVENANCE.txt + .sha256 + summary.json.
"""
import json, os, time, hashlib, subprocess, random, collections, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
UA = "silent-locus-lane-scanner/1.0"
BASE = "http://web.archive.org/cdx/search/cdx"
FROMA, TO = "20260501", "20260731"
FL = "timestamp,original,statuscode,mimetype,digest"

# (slug, matchType, url_param, provider_label)
TARGETS = [
    ("r.jina.ai_domain", "domain", "r.jina.ai", "OpenAI-launder-marker"),
    ("api.allorigins.win_domain", "domain", "api.allorigins.win", "OpenAI-launder-marker"),
    ("pastebin.com_domain", "domain", "pastebin.com", "dead-drop"),
    ("webhook.site_28efa24e-f830-4d9f-a12b-fbb9e5035031_exact", "exact",
     "webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031", "dead-drop"),
    ("ntfy.sh_c6836_prefix", "prefix", "ntfy.sh/c6836", "dead-drop"),
    ("ntfy.sh_kz1wu398dnq_prefix", "prefix", "ntfy.sh/kz1wu398dnq", "dead-drop"),
    ("ntfy.sh_mha3x_prefix", "prefix", "ntfy.sh/mha3x", "dead-drop"),
    ("ntfy.sh_o54445_prefix", "prefix", "ntfy.sh/o54445", "dead-drop"),
    ("ntfy.sh_pz4kopsh1_prefix", "prefix", "ntfy.sh/pz4kopsh1", "dead-drop"),
    ("jqp.vercel.app_api_prefix", "prefix", "jqp.vercel.app/api/", "relay"),
    ("hysandbox.tencent-cloud.com_domain", "domain", "hysandbox.tencent-cloud.com", "fleet-infra"),
    ("pre-amap-pc-ssr.amap.com_prefix", "prefix", "pre-amap-pc-ssr.amap.com", "fleet-infra"),
    ("da.gd_domain", "domain", "da.gd", "Anthropic-tradecraft"),
]

def cdx(slug, mtype, url):
    q = (f"{BASE}?url={url}&matchType={mtype}&from={FROMA}&to={TO}"
         f"&output=json&fl={FL}&limit=20000")
    for attempt in range(1, 4):
        t0 = time.time()
        r = subprocess.run(
            ["curl", "-sS", "-m", "150", "-A", UA, q],
            capture_output=True, text=True)
        dur = time.time() - t0
        body = r.stdout
        if r.returncode == 0 and body.strip().startswith("["):
            return {"ok": True, "body": body, "dur_s": round(dur, 1),
                    "attempts": attempt, "query": q}
        flake = r.returncode != 0 or "Temporarily Offline" in body or "504" in body or body.strip() == ""
        print(f"  attempt {attempt} flake (rc={r.returncode}, dur={dur:.1f}s, "
              f"head={body[:80]!r})", flush=True)
        if attempt < 3:
            time.sleep(random.uniform(45, 90))
    return {"ok": False, "body": "", "dur_s": None, "attempts": 3, "query": q}

progress_path = os.path.join(OUT, "progress.json")
progress = {}
if os.path.exists(progress_path):
    progress = json.load(open(progress_path))

summary = {}
for slug, mtype, url, label in TARGETS:
    if slug in progress and progress[slug].get("ok"):
        print(f"SKIP {slug} (done)", flush=True)
        summary[slug] = progress[slug]["stats"]
        continue
    print(f"QUERY {slug} matchType={mtype}", flush=True)
    res = cdx(slug, mtype, url)
    raw_path = os.path.join(OUT, f"{slug}.cdx.json")
    stats = {"matchType": mtype, "url": url, "label": label,
             "ok": res["ok"], "attempts": res["attempts"],
             "dur_s": res["dur_s"], "capture_rows": 0, "unique_digests": 0,
             "per_day": {}, "status2xx": 0, "capped": False}
    if res["ok"]:
        open(raw_path, "w").write(res["body"])
        try:
            rows = json.loads(res["body"])
            if rows and rows[0] == FL.split(","):
                rows = rows[1:]
            stats["capture_rows"] = len(rows)
            digests = set()
            per_day = collections.Counter()
            for r in rows:
                ts, orig, sc, mt, dg = r[0], r[1], r[2], r[3], r[4]
                digests.add(dg)
                per_day[ts[:8]] += 1
                if str(sc).startswith("2"):
                    stats["status2xx"] += 1
            stats["unique_digests"] = len(digests)
            stats["per_day"] = dict(sorted(per_day.items()))
            stats["capped"] = len(rows) >= 20000
            if rows:
                stats["first_ts"] = rows[0][0]
                stats["last_ts"] = rows[-1][0]
        except Exception as e:
            stats["parse_error"] = str(e)
        prov = (f"target={url} matchType={mtype} window={FROMA}-{TO}\n"
                f"query={res['query']}\n"
                f"retrieved_utc={datetime.datetime.now(datetime.timezone.utc).isoformat()}\n"
                f"method=curl http://web.archive.org:80/cdx/search/cdx UA={UA}\n"
                f"attempts={res['attempts']} dur_s={res['dur_s']}\n"
                f"label={label}\n")
        open(raw_path + ".PROVENANCE.txt", "w").write(prov)
        h = hashlib.sha256(open(raw_path, "rb").read()).hexdigest()
        open(raw_path + ".sha256", "w").write(f"{h}  {os.path.basename(raw_path)}\n")
    progress[slug] = {"ok": res["ok"], "stats": stats}
    json.dump(progress, open(progress_path, "w"), indent=1)
    summary[slug] = stats
    print(f"  rows={stats['capture_rows']} digests={stats['unique_digests']} "
          f"capped={stats['capped']}", flush=True)
    time.sleep(random.uniform(6, 12))

json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
print("DONE", json.dumps({k: (v["capture_rows"], v["unique_digests"]) for k, v in summary.items()}, indent=1))
