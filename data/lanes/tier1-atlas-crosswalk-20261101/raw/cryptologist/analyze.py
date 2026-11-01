#!/usr/bin/env python3
"""Shapes-only cryptology scan over atlas_*.bin captures.
NEVER prints token values, keys, query-string values, or full URLs with
credentials. Outputs: pattern counts, masked shapes, host names (public
board hosts from probe file are public endpoints, not secrets), query
parameter NAMES only, and SHA-256 fingerprints of candidate strings so a
cross-board match can be verified byte-for-byte without reproducing it.
"""
import glob, hashlib, json, os, re, sys
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qsl

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/general-hunt/raw/0/2026-11-01T114014Z")
OUT = os.path.expanduser("~/workspace/silent-locus/data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist")

def mask(s):
    # Keep structure, hide characters: letters->A, digits->9, others kept.
    out = []
    for ch in s:
        if ch.isalpha(): out.append('A')
        elif ch.isdigit(): out.append('9')
        else: out.append(ch)
    return ''.join(out)

def shape_of(s):
    # e.g. AAAA-9999-AAAA ; compress runs
    m = mask(s)
    return re.sub(r'A+', lambda x: f"A{len(x.group(0))}", m)

PATTERNS = {
    "uuid_hyphenated": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "uuid_hex32": re.compile(r"\b[0-9a-fA-F]{32}\b"),
    "hex40": re.compile(r"\b[0-9a-fA-F]{40}\b"),
    "hex64": re.compile(r"\b[0-9a-fA-F]{64}\b"),
    "jwt_like_3seg": re.compile(r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "base64_long": re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b"),
    "bearer_header_shape": re.compile(r"Authorization:\s*Bearer\s+\S+", re.I),
    "api_key_assign": re.compile(r"(?i)(api[_-]?key|apikey|secret|token|auth)[\"'\s:=]+[^\s\"']{8,}"),
    "email_shape": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "slug_id_path": re.compile(r"/[A-Za-z0-9_-]{16,}(?:/[A-Za-z0-9_-]{8,})?"),
    "percent_encoded_seq": re.compile(r"(?:%[0-9a-fA-F]{2}){3,}"),
    "unicode_escape": re.compile(r"\\u[0-9a-fA-F]{4}"),
    "hex_escape": re.compile(r"\\x[0-9a-fA-F]{2}"),
    "html_entity": re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);"),
}
ZW = {"U+200B": "\u200b", "U+200C": "\u200c", "U+200D": "\u200d", "U+FEFF": "\ufeff", "U+2060": "\u2060",
      "U+00AD": "\u00ad", "U+180E": "\u180e"}
FILES = sorted(glob.glob(os.path.join(BASE, "atlas_*.bin")))
per_file = {}
# token candidate -> set of files ; token fingerprint map
cand_files = defaultdict(set)
cand_shape = {}
cand_len = {}
# exact line -> set of files
line_files = defaultdict(set)
line_len = {}
line_first_words = {}
# host -> files ; query param name -> files
host_files = defaultdict(set)
qparam_files = defaultdict(set)
qparam_shape = Counter()
url_scheme = Counter()
relay_hosts = Counter()
total = Counter()

for path in FILES:
    name = os.path.basename(path)
    raw = open(path, "rb").read()
    try:
        text = raw.decode("utf-8")
        decodable = True
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        decodable = False
    d = {"bytes": len(raw), "decodable_utf8": decodable,
         "bom": raw.startswith(b"\xef\xbb\xbf"),
         "crlf_lines": text.count("\r\n"), "lf_lines": text.count("\n"),
         "null_bytes": raw.count(b"\x00"),
         "non_ascii_chars": sum(1 for c in text if ord(c) > 127),
         "zw": {}, "patterns": {}, "pattern_shapes": {},
         "hosts": [], "qparams": [], "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0)}
    for zwname, zwch in ZW.items():
        n = text.count(zwch)
        if n: d["zw"][zwname] = n
    for pname, rx in PATTERNS.items():
        hits = rx.findall(text)
        # bearer/api_key hits are whole matches; count only
        d["patterns"][pname] = len(hits)
        shapes = Counter()
        if pname in ("uuid_hyphenated", "uuid_hex32", "hex40", "hex64", "jwt_like_3seg"):
            for h in hits:
                s = h if isinstance(h, str) else h[0]
                shapes[shape_of(s)] += 1
        d["pattern_shapes"][pname] = dict(shapes)
    # candidate high-entropy tokens: standalone alnum/_/- strings len>=20,
    # not pure URL path words; hash them for cross-file matching
    for m in re.finditer(r"(?<![A-Za-z0-9_/\-.])[A-Za-z0-9_-]{20,}(?![A-Za-z0-9_/\-.])", text):
        tok = m.group(0)
        if tok.lower().startswith(("http", "www")): continue
        if re.fullmatch(r"[a-z]+", tok) or re.fullmatch(r"[A-Z]+", tok): continue
        h = hashlib.sha256(tok.encode()).hexdigest()
        cand_files[h].add(name)
        cand_shape[h] = shape_of(tok)
        cand_len[h] = len(tok)
    # lines
    for ln in text.splitlines():
        s = ln.strip()
        if len(s) >= 20:
            h = hashlib.sha256(s.encode()).hexdigest()
            line_files[h].add(name)
            line_len[h] = len(s)
            # first 3 words only if they are plain words (no token chars)
            words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", s)[:4]
            line_first_words[h] = " ".join(words)
    # URLs: hosts + query param names only
    for m in re.finditer(r"https?://[^\s\"'<>\)\]]+", text):
        u = m.group(0).rstrip(".,;")
        try:
            p = urlparse(u)
        except Exception:
            continue
        if p.hostname:
            host_files[p.hostname].add(name)
            url_scheme[p.scheme] += 1
            if any(k in p.hostname for k in ("proxy", "relay", "tunnel", "vercel", "workers.dev", "onrender", "fly.dev", "pages.dev", "railway", "chatgpt.site")):
                relay_hosts[p.hostname] += 1
        if p.query:
            for k, v in parse_qsl(p.query, keep_blank_values=True):
                qparam_files[k].add(name)
                qparam_shape[k] += 1
    per_file[name] = d

cross_tokens = {h: sorted(fs) for h, fs in cand_files.items() if len(fs) >= 2}
cross_lines = {h: sorted(fs) for h, fs in line_files.items() if len(fs) >= 2}
multi_hosts = {h: sorted(fs) for h, fs in host_files.items() if len(fs) >= 2}

# footer / signature structure: last 5 non-empty lines per file, classified
footer_classes = Counter()
footer_examples = defaultdict(list)
for path in FILES:
    name = os.path.basename(path)
    text = open(path, "rb").read().decode("utf-8", errors="replace")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for ln in lines[-5:]:
        low = ln.lower()
        cls = None
        if re.search(r"powered by|built with|made with", low): cls = "powered-by/made-with line"
        elif re.search(r"generated|signed|signature", low): cls = "generated/signed line"
        elif re.search(r"^#+\s", ln): cls = "markdown heading"
        elif ln.startswith(("---", "***", "===")): cls = "rule separator"
        elif re.search(r"copyright|©|\(c\)", low): cls = "copyright line"
        elif re.search(r"http", low): cls = "closing URL line"
        elif re.search(r"^\[.*\]\(.*\)", ln): cls = "closing markdown link"
        if cls:
            footer_classes[cls] += 1
            if len(footer_examples[cls]) < 5:
                footer_examples[cls].append(name)

summary = {
    "files": len(FILES),
    "total_bytes": sum(d["bytes"] for d in per_file.values()),
    "per_file": per_file,
    "pattern_totals": {p: sum(d["patterns"][p] for d in per_file.values()) for p in PATTERNS},
    "cross_token_matches": [{"sha256": h, "shape": cand_shape[h], "len": cand_len[h], "files": fs}
                            for h, fs in sorted(cross_tokens.items(), key=lambda kv: -len(kv[1]))],
    "cross_line_matches": [{"sha256": h, "len": line_len[h], "first_words": line_first_words[h], "n_files": len(fs), "files": fs}
                           for h, fs in sorted(cross_lines.items(), key=lambda kv: -len(kv[1]))],
    "multi_file_hosts": [{"host": h, "files": fs} for h, fs in sorted(multi_hosts.items())],
    "host_count": len(host_files),
    "query_param_names": [{"param": k, "n_files": len(fs), "files": sorted(fs)} for k, fs in sorted(qparam_files.items())],
    "url_schemes": dict(url_scheme),
    "relay_like_hosts": dict(relay_hosts),
    "footer_classes": dict(footer_classes),
    "footer_examples": dict(footer_examples),
}
json.dump(summary, open(os.path.join(OUT, "analysis.json"), "w"), indent=1)
print("files:", summary["files"], "bytes:", summary["total_bytes"])
print("pattern totals:", summary["pattern_totals"])
print("cross tokens:", len(summary["cross_token_matches"]))
print("cross lines:", len(summary["cross_line_matches"]))
print("multi hosts:", len(summary["multi_file_hosts"]))
print("qparams:", list(qparam_files.keys()))
print("footer:", dict(footer_classes))
