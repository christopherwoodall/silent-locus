import json, re, time, urllib.request, urllib.error, urllib.parse

def fetch(q):
    url = "https://urlquery.net/api/htmx/search/?q=" + urllib.parse.quote(q) + "&limit=100&offset=0"
    cur = "https://urlquery.net/search?q=" + urllib.parse.quote(q)
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "swarmtraces-hunt/fresh-check", "HX-Current-URL": cur})
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)

QUERIES = [
    "url.domain:amap.com date:[2026-10-13 TO 2026-10-14]",
    "url.domain:gaode.com date:[2026-10-13 TO 2026-10-14]",
    "uqscan= date:[2026-10-13 TO 2026-10-14]",
]
for q in QUERIES:
    status, body = fetch(q)
    uuids = sorted(set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", body)))
    dates = sorted(set(re.findall(r"2026-10-1[3-4]T\d{2}:\d{2}:\d{2}Z", body)))
    open("q_" + re.sub(r"\W+", "_", q)[:40] + ".html", "w").write(body)
    print(f"q={q!r}\n  status={status} bytes={len(body)} uuids={len(uuids)} dates={dates[:8]}")
    time.sleep(5)
