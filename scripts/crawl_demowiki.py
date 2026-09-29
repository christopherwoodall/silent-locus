#!/usr/bin/env python3
"""Read-only crawl of prowiki.org/demo/wiki.cgi (DemoWiki, the SIXTH swarm wiki).

Captures: RecentChanges feed (days=3650), page index (spx), and for every
edited page: current page HTML + history HTML. ~2s pacing, no writes.
Saves raw HTML under data/2021-10-30-demowiki/raw/ and parsed records to
data/2021-10-30-demowiki/demowiki_crawl.json.
"""
import os, re, json, time, hashlib, urllib.request
from datetime import datetime, timezone

BASE_URL = "https://prowiki.org/demo/wiki.cgi"
UA = "demowiki-research/1.0 (read-only research crawl; contact: research)"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "2021-10-30-demowiki")
RAW = OUT + "/raw"
NOW = datetime.now(timezone.utc).isoformat()


def fetch(path, name):
    url = BASE_URL + path
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        data = resp.read()
    fp = "%s/%s.html" % (RAW, name)
    with open(fp, "wb") as f:
        f.write(data)
    print("fetched %-40s %d bytes" % (name, len(data)))
    time.sleep(2.0)
    return data.decode("iso-8859-1", "replace"), fp, hashlib.sha256(data).hexdigest()


def parse_rc(t):
    """entries: (page_id, diff_rev, time_str, n_changes, summary, author)"""
    out = []
    day = None
    for m in re.finditer(r"<p><strong>(.*?)</strong></p>|<li>(.*?)</li>", t, re.S):
        if m.group(1):
            day = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            continue
        li = m.group(2)
        diff = re.search(r"diff=(\d+)&amp;id=([^&'\"]+)", li)
        page_m = re.search(r"wiki\.cgi\?([A-Za-z0-9_]+)' class='body'", li)
        txt = re.sub(r"<[^>]+>", "", li).strip()
        # author = last dotted token sequence / name at end
        author = None
        am = re.search(r"\.\s*\.\s*\.\s*(.+?)$", txt)
        if am:
            author = am.group(1).strip()
        summ = re.search(r"\[([^\]]+)\]", txt)
        tm = re.search(r"(\d{1,2}:\d{2})", txt)
        out.append({
            "rc_day": day,
            "page_id": page_m.group(1) if page_m else None,
            "diff_rev": int(diff.group(1)) if diff else None,
            "time_str": tm.group(1) if tm else None,
            "summary": summ.group(1) if summ else None,
            "author": author,
        })
    return out


def parse_history(t):
    revs = []
    for m in re.finditer(r"<li>(.*?)</li>", t, re.S):
        li = m.group(1)
        old = re.search(r"oldid=(\d+)", li)
        txt = re.sub(r"<[^>]+>", "", li).strip()
        revs.append({"rev": old.group(1) if old else None, "text": txt[:200]})
    return revs


def page_text(t):
    # crude: strip to body text between <hr> markers
    body = re.sub(r"(?s)^.*?<hr>\s*", "", t, count=1)
    body = re.sub(r"(?s)<hr>.*$", "", body)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:20000]


def main():
    import os
    os.makedirs(RAW, exist_ok=True)
    files = []
    rc_t, fp, sha = fetch("?action=browse&id=RecentChanges&days=3650", "recentchanges_days3650")
    files.append({"name": "recentchanges_days3650", "url": BASE_URL + "?action=browse&id=RecentChanges&days=3650",
                  "sha256": sha, "bytes": len(rc_t)})
    rc_entries = parse_rc(rc_t)
    spx_t, fp2, sha2 = fetch("?action=spx&lang=1", "pageindex_spx")
    files.append({"name": "pageindex_spx", "url": BASE_URL + "?action=spx&lang=1",
                  "sha256": sha2, "bytes": len(spx_t)})
    rss_t, fp3, sha3 = fetch("?action=browse&id=RecentChangesRss&days=3650", "recentchanges_rss")
    files.append({"name": "recentchanges_rss", "url": BASE_URL + "?action=browse&id=RecentChangesRss&days=3650",
                  "sha256": sha3, "bytes": len(rss_t)})

    pages = sorted({e["page_id"] for e in rc_entries if e["page_id"]})
    page_recs = []
    for pid in pages:
        t, fp, sha = fetch("?%s" % pid, "page_%s" % pid)
        files.append({"name": "page_%s" % pid, "url": BASE_URL + "?%s" % pid,
                      "sha256": sha, "bytes": len(t)})
        h, fph, shah = fetch("?action=history&id=%s" % pid, "history_%s" % pid)
        files.append({"name": "history_%s" % pid, "url": BASE_URL + "?action=history&id=%s" % pid,
                      "sha256": shah, "bytes": len(h)})
        page_recs.append({"page_id": pid, "body_text": page_text(t),
                          "body_sha256": hashlib.sha256(t.encode()).hexdigest(),
                          "history": parse_history(h)})
    crawl = {"crawled_at_utc": NOW, "wiki": "prowiki.org/demo/wiki.cgi",
             "rc_entries": rc_entries, "pages": page_recs, "files": files}
    with open(OUT + "/demowiki_crawl.json", "w") as f:
        json.dump(crawl, f, indent=1)
    print("pages:", len(pages), "| rc entries:", len(rc_entries))


if __name__ == "__main__":
    main()
