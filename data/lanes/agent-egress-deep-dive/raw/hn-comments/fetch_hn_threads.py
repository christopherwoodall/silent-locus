#!/usr/bin/env python3
"""Fetch HN threads via the public Firebase item API, idempotent.

Lane rule (task brief, overrides the repo-wide never-redact rule for one
field only): the poster-identity field is stripped from every stored item
before writing, and is never printed. All other bytes are kept verbatim.
Signed query strings, if present inside comment text, stay in the raw
capture only; the working note must carry parameter names and path shape
only, never copied signed values.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOTS = {
    # role: [ids] -- each id gets its own capture file (item + descendants)
    "ranked": ["49535519", "49429926", "46622328", "46624950"],
    "appendix": ["48349487", "48827858"],
    "context": ["50246658"],
    "killed": ["48272354", "47190721", "46403097", "48052629", "49605924",
               "48414158", "50249935", "48916975", "47541805", "50165308",
               "48838376"],
}
# Extra parent fetches (context only, stored inside the child's capture):
PARENTS = {"49535519": "49535276"}


def fetch_item(item_id):
    out = subprocess.run(
        ["curl", "-sS", "--max-time", "60",
         f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed for {item_id}: {out.stderr[:200]}")
    if not out.stdout.strip() or out.stdout.strip() == "null":
        return None
    return json.loads(out.stdout)


def clean(item):
    item = dict(item)
    item.pop("by", None)  # lane rule: no poster identity stored or printed
    return item


def fetch_thread(root_id):
    items = {}
    queue = [root_id]
    parent_id = PARENTS.get(root_id)
    if parent_id:
        queue.append(parent_id)
    seen = set()
    while queue:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        item = fetch_item(cur)
        if item is None:
            items[cur] = {"id": int(cur), "missing": True}
            continue
        items[cur] = clean(item)
        for kid in item.get("kids") or []:
            if str(kid) not in seen:
                queue.append(str(kid))
    return items


def main():
    progress_path = BASE / "progress.json"
    progress = {}
    if progress_path.exists():
        progress = json.loads(progress_path.read_text())
    force = "--force" in sys.argv
    for role, ids in ROOTS.items():
        for rid in ids:
            out_path = BASE / f"{rid}.json"
            if out_path.exists() and not force and progress.get(rid, {}).get("status") == "done":
                print(f"SKIP {rid} (already captured)")
                continue
            try:
                items = fetch_thread(rid)
                n = len(items)
                n_comments = sum(1 for v in items.values() if v.get("type") == "comment")
                payload = {"root_id": int(rid), "role": role,
                           "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "method": "GET https://hacker-news.firebaseio.com/v0/item/<id>.json via curl, recursive over kids",
                           "item_count": n, "comment_count": n_comments,
                           "items": items}
                out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                prov = (f"source URL: https://hacker-news.firebaseio.com/v0/item/{rid}.json "
                        f"(recursive over kids; parent also fetched for 49535519)\n"
                        f"retrieval time (UTC): {payload['fetched_at_utc']}\n"
                        f"method: public HN Firebase item API, GET via curl, no login, no POST\n"
                        f"poster-identity field stripped before writing per lane brief; "
                        f"all other item bytes verbatim\n")
                (BASE / f"{rid}.PROVENANCE.txt").write_text(prov)
                import hashlib
                h = hashlib.sha256(out_path.read_bytes()).hexdigest()
                (BASE / f"{rid}.sha256").write_text(f"{h}  {rid}.json\n")
                progress[rid] = {"status": "done", "role": role,
                                 "item_count": n, "comment_count": n_comments,
                                 "fetched_at_utc": payload["fetched_at_utc"]}
                progress_path.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")
                print(f"OK {rid} role={role} items={n} comments={n_comments}")
            except Exception as e:  # noqa: BLE001 - record failure, keep going
                progress[rid] = {"status": "failed", "role": role, "error": str(e)[:300]}
                progress_path.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")
                print(f"FAIL {rid}: {e}")
    print("DONE")


if __name__ == "__main__":
    main()
