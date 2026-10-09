#!/usr/bin/env python3
"""Collapse url-farm URLs to deduplicated hosts with benign stripped.
Read-only on inputs. Writes hosts-deduped.json. No commits.
"""
import json, re, os, sys
from urllib.parse import urlparse

FARM = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(FARM, "hosts-deduped.json")

# ---------- 1. Load ALL available URL entries (url -> count, datasets, examples)
entries = {}  # url -> {count, datasets:set, example_urls:set, first_examples:[]}

def add(url, count, dataset, examples):
    if not url:
        return
    e = entries.setdefault(url, {"count": 0, "datasets": set(), "examples": []})
    e["count"] += count
    if dataset:
        e["datasets"].add(dataset)
    for ex in (examples or [])[:5]:
        if len(e["examples"]) < 8 and ex not in e["examples"]:
            e["examples"].append(ex)

def ex_str(ex):
    """Distill one example URL from an example dict/str."""
    if isinstance(ex, str):
        return ex
    if isinstance(ex, dict):
        for k in ("url", "task"):
            v = ex.get(k)
            if v:
                return v
    return ""

src_urls_seen = {}
order = [("group-A.json", None), ("group-D.json", None),
         ("group-B.compact.json", None), ("merged.json", None)]

# group-A
g = json.load(open(os.path.join(FARM, "group-A.json")))
for u in g.get("urls", []):
    add(u.get("url", ""), u.get("count", 1), "group-A",
        [x if isinstance(x, str) else x.get("url", "") for x in (u.get("examples") or [])])
src_urls_seen["group-A.json"] = len(g.get("urls", []))

# group-D
g = json.load(open(os.path.join(FARM, "group-D.json")))
for u in g.get("urls", []):
    add(u.get("url", ""), u.get("count", 1), u.get("dataset", "group-D"),
        [x if isinstance(x, str) else x.get("url", "") for x in (u.get("examples") or [])])
src_urls_seen["group-D.json"] = len(g.get("urls", []))

# group-B compact: top100 per tier only (full file gone; see DATA GAP note)
g = json.load(open(os.path.join(FARM, "group-B.compact.json")))
n_b = 0
for tier, lst in g.get("url_tier_top100", {}).items():
    for u in lst:
        add(u.get("url", ""), u.get("count", 1), u.get("dataset", "group-B"),
            [ex.get("url", "") if isinstance(ex, dict) else ex for ex in (u.get("examples") or [])])
        n_b += 1
src_urls_seen["group-B.compact.json"] = n_b

# merged.json url_tier_top: only add URLs not already loaded (avoid double-count)
g = json.load(open(os.path.join(FARM, "merged.json")))
n_m, n_m_new = 0, 0
for tier, lst in g.get("url_tier_top", {}).items():
    for u in lst:
        url = u.get("url", "")
        n_m += 1
        if url and url not in entries:
            add(url, u.get("count", 1), ",".join(u.get("datasets", []) or ["merged-top"]),
                u.get("examples", []))
            n_m_new += 1
src_urls_seen["merged.json top lists"] = n_m

# ---------- 2. Normalize to host
def norm_host(url):
    try:
        netloc = urlparse(url).netloc
    except Exception:
        return None, url
    host = netloc.split("@")[-1]  # strip userinfo
    host = host.split(":")[0] if not host.startswith("[") else host.split("]")[0] + "]"
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    host = host.lower().strip().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    try:
        host = host.encode("ascii").decode("ascii")
    except UnicodeEncodeError:
        try:
            host = host.encode("idna").decode("ascii")
        except Exception:
            pass
    return host or None, url

hosts = {}  # host -> {count, datasets:set, url_list:[(url,count)]}
unparseable = 0
for url, e in entries.items():
    host, _ = norm_host(url)
    if not host:
        unparseable += 1
        continue
    h = hosts.setdefault(host, {"count": 0, "datasets": set(), "urls": []})
    h["count"] += e["count"]
    h["datasets"] |= e["datasets"]
    h["urls"].append((url, e["count"]))
    for ex in e["examples"][:2]:
        s = ex_str(ex)
        if s and s not in h["urls"] and len(h["examples"] if False else []) == 0:
            pass

for h in hosts.values():
    h["urls"].sort(key=lambda x: -x[1])

# ---------- 3. Classify
IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
IPV6 = re.compile(r"^[0-9a-fA-F:]+::?[0-9a-fA-F:]*$|^::$")

def is_ip(host):
    return bool(IPV4.match(host)) or ":" in host

PKG_SUFFIXES = (".ubuntu.com", "pypi.org", "files.pythonhosted.org",
                "registry.npmjs.org", "registry.yarnpkg.com", "npmjs.com",
                "deb.debian.org", "debian.org", "conda.anaconda.org",
                "repo.anaconda.com", "repo.continuum.io", "anaconda.com",
                "anaconda.org", "cran.r-project.org", "r-project.org",
                "ctan.org", "mirrors.ctan.org", "pypi.python.org",
                "ppa.launchpad.net", "launchpad.net", "rubygems.org",
                "packagist.org", "nuget.org", "crates.io", "goproxy.io",
                "proxy.golang.org", "storage.googleapis.com",)
PKG_HOST = ("pypi.org", "npmjs.com", "anaconda.com", "rubygems.org",
            "nuget.org", "crates.io", "ctan.org", "security.ubuntu.com",
            "archive.ubuntu.com", "us.archive.ubuntu.com", "deb.debian.org",
            "conda.anaconda.org", "repo.anaconda.com", "files.pythonhosted.org",
            "registry.npmjs.org", "registry.yarnpkg.com", "proxy.golang.org",
            "ppa.launchpad.net", "mirrors.edge.kernel.org", "downloads.python.org")
WIKI_SUFFIX = (".wikipedia.org", ".wikimedia.org", ".wiktionary.org")
WIKI_HOST = ("wikipedia.org", "wikimedia.org", "wiktionary.org", "wikidata.org",
             "wikiquote.org", "wikibooks.org", "wikisource.org", "wikinews.org",
             "wikiversity.org", "wikivoyage.org", "mediawiki.org")
DOCS_HOST = ("docs.python.org", "readthedocs.org", "readthedocs.io",
             "developer.mozilla.org", "learn.microsoft.com", "docs.microsoft.com",
             "developer.apple.com", "docs.rs", "godoc.org", "pkg.go.dev",
             "docs.oracle.com", "docs.aws.amazon.com", "cloud.google.com",
             "docs.docker.com")
CDN_HOST = ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com",
            "unpkg.com", "cdn.jsdelivr.net")
SUSP_PATH = ("webhook", "exfil", "c2", "shell", "payload", "beacon",
             "keylog", "dump", "steal", "inject", "phish", "malware",
             "bypass", "jailbreak")
SEARCH_HOST = ("google.com", "bing.com", "duckduckgo.com", "yahoo.com",
               "baidu.com", "yandex.com", "startpage.com", "search.brave.com")
LOCAL_HOST = ("localhost", "127.0.0.1", "::1", "0.0.0.0", "local")

PROXY_LAUNDER = ("jina.ai", "r.jina.ai", "allorigins.win", "corsproxy.io",
                 "cors-anywhere", "thingproxy", "corsproxy.org", "proxy.cors.sh",
                 "api.allorigins.win", "cors.isomorphic-git.org",
                 "api.codetabs.com", "whateverorigin.org", "jsonp.afeld.me")
EXFIL_C2 = ("webhook.site", "ntfy.sh", "discord.com", "discordapp.com",
            "api.telegram.org", "t.me", "telegram.org", "pastebin.com",
            "paste.rs", "0x0.st", "termbin.com", "ix.io", "hastebin.com",
            "controlc.com", "rentry.co", "paste.ee", "dpaste.com",
            "transfer.sh", "file.io", "requestbin.com", "pipedream.net",
            "beeceptor.com", "webhookrelay.com", "hook.us", "postb.in",
            "ptsv2.com", "enformed.io", "webhook.glitch.me",
            "requestcatcher.com", "webhookinbox.com", "temp.sh",
            "uguu.se", "catbox.moe", "litterbox.catbox.moe", "pomf.cat",
            "bashupload.com", "oshi.at", "send.vis.ee", "wormhole.app")
TUNNEL = ("ngrok.io", "ngrok.com", "trycloudflare.com", "localtunnel.me",
          "bore.pub", "localhost.run", "serveo.net", "zrok.io",
          "boreproxy", "cloudflared", "pagekite.me", "tunnelkit")
SHORT = ("bit.ly", "t.co", "tinyurl.com", "goo.gl", "is.gd", "buff.ly",
         "ow.ly", "rb.gy", "cutt.ly", "rebrand.ly", "s.id", "shorturl.at",
         "t.ly", "lnkd.in", "tiny.cc", "tr.im", "cli.gs", "shorte.st",
         "adf.ly", "bitly.com", "hyperurl.co")
GITHUB_FILE = ("gist.githubusercontent.com", "raw.githubusercontent.com",
               "objects.githubusercontent.com", "gist.github.com",
               "raw.github.com", "codeload.github.com")

def host_matches(host, marks):
    # strict domain-boundary match: exact or subdomain only
    return host in marks or any(host.endswith("." + m) for m in marks)

kept, dropped = [], []
for host, h in hosts.items():
    datasets = sorted(h["datasets"])
    example_urls = [u for u, c in h["urls"][:3]]
    rec = {"host": host, "total_count": h["count"], "datasets": datasets,
           "example_urls": example_urls}

    # --- DROP (benign)
    reason = None
    if host in LOCAL_HOST or host.endswith(".local") or host.endswith(".internal") \
       or host.endswith(".localhost") or host.endswith(".home.arpa") \
       or host.endswith(".test") or host.endswith(".example") or host.endswith(".invalid"):
        reason = "localhost/loopback/link-local"
    elif host_matches(host, PKG_SUFFIXES) or host in PKG_HOST:
        reason = "package mirror / registry"
    elif host_matches(host, WIKI_SUFFIX) or host in WIKI_HOST:
        reason = "wikipedia/wikimedia/wiktionary"
    elif host in DOCS_HOST or host.endswith(".readthedocs.io") or host.endswith(".readthedocs.org"):
        reason = "documentation site"
    elif host in CDN_HOST:
        paths = " ".join(u.lower() for u, c in h["urls"])
        if any(s in paths for s in SUSP_PATH):
            rec["tier"] = "CDN-SUSPICIOUS-PATH"
            kept.append(rec); continue
        reason = "font/CDN"
    elif host == "github.com" or host.endswith(".github.com"):
        reason = "github.com (kept only gist/raw/objects file hosts)"
    elif host in SEARCH_HOST or host.endswith(".google.com") or host.endswith(".bing.com") \
         or host.endswith(".duckduckgo.com"):
        paths = [urlparse(u).path.lower() for u, c in h["urls"]]
        if any(p.startswith("/api") for p in paths):
            rec["tier"] = "SEARCH-API-SHAPED"
            kept.append(rec); continue
        reason = "search frontend"
    elif host.endswith(".onion") or host.endswith(".i2p"):
        rec["tier"] = "onion/i2p"
        kept.append(rec); continue
    elif host_matches(host, PROXY_LAUNDER):
        rec["tier"] = "proxy-launder"; kept.append(rec); continue
    elif host_matches(host, EXFIL_C2):
        rec["tier"] = "exfil/c2"; kept.append(rec); continue
    elif host_matches(host, TUNNEL):
        rec["tier"] = "tunnel"; kept.append(rec); continue
    elif host_matches(host, SHORT):
        rec["tier"] = "url-shortener"; kept.append(rec); continue
    elif host in GITHUB_FILE:
        rec["tier"] = "github-file-host"; kept.append(rec); continue
    elif is_ip(host) and host not in LOCAL_HOST:
        rec["tier"] = "ip-literal"; kept.append(rec); continue
    else:
        rec["tier"] = "UNKNOWN"
        kept.append(rec); continue
    if reason:
        dropped.append({"host": host, "total_count": h["count"], "reason": reason})

# ---------- 4. Dedupe check
all_hosts = [r["host"] for r in kept] + [r["host"] for r in dropped]
assert len(all_hosts) == len(set(all_hosts)), "DUPLICATE HOST STRINGS FOUND"
dedupe_ok = True

kept_sorted = sorted(kept, key=lambda r: -r["total_count"])
dropped_sorted = sorted(dropped, key=lambda r: -r["total_count"])
tier_counts = {}
for r in kept:
    tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1

out = {
    "kept": kept_sorted,
    "dropped": dropped_sorted,
    "stats": {
        "unique_urls_in": len(entries),
        "unique_hosts": len(hosts),
        "unparseable_urls": unparseable,
        "kept": len(kept),
        "dropped": len(dropped),
        "kept_by_tier": tier_counts,
        "sources": src_urls_seen,
    },
    "notes": [
        {"DATA GAP": "Full group-B.json (276MB, 188,094 unique URLs) was compacted and the "
         "full file is not present on local disk; group-B.compact.json carries only "
         "top-100 per tier. Host collapse covers all available URLs (group-A full, "
         "group-D full, group-B top100s, merged.json top lists). Re-run farm_groupB.py "
         "on restored raw data and re-collapse for full coverage."},
        {"COUNT SEMANTICS": "total_count = sum of occurrence counts across loaded "
         "entries. Group-B top100 counts are partial (top-only)."},
        {"NEVER REDACT": "example_urls kept verbatim, full values."},
    ],
}
json.dump(out, open(OUT, "w"), indent=1)

print("unique_urls_in:", len(entries))
print("unique_hosts:", len(hosts))
print("kept:", len(kept), "dropped:", len(dropped))
print("kept_by_tier:", tier_counts)
print("DEDUPE CHECK: PASS (no duplicate host strings in kept+dropped)")
print("top-10 kept:")
for r in kept_sorted[:10]:
    print(" ", r["total_count"], r["tier"], r["host"])
print("top-5 dropped:")
for r in dropped_sorted[:5]:
    print(" ", r["total_count"], r["reason"], r["host"])
print("wrote", OUT)
