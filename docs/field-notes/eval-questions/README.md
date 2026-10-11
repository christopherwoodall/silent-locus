# eval-questions collection (EVALHUNT)

Banked 2026-10-05. **10,201 questions across 11 evals** (DeepSearchQA banked
separately, untouched). Raw downloads are byte-identical under each
`<eval-slug>/raw/`; normalized questions in `<eval-slug>/questions.jsonl`.
Per-eval provenance, counts, and quirks in `<eval-slug>/NOTES.md`. Licenses
are recorded per eval (see the table below and `EVAL_QUESTIONS.md`).
Tooling (stdlib-only parquet reader + normalizer) in `_tools/`.

## Unified corpus

| Artifact | Contents |
|---|---|
| `all-questions.jsonl` | All 10,201 questions in one file, enriched 2026-10-05. Schema per line: `eval, eval_org, question_id, question, topic, license, retrieved, expected_sources[]` (`expected_sources` = expected-source domains/URLs from metadata) |
| [EVAL_QUESTIONS.md](EVAL_QUESTIONS.md) | Unified-corpus document: per-eval question counts, license per eval, enrichment provenance |
| [HUNT-QUERIES.md](HUNT-QUERIES.md) | Hunt brief: top 50 ranked fingerprint phrases (corpus-uniqueness × entity rarity × trace-likelihood) with urlquery.net (`q=`, `url.domain:`) and urlscan.io (`page.title:`, `task.url:`, `domain:`) query conventions. Precedent: DeepSearchQA dsqa_250 verbatim-matched the 2026-06-17 DoE incident task — one verbatim hit is gold |

## Banked question sets (10,201 questions total)

| eval | banked / expected | license | notes |
|---|---|---|---|
| openai-simpleqa | 4326 / 4326 ✓ | MIT | per-question urls in metadata |
| google-facts-grounding | 860 / 860 ✓ | cc-by-4.0 | |
| google-frames | 824 / 824 ✓ | apache-2.0 | |
| assistantbench | 181 / 214 ⚠ | apache-2.0 | public test file really is 181 (verified via datasets-server parquet); paper's 214 = test 181 + dev 33 |
| mind2web | 1009 / 2350 ⚠ | cc-by-4.0 | train only; test.zip password-encrypted (`mind2web`, public) and authors forbid redistributing unzipped test data — test count verified 1341, sum = 2350 ✓ |
| webvoyager | 643 / 643 ✓ | apache-2.0 | inventory URL (tasks_test.jsonl) is a 1-task stub; real set is WebVoyager_data.jsonl (also banked) |
| webarena | 812 / 812 ✓ | apache-2.0 | self-hosted env tasks, limited live-web trace value |
| tau-bench | 165 / 165 ✓ | MIT | 50 airline + 115 retail |
| sealqa | 619 / 619 ✓ | apache-2.0 | parsed with custom stdlib parquet reader (see NOTES.md) |
| webwalkerqa | 680 / 680 ✓ | apache-2.0 | |
| openai-mle-bench | 82 / 75 ⚠ | MIT | repo ships 82 task descriptions vs paper's 75 |

## Raw-only / skipped

- swe-bench, anthropic-evals: wrong shape (banked raw only, by design)
- xbench-deepsearch: encrypted by design; decrypt trivial (XOR+canary) but author asks not to upload plaintext online — encrypted raw banked, plaintext skipped
- browsecomp, browsecomp-zh: encrypted by design, no public key — encrypted raw banked
- gaia, humanitys-last-exam: HF gated (401 unauthenticated) — nothing banked
- meta / xai / deepseek: no public eval corpus found (per inventory)
