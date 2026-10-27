#!/usr/bin/env python3
"""Parallel HN thread fetcher (replaces the sequential scripts for speed).

Same lane rules as fetch_hn_threads.py: poster-identity field stripped
before writing, never printed; all other bytes verbatim. Idempotent per
root: existing done roots are skipped. Progress in progress.json (merged,
never clobbered: read-modify-write under a file lock via atomic rename
is not used here because this is the only writer after the sequential
fetchers were stopped).
"""
import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOTS = {
    "ranked": ["46622328", "46624950"],
    "appendix": ["48349487", "48827858"],
    "context": ["50246658"],
    "killed": ["48272354", "47190721", "46403097", "48052629", "49605924",
               "48414158", "50249935", "48916975", "47541805", "50165308",
               "48838376"],
}
WORKERS = 16


def fetch_item(item_id):
    for attempt in range(3):
        out = subprocess.run(
            ["curl", "-sS", "--max-time", "60",
             f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"],
            capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip() and out.stdout.strip() != "null":
            item = json.loads(out.stdout)
            item.pop("by", None)
            return item
        time.sleep(2 * (attempt + 1))
    return {"id": int(item_id), "missing": True}


def fetch_thread(root_id):
    items = {}
    frontier = [root_id]
    seen = set()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        while frontier:
            batch = [i for i in frontier if i not in seen]
            frontier = []
            for cur in batch:
                seen.add(cur)
            results = list(pool.map(fetch_item, batch))
            for item in results:
                items[str(item["id"])] = item
                for kid in item.get("kids") or []:
                    if str(kid) not in seen:
                        frontier.append(str(kid))
    return items


def main():
    progress_path = BASE / "progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {}
    for role, ids in ROOTS.items():
        for rid in ids:
            out_path = BASE / f"{rid}.json"
            if out_path.exists() and progress.get(rid, {}).get("status") == "done":
                print(f"SKIP {rid}", flush=True)
                continue
            try:
                items = fetch_thread(rid)
                n = len(items)
                n_comments = sum(1 for v in items.values() if v.get("type") == "comment")
                payload = {"root_id": int(rid), "role": role,
                           "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "method": "GET https://hacker-news.firebaseio.com/v0/item/<id>.json via curl (16-way parallel), recursive over kids",
                           "item_count": n, "comment_count": n_comments,
                           "items": items}
                out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                prov = (f"source URL: https://hacker-news.firebaseio.com/v0/item/{rid}.json "
                        f"(recursive over kids)\n"
                        f"retrieval time (UTC): {payload['fetched_at_utc']}\n"
                        f"method: public HN Firebase item API, GET via curl, no login, no POST\n"
                        f"poster-identity field stripped before writing per lane brief; "
                        f"all other item bytes verbatim\n")
                (BASE / f"{rid}.PROVENANCE.txt").write_text(prov)
                h = hashlib.sha256(out_path.read_bytes()).hexdigest()
                (BASE / f"{rid}.sha256").write_text(f"{h}  {rid}.json\n")
                progress[rid] = {"status": "done", "role": role,
                                 "item_count": n, "comment_count": n_comments,
                                 "fetched_at_utc": payload["fetched_at_utc"]}
                progress_path.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")
                print(f"OK {rid} role={role} items={n} comments={n_comments}", flush=True)
            except Exception as e:  # noqa: BLE001
                progress[rid] = {"status": "failed", "role": role, "error": str(e)[:300]}
                progress_path.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")
                print(f"FAIL {rid}: {e}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
