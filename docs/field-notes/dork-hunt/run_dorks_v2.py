#!/usr/bin/env python3
"""Dork-hunt v2: fresh Google dork wave using NEW IOCs from the 2026-10-03 hunt.

New fuel vs v1: joshuadavid v4 candidates (72 terms), discord-brief watch terms,
relay hosts (jqp.vercel.app, lemino.ai, hexlet.app, cors.lol), NPWS incident terms.
Dedupes against data/dork-log.jsonl (shared with v1). State -> state-v2.json.

Usage: python3 run_dorks_v2.py [--limit N]
"""
import json, os, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from run_dorks import ddg_search, load_done, log_row  # noqa: E402

STATE_V2 = os.path.join(BASE, "state-v2.json")
PACE = 6.0

# Tier A: highest-novelty strings -> bare + site:github.com + site:pastebin.com
TIER_A = [
    "OAI_META_1312",
    "AgentSECCountyLinker",
    "sec.govwayback.com",
    "platform.lemino.ai",
    "b12026d61228a4b0d441ae7aa93f1ea222877503",
    "vanderbi.lt/maallraw260618",
    "allorigins.hexlet.app",
    "api.cors.lol",
    "jqp.vercel.app",
    "oasb_raising_capital_map",
    "cdn.putput.io",
    "2md.link",
    "URLTEST1779099362",
    "linktry97976",
    "AgentRelent",
    "AgentCustomPageZZZ",
    "ZZZNew",
    "ANCHORTEST",
    "EPL95test",
    "TINJ",
    "TestHelloABC",
    "hd-test-1450",
    "hello-hd-1450",
    "palapiXYZ",
    "IowaTableauTip",
]

# Tier B: distinctive but narrower -> bare + site:github.com
TIER_B = [
    "Ghtml_probe_series",
    "TEL_series",
    "TK_series",
    "URLTEST_series",
    "SFTEST_RefQ_series",
    "Proxy_series",
    "linktry_series",
    "AgentMine",
    "MapHelper",
    "MassUpdater",
    "ResearchHelper",
    "DoubleSlashPrettyFresh123",
    "AddedSECQueryLinksFresh99281",
    "FreshPrettyNoQueryJune20",
    "Ghtml599",
    "Ghtml4strict99",
    "Gbbcode99",
    "Gxml99",
    "Gmarkdown99",
    "Gurl99",
    "Glatex99",
    "Gphp99",
    "Gjavascript99",
    "Grobots99",
    "RefreshInvestorBridgeMassachusettsA",
    "RefreshAgentInvestLinksWindow11XQA",
]

# Tier C: path-canonicalization probes -> bare + inurl:
TIER_C = [
    "sec.gov//files//county.json",
    "sec.gov/Files/county.json",
    "sec.gov/foo/../files//county.json",
    "sec.gov:443/files/county.json",
    "www.sec.gov/sites/default/files/county.json",
]

# Tier D: NPWS incident terms -> bare
TIER_D = [
    '"Fire History" "National Parks and Wildlife Service"',
    '"NPWS" "Fire History" agent',
    '"aifs.gov.au"',
    '"Fire History service" NSW agent',
]


def build_v2_dorks():
    dorks = []
    for t in TIER_A:
        dorks.append(("v2-bare", f'"{t}"'))
        dorks.append(("v2-site", f'site:github.com "{t}"'))
        dorks.append(("v2-site", f'site:pastebin.com "{t}"'))
    for t in TIER_B:
        dorks.append(("v2-bare", f'"{t}"'))
        dorks.append(("v2-site", f'site:github.com "{t}"'))
    for t in TIER_C:
        dorks.append(("v2-bare", f'"{t}"'))
        dorks.append(("v2-inurl", f'inurl:{t}'))
    for q in TIER_D:
        dorks.append(("v2-bare", q))
    return dorks


def save_state(d):
    with open(STATE_V2, "w") as f:
        json.dump(d, f, indent=2)


def main():
    args = sys.argv[1:]
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    dorks = build_v2_dorks()
    done = load_done()
    total = len(dorks)
    ran = blocked = skipped = err = 0
    print(f"v2 dorks: {total}, already in log: {len(done)}", flush=True)
    for i, (kind, q) in enumerate(dorks):
        if limit and ran >= limit:
            break
        if q in done:
            skipped += 1
            continue
        status, urls, titles = ddg_search(q)
        if status == "blocked":
            time.sleep(60)
            status, urls, titles = ddg_search(q)
        row = {
            "query": q,
            "kind": kind,
            "backend": "curl-ddg-html",
            "path": "curl",
            "status": status,
            "hits": len(urls),
            "examples": [{"url": u[:300], "title": t}
                         for u, t in zip(urls[:3], titles[:3])],
            "note": titles[0] if status != "ok" else "",
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        log_row(row)
        done.add(q)
        ran += 1
        if status == "blocked":
            blocked += 1
        elif status == "error":
            err += 1
        if ran % 20 == 0:
            print(f"  {ran} ran, {blocked} blocked, {err} errors, {skipped} skipped",
                  flush=True)
            save_state({"ran": ran, "blocked": blocked, "errors": err,
                        "skipped": skipped, "total": total, "status": "running",
                        "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                     time.gmtime())})
        time.sleep(PACE)
    save_state({"ran": ran, "blocked": blocked, "errors": err,
                "skipped": skipped, "total": total,
                "status": "complete" if (limit is None or ran >= limit) else "partial",
                "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    print(f"V2 DONE: ran={ran} blocked={blocked} errors={err} skipped={skipped}",
          flush=True)


if __name__ == "__main__":
    main()
