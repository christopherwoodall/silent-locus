#!/usr/bin/env python3
"""Under-farmed engine dork sweep: Bing, Brave, Mojeek, Marginalia.

Status after probing (2026-10-04):
- Bing: anti-bot decoy SERPs (same query -> different unrelated results). UNUSABLE.
- Brave: HTTP 429 on first request. HARD STOP.
- Mojeek: JS CAPTCHA challenge. BLOCKED.
- Marginalia (old-search.marginalia.nu): JS wait gate, passable via sst token +
  Referer header. Flaky/adaptive. Attempt all dorks with gentle pacing.

Only Marginalia is attempted here. Results -> /tmp/engine_dorks_results.jsonl
"""
import json, re, subprocess, time, urllib.parse, os

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://old-search.marginalia.nu"
CJ = "/tmp/marg_cj.txt"
OUT = "/tmp/engine_dorks_results.jsonl"

DORKS = [
    '"uqscan="',
    '"uqcors.html"',
    '"uqtag="',
    '"sub_poi_navi"',
    'is.gd "uqscan"',
    'is.gd "?x="',
    'lhr.life "probe.html"',
    'lhr.life "uqcors"',
    '"mark=" "validation=v" "TimeTrendData"',
    '"AGE115EXTRACT1"',
    '"MassCountyData"',
]


def curl(url, referer=None, timeout=30):
    cmd = ["curl", "-sL", "-A", UA, "--max-time", str(timeout),
           "-c", CJ, "-b", CJ, "-w", "\n%{http_code}", url]
    if referer:
        cmd[1:1] = ["-H", f"Referer: {referer}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body


def parse_results(body):
    """Returns (status, count, urls, titles)."""
    if "Wait For A Moment" in body:
        return "challenged", None, [], []
    if re.search(r"No search results found|Showing 0 search results", body):
        return "ok", 0, [], []
    m = re.search(r"Showing\s+(\d+)\s+search results", body)
    count = int(m.group(1)) if m else None
    # isolate results section
    i = body.find('id="results"')
    seg = body[i:] if i > 0 else body
    # result links: absolute http(s) hrefs, not marginalia itself, not /search? filters
    urls, titles = [], []
    for hm, tm in re.findall(
            r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', seg, re.S):
        if "marginalia" in hm:
            continue
        t = re.sub(r"<[^>]+>", "", tm)
        t = re.sub(r"\s+", " ", t).strip()
        if hm not in urls:
            urls.append(hm)
            titles.append(t[:160])
    return "ok", count, urls, titles


def marg_search(query):
    wait_url = BASE + "/search?query=" + urllib.parse.quote(query)
    code, body = curl(wait_url)
    if code != "200":
        return "error", None, [], [f"wait page http {code}"]
    m = re.search(r"location\.replace\('([^']+)'\)", body)
    if not m:
        # maybe results came back directly
        return parse_results(body)
    token_url = BASE + m.group(1)
    time.sleep(8)
    code2, body2 = curl(token_url, referer=wait_url)
    st, count, urls, titles = parse_results(body2)
    if st == "challenged":
        # one retry with fresh token
        m2 = re.search(r"location\.replace\('([^']+)'\)", body2)
        if not m2:
            return "blocked", None, [], ["challenge, no token"]
        time.sleep(6)
        code3, body3 = curl(BASE + m2.group(1), referer=wait_url)
        st, count, urls, titles = parse_results(body3)
        if st == "challenged":
            return "blocked", None, [], ["challenge persisted after retry"]
    return st, count, urls, titles


def main():
    if os.path.exists(CJ):
        os.remove(CJ)
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["query"])
                except Exception:
                    pass
    for qi, q in enumerate(DORKS):
        if q in done:
            print(f"  skip (done): {q}", flush=True)
            continue
        st, count, urls, titles = marg_search(q)
        row = {
            "engine": "marginalia",
            "query": q,
            "status": st,
            "hits": count if count is not None else len(urls),
            "urls": urls[:25],
            "titles": titles[:25],
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with open(OUT, "a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"[{qi+1}/{len(DORKS)}] {q!r}: {st} hits={row['hits']}",
              flush=True)
        time.sleep(20)  # gentle: marginalia asks bots not to barrage
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
