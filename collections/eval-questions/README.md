# eval-questions collection (EVALHUNT / W2-DOWNLOADS)

Banked 2026-10-05. Raw downloads are byte-identical under each `<eval-slug>/raw/`.
Normalized questions in `<eval-slug>/questions.jsonl`: one JSON object per line with
`eval, eval_org, question_id, question, topic, license, retrieved`.
Per-eval provenance, counts, and quirks in `<eval-slug>/NOTES.md`.
Tooling (stdlib-only parquet reader + normalizer) in `_tools/`.

## Banked question sets (10,201 questions total)

| eval | banked / expected | notes |
|---|---|---|
| openai-simpleqa | 4326 / 4326 ✓ | per-question urls in metadata |
| google-facts-grounding | 860 / 860 ✓ | |
| google-frames | 824 / 824 ✓ | |
| assistantbench | 181 / 214 ⚠ | public test file really is 181 (verified via datasets-server parquet); paper's 214 = test 181 + dev 33 |
| mind2web | 1009 / 2350 ⚠ | train only; test.zip password-encrypted (`mind2web`, public) and authors forbid redistributing unzipped test data — test count verified 1341, sum = 2350 ✓ |
| webvoyager | 643 / 643 ✓ | inventory URL (tasks_test.jsonl) is a 1-task stub; real set is WebVoyager_data.jsonl (also banked) |
| webarena | 812 / 812 ✓ | self-hosted env tasks, limited live-web trace value |
| tau-bench | 165 / 165 ✓ | 50 airline + 115 retail |
| sealqa | 619 / 619 ✓ | parsed with custom stdlib parquet reader (see NOTES.md) |
| webwalkerqa | 680 / 680 ✓ | |
| openai-mle-bench | 82 / 75 ⚠ | repo ships 82 task descriptions vs paper's 75 |

## Raw-only / skipped

- swe-bench, anthropic-evals: wrong shape (banked raw only, by design)
- xbench-deepsearch: encrypted by design; decrypt trivial (XOR+canary) but author asks not to upload plaintext online — encrypted raw banked, plaintext skipped
- browsecomp, browsecomp-zh: encrypted by design, no public key — encrypted raw banked
- gaia, humanitys-last-exam: HF gated (401 unauthenticated) — nothing banked
- meta / xai / deepseek: no public eval corpus found (per inventory)
