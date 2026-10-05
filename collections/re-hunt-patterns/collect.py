#!/usr/bin/env python3
"""
Lane 2 — pattern blind-spot re-audit (re-hunt).

Systematically kill keyword-blindness of the "OpenAI Research" class:
generate variant grammars for EVERY marker previously graded zero or
under-searched (spaced/unspaced/underscore/hyphen/camel/lower/upper,
URL-encoded forms, Jun-17 param names, dsqa_* shapes, gov targets,
LAC payloads) and sweep all four corpora with every variant.

Corpora are READ-ONLY. Hits are keep-all + annotated into data/hits.jsonl;
never merged into canonical datasets.

Idempotent: re-run resumes via fingerprint — if state.json shows a
completed run with an unchanged fingerprint (pattern table + corpus
file sizes/mtimes), the run is a no-op. Otherwise outputs are rebuilt
deterministically (no duplicates, no invented rows).

Outputs (under collections/re-hunt-patterns/):
  pattern-matrix.jsonl  {"pattern","variant_of","regex","case_insensitive",
                        "corpora":{"urlquery":n,"collusion-wiki":n,"rubygems":n,"arquivo-pt":n}}
  data/hits.jsonl       {"pattern","corpus","record_id","matched_field",
                        "matched","excerpt","timestamp"}
  state.json            lane, patterns_total, corpora_swept, items_collected,
                        status, watermarks, fingerprint
"""

import gzip
import hashlib
import json
import os
import re
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
ELASTIC = os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports")
ARQUIVO_RAW = os.path.expanduser(
    "~/workspace/silent-locus/data/2026-10-01-arquivo-pt/raw")

# (pattern_id, variant_of, regex, case_insensitive)
# NOTE: case-insensitive regexes are written in LOWERCASE and matched against
# lowered text; case-sensitive ones are matched against original text.
PATTERNS = [
    # --- "OpenAI Research" marker family (variant_of: openai-research) ---
    ("or_spaced", "openai-research", r"openai[ \t]+research", True),
    ("or_nospace_ci", "openai-research", r"openairesearch", True),
    ("or_nospace_lower", "openai-research", r"openairesearch", False),
    ("or_nospace_camel", "openai-research", r"OpenAIResearch", False),
    ("or_nospace_upper", "openai-research", r"OPENAIRESEARCH", False),
    ("or_underscore", "openai-research", r"openai_research", True),
    ("or_hyphen", "openai-research", r"openai-research", True),
    ("or_hyphen_trailing", "openai-research", r"openai-research-", True),
    ("or_reversed", "openai-research", r"research[-_ ]openai", True),
    ("or_dot", "openai-research", r"openai\.research", True),
    ("or_sep_tolerant", "openai-research", r"open[ _.\-]?ai[ _.\-]?research", True),
    # --- oai* tag family (variant_of: oai-tag) ---
    ("tag_oai_generic", "oai-tag", r"(?:^|[^a-z0-9])oai", True),
    ("tag_oai_digits", "oai-tag", r"oai[0-9]+", True),
    ("tag_oai_upper_cs", "oai-tag", r"(?:^|[^A-Za-z0-9])OAI", False),
    ("tag_oai_hyphen", "oai-tag", r"oai-", True),
    ("tag_zz_eq_oai", "oai-tag", r"zz=oai", True),
    ("tag_zz_eq_oai_digits", "oai-tag", r"zz=oai[0-9]+", True),
    ("tag_zz_enc_eq_oai", "oai-tag", r"zz%3doai", True),
    ("tag_qmark_oai", "oai-tag", r"[?&]oai", True),
    # --- Jun-17 DoE param family (variant_of: doe-param) ---
    ("param_stateid_mixed", "doe-param", r"State_Id", False),
    ("param_stateid_lower", "doe-param", r"state_id", False),
    ("param_stateid_upper", "doe-param", r"STATE_ID", False),
    ("param_stateid_nospace", "doe-param", r"stateid", False),
    ("param_stateid_camel", "doe-param", r"stateId", False),
    ("param_stateid_ci", "doe-param", r"state[-_]?id", True),
    ("param_measureid_mixed", "doe-param", r"Measure_Id", False),
    ("param_measureid_lower", "doe-param", r"measure_id", False),
    ("param_measureid_upper", "doe-param", r"MEASURE_ID", False),
    ("param_measureid_camel", "doe-param", r"measureId", False),
    ("param_measureid_ci", "doe-param", r"measure[-_]?id", True),
    ("param_surveyyearkey_mixed", "doe-param", r"survey_Year_Key", False),
    ("param_surveyyearkey_lower", "doe-param", r"survey_year_key", False),
    ("param_surveyyearkey_title", "doe-param", r"Survey_Year_Key", False),
    ("param_surveyyearkey_camel", "doe-param", r"surveyYearKey", False),
    ("param_surveyyearkey_pascal", "doe-param", r"SurveyYearKey", False),
    ("param_surveyyearkey_ci", "doe-param", r"survey[-_]?year[-_]?key", True),
    ("param_stateid_enc_eq", "doe-param", r"state_id%3d", True),
    ("param_measureid_enc_eq", "doe-param", r"measure_id%3d", True),
    ("param_surveyyearkey_enc_eq", "doe-param", r"survey_year_key%3d", True),
    ("frag_sqli_enc", "doe-param", r"1%20or%201%3d1", True),
    ("frag_sqli_plain", "doe-param", r"1 or 1=1", True),
    ("ladder_stateid_zero", "doe-param", r"state_id\s*=\s*0(?![0-9])", True),
    ("ladder_stateid_neg1", "doe-param", r"state_id\s*=\s*-1", True),
    ("ladder_stateid_99", "doe-param", r"state_id\s*=\s*99(?![0-9])", True),
    ("ladder_stateid_999", "doe-param", r"state_id\s*=\s*999(?![0-9])", True),
    ("ladder_stateid_empty", "doe-param", r"state_id=(?=&|$|\")", True),
    ("ladder_surveyyearkey_9", "doe-param", r"survey_year_key\s*=\s*9(?![0-9])", True),
    ("ladder_measureid_130", "doe-param", r"measure_id\s*=\s*130(?![0-9])", True),
    # --- DeepSearchQA family (variant_of: deepsearchqa) ---
    ("dsqa_underscore_ci", "deepsearchqa", r"dsqa_", True),
    ("dsqa_underscore_upper", "deepsearchqa", r"DSQA_", False),
    ("dsqa_hyphen", "deepsearchqa", r"dsqa-", True),
    ("deepsearchqa_ci", "deepsearchqa", r"deepsearchqa", True),
    ("deepsearchqa_upper", "deepsearchqa", r"DEEPSEARCHQA", False),
    ("deepsearchqa_hyphen", "deepsearchqa", r"deep-search-qa", True),
    ("deepsearchqa_underscore", "deepsearchqa", r"deep_search_qa", True),
    ("dsqa_250", "deepsearchqa", r"dsqa_250", True),
    # --- gov target family (variant_of: target-gov) ---
    ("tgt_civilrightsdata", "target-gov", r"civilrightsdata", True),
    ("tgt_civil_rights_data", "target-gov", r"civil-rights-data", True),
    ("tgt_nces_host", "target-gov", r"nces\.ed\.gov", True),
    ("tgt_nces", "target-gov", r"(?<![a-z0-9])nces(?![a-z0-9])", True),
    ("tgt_crdc", "target-gov", r"(?<![a-z0-9])crdc(?![a-z0-9])", True),
    ("tgt_beagov", "target-gov", r"bea\.gov", True),
    ("tgt_beagov_register", "target-gov",
     r"bea.{0,60}(register|signup|sign[ -]?up)", True),
    ("tgt_beagov_apikey", "target-gov", r"bea.{0,60}api[ _-]?key", True),
    ("tgt_censusgov", "target-gov", r"census\.gov", True),
    ("tgt_census_apikey", "target-gov", r"census.{0,80}api[ _-]?key", True),
    # --- LAC payload family (variant_of: lac-payload) ---
    ("lac_id_quote", "lac-payload", r"idnumber=%27", True),
    ("lac_csv_enc", "lac-payload", r"1%2c2", True),
    ("lac_csv_param", "lac-payload", r"idnumber=1%2c2", True),
    ("lac_xss_doubleenc", "lac-payload", r"%253c", True),
    ("lac_bigint", "lac-payload", r"2147483648", True),
    ("lac_abc_param", "lac-payload", r"idnumber=abc", True),
    ("lac_dotjson_param", "lac-payload", r"idnumber=\d+\.json", True),
    ("lac_dotjson_generic", "lac-payload", r"\.json\b", True),
    ("lac_output", "lac-payload", r"[?&]output=", True),
    ("lac_raw", "lac-payload", r"[?&]raw=", True),
    ("lac_urlparam", "lac-payload", r"[?&]url=", True),
    ("lac_debug1", "lac-payload", r"debug=1", True),
    ("lac_debug_false", "lac-payload", r"debug=false", True),
    ("lac_op_format", "lac-payload", r"[?&]op=(json|xml|record)", True),
    ("lac_wbdisable", "lac-payload", r"wbdisable", True),
    ("lac_downloadtoken_abc", "lac-payload", r"downloadtoken=dt--abc--dt", True),
    ("lac_format", "lac-payload", r"[?&]format=(xml|csv|html)", True),
]

CORPORA = [
    ("urlquery", os.path.join(ELASTIC,
        "urlquery-incidents-20260928T022324Z.jsonl.gz"), "es"),
    ("collusion-wiki", os.path.join(ELASTIC,
        "collusion-wiki-20260928T025051Z.jsonl.gz"), "es"),
    ("rubygems", os.path.join(ELASTIC,
        "rubygems-goimport-campaign-20260928T022324Z.jsonl.gz"), "es"),
    ("arquivo-pt", ARQUIVO_RAW, "arquivo"),
]

COMPILED = [(pid, vo, re.compile(rx), ci) for pid, vo, rx, ci in PATTERNS]


def fingerprint():
    h = hashlib.sha256()
    h.update(json.dumps(PATTERNS, sort_keys=True).encode())
    for cname, path, kind in CORPORA:
        if kind == "es":
            st = os.stat(path)
            h.update(f"{cname}|{path}|{st.st_size}|{st.st_mtime}\n".encode())
        else:
            for fn in sorted(os.listdir(path)):
                if not fn.endswith(".jsonl.gz"):
                    continue
                fp = os.path.join(path, fn)
                st = os.stat(fp)
                h.update(f"{cname}|{fp}|{st.st_size}|{st.st_mtime}\n".encode())
    return h.hexdigest()


def find_field(obj, rx, ci, prefix=""):
    """First dotted path of a string value matching rx (values only)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            r = find_field(v, rx, ci, p)
            if r:
                return r
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            r = find_field(v, rx, ci, f"{prefix}[{i}]")
            if r:
                return r
    elif isinstance(obj, str):
        hay = obj.lower() if ci else obj
        try:
            if rx.search(hay):
                return prefix
        except Exception:
            return None
    return None


def excerpt_of(text, span):
    s, e = span
    a = max(0, s - 80)
    b = min(len(text), e + 80)
    x = text[a:b].replace("\n", " ").replace("\r", " ")
    x = re.sub(r"\s+", " ", x)
    return x[:220]


def sweep():
    counts = {pid: {c: 0 for c, _, _ in CORPORA} for pid, _, _, _ in PATTERNS}
    watermarks = {}
    total_hits = 0
    hits_path = os.path.join(BASE, "data", "hits.jsonl")
    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    t0 = time.time()

    with open(hits_path, "w") as hf:
        for cname, path, kind in CORPORA:
            files = [path] if kind == "es" else sorted(
                os.path.join(path, fn) for fn in os.listdir(path)
                if fn.endswith(".jsonl.gz"))
            for fp in files:
                n = 0
                with gzip.open(fp, "rt", encoding="utf-8",
                               errors="replace") as f:
                    for line in f:
                        n += 1
                        line = line.rstrip("\n")
                        if not line:
                            continue
                        if kind == "es":
                            try:
                                rec = json.loads(line)
                            except Exception:
                                continue
                            text = line
                            src = rec.get("_source", {})
                            rid = rec.get("_id", "?")
                            ts = src.get("@timestamp", "")
                        else:  # arquivo-pt cdx: match against the URL only
                            try:
                                rec = json.loads(line)
                            except Exception:
                                continue
                            text = rec.get("url", "") or ""
                            src = None
                            rid = rec.get("urlkey") or text
                            ts = rec.get("timestamp", "")
                        if not text:
                            continue
                        lowered = text.lower()
                        for pid, _vo, rx, ci in COMPILED:
                            hay = lowered if ci else text
                            m = rx.search(hay)
                            if not m:
                                continue
                            counts[pid][cname] += 1
                            total_hits += 1
                            field = "url" if kind == "arquivo" else (
                                find_field(src, rx, ci) or "_source")
                            span = m.span()
                            src_text = text if len(hay) == len(text) else hay
                            row = {
                                "pattern": pid,
                                "corpus": cname,
                                "record_id": rid,
                                "matched_field": field,
                                "matched": m.group(0)[:80],
                                "excerpt": excerpt_of(src_text, span),
                                "timestamp": ts,
                            }
                            hf.write(json.dumps(row, ensure_ascii=False) + "\n")
                watermarks.setdefault(cname, {})[os.path.basename(fp)] = n
    return counts, watermarks, total_hits, time.time() - t0


def main():
    fp = fingerprint()
    state_path = os.path.join(BASE, "state.json")
    if os.path.exists(state_path):
        try:
            with open(state_path) as f:
                st = json.load(f)
            if st.get("status") == "complete" and st.get("fingerprint") == fp:
                print(f"re-hunt-patterns: already complete "
                      f"({st['patterns_total']} patterns, "
                      f"{st['items_collected']} hits); fingerprint unchanged — "
                      f"no-op.")
                return 0
        except Exception:
            pass

    counts, watermarks, total_hits, elapsed = sweep()

    matrix_path = os.path.join(BASE, "pattern-matrix.jsonl")
    with open(matrix_path, "w") as mf:
        for pid, vo, rx, ci in PATTERNS:
            mf.write(json.dumps({
                "pattern": pid,
                "variant_of": vo,
                "regex": rx,
                "case_insensitive": ci,
                "corpora": {c: counts[pid][c] for c, _, _ in CORPORA},
            }, ensure_ascii=False) + "\n")

    state = {
        "lane": "re-hunt-patterns (lane 2: pattern blind-spot re-audit)",
        "patterns_total": len(PATTERNS),
        "corpora_swept": [c for c, _, _ in CORPORA],
        "items_collected": total_hits,
        "status": "complete",
        "elapsed_s": round(elapsed, 1),
        "watermarks": watermarks,
        "fingerprint": fp,
        "ran_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    print(f"re-hunt-patterns: swept {len(PATTERNS)} patterns over "
          f"{len(CORPORA)} corpora in {elapsed:.1f}s; "
          f"{total_hits} hits -> data/hits.jsonl; matrix -> pattern-matrix.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
