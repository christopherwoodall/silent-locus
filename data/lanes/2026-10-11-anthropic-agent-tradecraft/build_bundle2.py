#!/usr/bin/env python3
"""Build Factum bundle 2 for lane 2026-10-11-anthropic-agent-tradecraft.

infra.ioc records: GTG actor designators, domain/IP/file/hash IOCs from the
Sep 2026 threat-intelligence report, malware/tool names, eval/benchmark
markers, containment architecture markers, incident-transcript URL.
Source: ~/workspace/anthropic-ioc-hunt-2026-10-11.md (raw cached in raw/).
All records graded UPSTREAM (Anthropic self-reporting via hunt notes).

Defanging note: the coordinator report writes domains/IPs defanged ([.]/[:]).
Terms are stored plain (re-fanged) per corpus convention; the verbatim
defanged rendering is in raw/ and noted in provenance.
"""
import json, datetime

LANE = "2026-10-11-anthropic-agent-tradecraft"
ACTOR = "subagent-anthropic-tradecraft-ingest"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
RAW = "data/lanes/2026-10-11-anthropic-agent-tradecraft/raw/anthropic-ioc-hunt-2026-10-11.md"
THREAT_URL = "https://www.anthropic.com/threat-intelligence-report-september-2026"

def prov(detail):
    return (f"Anthropic blog IOC + behavioral pattern hunt 2026-10-11; "
            f"source report (defanged in report): {THREAT_URL}; {detail}; raw: {RAW}")

SOURCES = [
    ("src-threat", THREAT_URL, "anthropic.com", "web",
     "Detecting and countering misuse of AI: September 2026 (Anthropic threat intelligence report, 2026-09-10; activity Dec 2025-Aug 2026)"),
    ("src-align", "https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents",
     "anthropic.com", "web",
     "An alignment assessment of recent cybersecurity incidents (Anthropic research, 2026-09-09)"),
    ("src-auto", "https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures",
     "anthropic.com", "web",
     "Automated researchers can reliably mitigate alignment failures (Anthropic research, 2026-08-28)"),
    ("src-cvp", "https://www.anthropic.com/news/cyber-verification-program",
     "anthropic.com", "web",
     "Expanding the Cyber Verification Program (Anthropic news, 2026-10-06)"),
    ("src-contain", "https://www.anthropic.com/engineering/how-we-contain-claude",
     "anthropic.com", "web",
     "How we contain Claude across products (Anthropic engineering, 2026-05-25)"),
    ("src-enzyme", "https://www.anthropic.com/news/claude-discovers-novel-enzyme-system",
     "anthropic.com", "web",
     "Claude discovers a novel enzyme system (Anthropic news, 2026-09-23)"),
]

# (term, category, source_ref, provenance_detail, extra_tags)
IOCS = []

def add(term, category, sref, detail, **tags):
    IOCS.append((term, category, sref, prov(detail), tags))

# --- Actor designators (Anthropic-internal; cross-reference keys for CTI pipelines)
DESIGNATORS = {
    "GTG-20006": "Russian espionage; operator handle 'JackPoterz'; attribution consistent with Midnight Blizzard",
    "GTG-50014": "ShinyHunters affiliates; aliases MeowSHA / frkoo / blazespider; Telegram bot @Soraki_Bot",
    "GTG-50021": "Russian/Ukrainian speakers; alias 'kl1zy'; fraudulent AI reseller",
    "GTG-50020": "Russian-speaking financial; hit AI vendors for eval-sandbox keys",
    "GTG-50029": "French-speaking hacktivist; tools 'fafsearch' doxxing platform, BeEF browser C2",
    "GTG-10007": "agent swarms with lead agent -> many subagents; 13-agent collection fleet",
    "GTG-04001": "Politology/Africa Corps/Wagner->SVR via Radio Lengo Songo 98.9 FM, CAR",
    "GTG-84002": "UAE-directed; 'Deadshot' persona; ~300 inauthentic accounts; ghost UN HRC-62 testimony",
    "GTG-54009": "'S2T Unlocking Cyberspace', Israeli-Singaporean",
    "GTG-27005": "'DronDoc'/'Serafim' autonomous FPV kamikaze drone swarm (Lancet-class; 'Sibiryachok', TRIIT interceptor, Zvezdochyot-Serafim, swarm-opi5, Medovik, Nebo-22)",
    "GTG-17002": "PLA Academy of Military Sciences EW/air-defense-suppression suite (16 modules, Taiwan scenario, 12 targets)",
    "GTG-17003": "directed-energy intel collection",
    "GTG-27006": "Russia procurement (German three-axis fluxgate magnetometers, space-grade PV wafers via China/HK intermediaries)",
}
for desig, desc in DESIGNATORS.items():
    add(desig, "actor-designator", "src-threat",
        f"Anthropic-internal actor designator: {desc}", **{"ioc.actor": desig})

# --- GTG-20006: domains
D20006 = ["ms365-live.com", "teams.ms365-live.com", "m365-owa.com", "owa-ms365.com",
          "ms365-device.com", "mslivetest.duckdns.org", "my-invite.org",
          "chamber-ua.org", "chathamhouse.eu", "ukrinform-share.net",
          "statistic-ms.live", "static-ms.live", "ad-g.org", "docs-viewer.org",
          "wa-connect.eu", "mygreatmarket.org", "mygreatmarket.com",
          "cdncounter.net", "static.cdncounter.net", "stuseamandesilt.org",
          "api.stuseamandesilt.org", "cdn.stuseamandesilt.org",
          "update.stuseamandesilt.org", "itechx.tel", "pdfviewer2024.b-cdn.net",
          "meridian-protocol.org", "meridiangroup-corp.com",
          "projectnightcrawler.dev", "metricwave.org", "mgsend.org",
          "wa-meeting.com", "russianearabroad.com", "russianearabroad.org"]
for d in D20006:
    add(d, "domain", "src-threat", "GTG-20006 domain", **{"ioc.actor": "GTG-20006"})
for e in ["anna.manager@russianearabroad.net", "events@embassy-protocol.int"]:
    add(e, "email", "src-threat", "GTG-20006 operator email", **{"ioc.actor": "GTG-20006"})
for ip in ["104.145.210.184", "31.57.243.154", "104.194.151.133", "104.194.159.55",
           "144.172.114.192", "213.145.86.112", "2.26.53.194", "148.135.195.111",
           "185.198.234.26", "185.198.234.101", "149.54.42.106", "104.194.149.228",
           "38.146.28.132", "38.146.28.75"]:
    add(ip, "ip", "src-threat", "GTG-20006 IP", **{"ioc.actor": "GTG-20006"})
for f in ["msedgeupdate_v3.exe", "msedgeupdate.exe", "version.dll", "WUEngine.exe",
          "DiagHost.exe", "client_20260507093021_4286d211_x64.exe", "fix_network.apk"]:
    add(f, "filename", "src-threat", "GTG-20006 file", **{"ioc.actor": "GTG-20006"})
add("be99857449d2856dd5a84e21c8a3d5e0e01456adb44062ddec5a6b4970d8d42c", "sha256",
    "src-threat", "GTG-20006 file hash", **{"ioc.actor": "GTG-20006"})
add("918fa52ae45ed60ba7cc8bdc99c3cbe9ab92e0375ec31fc05d0d4513be11c593", "sha256",
    "src-threat", "GTG-20006 file hash", **{"ioc.actor": "GTG-20006"})
for m in ["PowerChrome", "WUEngine", "Shadow C2", "MiniPlasma", "CloudSyncSvc",
          "GiftDrop", "DarkSword"]:
    note = ("Windows malware" if m in ("PowerChrome", "WUEngine", "Shadow C2", "MiniPlasma", "CloudSyncSvc")
            else "GiftDrop = rebranded GiftsExpress Android surveillance RAT" if m == "GiftDrop"
            else "iOS exploit chain")
    add(m, "malware", "src-threat", f"GTG-20006 {note}", **{"ioc.actor": "GTG-20006"})
for t, note in [("Embassy Kit", "Microsoft 365 device-code-phishing token-theft framework"),
                ("WPPConnect", "WhatsApp automation library"),
                ("CaptiveCrunch", "Microsoft name for hotel-WiFi DNS-hijack theft"),
                ("ClickFix", "lure type")]:
    add(t, "tool", "src-threat", f"GTG-20006 tooling: {note}", **{"ioc.actor": "GTG-20006"})
add("JackPoterz", "marker", "src-threat", "GTG-20006 operator handle", **{"ioc.actor": "GTG-20006"})

# --- GTG-50014: domains
D50014 = ["updatebeacon.duckdns.org", "esvfecawvjmchjslqyemho2fiduc59wzn.oast.fun",
          "soraki-proxy.20245aad98d27b1b1a2f0f103e1d7ee0.workers.dev", "soraki.cc",
          "soraki.work", "policenationale.cc", "autoshop.policenationale.cc",
          "emailsecure.email", "mozilla.ws", "signin-1psswoord.com", "on-pssword.com",
          "ari-chain.com", "arichain.network", "bitmart-mystery.com", "defi-claim.xyz",
          "service-infos.info", "0x0.st"]
for d in D50014:
    note = "GTG-50014 domain" + ("; 0x0.st used for curl exfil" if d == "0x0.st" else "")
    add(d, "domain", "src-threat", note, **{"ioc.actor": "GTG-50014"})
add("s3.ap-tokyo.megas4.com", "url", "src-threat", "GTG-50014 exfil bucket host", **{"ioc.actor": "GTG-50014"})
add("s3.eu-central-1.s4.mega.io", "url", "src-threat",
    "GTG-50014 exfil bucket host; bucket name 'fuckyoubasil'", **{"ioc.actor": "GTG-50014"})
for g, note in [("-1003893854338", 'Telegram group "ClintonHog"'),
                ("-1003311614569", 'Telegram group "ChatMignon" (471 forum topics)')]:
    add(g, "telegram-group", "src-threat", f"GTG-50014 {note}", **{"ioc.actor": "GTG-50014"})
for b in ["8632748474", "8664033117", "8628746407", "8709258476"]:
    add(b, "telegram-bot", "src-threat", "GTG-50014 Telegram bot id", **{"ioc.actor": "GTG-50014"})
add("8179098353", "telegram-user", "src-threat", "GTG-50014 Telegram user id", **{"ioc.actor": "GTG-50014"})
add("@Soraki_Bot", "marker", "src-threat", "GTG-50014 Telegram bot handle", **{"ioc.actor": "GTG-50014"})
for ip in ["162.128.129.106", "195.178.110.131", "45.148.10.242", "92.118.39.3",
           "185.65.134.246", "185.65.134.199", "193.32.249.161", "193.32.249.164",
           "193.32.249.170", "104.36.50.54", "104.193.135.207", "91.171.138.169",
           "176.177.12.62", "2a04:cec0:1185:34f2:a150:7081:caed:448e",
           "2a01:e0a:2e2:aa40:b15d:5d28:6f4a:8d53"]:
    add(ip, "ip", "src-threat", "GTG-50014 egress IP", **{"ioc.actor": "GTG-50014"})
for a in ["MeowSHA", "frkoo", "blazespider"]:
    add(a, "marker", "src-threat", "GTG-50014 alias", **{"ioc.actor": "GTG-50014"})

# --- GTG-50021 / GTG-50020 / GTG-50029
for d in ["awstore.cloud", "kiro.cheap", "sys-tools.cfd", "aws-us-east-3.com",
          "holdboost.store", "deltaclient.xyz", "iymkjuzymkapovrntoxy.supabase.co"]:
    add(d, "domain", "src-threat", "GTG-50021 fraudulent AI reseller storefront domain",
        **{"ioc.actor": "GTG-50021"})
add("kl1zy", "marker", "src-threat", "GTG-50021 alias", **{"ioc.actor": "GTG-50021"})
for ip in ["141.133.125.208", "167.250.111.136", "178.16.54.141", "37.27.103.22",
           "194.163.183.216", "202.66.167.230", "146.103.101.253", "146.103.97.169"]:
    add(ip, "ip", "src-threat", "GTG-50020 egress IP (hit AI vendors for eval-sandbox keys)",
        **{"ioc.actor": "GTG-50020"})
for ip in ["139.59.2.243", "158.173.46.118", "146.70.116.131", "149.22.83.6",
           "138.199.60.29", "138.199.6.208", "103.216.220.19", "103.124.165.199",
           "103.141.60.144", "34.156.199.132", "34.156.95.176", "136.144.242.56",
           "163.172.157.53"]:
    add(ip, "ip", "src-threat", "GTG-50029 IP", **{"ioc.actor": "GTG-50029"})
for d in ["frntrs-analytics.dedyn.io",
          "frntrs-analytics-863060591218.europe-west1.run.app",
          "prod-artfkt.com", "fafwatch.xyz"]:
    add(d, "domain", "src-threat", "GTG-50029 domain", **{"ioc.actor": "GTG-50029"})
for o in ["3ell6n47y3ct4a3x67fbuz62q2mk2l4vo6eacho2suzftdshsnrfopyd.onion",
          "6mshbvhvzhdgumwwazf4jcep2xx4kdk6n4wgffc46msu2gc3j3t2fpad.onion"]:
    add(o, "onion", "src-threat", "GTG-50029 .onion", **{"ioc.actor": "GTG-50029"})
add("fafsearch", "tool", "src-threat", "GTG-50029 doxxing platform", **{"ioc.actor": "GTG-50029"})
add("BeEF", "tool", "src-threat", "GTG-50029 browser C2", **{"ioc.actor": "GTG-50029"})

# --- Cluster markers
for term, actor, note in [
        ("Deadshot", "GTG-84002", "UAE-directed cluster persona; ~300 inauthentic accounts"),
        ("S2T Unlocking Cyberspace", "GTG-54009", "Israeli-Singaporean cluster"),
        ("DronDoc", "GTG-27005", "autonomous FPV kamikaze drone swarm"),
        ("Serafim", "GTG-27005", "autonomous FPV kamikaze drone swarm"),
        ("Sibiryachok", "GTG-27005", "Lancet-class drone"),
        ("Zvezdochyot-Serafim", "GTG-27005", "drone system"),
        ("swarm-opi5", "GTG-27005", "drone system"),
        ("Medovik", "GTG-27005", "drone system"),
        ("Nebo-22", "GTG-27005", "drone system"),
        ("SHANKI", None, "Kenya astroturfing operation"),
        ("Elkins Marketer", None, "Kenya astroturfing operation"),
        ("Radio Lengo Songo 98.9 FM", "GTG-04001", "CAR influence vector"),
        ("PentAGI", None, "public offensive agent framework on GitHub; track forks, Docker images, deployment IPs")]:
    add(term, "marker", "src-threat", note, **({"ioc.actor": actor} if actor else {}))

# --- Eval / benchmark markers
for term, sref, note in [
        ("CyScenarioBench", "src-cvp", "multi-stage offensive-ops benchmark; Opus 5.5 scores: no-CVP 0/50, Defense 4/50, Red Team 34/50"),
        ("Gray Swan Agent Red Teaming", "src-contain", "prompt-injection benchmark; Opus 4.7 ASR ~0.1% single / 5-6% after 100 adaptive attempts"),
        ("Petri", "src-auto", "open-source adversarial multi-turn misalignment simulator"),
        ("ConfAIde", "src-auto", "alignment benchmark"),
        ("PrivaCI-Bench", "src-auto", "alignment benchmark"),
        ("PrivacyLens", "src-auto", "alignment benchmark"),
        ("Epoch Capabilities Index", "src-auto", "capabilities index")]:
    add(term, "eval-name", sref, note)

# --- Containment architecture markers
for term, note in [
        ("gVisor", "claude.ai: ephemeral gVisor containers, per-session filesystem, server-side only"),
        ("Seatbelt", "Claude Code sandbox on macOS"),
        ("bubblewrap", "Claude Code sandbox on Linux; open-sourced sandbox runtime"),
        ("red.anthropic.com", "coordinated disclosure endpoint"),
        ("api.anthropic.com", "Files API; abused via attacker-supplied keys for egress"),
        ("portal.anthropic.com", "Cyber Verification Program application portal"),
        ("alignment.anthropic.com", "Alignment Science blog; open-sourced alignment research harness"),
        ("multiagent_20261001", "Dynamic Workflows (Claude Managed Agents) multiagent type, public beta 2026-10-09"),
        ("managed-agents-2026-04-01", "Dynamic Workflows beta header"),
        ("claude.ai/code/session_", "Claude Code session URL pattern (attribution trailer)")]:
    add(term, "marker", "src-contain", note)

add("https://github.com/anthropics/mythos-5-incident-transcript", "url", "src-align",
    "public incident transcript repo; behavioral goldmine for prompt/CoT patterns preceding real-world harm")

# --- Build records
records = []
for ref, locator, platform, stype, title in SOURCES:
    records.append({
        "kind": "source", "ref": ref,
        "body": {"locator": locator, "platform": platform,
                 "source_type": stype, "title": title},
        "tags": {"lane": LANE, "grade": "UPSTREAM"},
    })

# dedup within batch by (term, category)
seen = set()
for i, (term, category, sref, p, tags) in enumerate(IOCS):
    key = (term.lower(), category)
    assert key not in seen, f"duplicate ioc in batch: {key}"
    seen.add(key)
    t = {"lane": LANE, "grade": "UPSTREAM"}
    t.update(tags)
    records.append({
        "kind": "observation", "ref": f"ioc-{i:03d}",
        "body": {"type": "infra.ioc",
                 "data": {"term": term, "category": category,
                          "provenance": p, "status": "active"},
                 "data_schema": "urn:factum:infra:ioc:1",
                 "files": [], "observed_at": NOW,
                 "source": "@" + sref, "time_basis": "received_by_factum"},
        "tags": t,
    })

refs = [r["ref"] for r in records]
assert len(refs) == len(set(refs)), "duplicate refs"
assert all(len(r) <= 64 for r in refs), "ref too long"

bundle = {"bundle": 2, "actor": ACTOR,
          "idempotency_key": "anthropic-tradecraft-2026-10-11-bundle-2",
          "records": records}

out = "data/lanes/2026-10-11-anthropic-agent-tradecraft/bundle-2.json"
with open(out, "w") as f:
    json.dump(bundle, f, indent=1)
print(f"wrote {out}: {len(records)} records ({len(SOURCES)} sources, {len(IOCS)} iocs)")
