#!/usr/bin/env python3
"""Explicit-events re-explosion for the university-shorteners family.

Christopher's explicit-events rule: no consolidation in primary indexes.
Every observable event is its own doc. This script re-explodes the
consolidated university-shorteners material (raw stats captures) into
one JSON doc per event:

  - yourls_referrer_url : one doc per referrer-URL row of a YOURLS
                          "Traffic sources" table (host + full URL + hits)
  - yourls_daily_hits   : one doc per (stats page, date) daily-hits point
  - yourls_country_hits : one doc per (stats page, country) location row
  - yourls_stats_page   : one doc per stats-page observation (page-level
                          fields as observed at capture time — the parent
                          observation of the row docs, not a cross-page
                          rollup)

Offline partial reconstruction only (1,520 rows from the September 28 raw
captures; the canonical 1,591-row events.jsonl also includes 71 Common Crawl
and Wayback rows). It MUST NOT be regenerated from these original captures.
Use --output with a new, distinct path; existing
files (including the canonical file) are never overwritten. This tool does not
update PROVENANCE.md or SHA256SUMS.

The JSONL is directly loadable by the local-push script: one JSON doc
per line, shared-schema top-level fields only
(notes/gems-es-mapping.json), dataset-specific info in `labels`
(flattened), deterministic labels.event_id for idempotent loads.

Read-only: parses existing evidence files; no live fetching.
"""
import argparse
import json, os, re, hashlib
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUTDIR = os.path.join(BASE, "data", "2026-05-12-university-shorteners-events")
OUT = os.path.join(OUTDIR, "events.jsonl")

INSTANCES = {
    "goto.unm.edu":   {"org": "University of New Mexico", "scope": "university"},
    "u.ethz.ch":      {"org": "ETH Zürich",               "scope": "university"},
    "go.uvm.edu":     {"org": "University of Vermont",    "scope": "university"},
    "url.popcat.xyz": {"org": "popcat.xyz",               "scope": "community"},
}

OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}
def sha12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_month_day_year(s, default_year=None):
    # "Mar 22, 2023" / "Mar 27" (+year) -> ISO date
    s = s.strip()
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%b %d", "%B %d"):
        try:
            dt = datetime.strptime(s, fmt)
            if "%Y" not in fmt:
                dt = dt.replace(year=default_year or 2026)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def base_doc(instance, slug, source_url, retrieved_at, evidence_file, record_kind,
             event_id, description, matched_string, note, extra_labels, tags):
    meta = INSTANCES[instance]
    labels = {
        "shortener.instance": instance,
        "shortener.org": meta["org"],
        "shortener.scope": meta["scope"],
        "short_url": "https://%s/%s" % (instance, slug),
        "source_stats_url": source_url,
        "event_id": event_id,
        "granularity": "event",
    }
    labels.update(extra_labels)
    if isinstance(labels.get("best_day"), dict):
        best_day = labels.pop("best_day")
        labels.update({"best_day." + key: value for key, value in best_day.items()})
    return {
        "@timestamp": retrieved_at,
        "description": description,
        "event": {"created": retrieved_at, "dataset": "2026-05-12-university-shorteners"},
        "file": os.path.relpath(evidence_file, BASE),
        "fingerprint": hashlib.sha256(event_id.encode("utf-8")).hexdigest(),
        "labels": labels,
        "matched_string": matched_string,
        "note": note,
        "observer": OBSERVER,
        "record_kind": record_kind,
        "retrieved_at": retrieved_at,
        "retrieved_via": "offline re-parse of archived raw stats capture (read-only; hosted-Elastic writes paused)",
        "sha256": file_sha256(evidence_file),
        "size_bytes": os.path.getsize(evidence_file),
        "source_url": source_url,
        "status": "archived-capture",
        "tags": tags,
    }


def scope_tag(instance):
    return "scope:" + INSTANCES[instance]["scope"]


# ---------------------------------------------------------------- main JSONs
def explode_referrer_json(path):
    """The *_referrer_urls_daily_*.json captures (5 pages)."""
    docs = []
    d = json.load(open(path))
    slug = d["slug"]
    source_url = d["source_url"]
    retrieved_at = d["retrieved_at"]
    instance = source_url.split("//")[1].split("/")[0]
    tags = ["yourls", "public-stats", "explicit-event", "read-only", scope_tag(instance)]

    # 1) one doc per referrer-URL row. The offline extraction occasionally
    # lists the same (host, url) twice (91 dup pairs, 11 with differing
    # hit counts) — keep every occurrence as its own event doc with a
    # distinct event_id rather than silently dropping data.
    from collections import Counter as _Counter
    occ_total = _Counter()
    for h in d.get("referrer_hosts", []):
        for u in h.get("urls", []):
            occ_total[(h.get("host"), u.get("url"))] += 1
    occ_seen = _Counter()
    for h in d.get("referrer_hosts", []):
        host = h.get("host")
        for u in h.get("urls", []):
            url, hits = u.get("url"), u.get("hits")
            occ_seen[(host, url)] += 1
            n = occ_seen[(host, url)]
            suffix = ":dup%d" % n if occ_total[(host, url)] > 1 else ""
            eid = "yourls:%s:%s:refurl:%s%s" % (instance, slug, sha12(url or ""), suffix)
            extra = {"record": "referrer_url", "referrer_host": host,
                     "referrer_url": url, "hits": hits,
                     "host_total_hits": h.get("total_hits"),
                     "host_url_count": h.get("url_count")}
            if suffix:
                extra["occurrence_note"] = (
                    "extraction lists this (host, url) %d times with hit counts %s; "
                    "this doc is occurrence %d of %d" % (
                        occ_total[(host, url)],
                        [x.get("hits") for x in
                         [uu for hh in d.get("referrer_hosts", []) for uu in hh.get("urls", [])
                          if hh.get("host") == host and uu.get("url") == url]],
                        n, occ_total[(host, url)]))
            docs.append(base_doc(
                instance, slug, source_url, retrieved_at, path,
                "yourls_referrer_url", eid,
                "YOURLS referrer URL row: %s — %d hit(s) on %s stats page" % (host, hits, slug),
                url, "One row of the YOURLS 'Traffic sources' table as observed "
                     "in the archived stats capture. Explicit event; not aggregated.",
                extra, tags))

    # 2) one doc per daily-hits point
    for series, key, note in (("all_time", "daily_all_time",
                               "YOURLS all-time daily series is decimated (~6-week sampling); zero-hit days included"),
                              ("last_30", "daily_last_30", "Full-resolution last-30-days daily series")):
        for row in d.get(key, []) or []:
            date_raw = row.get("date")
            iso = parse_month_day_year(date_raw)
            eid = "yourls:%s:%s:day:%s:%s" % (instance, slug, series, iso or sha12(date_raw or ""))
            docs.append(base_doc(
                instance, slug, source_url, retrieved_at, path,
                "yourls_daily_hits", eid,
                "YOURLS daily hits: %s — %d hit(s) (%s series)" % (date_raw, row.get("hits"), series),
                "%s %d" % (date_raw, row.get("hits")),
                "One point of the YOURLS daily-hits chart as observed. " + note,
                {"record": "daily_hits", "date_raw": date_raw, "date": iso,
                 "hits": row.get("hits"), "series": series, "series_note": note},
                tags))

    # 3) one page-observation doc (parent of the rows, not a cross-page rollup)
    eid = "yourls:%s:%s:page:%s" % (instance, slug, retrieved_at[:10])
    docs.append(base_doc(
        instance, slug, source_url, retrieved_at, path,
        "yourls_stats_page", eid,
        "YOURLS stats page observed: https://%s/%s (capture %s)" % (instance, slug, retrieved_at),
        "https://%s/%s" % (instance, slug),
        "Page-level observation as captured (long URL, creation date, best day). "
        "Parent record of the per-row event docs from the same capture.",
        {"record": "page_observation", "long_url": d.get("long_url"),
         "created_raw": d.get("created"), "best_day": d.get("best_day"),
         "referrer_host_count": len(d.get("referrer_hosts", [])),
         "referrer_url_rows": sum(len(h.get("urls", [])) for h in d.get("referrer_hosts", []))},
        tags))
    return docs


# ---------------------------------------------------------------- vbudg (txt)
def explode_vbudg_txt(path):
    docs = []
    txt = open(path).read()
    instance, slug = "goto.unm.edu", "vbudg"
    source_url = "https://goto.unm.edu/vbudg+"
    retrieved_at = "2026-09-28T09:05:00Z"  # "2026-09-28 ~04:05 CDT"
    tags = ["yourls", "public-stats", "explicit-event", "read-only", scope_tag(instance)]
    long_url = re.search(r"Long URL: (\S+)", txt).group(1)
    created = re.search(r"CREATED: (.+)", txt).group(1).strip()

    # referrer row
    m = re.search(r"REFERRERS.*?\n(\S.*): (\d+)\n", txt, re.S)
    if m:
        ref, hits = m.group(1).strip(), int(m.group(2))
        eid = "yourls:%s:%s:refurl:%s" % (instance, slug, sha12(ref))
        docs.append(base_doc(
            instance, slug, source_url, retrieved_at, path, "yourls_referrer_url", eid,
            "YOURLS referrer row: %s — %d hit(s) (control page)" % (ref, hits),
            ref, "Control page: 4 hits all-time, one internal referrer, zero agent markers.",
            {"record": "referrer_url", "referrer_host": ref, "referrer_url": ref,
             "hits": hits, "control_page": True}, tags))
    # daily rows from "(daily series: Mar 27: 2, Mar 28: 1, Apr 01: 1)"
    m = re.search(r"daily series: ([^)]+)\)", txt)
    if m:
        for part in m.group(1).split(","):
            dm, hv = [x.strip() for x in part.split(":")]
            iso = parse_month_day_year(dm, default_year=2025)
            eid = "yourls:%s:%s:day:control:%s" % (instance, slug, iso)
            docs.append(base_doc(
                instance, slug, source_url, retrieved_at, path, "yourls_daily_hits", eid,
                "YOURLS daily hits: %s — %s hit(s) (control page)" % (dm, hv),
                "%s %s" % (dm, hv), "Control-page daily point.",
                {"record": "daily_hits", "date_raw": dm, "date": iso,
                 "hits": int(hv), "series": "control"}, tags))
    # page observation
    alltime = int(re.search(r"ALL TIME (\d+) hits?", txt).group(1))
    eid = "yourls:%s:%s:page:2026-09-28" % (instance, slug)
    docs.append(base_doc(
        instance, slug, source_url, retrieved_at, path, "yourls_stats_page", eid,
        "YOURLS stats page observed: control page vbudg (4 hits all-time)",
        "https://goto.unm.edu/vbudg",
        "Control page — zero agent-toolkit markers; agent traffic concentrates on other slugs.",
        {"record": "page_observation", "long_url": long_url, "created_raw": created,
         "all_time_hits": alltime, "control_page": True}, tags))
    return docs


# ---------------------------------------------------------------- UVM (txt)
def explode_uvm_txt(path, slug):
    docs = []
    txt = open(path).read()
    instance = "go.uvm.edu"
    source_url = "https://go.uvm.edu/%s+" % slug
    retrieved_at = "2026-09-28T11:40:00Z"  # "2026-09-28 ~06:40 CDT"
    tags = ["yourls", "public-stats", "explicit-event", "read-only", scope_tag(instance),
            "referrers-owner-only"]
    long_url = re.search(r"Long URL: (\S+)", txt).group(1)
    created = re.search(r"CREATED: (.+)", txt).group(1).strip()
    alltime = int(re.search(r"ALL TIME (\d+) hits?", txt).group(1))
    best = re.search(r"BEST DAY: (.+)", txt).group(1).strip()

    # country rows
    m = re.search(r"LOCATION: (.+)", txt)
    if m:
        for part in m.group(1).split(","):
            part = part.strip().rstrip(".")
            cm = re.match(r"([A-Z]{2}): (\d+)", part)
            if not cm:
                continue
            cc, hits = cm.group(1), int(cm.group(2))
            eid = "yourls:%s:%s:country:%s" % (instance, slug, cc)
            docs.append(base_doc(
                instance, slug, source_url, retrieved_at, path, "yourls_country_hits", eid,
                "YOURLS location row: %s — %d hit(s) on %s" % (cc, hits, slug),
                "%s %d" % (cc, hits),
                "One row of the YOURLS 'Traffic location' table. Referrers are "
                "owner-only on this instance, so no referrer rows exist.",
                {"record": "country_hits", "country": cc, "hits": hits}, tags))
    # page observation
    eid = "yourls:%s:%s:page:2026-09-28" % (instance, slug)
    docs.append(base_doc(
        instance, slug, source_url, retrieved_at, path, "yourls_stats_page", eid,
        "YOURLS stats page observed: UVM %s (%d hits all-time; referrers owner-only)" % (slug, alltime),
        "https://go.uvm.edu/%s" % slug,
        "Control venue: public stats expose traffic + location only; "
        "'Traffic Sources' (referrers) requires NetID login per UVM KB.",
        {"record": "page_observation", "long_url": long_url, "created_raw": created,
         "all_time_hits": alltime, "best_day": best,
         "referrers": "owner-only-not-exposed", "control_page": True}, tags))
    return docs


# ---------------------------------------------------------------- popcat (txt)
def explode_popcat_txt(path, code):
    txt = open(path).read()
    instance = "url.popcat.xyz"
    source_url = "https://url.popcat.xyz/%s/info" % code
    retrieved_at = "2026-09-28T04:40:00Z"  # "2026-09-28 ~04:40 UTC"
    tags = ["yourls", "public-stats", "explicit-event", "read-only", scope_tag(instance)]
    target = re.search(r"Redirects to: (\S+)", txt).group(1)
    clicks = int(re.search(r"Clicks: (\d+)", txt).group(1))
    eid = "yourls:%s:%s:page:2026-09-28" % (instance, code)
    return [base_doc(
        instance, code, source_url, retrieved_at, path, "yourls_stats_page", eid,
        "Shortener info page observed: %s — %d clicks, redirects to %s" % (code, clicks, target),
        "https://url.popcat.xyz/%s" % code,
        "Community shortener still serving agent-planted redirect to a ChatGPT conversation.",
        {"record": "page_observation", "long_url": target, "clicks": clicks}, tags)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True,
                        help="New offline JSONL path; must not exist or be the canonical file")
    args = parser.parse_args(argv)
    output = os.path.abspath(args.output)
    if os.path.realpath(output) == os.path.realpath(OUT):
        parser.error("refusing canonical events.jsonl: partial reconstruction would lose later captures")
    if os.path.lexists(output):
        parser.error("output already exists; refusing to overwrite")
    if not os.path.isdir(os.path.dirname(output)):
        parser.error("output parent directory does not exist")
    docs = []
    # 5 rich JSON captures
    for f in sorted(os.listdir(os.path.join(BASE, "data", "2026-09-28-university-shorteners", "raw", "goto-unm-edu"))):
        if f.endswith("_referrer_urls_daily_2026-09-28.json"):
            docs += explode_referrer_json(os.path.join(BASE, "data", "2026-09-28-university-shorteners", "raw", "goto-unm-edu", f))
    docs += explode_referrer_json(os.path.join(BASE, "data", "2026-09-28-university-shorteners", "raw", "u-ethz-ch",
                                               "nB1nv_referrer_urls_daily_2026-09-28.json"))
    # vbudg control
    docs += explode_vbudg_txt(os.path.join(BASE, "data", "2026-09-28-university-shorteners-batch2", "raw", "goto-unm-edu",
                                          "vbudg_stats_2026-09-28.txt"))
    # UVM controls
    for slug in ("-4s0q", "tgmtq", "xc26"):
        docs += explode_uvm_txt(os.path.join(BASE, "data", "2026-09-28-university-shorteners-batch3", "raw", "go-uvm-edu",
                                             "%s_stats_2026-09-28.txt" % slug), slug)
    # popcat
    for code in ("5vtSk2RG2f", "IRZTIxDlZ"):
        docs += explode_popcat_txt(os.path.join(BASE, "data", "2026-09-28-university-shorteners", "raw", "url-popcat-xyz",
                                                "%s_info_2026-09-28.txt" % code), code)

    # dedupe on event_id (keep first)
    seen, uniq = set(), []
    for d in docs:
        eid = d["labels"]["event_id"]
        if eid not in seen:
            seen.add(eid)
            uniq.append(d)

    # schema check: top-level fields must be in the shared mapping
    allowed = set(json.load(open(os.path.join(BASE, "notes", "gems-es-mapping.json")))["mappings"]["properties"])
    bad = set()
    for d in uniq:
        bad |= (set(d.keys()) - allowed)
    assert not bad, "unexpected top-level fields: %s" % bad

    with open(output, "x", encoding="utf-8") as f:
        for d in uniq:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    # counts by record_kind
    from collections import Counter
    kinds = Counter(d["record_kind"] for d in uniq)
    print("wrote %d partial-reconstruction docs to %s" % (len(uniq), output))
    for k, n in sorted(kinds.items()):
        print("  %-22s %d" % (k, n))


if __name__ == "__main__":
    main()
