#!/usr/bin/env python3
"""Mechanical inventory builder for HN Collector C captures.

Reads the captured Algolia page arrays and writes TSV inventories.
No author names, no comment text, no judgement: item id, kind, title
(story title, or the parent story title for comments), date (UTC),
HN item URL, matched term/tag, source file, and parent story id.
"""
import json
import glob
import datetime
import os

OUT = os.path.dirname(os.path.abspath(__file__))

TERMS = ["model fetched", "hallucinated URL", "signed URL",
         "called home", "agent exfiltration", "model exfiltrated"]


def slug(term):
    return term.replace(" ", "_")


def clean(s):
    if s is None:
        return ""
    return str(s).replace("\t", " ").replace("\n", " ").replace("\r", " ").strip()


def rows_for(files, label):
    rows = []
    for f in files:
        base = os.path.basename(f)
        # filename form: <slug>__<tag>[__pre20251101].json
        stem = base[:-5]
        parts = stem.split("__")
        term = parts[0].replace("_", " ")
        tag = parts[1]
        pages = json.load(open(f))
        for pg in pages:
            for hit in pg.get("hits", []):
                oid = hit.get("objectID", "")
                kind = hit.get("_tags", [tag])[0] if hit.get("_tags") else tag
                title = hit.get("title") or hit.get("story_title") or ""
                ts = hit.get("created_at_i")
                date = (datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
                        if ts else "")
                rows.append([oid, kind, clean(title), date,
                             f"https://news.ycombinator.com/item?id={oid}",
                             term, tag, hit.get("story_id", "") or "", base])
    return rows


def write_tsv(path, rows):
    header = ["item_id", "kind", "title_or_story_title", "date_utc",
              "hn_url", "matched_term", "tag", "parent_story_id",
              "source_file"]
    with open(path, "w") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    return len(rows)


def main():
    filt = []
    for t in TERMS:
        for tag in ("story", "comment"):
            filt.extend(glob.glob(os.path.join(OUT, f"{slug(t)}__{tag}.json")))
    pre = []
    for t in TERMS:
        for tag in ("story", "comment"):
            pre.extend(glob.glob(os.path.join(OUT, f"{slug(t)}__{tag}__pre20251101.json")))
    n_c = write_tsv(os.path.join(OUT, "candidates-C.tsv"), rows_for(sorted(filt), "cand"))
    n_x = write_tsv(os.path.join(OUT, "context-pre20251101.tsv"), rows_for(sorted(pre), "ctx"))
    # unique ids + per-file date ranges for COVERAGE.md
    print(f"candidates rows={n_c} context rows={n_x}")
    for path in sorted(filt + pre):
        pages = json.load(open(path))
        hits = [h for p in pages for h in p["hits"]]
        ids = {h["objectID"] for h in hits}
        ts = [h["created_at_i"] for h in hits if h.get("created_at_i")]
        lo = datetime.datetime.utcfromtimestamp(min(ts)).isoformat() + "Z" if ts else "-"
        hi = datetime.datetime.utcfromtimestamp(max(ts)).isoformat() + "Z" if ts else "-"
        print(f"{os.path.basename(path)} hits={len(hits)} unique_ids={len(ids)} range={lo}..{hi}")
    all_ids = set()
    for path in filt:
        for p in json.load(open(path)):
            all_ids.update(h["objectID"] for h in p["hits"])
    print(f"candidates unique item ids across terms/tags: {len(all_ids)}")


if __name__ == "__main__":
    main()
