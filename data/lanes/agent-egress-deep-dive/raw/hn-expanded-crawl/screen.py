#!/usr/bin/env python3
"""Screen fetched HN captures into a review table.

Reads every *--story.json / *--comment.json capture in this dir, dedups
by HN id, and flags rows by literal-term presence and shape keywords.
Output: screening.tsv + screening.json in this dir (working files, not
raw captures). No poster handles are read or written: the capture files
already have the author field removed.
Signed-URL safety: snippets in the screening output cut any URL at the
first '?' so no signed query string, signature, or token is copied.
Only parameter names and path shape are noted separately by the reviewer.
"""
import json, os, re, glob, html

OUT = os.path.dirname(os.path.abspath(__file__))
KNOWN = {49379079, 49535519, 49429926, 46622328, 48349487, 48827858,
         48272354, 47190721, 46403097, 48052629, 49605924, 48414158,
         50249935, 48916975, 47541805, 50165308, 48838376, 50246658}

SHAPE_PATTERNS = {
    "meta-addr": r"169\.254\.169\.254|100\.100\.100\.200|metadata\.google\.internal|fd00:ec2::254|168\.63\.129\.16",
    "unshare-flag": r"unshare\s+(-[Urmc]+|--user|--map-[a-z-]+user)",
    "routify": r"routify",
    "aliyuncs": r"aliyuncs",
    "sanmaohe": r"sanmaohe",
    "proxy-temp": r"proxy_temp_file",
    "dl-exec": r"(curl\s+-o|wget\s+-O).{0,120}(run|exec|chmod\s+\+x|sh\b|bash\b)|\bdownload.{0,40}(then|and).{0,40}(run|execut)",
    "exfil": r"exfiltrat",
    "called-home": r"called home|call home|phoning home",
    "model-fetched": r"model (fetched|fetch|downloaded|called)|fetched (a |an |the )?url|hallucinat\w* url|signed url",
    "agent-words": r"\bagent\b|\bmodel\b|\bllm\b|claude|qwen|gpt|cursor|harness|sandbox",
}

def clean_text(s):
    if not s:
        return ""
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).strip()

def strip_url_params(s):
    # Cut every URL at '?' so no signed query string survives in notes.
    return re.sub(r"(https?://\S+?)\?\S*", r"\1[query-stripped]", s)

def main():
    rows = {}
    coverage = {}
    for path in sorted(glob.glob(os.path.join(OUT, "*--story.json")) +
                       glob.glob(os.path.join(OUT, "*--comment.json"))):
        cap = json.load(open(path))
        label, tag = cap["term_label"], cap["tag"]
        coverage[f"{label}:{tag}"] = {
            "file": os.path.basename(path),
            "queries": cap["queries"],
            "top_totals": cap["top_range_reported_totals"],
            "splits": len(cap["date_splits"]),
            "capped_despite_splits": cap["capped_despite_splits"],
            "fetched": cap["fetched_count"],
        }
        for h in cap["hits"]:
            oid = int(h["objectID"])
            title = clean_text(h.get("title") or h.get("story_title") or "")
            body = clean_text(h.get("story_text") or h.get("comment_text") or "")
            text = (title + " " + body).strip()
            entry = rows.setdefault(oid, {
                "id": oid, "type": None, "date": h.get("created_at", "")[:10],
                "title": title, "terms": [], "flags": [], "text_len": len(text),
                "overlap_known": oid in KNOWN,
            })
            entry["terms"].append(f"{label}:{tag}")
            if tag == "story":
                entry["type"] = "story"
            elif entry["type"] is None:
                entry["type"] = "comment"
            low = text.lower()
            for name, pat in SHAPE_PATTERNS.items():
                if re.search(pat, low) and name not in entry["flags"]:
                    entry["flags"].append(name)
            # literal presence per term query (client-side exact check)
            for q in cap["queries"]:
                if q.lower() in low and f"lit:{q}" not in entry["terms"]:
                    entry["terms"].append(f"lit:{q}")
            entry["_text"] = text
    # Write screening table (snippets only, URL params stripped)
    out_rows = []
    for oid, e in sorted(rows.items()):
        text = e.pop("_text")
        snippet = strip_url_params(text)[:600]
        out_rows.append({**e, "snippet": snippet, "n_terms": len(e["terms"])})
    with open(os.path.join(OUT, "screening.json"), "w") as f:
        json.dump({"coverage": coverage, "unique_ids": len(out_rows),
                   "rows": out_rows}, f, indent=1)
    with open(os.path.join(OUT, "screening.tsv"), "w") as f:
        f.write("id\ttype\tdate\ttitle\tflags\toverlap_known\tterms\tsnippet\n")
        for r in out_rows:
            f.write("\t".join([
                str(r["id"]), r["type"] or "", r["date"],
                r["title"].replace("\t", " ")[:200],
                ",".join(r["flags"]), str(r["overlap_known"]),
                ",".join(r["terms"]),
                r["snippet"].replace("\t", " ").replace("\n", " "),
            ]) + "\n")
    print(f"unique ids: {len(out_rows)}")
    print(f"coverage rows: {len(coverage)}")
    from collections import Counter
    print("flag counts:", dict(Counter(fl for r in out_rows for fl in r["flags"])))
    print("overlap ids present:", sorted(r["id"] for r in out_rows if r["overlap_known"]))

if __name__ == "__main__":
    main()
