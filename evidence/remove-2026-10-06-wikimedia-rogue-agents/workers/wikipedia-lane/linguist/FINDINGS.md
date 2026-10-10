# LINGUIST findings — language/content patterns, wikipedia edit hunt
Worker: linguist | Branch: wikipedia-edit-hunt-2026-10-06 | Coverage: 54 CSV diff URLs → 49 revisions (5 meta Web2Cit oldids nonexistent)
Scope note: agent-SHAPE markers only. No stylometric attribution to any human identity. All claims graded OBSERVED / INFERENCE / UPSTREAM.

## 1. Edit comments (complete, n=49)

Frequency table (from revisions.tsv; 1 empty comment excluded):

| comment | count |
|---|---|
| `test` | 17 |
| `Temporary technical sandbox initialization` | 7 |
| `sandbox test` | 6 |
| `sandbox` | 3 |
| `test external link` | 2 |
| `t` | 2 |
| `sandbox test link` | 2 |
| `clear sandbox` | 2 |
| `Sandbox link test` | 2 |
| `тест` | 1 |
| `testing external link` | 1 |
| `test link` | 1 |
| `temp` | 1 |
| `OCR test` | 1 |

OBSERVED facts:
- 48 of 49 comments are single short functional tokens; zero descriptive, zero conversational, zero typo'd summaries. The entire vocabulary is ~10 test-words (test/sandbox/link/external/clear/temp/OCR) recombined.
- Link-test comment cluster: `test link` / `sandbox test link` (x2) / `test external link` (x2) / `testing external link` / `Sandbox link test` (x2) — near-identical paraphrase variants across different accounts and wikis. INFERENCE: suggests a natural-language intent ("test external link") being paraphrased per run, not a hardcoded string — consistent with an agent emitting summaries per-task rather than a human's stable habits or a copied template.
- `Temporary technical sandbox initialization` — byte-identical 7x across commons (1), incubator (5), meta (1), all by ~2026-* temp accounts on 2026-06-25 within ~2h. OBSERVED: this is NOT any MediaWiki default or tool-generated summary; it is a bespoke multi-word template string. INFERENCE: agent-side boilerplate used for a distinct operation phase (bulk "technical initialization" run on Jun 25). Its formality ("technical sandbox initialization") reads like task-language from an instruction, not an organic editor's summary.
- `t` (x2, incubator 7226109/7226110, seconds apart, same ~2026-* run sequence) and `temp` (x1, incubator 7226107) — degenerate minimal summaries inside a rapid same-minute burst, plausibly a summarizer emitting fragments under a token budget or a fall-through default.
- 1 empty comment (en 1353492663, ~2026-28217-20, 2026-05-10) — the only commentless edit; also the only revision with a section header added (see §2).
- 1 non-English comment: `тест` (Bulgarian for "test") on bg.wikipedia sandbox (12923296, ~2026-31341-00). OBSERVED: operator localized the token for the target wiki's language. INFERENCE: intent-to-context adaptation — it rendered the test token in the wiki's language rather than pasting English. Language proficiency: minimal (single word), no fluency signal either way.
- MediaWiki-generated edit tags on sandbox rows are standard maintenance tags only (`mw-reverted`, `mw-manual-revert`, `mw-removed-redirect`, `mw-new-redirect`) — OBSERVED: the reverts were performed by the platform/patrollers, tags indicate revert *receipt*, not operator tooling.
- UPSTREAM (seed article): sandbox edits described as test edits by temp accounts ~2026-*. Corroborated in revisions.tsv (all sandbox users match `~2026-*` pattern, May–Jun 2026).

## 2. Diff content analysis (sandbox edits)

[collection in progress — extractor results to be appended]
