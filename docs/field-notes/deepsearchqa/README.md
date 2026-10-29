# Lane deepsearchqa — DeepSearchQA benchmark enumeration

**Canonical dataset:** `google/deepsearchqa` — https://huggingface.co/datasets/google/deepsearchqa
**Publisher:** Google DeepMind (benchmark; paper: DeepSearchQA technical report, arxiv 2601.20975)
**License:** Apache-2.0 · **Gated:** no · **Access:** public, no auth required
**Revision pinned:** `b2623f8653065c2672de6d941fc5434cd652376c`
**Source file:** `DSQA-full.csv` (355,106 bytes)
**CSV sha256:** `25d48dcf7efa872e5467032e8b8eedf38d301f59a252d0da95cda584baa78396`

**Contents:** 900 hand-crafted multi-step web-research questions, 17 domains.
Columns: `problem`, `problem_category`, `answer`, `answer_type`
(Single Answer 35% / Set Answer 65%).

## Why this exists

Transluce's 2026-10-01 report maps the June-17 DoE civilrightsdata.ed.gov
SQL-injection probe to benchmark task **dsqa_250**, and plausibly links the
DOJ/OJJDP arrest-stats probe to another DeepSearchQA question. Eval-benchmark
tasks driving live gov-site probing is a new attribution primitive. This lane
enumerates the question set so its distinctive strings can be hunted in agent
traffic, urlquery reports, and archive-capture logs.

## qid mapping (verified)

`dsqa_<NNN>` = 0-based row index in DSQA-full.csv. Confirmed: row index 250 is
the "civilrightsdata.ed.gov 2017-2018 school year ... ratio of full-time
equivalent school counselors to students reported as victims of race-related
harassment or bullying" question that Transluce identifies as dsqa_250.

## Files

| File | Content |
|---|---|
| `collect.py` | Idempotent collector: downloads DSQA-full.csv only if missing/sha-mismatch, verifies sha256, writes questions.jsonl + state.json. Polite: curl, ≤1 req/2s. |
| `data/DSQA-full.csv` | Upstream source file (verbatim). |
| `data/questions.jsonl` | 900 rows: `{"qid","question_text","source_url","tags"}`. question_text verbatim from the benchmark. No invented rows. |
| `state.json` | Lane watermark + collection metadata. |
| `fingerprints.md` | 6 priority fingerprint strings with exact-match grep patterns + hunting notes. |

## Tag summary (questions.jsonl)

49 rows tagged `gov-data`; agency-family tags include gov-education (5),
gov-census (9), gov-bea (3), gov-cdc (3), gov-fbi (3), gov-elections (4),
gov-education-ny/tx, gov-trade, gov-usda, gov-noaa, gov-bls, gov-cia,
gov-congress, gov-nps, gov-medicaid, gov-state-dept, gov-cpsc, gov-dot,
gov-archives, gov-abs-aus, gov-clinicaltrials.

`dsqa_250` carries tag `incident-match-doe-20260617` (evidence-backed).
No OJJDP/juvenile-justice question exists in the set — the DOJ "plausible"
match is unverified; do not claim it.

## Re-run

```bash
python3 collections/deepsearchqa/collect.py   # cache hit if DSQA-full.csv unchanged
python3 collections/deepsearchqa/collect.py --rev <sha>   # pin a different revision
```
