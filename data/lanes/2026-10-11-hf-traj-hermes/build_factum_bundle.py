#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-10-11-hf-traj-hermes.

Reads .work/ aggregates produced by extract.py (streaming pass over
evidence/hf-trajectories/raw/djlougen-hermes-agent-traces-filtered/data/train.jsonl,
349 MB, 3,679 rows) and emits one aggregated Factum bundle:

  1 source      dataset: DJLougen/hermes-agent-traces-filtered (HF)
  1 run         ingest-prep: streaming extraction run
 26 observation intel.behavior  one per distinct tool function (name + verbatim
                                description + corpus frequency)
100 observation intel.behavior  one per distinct shell first-token
                                (category shell-command)
136 observation infra.ioc       url-pattern: full URLs with >= 50 mentions
 50 observation infra.ioc       domain: top 50 hosts by mention count
  3 claim       OBSERVED extraction findings (model non-uniformity,
                <tools>-XML/field agreement, 26-vs-55 tool count discrepancy)

Giant-lane rule applies: 3,679 rows / 67,963 tool calls are aggregated, not
ingested 1:1. Methodology is recorded in the run record and PROVENANCE.md.

Pre-ingest dedup: exact-term grep against exported Factum batches
(data/records/*/records.jsonl). Exact term+type duplicates are skipped and
listed; near/term overlaps are annotated in tags (keep-all + annotate).

Usage: python3 build_factum_bundle.py <repo-root> > bundle.json
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from urllib.parse import urlparse

REPO = sys.argv[1]
LANE_DIR = os.path.join(REPO, "data/lanes/2026-10-11-hf-traj-hermes")
WORK = os.path.join(LANE_DIR, ".work")
LANE_TAG = "2026-10-11-hf-traj-hermes"
ACTOR = "agent:lane-ingest-2026-10-11-hf-traj-hermes"
DATASET = "djlougen-hermes-agent-traces-filtered"
HARNESS = "hermes-agent"
MODEL = "multiple-frontier-models"
OBSERVED_AT = "2026-04-04T21:21:35Z"  # api_card lastModified: dataset revision

URL_MIN_COUNT = 50
HOST_TOP_N = 50


def S(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(str(x) for x in v)
    return str(v)


def base_tags(grade="OBSERVED"):
    return {
        "lane": LANE_TAG,
        "grade": grade,
        "model": MODEL,
        "harness": HARNESS,
        "source_dataset": DATASET,
    }


def build_corpus_term_index():
    """One streaming pass over exported Factum batches.

    Returns {(record_type, term): True} for infra.ioc terms and
    intel.behavior categories. Single pass -- no per-candidate scans.
    """
    import glob
    index = {}
    term_re = re.compile(r'"type":"(infra\.ioc|intel\.behavior)".*?"term":"((?:[^"\\]|\\.)*)"')
    cat_re = re.compile(r'"type":"intel\.behavior".*?"category":"((?:[^"\\]|\\.)*)"')
    for p in glob.glob(os.path.join(REPO, "data/records", "*", "records.jsonl")):
        try:
            with open(p, errors="replace") as f:
                for line in f:
                    if '"infra.ioc"' in line:
                        for m in term_re.finditer(line):
                            if m.group(1) == "infra.ioc":
                                index[("infra.ioc", m.group(2))] = True
                    if '"intel.behavior"' in line:
                        for m in cat_re.finditer(line):
                            index[("intel.behavior", m.group(1))] = True
        except OSError:
            continue
    return index


def main():
    stats = json.load(open(os.path.join(WORK, "extraction_stats.json")))
    functions = json.load(open(os.path.join(WORK, "functions.json")))
    urls = json.load(open(os.path.join(WORK, "urls.json")))
    commands = json.load(open(os.path.join(WORK, "commands.json")))

    assert stats["rows_total"] == 3679
    assert len(functions) == stats["distinct_functions_defined"] == 26

    # --- batch-internal dedup by key field ---
    fn_names = [f["name"] for f in functions]
    assert len(set(fn_names)) == len(fn_names), "duplicate function names"
    url_terms = [u["url"] for u in urls]
    assert len(set(url_terms)) == len(url_terms), "duplicate urls"

    # --- URL / host selection ---
    url_sel = [u for u in urls if u["count"] >= URL_MIN_COUNT]
    hosts_m = Counter()
    hosts_d = Counter()
    for u in urls:
        try:
            h = urlparse(u["url"]).hostname or "(none)"
        except Exception:
            h = "(parse-error)"
        hosts_d[h] += 1
        hosts_m[h] += u["count"]
    host_sel = [h for h, _ in hosts_m.most_common(HOST_TOP_N)]

    # --- shell first-token aggregation with exemplars ---
    tok_inv = Counter()
    tok_distinct = Counter()
    tok_ex = {}
    for c in commands:
        cmd = c["command"]
        m = re.match(r"\s*(\S+)", cmd)
        t0 = m.group(1) if m else "(empty)"
        tok_inv[t0] += c["count"]
        tok_distinct[t0] += 1
        tok_ex.setdefault(t0, []).append((c["count"], cmd))
    for t0 in tok_ex:
        tok_ex[t0].sort(reverse=True)

    skipped_dupes = []

    # single-pass corpus term index (exact term+type matches)
    corpus_index = build_corpus_term_index()

    def check(term, rtype):
        # JSON-escaped form of the term as it appears in exported batches
        esc = term.replace("\\", "\\\\").replace('"', '\\"')
        if (rtype, esc) in corpus_index:
            skipped_dupes.append((rtype, term))
            return False
        return True

    # also dedup function-name categories against existing intel.behavior
    fn_overlap = [f for f in fn_names if ("intel.behavior", f) in corpus_index]

    records = []

    # --- source ---
    records.append({
        "kind": "source", "ref": "src",
        "body": {
            "source_type": "dataset",
            "locator": "https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered",
            "title": ("DJLougen/hermes-agent-traces-filtered: Hermes Agent "
                      "Reasoning Traces - Quality Filtered (3,679 rows, "
                      "apache-2.0); structurally filtered subset of "
                      "lambda/hermes-agent-reasoning-traces (7,646 -> 3,679)"),
            "platform": ("Hugging Face datasets API; retrieved 2026-10-07T23:55:16Z "
                         "via curl (dataset revision sha f91a8ef669194408a706741cd6f32a1686a8fd; "
                         "api lastModified 2026-04-04T21:21:35Z)"),
        },
        "tags": dict(base_tags(), **{
            "retrieved": "2026-10-07T23:55:16Z",
            "local_path": ("evidence/hf-trajectories/raw/"
                           "djlougen-hermes-agent-traces-filtered/data/train.jsonl"),
        }),
    })

    # --- run ---
    records.append({
        "kind": "run", "ref": "run",
        "body": {
            "run_kind": "ingest-prep",
            "started": "2026-10-11T00:54:00-05:00",
            "tool": "extract.py + build_factum_bundle.py (lane-local)",
            "params": {
                "method": ("streaming row-by-row JSONL parse (never loads 349MB "
                           "into memory); function defs from row-level 'tools' "
                           "field AND system-prompt <tools> XML (plain JSON, "
                           "parsed on all 3,679 rows); tool invocations from "
                           "<tool_call> JSON blocks; URLs via regex over all "
                           "conversation values; shell commands from "
                           "terminal/execute_code/shell tool_call arguments; "
                           "progress in .work/progress.json"),
                "aggregation": (f"26 distinct functions (1 record each); shell "
                                f"commands aggregated by first token ({len(tok_inv)} "
                                f"tokens); URLs: {len(url_sel)} with >={URL_MIN_COUNT} "
                                f"mentions -> url-pattern records; top {HOST_TOP_N} "
                                f"hosts by mention count -> domain records"),
                "pre_ingest_dedup": ("in-batch dedup by key field (function "
                                     "name, URL term); single-pass exact-term "
                                     "index over exported Factum batches; "
                                     "exact term+type duplicates skipped, "
                                     "function-name category overlaps: "
                                     + (", ".join(fn_overlap) if fn_overlap else "none")),
            },
            "coverage": {
                "complete": True, "scanned": 3679, "total": 3679,
                "description": ("3,679 rows, 67,963 <tool_call> blocks parsed "
                                "(0 parse failures), 93,781 URL mentions "
                                "(20,651 distinct URLs), 24,911 distinct shell "
                                "commands from 3,227 rows"),
            },
        },
        "tags": base_tags(),
    })

    # --- 26 function inventory records ---
    for f in functions:
        name = f["name"]
        desc = (f["description"]
                + f"\n\nCorpus frequency (DJLougen/hermes-agent-traces-filtered, "
                f"3,679 rows): defined in {f['rows_defined']} rows; "
                f"{f['invocations']} tool-call invocations; "
                f"{f['description_variants']} description variant(s). "
                f"System-prompt <tools> XML function-name sets agree 100% "
                f"with the row-level tools field (verified on all 3,679 rows).")
        tags = dict(base_tags(), **{
            "rows_defined": S(f["rows_defined"]),
            "invocations": S(f["invocations"]),
            "description_variants": S(f["description_variants"]),
        })
        records.append({
            "kind": "observation", "ref": "fn-" + re.sub(r"[^a-z0-9-]", "-", name.lower())[:60],
            "body": {
                "type": "intel.behavior",
                "data_schema": "urn:factum:intel:behavior:1",
                "data": {
                    "category": name,
                    "description": desc,
                    "models_affected": ["multiple-frontier-models (upstream: dataset card)"],
                    "provenance": ("DJLougen/hermes-agent-traces-filtered "
                                    "function inventory (Hermes agent harness)"),
                },
                "source": "@src",
                "observed_at": OBSERVED_AT,
                "time_basis": "source_metadata",
                "files": [],
            },
            "tags": tags,
        })

    # --- shell first-token records ---
    used_refs = set(r["ref"] for r in records)
    for t0, inv in tok_inv.most_common():
        ex = [cmd for _, cmd in tok_ex[t0][:5]]
        desc = (f"Shell first-token '{t0}' invoked {inv} times across "
                f"{tok_distinct[t0]} distinct command strings in the hermes "
                f"agent traces (terminal/execute_code/shell tool calls). "
                f"Top verbatim exemplars:\n"
                + "\n".join(f"- {c}" for c in ex))
        slug = re.sub(r"[^a-z0-9-]", "-", t0.lower())[:40] or "empty"
        ref = "sh-" + slug
        n = 2
        while ref in used_refs:  # slug collisions (punctuation normalized away)
            ref = f"sh-{slug}-{n}"
            n += 1
        used_refs.add(ref)
        records.append({
            "kind": "observation", "ref": ref,
            "body": {
                "type": "intel.behavior",
                "data_schema": "urn:factum:intel:behavior:1",
                "data": {
                    "category": "shell-command",
                    "description": desc,
                    "models_affected": ["multiple-frontier-models (upstream: dataset card)"],
                    "provenance": ("DJLougen/hermes-agent-traces-filtered "
                                    "shell-command aggregation (Hermes agent harness)"),
                },
                "source": "@src",
                "observed_at": OBSERVED_AT,
                "time_basis": "source_metadata",
                "files": [],
            },
            "tags": dict(base_tags(), **{
                "first_token": t0,
                "invocations": S(inv),
                "distinct_commands": S(tok_distinct[t0]),
            }),
        })

    # --- URL records ---
    n_url = 0
    for u in url_sel:
        term = u["url"]
        if not check(term, "infra.ioc"):
            continue
        n_url += 1
        records.append({
            "kind": "observation", "ref": f"url-{n_url:04d}",
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {
                    "term": term,
                    "category": "url-pattern",
                    "provenance": (f"2026-10-11-hf-traj-hermes aggregation of "
                                    f"DJLougen/hermes-agent-traces-filtered "
                                    f"data/train.jsonl; {u['count']} mentions "
                                    f"across 3,679 rows"),
                    "status": "candidate",
                },
                "source": "@src",
                "observed_at": OBSERVED_AT,
                "time_basis": "source_metadata",
                "files": [],
            },
            "tags": dict(base_tags(), **{"mentions": S(u["count"])}),
        })

    # --- host records ---
    n_host = 0
    for h in host_sel:
        if not check(h, "infra.ioc"):
            continue
        n_host += 1
        records.append({
            "kind": "observation", "ref": f"host-{n_host:04d}",
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {
                    "term": h,
                    "category": "domain",
                    "provenance": (f"2026-10-11-hf-traj-hermes aggregation of "
                                    f"DJLougen/hermes-agent-traces-filtered "
                                    f"data/train.jsonl; {hosts_m[h]} URL mentions "
                                    f"({hosts_d[h]} distinct URLs) across 3,679 rows"),
                    "status": "candidate",
                },
                "source": "@src",
                "observed_at": OBSERVED_AT,
                "time_basis": "source_metadata",
                "files": [],
            },
            "tags": dict(base_tags(), **{
                "mentions": S(hosts_m[h]),
                "distinct_urls": S(hosts_d[h]),
            }),
        })

    # --- claims ---
    claims = [
        ("model-nonuniform",
         "model uniformity",
         "Rows carry no model field (keys: category, conversations, id, "
         "subcategory, task, tools; 0 of 3,679 rows have a model key). The "
         "dataset card states 'Source model: Multiple frontier models' "
         "(README 'How This Compares' table). The traces are NOT uniformly "
         "hermes; tagged model=multiple-frontier-models.",
         "OBSERVED"),
        ("tools-xml-agreement",
         "tool-definition source agreement",
         "Function definitions parsed from the system-prompt <tools> XML "
         "agree 100% with the row-level 'tools' field (name sets identical) "
         "on all 3,679 rows; 67,963 <tool_call> blocks parsed with 0 "
         "failures.",
         "OBSERVED"),
        ("tool-count-discrepancy",
         "tool-count discrepancy vs README",
         "The dataset README claims '55 unique tools' but the extraction "
         "found 26 distinct function names across all 3,679 rows "
         "(single description variant each).",
         "OBSERVED"),
    ]
    for slug, prop, value, basis in claims:
        records.append({
            "kind": "claim", "ref": "claim-" + slug,
            "body": {
                "subject": "@run",
                "property": prop,
                "value": value,
                "basis": basis,
                "cites": ["@run"],
            },
            "tags": base_tags(),
        })

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "factum-lane-ingest-2026-10-11-hf-traj-hermes",
        "tags": {"lane": LANE_TAG},
        "records": records,
    }
    json.dump(bundle, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")
    print(f"bundle: {len(records)} records "
          f"(1 source + 1 run + 26 fn + {len(tok_inv)} shell + "
          f"{n_url} url + {n_host} host + {len(claims)} claims); "
          f"skipped exact dupes: {len(skipped_dupes)}",
          file=sys.stderr)
    if skipped_dupes:
        with open(os.path.join(WORK, "skipped_dupes.json"), "w") as f:
            json.dump([{"type": t, "term": x} for t, x in skipped_dupes], f, indent=1)


if __name__ == "__main__":
    main()
