#!/usr/bin/env python3
"""CRYPTOGRAPHER main analysis. Reads cryptolib, writes out/*.json."""
import json, os, re, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cryptolib import *
from collections import Counter, defaultdict

# ================= 1. BASE64 DECODE + LANGUAGE =================
b64_findings = []          # per-blob records (deduped by sha256)
seen_blob = set()
lang_agg = Counter()
diacritic_blobs = Counter()

def record_blob(txt, origin):
    h = hashlib.sha256(txt.encode("utf-8", "replace")).hexdigest()[:16]
    if h in seen_blob:
        return
    seen_blob.add(h)
    verdict, det = lang_score(txt)
    lang_agg[verdict] += 1
    diac = {"ä": "ä" in txt, "ö": "ö" in txt, "ü": "ü" in txt, "ß": "ß" in txt,
            "é": "é" in txt, "è": "è" in txt, "ç": "ç" in txt, "à": "à" in txt}
    if any(diac.values()):
        diacritic_blobs[verdict] += 1
    # code-density heuristic
    codey = bool(re.search(r"(function|var |const |document\.|window\.|=>|navigator\.)", txt[:4000]))
    rec = {"sha16": h, "len": len(txt), "verdict": verdict, "det": det,
           "origin": origin, "diacritics": [k for k, v in diac.items() if v],
           "codey": codey, "head": txt[:600].replace("\n", "\\n")}
    # keep full text for DE/FR verdicts only (evidence rule), else head
    if verdict in ("de", "fr", "mixed/de", "mixed/fr"):
        rec["full"] = txt
    b64_findings.append(rec)

n_strings = 0
n_candidates = 0

def scan_value_for_b64(val, origin):
    """Scan a string for base64 blobs, incl. URL-encoded forms (httpbun %2B/%2F)."""
    global n_candidates
    # pass 1: raw text
    texts = [val]
    # pass 2: URL-decoded text (catches %2B %2F %3D encoded base64 in URL paths)
    try:
        from urllib.parse import unquote
        uq = unquote(val)
        if uq != val:
            texts.append(uq)
    except Exception:
        pass
    for t in texts:
        if len(t) < 100:
            continue
        # dedicated /base64/ path extractor: capture the path segment after 'base64/'
        for m in re.finditer(r"base64/([A-Za-z0-9+/_=~-]{60,})", t):
            seg = m.group(1).rstrip("~")
            n_candidates += 1
            txt = try_b64(seg)
            if txt:
                record_blob(txt, origin + "|b64path")
        for m in B64_RE.finditer(t):
            cand = m.group(0)
            if re.fullmatch(r"[0-9a-fA-F]+", cand) or re.fullmatch(r"[0-9]+", cand):
                continue
            n_candidates += 1
            txt = try_b64(cand)
            if txt:
                record_blob(txt, origin)

for cname, idx, path, val in iter_event_strings():
    n_strings += 1
    if len(val) < 60:
        continue
    scan_value_for_b64(val, f"{cname}#{idx}:{path}")

# raw files (json/txt/html)
for fp in iter_raw_files():
    try:
        data = open(fp, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if len(data) < 100:
        continue
    scan_value_for_b64(data, "raw:" + os.path.relpath(fp, BASE))

json.dump({"n_strings_scanned": n_strings, "n_b64_candidates": n_candidates,
           "n_unique_decoded": len(b64_findings),
           "lang_aggregate": dict(lang_agg),
           "diacritic_blobs": dict(diacritic_blobs)},
          open(os.path.join(OUT, "b64_summary.json"), "w"), indent=1)
json.dump(b64_findings, open(os.path.join(OUT, "b64_blobs.json"), "w"), indent=1)

# ================= 2. HEX DECODE -> WORDLIST =================
HEX_RE = re.compile(r"\b[0-9a-fA-F]{8,64}\b")
hex_hits = []
hex_total = 0
hex_printable = 0
for cname, idx, path, val in iter_event_strings():
    for m in HEX_RE.finditer(val):
        hs = m.group(0)
        if len(hs) % 2:
            continue
        # skip UUIDs / fingerprints (structural) — keep, but flag
        hex_total += 1
        try:
            raw = bytes.fromhex(hs)
        except ValueError:
            continue
        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if not txt.isprintable() or len(txt.strip()) < 4:
            continue
        hex_printable += 1
        toks = re.findall(r"[A-Za-zäöüÄÖÜßéèêàç]{4,}", txt.lower())
        de_hit = [t for t in toks if t in DE_WORDS]
        fr_hit = [t for t in toks if t in FR_WORDS]
        if de_hit or fr_hit:
            hex_hits.append({"hex": hs, "decoded": txt, "de": de_hit, "fr": fr_hit,
                             "origin": f"{cname}#{idx}:{path}"})

json.dump({"hex_strings_total": hex_total, "hex_printable_decodes": hex_printable,
           "wordlist_hits": hex_hits},
          open(os.path.join(OUT, "hex_hits.json"), "w"), indent=1)

# ================= 3. TAG-GRAMMAR TOKENS vs WORDLISTS =================
TAG_FIELDS = ("uqscan", "uqtag", "fleet_tag", "matched_string", "oai", "zz", "oai_tag")
tag_values = []
for cname, idx, path, val in iter_event_strings():
    pl = path.lower()
    if any(t in pl for t in TAG_FIELDS) and isinstance(val, str) and len(val) < 300:
        tag_values.append((val, f"{cname}#{idx}:{path}"))

token_counter = Counter()
char_counter = Counter()
word_hits = []   # (token, lang, origin)
folded_hits = []
seen_tok_origin = set()
for val, origin in tag_values:
    char_counter.update(val)
    # split into alpha tokens on digits/case/underscores
    parts = re.findall(r"[A-Za-zäöüÄÖÜßéèêëàç]{3,}", val)
    for p in parts:
        pl = p.lower()
        token_counter[pl] += 1
        key = (pl, origin)
        if key in seen_tok_origin:
            continue
        seen_tok_origin.add(key)
        if len(pl) >= 4 and pl in DE_WORDS:
            word_hits.append({"token": p, "lang": "de", "origin": origin, "tag": val})
        elif len(pl) >= 4 and pl in FR_WORDS:
            word_hits.append({"token": p, "lang": "fr", "origin": origin, "tag": val})
        if pl in FOLDED_DE:
            folded_hits.append({"token": p, "lang": "de-folded", "origin": origin, "tag": val})
        if pl in FOLDED_FR:
            folded_hits.append({"token": p, "lang": "fr-folded", "origin": origin, "tag": val})

# digraph anomaly: German 'sch', 'ch', 'ck' density vs English 'th','wh'
def digraph_density(tokens, digraphs):
    tot = sum(len(t) for t in tokens)
    c = sum(t.count(d) for t in tokens for d in digraphs)
    return c / max(tot, 1)

toks = list(token_counter.keys())
de_digraphs = ["sch", "ch", "ck", "tz", "pf", "qu", "ei", "ie", "au", "eu", "ä", "ö", "ü", "ß"]
fr_digraphs = ["ou", "oi", "ai", "ei", "eu", "au", "ch", "gn", "qu", "é", "è", "ê", "à", "ç"]
en_digraphs = ["th", "wh", "sh", "ck", "ee", "oo", "ou"]

json.dump({
    "n_tag_values": len(tag_values),
    "n_distinct_tokens": len(token_counter),
    "top_tokens": token_counter.most_common(60),
    "char_distribution": dict(sorted(char_counter.items())),
    "non_ascii_chars_in_tags": {c: n for c, n in char_counter.items() if ord(c) > 127},
    "digraph_density": {
        "de_markers": round(digraph_density(toks, de_digraphs), 5),
        "fr_markers": round(digraph_density(toks, fr_digraphs), 5),
        "en_markers": round(digraph_density(toks, en_digraphs), 5),
    },
    "wordlist_hits": word_hits,
    "folded_diacritic_hits": folded_hits,
}, open(os.path.join(OUT, "tag_grammar.json"), "w"), indent=1)

# ================= 4. WEBHOOK/BEACON FILES =================
special = []
for rel in ["raw/a7753b69-bxua-tokens.txt",
            "raw/cbcb10de-jinacache-page.html",
            "raw/a7753b69-running-page-from-referer.html"]:
    fp = os.path.join(CORP, rel)
    if os.path.exists(fp):
        txt = open(fp, encoding="utf-8", errors="replace").read()
        verdict, det = lang_score(txt)
        special.append({"file": rel, "len": len(txt), "verdict": verdict, "det": det,
                        "head": txt[:500].replace("\n", "\\n")})
# webhook-deaddrop events: scan their text fields for any body-ish content
for cname, idx, path, val in iter_event_strings():
    if cname == "2026-05-12-webhook-deaddrops" and len(val) > 200:
        verdict, det = lang_score(val)
        if verdict in ("de", "fr", "mixed/de", "mixed/fr"):
            special.append({"file": f"webhook-deaddrops#{idx}:{path}", "len": len(val),
                            "verdict": verdict, "det": det, "head": val[:500]})

json.dump(special, open(os.path.join(OUT, "webhook_beacon.json"), "w"), indent=1)

print("done", len(b64_findings), "blobs;", len(hex_hits), "hex hits;",
      len(word_hits), "word hits;", len(folded_hits), "folded hits")
print("lang_agg:", dict(lang_agg))
