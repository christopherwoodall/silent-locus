#!/usr/bin/env python3
"""Time-scoped revision-history grep for incident markers — CHECKPOINTED + SHARDED.

Resumable: completed (host, date) combos are recorded in a state file and
skipped on restart. Hits append incrementally. A lock file prevents
overlapping runs. Writes DONE when all combos complete.

Sharding: set SHARD="i/n" (e.g. "0/4") to process only combos where
combo_index % n == i. Each shard uses its own state/hits/lock/DONE files,
so shards never contend. Unset SHARD processes everything (single-run mode).

Safe to re-run any number of times; safe to kill at any point.
"""
import json, re, time, urllib.parse, urllib.request, os, hashlib, fcntl

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/revhistory-grep")
RAW = os.path.join(BASE, "raw")
os.makedirs(RAW, exist_ok=True)

shard_env = os.environ.get("SHARD", "")
if shard_env:
    shard_i, shard_n = (int(x) for x in shard_env.split("/"))
    SUF = f"-shard{shard_i}"
else:
    shard_i, shard_n, SUF = 0, 1, ""
STATE = os.path.join(BASE, f"state{SUF}.json")
HITS = os.path.join(BASE, f"hits{SUF}.jsonl")
LOCK = os.path.join(BASE, f".lock{SUF}")
DONE = os.path.join(BASE, f"DONE{SUF}")

UA = "silent-locus-research/1.0 (research revision-history census; contact via repo)"

WIKIS = {
    "incubator.wikimedia.org": "Incubator:Sandbox",
    "commons.wikimedia.org": "Commons:Sandbox",
    "meta.wikimedia.org": "Meta:Sandbox",
    "www.mediawiki.org": "Project:Sandbox",
    "en.wikipedia.org": "Wikipedia:Sandbox",
    "simple.wikipedia.org": "Wikipedia:Sandbox",
    "test.wikipedia.org": "Wikipedia:Sandbox",
    "test2.wikipedia.org": "Wikipedia:Sandbox",
    "bg.wikipedia.org": "Уикипедия:Пясъчник",
}
DATES = ["2026-05-10", "2026-05-13", "2026-05-18", "2026-05-21",
         "2026-05-25", "2026-05-27", "2026-06-18", "2026-06-25"]

PATTERNS = [
    ("lifeval", re.compile(r"lifeval", re.I)),
    ("temp-technical-sandbox-init", re.compile(r"temporary technical sandbox initialization", re.I)),
    ("sandbox-initialization", re.compile(r"sandbox initialization", re.I)),
    ("temp-account-test", re.compile(r"temp-account test", re.I)),
    ("api-temp-account", re.compile(r"API temp-account", re.I)),
    ("zz-oai-grammar", re.compile(r"zz\s*=\s*oai\d+", re.I)),
]

def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {"completed": [], "total_revs": 0}

def save_state(s):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=1)
    os.replace(tmp, STATE)

def api(host, params):
    q = urllib.parse.urlencode(params)
    url = f"https://{host}/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                return json.loads(body), hashlib.sha256(body).hexdigest()
        except Exception as e:
            last = e
            time.sleep(10)
    raise RuntimeError(f"FAILED {host} {params.get('titles')}: {last}")

def main():
    lockf = open(LOCK, "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("LOCKED: another run in progress, exiting")
        return
    log = open(os.path.join(BASE, f"run{SUF}.log"), "a")
    hitsf = open(HITS, "a")
    state = load_state()
    done_set = set(state["completed"])
    combos = [(h, d) for h in WIKIS for d in DATES]
    mine = [c for idx, c in enumerate(combos) if idx % shard_n == shard_i]
    remaining = [c for c in mine if f"{c[0]}|{c[1]}" not in done_set]
    log.write(f"START {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
              f"shard={shard_env or 'all'} remaining={len(remaining)}/{len(mine)}\n")
    log.flush()
    try:
        for host, date in remaining:
            title = WIKIS[host]
            start, end = f"{date}T00:00:00Z", f"{date}T23:59:59Z"
            tag = f"{host}__{date}"
            cont, page_n, ok = None, 0, True
            while True:
                params = {
                    "action": "query", "prop": "revisions", "titles": title,
                    "rvstart": end, "rvend": start, "rvdir": "older",
                    "rvprop": "ids|timestamp|user|comment|content",
                    "rvslots": "main", "format": "json", "formatversion": "2",
                    "rvlimit": "max",
                }
                if cont:
                    params["rvcontinue"] = cont
                try:
                    data, sha = api(host, params)
                except RuntimeError as e:
                    log.write(f"{tag} ERROR {e}\n"); log.flush()
                    ok = False
                    break
                page_n += 1
                fn = os.path.join(RAW, f"{tag}__p{page_n}.json")
                with open(fn, "w") as f:
                    json.dump({"_provenance": {"host": host, "title": title,
                             "window": [start, end],
                             "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                             "sha256": sha}, "response": data}, f)
                pages = data.get("query", {}).get("pages", [])
                if pages and "missing" in pages[0]:
                    log.write(f"{tag} MISSING-PAGE {title}\n"); log.flush()
                    break
                revs = pages[0].get("revisions", []) if pages else []
                state["total_revs"] += len(revs)
                for rv in revs:
                    content = (rv.get("slots", {}).get("main", {}).get("content") or "")
                    for pname, pat in PATTERNS:
                        m = pat.search(content)
                        if m:
                            s = max(0, m.start() - 60)
                            hitsf.write(json.dumps({
                                "wiki": host, "page": title, "revid": rv.get("revid"),
                                "timestamp": rv.get("timestamp"), "user": rv.get("user"),
                                "comment": rv.get("comment"), "pattern": pname,
                                "snippet": content[s:m.end() + 60].replace("\n", " ")[:200],
                            }) + "\n")
                            hitsf.flush()
                cont = data.get("continue", {}).get("rvcontinue")
                if not cont:
                    break
                time.sleep(2)
            if ok:
                done_set.add(f"{host}|{date}")
                state["completed"] = sorted(done_set)
                save_state(state)
                log.write(f"{tag} COMPLETE ({len(done_set)}/{len(mine)})\n"); log.flush()
            time.sleep(2)
    finally:
        hitsf.close()
        log.write(f"STOP total_revs={state['total_revs']} completed={len(done_set)}/{len(mine)}\n")
        log.close()
        try:
            os.unlink(LOCK)
        except OSError:
            pass
    if len(done_set) == len(mine):
        with open(DONE, "w") as f:
            f.write(f"completed {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
                    f"revs={state['total_revs']}\n")
        print(f"DONE shard {shard_env or 'all'}: {len(mine)} combos, revs={state['total_revs']}")
    else:
        print(f"PARTIAL shard {shard_env or 'all'}: {len(done_set)}/{len(mine)} combos, revs={state['total_revs']}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
