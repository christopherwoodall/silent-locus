#!/usr/bin/env python3
"""Fetch current revision (content, timestamp, user, comment, tags) for every
distinct page in hits-literal.json, paced >=5s, then emit grading input.
Cache: raw/incubator.wikimedia.org/revfetch-<pageid>.json
"""
import json, os, subprocess, time, urllib.parse, datetime

API = "https://incubator.wikimedia.org/w/api.php"
SWEEP = "raw/incubator.wikimedia.org"
PACE = 5.2

def curl_json(url):
    for attempt in (1, 2):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-w", "\n%{http_code}",
             "--compressed", url], capture_output=True, text=True)
        body, _, code = p.stdout.rpartition("\n")
        try:
            status = int(code.strip())
        except ValueError:
            status = 0
        if status == 200:
            try:
                return status, json.loads(body)
            except json.JSONDecodeError:
                return status, {"_raw": body[:1000]}
        time.sleep(15)
    return status, {"_error": True}

def main():
    recs = json.load(open(os.path.join(SWEEP, "hits-literal.json")))
    pages = {}
    for r in recs:
        pages[r["pageid"]] = r["title"]
    print(f"{len(pages)} distinct pages to fetch", flush=True)
    last = 0.0
    done = 0
    for pid, title in pages.items():
        out = os.path.join(SWEEP, f"revfetch-{pid}.json")
        if os.path.exists(out):
            done += 1
            continue
        wait = PACE - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
        last = time.time()
        params = {"action": "query", "prop": "revisions",
                  "pageids": str(pid), "rvprop": "ids|timestamp|user|comment|tags",
                  "rvslots": "main", "rvlimit": "1", "format": "json"}
        status, data = curl_json(API + "?" + urllib.parse.urlencode(params))
        with open(out, "w") as f:
            json.dump({"pageid": pid, "title": title, "http": status,
                       "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       "response": data}, f, ensure_ascii=False)
        done += 1
        if done % 20 == 0:
            print(f"  ...{done}/{len(pages)}", flush=True)
    print("done", flush=True)

if __name__ == "__main__":
    main()
