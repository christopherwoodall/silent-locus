#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-09-29-separate-eval-test.

Reads the legacy events.jsonl VERBATIM (no retyping) and emits:
  - 1 run record (extraction)
  - 1 source record (the legacy events.jsonl)
  - 19 source records (upstream URLs + one repo-local note)
  - 9 claim records (graded verdicts, full verbatim label bodies)

Claim shape follows the corpus convention (e.g. claim_0513f195238b4a59abffb913a5651730):
subject = the extraction run, cites = [run] (+ captured JFrog
artifact/observation for the ExploitGym candidate), value = full verbatim
legacy record. Claims cannot cite source records (schema REFERENCE_TYPE
restricts cites to observation/sighting/artifact/claim/run); the upstream
URL sources stand as lane-tagged provenance records instead.
The JFrog GemStuffer post was captured separately via `factum capture`
(artifact/source/web.capture); those IDs are cited directly.
"""
import json
import sys

REPO = "/home/hatch/workspace/silent-locus"
LANE_DIR = f"{REPO}/data/lanes/2026-09-29-separate-eval-test"
LANE_TAG = "2026-09-29-separate-eval-test"
LANE_ID = "lane_40c7f11553c341f69565757813541c43"
ACTOR = "agent:lane-ingest-2026-09-29-separate-eval-test"
JFROG_ARTIFACT_ID = "artifact_20ba11686644455eb1c83b754bb8c71f"  # factum capture
JFROG_OBSERVATION_ID = "observation_d32d5721d4384c049fc27c02d295998f"  # web.capture

BASE_TAGS = {"lane": LANE_TAG, "legacy_dataset": LANE_TAG}


def tags(grade):
    t = dict(BASE_TAGS)
    t["grade"] = grade
    return t


SOURCES = [
    ("src-arxiv-2505-15216", "web",
     "https://arxiv.org/pdf/2505.15216",
     "BountyBench paper (arXiv 2505.15216)"),
    ("src-bountybench-repo", "web",
     "https://github.com/bountybench/bountybench",
     "BountyBench repository"),
    ("src-bountybench-blog", "web",
     "https://github.com/stanfordvl/sail-blog/blob/HEAD/_posts/2025-06-11-bountybench.md",
     "BountyBench SAIL blog post"),
    ("src-arxiv-2503-17332", "web",
     "https://arxiv.org/pdf/2503.17332",
     "CVE-Bench paper (arXiv 2503.17332)"),
    ("src-cvebench-repo", "web",
     "https://github.com/uiuc-kang-lab/cve-bench",
     "CVE-Bench repository"),
    ("src-arxiv-2410-03225", "web",
     "https://arxiv.org/html/2410.03225v2",
     "AutoPenBench paper (arXiv 2410.03225)"),
    ("src-autopenbench-repo", "web",
     "https://github.com/lucagioacchini/auto-pen-bench",
     "AutoPenBench repository"),
    ("src-arxiv-2408-08926", "web",
     "https://arxiv.org/abs/2408.08926",
     "Cybench paper (arXiv 2408.08926)"),
    ("src-cybench-readme", "web",
     "https://github.com/andyzorigin/cybench/blob/HEAD/benchmark/README.md",
     "Cybench benchmark README"),
    ("src-cyberai-landscape", "web",
     "https://github.com/evkir/cyberai/blob/HEAD/docs/competitive-landscape-2026.md",
     "ARTEMIS competitive-landscape entry (evkir/cyberai)"),
    ("src-terminator-sota", "web",
     "https://github.com/r00t-kim/terminator/blob/HEAD/research/llm_bug_bounty_sota_2024_2026.md",
     "LLM bug-bounty SOTA survey (r00t-kim/terminator)"),
    ("src-spartech-xbow", "web",
     "https://www.spartechsoftware.com/cybersecurity-news/xbow-achieves-a-groundbreaking-milestone-as-the-first-ai-system-to-surpass-human-hackers-in-the-hackerone-competition/",
     "XBOW HackerOne #1 milestone (Spartech Software)"),
    ("src-arxiv-2607-11288", "web",
     "https://arxiv.org/abs/2607.11288",
     "Mako paper (arXiv 2607.11288)"),
    ("src-rubygems-advisory", "web",
     "https://github.com/rubygems/blog/blob/HEAD/_posts/2026-07-22-security-advisory-legacy-api-key-leak.md",
     "RubyGems legacy API-key leak security advisory (2026-07-22)"),
    ("src-hackerone-rubygems", "web",
     "https://hackerone.com/rubygems",
     "RubyGems HackerOne program page"),
    ("src-hackerone-disclosed", "web",
     "https://github.com/ajaysenr/hackerone-disclosed-reports/blob/HEAD/by-year/2026.md",
     "hackerone-disclosed-reports by-year/2026.md (ajaysenr)"),
    ("src-rubyhack", "web",
     "https://www.rubyhack.ai",
     "rubyhack.ai GemStuffer report (Nightingale Collective)"),
    ("src-aitldr-rubyhack", "web",
     "https://ai-tldr.dev/releases/rubyhack-openai-rubygems-attack/",
     "rubyhack-openai-rubygems-attack (ai-tldr.dev)"),
    ("src-note-exploitgym", "repo-note",
     "notes/analyst-note-exploitgym-2026-09-28.md",
     "analyst-note-exploitgym-2026-09-28.md (repo-local note)"),
]

# candidate name -> extra cite IDs beyond the extraction run
EXTRA_CITES = {
    "Off-task exploration by escaped ExploitGym agents (favored hypothesis — red-teamed)": [
        JFROG_ARTIFACT_ID, JFROG_OBSERVATION_ID],
}


def main():
    events = []
    with open(f"{LANE_DIR}/events.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip():
                events.append(json.loads(line))
    assert len(events) == 9, f"expected 9 events, got {len(events)}"
    # intra-batch dedup by candidate name
    names = [e["labels"]["name"] for e in events]
    assert len(set(names)) == 9, f"duplicate candidate names: {names}"

    records = []

    records.append({
        "kind": "run",
        "ref": "run-ingest",
        "tags": tags("OBSERVED"),
        "body": {
            "run_kind": "extraction",
            "tool": "build_ingest.py (lane 2026-09-29-separate-eval-test)",
            "params": {
                "question": ("Red-team falsification: find a better explanation "
                             "for the July-7 RubyGems XSS/SSTI wave than "
                             "off-task exploration by escaped ExploitGym agents."),
                "source_corpus": "data/lanes/2026-09-29-separate-eval-test/events.jsonl",
                "record_kind": "eval_candidate",
            },
            "coverage": {
                "description": ("9 eval_candidate events (candidate benchmarks/operators "
                                "assessed as artifact source of the July-7 RubyGems wave); "
                                "labels preserved verbatim."),
                "scanned": 9,
                "total": 9,
                "complete": True,
            },
        },
    })

    records.append({
        "kind": "source",
        "ref": "src-events-jsonl",
        "tags": tags("OBSERVED"),
        "body": {
            "source_type": "submitted",
            "locator": "data/lanes/2026-09-29-separate-eval-test/events.jsonl",
            "title": "9 eval_candidate events (2026-09-29-separate-eval-test)",
        },
    })

    for ref, source_type, locator, title in SOURCES:
        records.append({
            "kind": "source",
            "ref": ref,
            "tags": tags("OBSERVED"),
            "body": {
                "source_type": source_type,
                "locator": locator,
                "title": title,
            },
        })

    for i, ev in enumerate(events):
        labels = ev["labels"]
        name = labels["name"]
        claim_tags = tags("INFERENCE")
        claim_tags["legacy_record_kind"] = ev["record_kind"]
        claim_tags["legacy_fingerprint"] = ev["fingerprint"]
        records.append({
            "kind": "claim",
            "ref": f"claim-candidate-{i}",
            "tags": claim_tags,
            "body": {
                "subject": "@run-ingest",
                "property": "july-7-rubygems-wave-artifact-source-verdict",
                "value": {
                    "record_kind": ev["record_kind"],
                    "dataset": ev["event"]["dataset"],
                    "legacy_fingerprint": ev["fingerprint"],
                    "timestamp": ev["@timestamp"],
                    "timestamp_source": labels["timestamp_source"],
                    "name": name,
                    "operator": labels["operator"],
                    "date": labels["date"],
                    "task_list": labels["task_list"],
                    "mechanism_match": labels["mechanism_match"],
                    "artifact_shape_fit": labels["artifact_shape_fit"],
                    "verdict": labels["verdict"],
                    "verdict_reason": labels["verdict_reason"],
                    "sources": labels["sources"],
                },
                "basis": "INFERENCE",
                "cites": ["@run-ingest"] + EXTRA_CITES.get(name, []),
                "note": ("Red-team falsification verdict on candidate artifact "
                         "source for the July-7 RubyGems XSS/SSTI wave "
                         "(worker 4, 2026-09-28). Verdict NO/WEAK is analyst "
                         "inference from public upstream sources; verbatim "
                         "sources list preserved in value.sources."),
            },
        })

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "separate-eval-test-ingest-2026-10-09",
        "lane": LANE_ID,
        "tags": tags("OBSERVED"),
        "records": records,
    }
    out = "/tmp/se-ingest/bundle.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=1)
    print(f"wrote {out}: {len(records)} records "
          f"({sum(1 for r in records if r['kind']=='claim')} claims, "
          f"{sum(1 for r in records if r['kind']=='source')} sources, "
          f"{sum(1 for r in records if r['kind']=='run')} runs)")


if __name__ == "__main__":
    main()
