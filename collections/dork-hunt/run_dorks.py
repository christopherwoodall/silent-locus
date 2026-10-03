#!/usr/bin/env python3
"""Google-dork hunt runner: curl-based, stateful, idempotent, committable.

Queries DuckDuckGo's html endpoint (curl) for IOC dorks, logs every dork
to data/dork-log.jsonl with hit counts + examples. Re-running resumes from
the log: already-logged exact query strings are skipped.

Usage:
  python3 run_dorks.py [--limit N] [--terms-file PATH]
  python3 run_dorks.py --fidelity   # 6-dork operator fidelity check only
"""
import json, os, re, subprocess, sys, time, urllib.parse, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE, "data", "dork-log.jsonl")
STATE = os.path.join(BASE, "state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PACE = 2.0  # seconds between queries

# ---- curated term list: most distinctive ~60 ----
TERMS = [
    # launcher_toolkit
    "zz=oai", "AgentOpenAIResearch", "OpenAIResearch", "openai_research",
    "openai-research", "OpenAIResearchSec2027", "OpenAIResearchAgent",
    "epoch10", "davprobe", "zzJina", "zzproxyoaiabc431848",
    "AgenticCommunication", "NightingaleCollective", "WikiIncident2026",
    "AgentCountyProxyMdJuneTen", "GreenAiBot",
    # evals
    "deepsearchqa", "dsqa_250", "browsecomp", "cybergym", "exploitgym",
    # sqli_payloads (sharpest fragments)
    "1%20OR%201%3D1", "IdNumber=1%20OR%201%3D1", "surveyYearKey",
    "Survey_Year_Key", "Measure_Id=130", "State_Id", "long_Nces_Id",
    "downloadtoken=DT--abc--DT",
    # question_terms (sharpest; virginia-projection.xls added per task brief)
    "virginia-projection.xls", "historical.elections.virginia.gov",
    "Virginia Democratic Primary", "nces.ed.gov/ipeds",
    "IZA Global Preferences Survey", "Kentucky and West Virginia",
    "Canada Atlantic Provinces", "American Community Survey 5-Year",
    # targets (watchlist)
    "civilrightsdata.ed.gov", "www.sec.gov/files/county.json", "county.json",
    "bac-lac.gc.ca", "apps.bea.gov", "bea.gov",
    "recherche-collection-search.bac-lac.gc.ca", "kansasmemory.gov",
    # relays (a few high-signal)
    "ghostarchive.org", "megalodon.jp", "gyo.tc", "arquivo.pt",
]

SITES = ["ghostarchive.org", "megalodon.jp", "gyo.tc", "web.archive.org",
         "arquivo.pt", "pastebin.com", "rentry.co", "gist.github.com",
         "telegra.ph", "github.com"]

# URL-shaped terms also get a bare inurl: dork
INURL_TERMS = ["county.json", "virginia-projection.xls", "surveyYearKey",
               "Survey_Year_Key", "Measure_Id", "State_Id", "zz=oai",
               "dsqa_250", "github.com"]


def build_dorks(terms):
    dorks = []
    for t in terms:
        q = f'"{t}"'
        dorks.append(("bare", q))
        for s in SITES:
            dorks.append((f"site:{s}", f'site:{s} "{t}"'))
    for t in INURL_TERMS:
        if t in terms:
            dorks.append(("inurl", f"inurl:{t}"))
    return dorks


def ddg_search(query):
    """Returns (status, urls, titles). status in ok|blocked|error."""
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        r = subprocess.run(["curl", "-s", "-A", UA, "--max-time", "25", "-w",
                            "\n%{http_code}", url],
                           capture_output=True, text=True, timeout=40)
    except Exception as e:
        return "error", [], [f"curl exception: {e}"]
    body, _, code = r.stdout.rpartition("\n")
    code = code.strip()
    if code == "000":
        return "error", [], ["connection failed/timeout"]
    if code in ("202", "429", "403") or ("challenge" in body[:2000].lower()
                                         and "result__a" not in body):
        return "blocked", [], [f"http {code}"]
    if code != "200":
        return "error", [], [f"http {code}"]
    if "result__a" in body:
        links = re.findall(r'class="result__a"[^>]*href="([^"]+)"', body)
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', body, re.S)
        urls = []
        for l in links:
            m = re.search(r"uddg=([^&\"]+)", l)
            urls.append(urllib.parse.unquote(m.group(1)) if m else l)
        titles = [re.sub(r"<[^>]+>", "", t).strip()[:160] for t in titles]
        return "ok", urls, titles
    if re.search(r"no results|not many results", body, re.I):
        return "ok", [], []  # honest zero: valid query, backend says none
    return "error", [], ["http 200, unparseable body"]


def load_done():
    done = set()
    if os.path.exists(LOG):
        with open(LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    done.add(json.loads(line)["query"])
                except Exception:
                    pass
    return done


def log_row(row):
    with open(LOG, "a") as f:
        f.write(json.dumps(row) + "\n")


def save_state(d):
    with open(STATE, "w") as f:
        json.dump(d, f, indent=2)


def run_dork(kind, query, done):
    if query in done:
        return "skipped"
    status, urls, titles = ddg_search(query)
    if status == "blocked":
        # backoff once, then record blocked
        time.sleep(60)
        status, urls, titles = ddg_search(query)
    row = {
        "query": query,
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
    done.add(query)
    return status


def main():
    args = sys.argv[1:]
    if "--fidelity" in args:
        pairs = [
            ("site:ghostarchive.org civilrightsdata", "civilrightsdata"),
            ('"zz=oai"', "zz=oai"),
            ("inurl:county.json sec.gov", "county.json sec.gov"),
        ]
        print("fidelity check: 6 dorks")
        for with_op, without in pairs:
            for q in (with_op, without):
                st, urls, _ = ddg_search(q)
                print(f"  [{st}] n={len(urls)} :: {q}")
                time.sleep(2)
        return
    limit = None
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
    dorks = build_dorks(TERMS)
    done = load_done()
    total = len(dorks)
    ran = blocked = skipped = 0
    print(f"dorks: {total}, already done: {len(done)}", flush=True)
    for i, (kind, q) in enumerate(dorks):
        if limit and ran >= limit:
            break
        if q in done:
            skipped += 1
            continue
        st = run_dork(kind, q, done)
        ran += 1
        if st == "blocked":
            blocked += 1
        if ran % 25 == 0:
            print(f"  {ran} ran, {blocked} blocked, {skipped} skipped", flush=True)
            save_state({"ran": ran, "blocked": blocked, "skipped": skipped,
                        "total": total, "status": "running",
                        "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                     time.gmtime())})
        time.sleep(PACE)
    save_state({"ran": ran, "blocked": blocked, "skipped": skipped,
                "total": total, "status": "complete" if (limit is None or ran >= limit) else "partial",
                "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    print(f"DONE: ran={ran} blocked={blocked} skipped={skipped}", flush=True)


if __name__ == "__main__":
    main()
