"""July-7 forensics payload extraction (by inspection only, never executed).

Reads raw Diffend captures from data/july7-gem-forensics/raw/, strips HTML tags,
unescapes entities, and extracts full text lines containing web-mechanism
markers. Output: data/july7-gem-forensics/payload-reconstructions.jsonl
(one record per gem/version capture with full payload strings).
"""
import os, re, json, html as htmlmod

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(PROJ, "data", "july7-gem-forensics", "raw")
OUT = os.path.join(PROJ, "data", "july7-gem-forensics",
                   "payload-reconstructions.jsonl")

MARKERS = [
    ("xss-script", re.compile(r"<script", re.I)),
    ("xss-onerror", re.compile(r"onerror\s*=", re.I)),
    ("xss-onload", re.compile(r"onload\s*=", re.I)),
    ("oast", re.compile(r"oast\.online", re.I)),
    ("webhook-site", re.compile(r"webhook\.site", re.I)),
    ("xss-alert", re.compile(r"alert\s*\(", re.I)),
    ("xss-js-uri", re.compile(r"javascript\s*:", re.I)),
    ("xss-svg", re.compile(r"<svg", re.I)),
    ("xss-img", re.compile(r"<img", re.I)),
    ("ssti-erb", re.compile(r"<%=\s*7\s*\*\s*7\s*%>", re.I)),
    ("ssti-erb-pct", re.compile(r"<%25=\s*7\s*\*\s*7\s*%>", re.I)),
    ("ssti-el", re.compile(r"\$\{\s*7\s*\*\s*7\s*\}", re.I)),
    ("ssti-jinja", re.compile(r"\{\{\s*7\s*\*\s*7\s*\}\}", re.I)),
    ("data-controller", re.compile(r"data-controller", re.I)),
    ("mathml", re.compile(r"<math", re.I)),
    ("metadata-field", re.compile(
        r"(summary|description|authors?|homepage|email)\s*[:=]", re.I)),
]

DIFFEND_CHROME = re.compile(
    r"Diffend|my\.diffend\.io|Compare|versions|View on|rubygems\.org/gems",
    re.I)


def text_lines(path):
    raw = open(path, "rb").read()
    h = raw.decode("utf-8", "ignore")
    # Diffend diff pages embed the file content as escaped text; unwrap twice.
    text = htmlmod.unescape(htmlmod.unescape(
        re.sub(r"<[^>]+>", "\n", h)))
    lines = []
    for ln in text.split("\n"):
        ln = re.sub(r"\s+", " ", ln).strip()
        if ln and len(ln) > 2:
            lines.append(ln)
    return lines


def classify(lines):
    hits = []
    for ln in lines:
        labels = [lab for lab, rx in MARKERS if rx.search(ln)]
        if labels and not DIFFEND_CHROME.search(ln):
            hits.append({"line": ln[:4000], "markers": labels})
    return hits


def main():
    recs = []
    for fn in sorted(os.listdir(RAW)):
        if fn.endswith(".html") and "__" in fn:
            name, rest = fn.split("__", 1)
            version = rest[:-5]
        elif fn.endswith(".html"):
            name, version = fn[:-5], "INDEX"
        else:
            continue
        lines = text_lines(os.path.join(RAW, fn))
        hits = classify(lines)
        recs.append({
            "gem": name,
            "version": version,
            "source_file": "raw/" + fn,
            "text_lines_scanned": len(lines),
            "payload_lines": hits,
            "payload_line_count": len(hits),
        })
    with open(OUT, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    with_markers = sum(1 for r in recs if r["payload_line_count"] > 0)
    print("captures: %d  with payload lines: %d" % (len(recs), with_markers))
    for r in recs:
        if r["payload_line_count"]:
            print("%s %s -> %d lines" % (r["gem"], r["version"],
                                         r["payload_line_count"]))


if __name__ == "__main__":
    main()
