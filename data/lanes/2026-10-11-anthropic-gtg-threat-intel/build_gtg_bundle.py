#!/usr/bin/env python3
"""Build the IOC Family A bundle: Anthropic GTG threat-intel infrastructure.

Extracts every domain, IP, email, hash, file name, malware family name,
tooling term, actor alias, Telegram ID, and exfil endpoint from section 3
of the Anthropic September 2026 threat report (coordinator report
anthropic-ioc-hunt-2026-10-11.md), dedups against the existing Factum
corpus, and writes data/lanes/2026-10-11-anthropic-gtg-threat-intel/bundle.json.

Usage:
  python3 build_gtg_bundle.py --dedup      # write DEDUP.md only
  python3 build_gtg_bundle.py --build      # write DEDUP.md + bundle.json
"""
import json, glob, re, sys, os

LANE = "2026-10-11-anthropic-gtg-threat-intel"
LANE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS = sorted(glob.glob(os.path.join(LANE_DIR, "..", "..", "..", "records", "*", "records.jsonl")))
OBSERVED_AT = "2026-09-10T00:00:00Z"  # full datetime required by urn:factum:core:observation:1 format
TIME_BASIS = "source_metadata"  # report publication date; activity window Dec 2025–Aug 2026 per report
PROV = "Anthropic 'Detecting and countering misuse of AI: September 2026' (2026-09-10), coordinator report 2026-10-11, section 3"

# (term, category, cluster, kind-tag, grade, note)
CANDIDATES = []

def add(terms, category, cluster, kind, grade="OBSERVED", note=""):
    for t in terms:
        CANDIDATES.append({
            "term": t, "category": category, "cluster": cluster,
            "kind": kind, "grade": grade, "note": note,
        })

# ---- GTG-20006: Russian espionage; operator handle JackPoterz; attribution
# consistent with Midnight Blizzard (per Anthropic, UPSTREAM)
G6 = "GTG-20006"
add("""ms365-live.com teams.ms365-live.com m365-owa.com owa-ms365.com ms365-device.com
mslivetest.duckdns.org my-invite.org chamber-ua.org chathamhouse.eu ukrinform-share.net
statistic-ms.live static-ms.live ad-g.org docs-viewer.org wa-connect.eu mygreatmarket.org
mygreatmarket.com cdncounter.net static.cdncounter.net stuseamandesilt.org itechx.tel
pdfviewer2024.b-cdn.net meridian-protocol.org meridiangroup-corp.com projectnightcrawler.dev
metricwave.org mgsend.org wa-meeting.com russianearabroad.com russianearabroad.org
russianearabroad.net embassy-protocol.int""".split(), "domain", G6, "domain")
add(["api.stuseamandesilt.org", "cdn.stuseamandesilt.org", "update.stuseamandesilt.org"],
    "domain", G6, "domain", grade="INFERENCE",
    note="report states stuseamandesilt.org has api/cdn/update subdomains; exact FQDNs composed from that statement")
add(["anna.manager@russianearabroad.net", "events@embassy-protocol.int"],
    "other", G6, "email-address")
add("""104.145.210.184 31.57.243.154 104.194.151.133 104.194.159.55 144.172.114.192
213.145.86.112 2.26.53.194 148.135.195.111 185.198.234.26 185.198.234.101
149.54.42.106 104.194.149.228 38.146.28.132 38.146.28.75""".split(), "ip", G6, "ip")
add(["msedgeupdate_v3.exe", "msedgeupdate.exe", "version.dll", "WUEngine.exe",
     "DiagHost.exe", "client_20260507093021_4286d211_x64.exe", "fix_network.apk"],
    "other", G6, "malware-file")
add(["be99857449d2856dd5a84e21c8a3d5e0e01456adb44062ddec5a6b4970d8d42c",
     "918fa52ae45ed60ba7cc8bdc99c3cbe9ab92e0375ec31fc05d0d4513be11c593"],
    "other", G6, "sha256-hash")
add(["PowerChrome", "WUEngine", "Shadow C2", "MiniPlasma", "CloudSyncSvc",
     "GiftDrop", "DarkSword"], "other", G6, "malware-family",
    note="GiftDrop = rebranded GiftsExpress Android surveillance RAT; DarkSword = iOS exploit chain; per Anthropic report")
add(["Embassy Kit", "WPPConnect", "CaptiveCrunch"], "marker", G6, "tooling",
    note="Embassy Kit = Microsoft 365 device-code-phishing token-theft framework; WPPConnect = WhatsApp automation library; CaptiveCrunch = hotel-WiFi DNS-hijack theft (Microsoft name)")
add(["JackPoterz"], "marker", G6, "actor-alias",
    note="operator handle; Anthropic attribution consistent with Midnight Blizzard")

# ---- GTG-50014: ShinyHunters affiliates; aliases MeowSHA/frkoo/blazespider; Telegram bot @Soraki_Bot
G14 = "GTG-50014"
add("""updatebeacon.duckdns.org esvfecawvjmchjslqyemho2fiduc59wzn.oast.fun
soraki-proxy.20245aad98d27b1b1a2f0f103e1d7ee0.workers.dev soraki.cc soraki.work
policenationale.cc autoshop.policenationale.cc emailsecure.email mozilla.ws
signin-1psswoord.com on-pssword.com ari-chain.com arichain.network bitmart-mystery.com
defi-claim.xyz service-infos.info 0x0.st""".split(), "domain", G14, "domain",
    note="0x0.st used for curl exfil")
add("""162.128.129.106 195.178.110.131 45.148.10.242 92.118.39.3 185.65.134.246
185.65.134.199 193.32.249.161 193.32.249.164 193.32.249.170 104.36.50.54
104.193.135.207 91.171.138.169 176.177.12.62
2a04:cec0:1185:34f2:a150:7081:caed:448e 2a01:e0a:2e2:aa40:b15d:5d28:6f4a:8d53""".split(),
    "ip", G14, "ip", note="egress IPs")
add(["-1003893854338", "-1003311614569"], "other", G14, "telegram-group",
    note="-1003893854338 = 'ClintonHog'; -1003311614569 = 'ChatMignon' with 471 forum topics")
add(["8632748474", "8664033117", "8628746407", "8709258476"], "other", G14, "telegram-bot")
add(["8179098353"], "other", G14, "telegram-user")
add(["Soraki_Bot", "MeowSHA", "frkoo", "blazespider"], "marker", G14, "actor-alias",
    note="Soraki_Bot = Telegram bot handle (@Soraki_Bot); MeowSHA/frkoo/blazespider = aliases")

DEADDROPS = [
    {"service": "s3.ap-tokyo.megas4.com", "endpoint_kind": "bin",
     "payload_summary": "exfil bucket 'fuckyoubasil' on megas4 S3 (ap-tokyo endpoint)",
     "cluster": G14, "note": "bucket name is attacker-chosen profanity; preserved verbatim per never-redact rule"},
    {"service": "s3.eu-central-1.s4.mega.io", "endpoint_kind": "bin",
     "payload_summary": "exfil bucket 'fuckyoubasil' on mega.io S3 (eu-central-1 endpoint)",
     "cluster": G14, "note": "bucket name is attacker-chosen profanity; preserved verbatim per never-redact rule"},
    {"service": "0x0.st", "endpoint_kind": "paste",
     "payload_summary": "curl-based exfil endpoint", "cluster": G14, "note": ""},
]

# ---- GTG-50021: Russian/Ukrainian speakers; alias kl1zy; fraudulent AI reseller
G21 = "GTG-50021"
add(["awstore.cloud", "kiro.cheap", "sys-tools.cfd", "aws-us-east-3.com",
     "holdboost.store", "deltaclient.xyz", "iymkjuzymkapovrntoxy.supabase.co"],
    "domain", G21, "domain", note="fraudulent AI reseller storefronts")
add(["kl1zy"], "marker", G21, "actor-alias")

# ---- GTG-50020: Russian-speaking financial; hit AI vendors for eval-sandbox keys
G20 = "GTG-50020"
add(["141.133.125.208", "167.250.111.136", "178.16.54.141", "37.27.103.22",
     "194.163.183.216", "202.66.167.230", "146.103.101.253", "146.103.97.169"],
    "ip", G20, "ip", note="egress IPs")

# ---- GTG-50029: French-speaking hacktivist; fafsearch doxxing platform; BeEF browser C2
G29 = "GTG-50029"
add(["139.59.2.243", "158.173.46.118", "146.70.116.131", "149.22.83.6",
     "138.199.60.29", "138.199.6.208", "103.216.220.19", "103.124.165.199",
     "103.141.60.144", "34.156.199.132", "34.156.95.176", "136.144.242.56",
     "163.172.157.53"], "ip", G29, "ip")
add(["frntrs-analytics.dedyn.io",
     "frntrs-analytics-863060591218.europe-west1.run.app",
     "prod-artfkt.com", "fafwatch.xyz"], "domain", G29, "domain")
add(["3ell6n47y3ct4a3x67fbuz62q2mk2l4vo6eacho2suzftdshsnrfopyd.onion",
     "6mshbvhvzhdgumwwazf4jcep2xx4kdk6n4wgffc46msu2gc3j3t2fpad.onion"],
    "domain", G29, "onion-service")
add(["fafsearch", "BeEF"], "marker", G29, "tooling",
    note="fafsearch = doxxing platform; BeEF = browser exploit framework used as C2")


def defanged(term):
    return term.replace(".", "[.]")


def dedup():
    """Grep the exported batches for each candidate term; return (novel, skipped)."""
    lines = []
    for f in RECORDS:
        for i, line in enumerate(open(f, errors="replace")):
            lines.append((f, line))
    novel, skipped = [], []
    for c in CANDIDATES:
        term = c["term"]
        variants = {term, defanged(term)}
        hits = []
        for f, line in lines:
            if any(v in line for v in variants):
                try:
                    r = json.loads(line)
                    hits.append((os.path.basename(os.path.dirname(f)),
                                 r.get("id"), r.get("tags", {}).get("lane")))
                except Exception:
                    hits.append((f, "?", "?"))
                if len(hits) > 5:
                    break
        if hits:
            skipped.append((c, hits))
        else:
            novel.append(c)
    return novel, skipped


def write_dedup_md(novel, skipped):
    out = ["# DEDUP — 2026-10-11-anthropic-gtg-threat-intel (Family A)",
           "",
           f"Scope: {len(RECORDS)} exported record batches under data/records/ (fuzzy `match` unavailable: worktree has no local index and rebuild is contended; grep over immutable exports used instead — lock-free).",
           f"Candidates: {len(CANDIDATES)} | Novel: {len(novel)} | Skipped (already in corpus): {len(skipped)}",
           "",
           "## Skipped (matches found in corpus)",
           ""]
    for c, hits in skipped:
        out.append(f"- `{c['term']}` [{c['cluster']}/{c['kind']}] — {len(hits)} hit(s):")
        for batch, rid, lane in hits[:5]:
            out.append(f"  - batch {batch} record {rid} lane={lane}")
    out += ["", "## Novel (submitted)", ""]
    for c in novel:
        out.append(f"- `{c['term']}` [{c['cluster']}/{c['kind']}/{c['grade']}]")
    open(os.path.join(LANE_DIR, "DEDUP.md"), "w").write("\n".join(out) + "\n")
    return len(novel), len(skipped)


def build_bundle(novel):
    records = [{
        "ref": "source",
        "kind": "source",
        "body": {
            "source_type": "published-report",
            "locator": "https://www.anthropic.com/threat-intelligence-report-september-2026",
            "title": "Detecting and countering misuse of AI: September 2026",
            "platform": "anthropic.com",
        },
        "tags": {"lane": LANE, "grade": "UPSTREAM",
                 "cached_path": "data/lanes/" + LANE + "/raw/anthropic-ioc-hunt-2026-10-11.md"},
    }]
    def slug(t):
        s = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
        return s[:48] or "term"
    seen_refs = set()
    for i, c in enumerate(novel):
        ref = f"ioc-{slug(c['term'])}"
        n = 1
        while ref in seen_refs:
            n += 1
            ref = f"ioc-{slug(c['term'])}-{n}"
        seen_refs.add(ref)
        prov = f"{PROV}; {c['cluster']}"
        if c["note"]:
            prov += f". {c['note']}"
        tags = {"lane": LANE, "grade": c["grade"], "cluster": c["cluster"], "ioc_kind": c["kind"]}
        records.append({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "source": "@source",
                "observed_at": OBSERVED_AT,
                "time_basis": TIME_BASIS,
                "data": {"term": c["term"], "category": c["category"],
                         "provenance": prov, "status": "candidate"},
            },
            "tags": tags,
        })
    for i, d in enumerate(DEADDROPS):
        prov = f"{PROV}; {d['cluster']}"
        if d["note"]:
            prov += f". {d['note']}"
        records.append({
            "ref": f"dead-drop-{i}",
            "kind": "observation",
            "body": {
                "type": "infra.dead_drop",
                "source": "@source",
                "observed_at": OBSERVED_AT,
                "time_basis": TIME_BASIS,
                "data": {"service": d["service"], "endpoint_kind": d["endpoint_kind"],
                         "payload_summary": d["payload_summary"]},
            },
            "tags": {"lane": LANE, "grade": "OBSERVED",
                     "cluster": d["cluster"], "ioc_kind": "exfil-endpoint"},
        })
    # intel.report for the report itself
    records.append({
        "ref": "report",
        "kind": "observation",
        "body": {
            "type": "intel.report",
            "source": "@source",
            "observed_at": OBSERVED_AT,
            "time_basis": TIME_BASIS,
            "data": {
                "lab": "Anthropic",
                "title": "Detecting and countering misuse of AI: September 2026",
                "url": "https://www.anthropic.com/threat-intelligence-report-september-2026",
                "report_date": "2026-09-10",
                "summary": ("Anthropic September 2026 threat report covering AI-misuse clusters "
                            "GTG-20006 (Russian espionage), GTG-50014 (ShinyHunters affiliates), "
                            "GTG-50021 (fraudulent AI reseller), GTG-50020 (financial), GTG-50029 "
                            "(French hacktivist), GTG-10007 (Chinese exploit foundry), bio/weapons/"
                            "influence clusters, and AI-specific tradecraft patterns."),
                "provenance": PROV,
                "cached_path": "data/lanes/" + LANE + "/raw/anthropic-ioc-hunt-2026-10-11.md",
            },
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })
    bundle = {
        "bundle": 2,
        "idempotency_key": "gtg-infra-2026-10-11/family-a",
        "actor": "agent:lane-ingest/gtg-infra",
        "records": records,
    }
    path = os.path.join(LANE_DIR, "bundle.json")
    json.dump(bundle, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {path}: {len(records)} records ({len(novel)} ioc + {len(DEADDROPS)} dead_drop + 1 report + 1 source)")
    return path


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dedup"
    print(f"candidates: {len(CANDIDATES)} (+{len(DEADDROPS)} dead_drop + 1 report)")
    novel, skipped = dedup()
    nn, ns = write_dedup_md(novel, skipped)
    print(f"dedup: {nn} novel, {ns} skipped -> DEDUP.md")
    if mode == "--build":
        build_bundle(novel)
