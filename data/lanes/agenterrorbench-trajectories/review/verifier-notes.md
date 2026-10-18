# AgentErrorBench trajectory review — verifier notes — 2026-10-16

## Method

Read every cited trajectory file from raw bytes. Recomputed sha256 for all
25 files and compared it with the finding's provenance hash and with the
sibling `.PROVENANCE.txt`. Extracted the cited step ranges and checked each
quote against the bytes. Checked observation history to test every
"never observed" claim. Ran Factum fuzzy `match` on 11 key terms and
grepped `data/records/` directly for the distinctive terms (authoritative
scan). Checked Reviewer B's kill list with 2 spot checks.

## Results

- KEEP: 23. KILL: 2 (A-012, A-016). OVERLAP: 0.
- Corrected quotes: 8 (A-001, A-003, A-009, A-010, A-011, A-013, A-014, A-017).
  Minor count corrections: B-001, B-008.
- Confidence lowered to MEDIUM on 5 (A-009, A-010, A-011, A-014, A-017):
  the filed "phantom object" premise died, but a weaker observed-object
  substitution survives.
- Provenance mismatches: 1 (A-016, see kill list).

## Kill list

- A-012 (Llama stoveburner-3 "hallucination"): KILLED. "stoveburner 3" is in
  the file's initial room observation; the agent went there, saw pot 2, and
  picked it up. Every element of the finding is contradicted by the bytes.
- A-016 (cross-task creditcard bleed): KILLED. Finding's sha256 does not
  match the bytes or the sibling `.PROVENANCE.txt` (transcription error).
  Substance: drawer 5 was opened at step 20 and creditcard 1 was observed in
  this same trajectory, so the action is grounded, not cross-task bleed.
  The novelty note's "verbatim in GPT-4o_012/027/040/054" is false
  (0 occurrences of that phrase in those files).

## Systematic reviewer error found

Reviewer A repeatedly filed "never observed" claims without reading the
observation history. In A-003, A-009, A-010, A-011, A-014, and A-017 the
"phantom" object or "unopened" container WAS observed, often opened and
handled, in the same trajectory. The surviving behavior family is
observed-object substitution (wrong class for the task), not phantom-object
confabulation. Reviewer A notes #3 ("phantom-object substitution ...
invent an id") inherits the same error. A-001's novelty note also wrongly
calls 020_057's "go to dresser 2" hallucinated; dresser 2 is in that file's
initial observation. Affected findings were kept with corrected quotes,
not as filed.

## Overlap

None. Factum fuzzy matches returned only unrelated records for all
11 key terms. Direct scans of `data/records/` found zero hits for
"agenterrorbench", "soapbottle", "dQw4w9WgXcQ", the CJK bleed token, or
unclosed-action-tag phrasing. Legacy-corpus grep found only unrelated
hits (an swe-bench parquet, wordlist term entries). All 23 survivors are
novel to the corpus.

## Ingest guidance

- The A-004 false-completion cluster (A-004, A-005, A-006, A-007, A-017
  step 17) spans 15 of 100 ALFWorld files. File once as a behavior
  profile with multiple trajectory observations, not as separate findings.
- The A-009/A-010/A-011/A-017/A-003 survivors form one observed-object
  substitution family. Consider one profile, not five findings.
- A-001/A-002/A-015 are one action-channel leakage family
  (unclosed tags / deliberation in the action string).
- B-004/B-005/B-006/B-007 are one buy-on-admitted-gap family; B-008 is
  separate (language bleed). Reviewer B's 7 kill decisions were
  spot-checked and stand (Qwen3-8B_002 S05, GPT-4o_004 S21: full-match
  claims, no admitted gap).

## Open doubts

1. A-002's "183 unclosed tags" recomputed as 193 net unclosed opens
   (method difference); the family-wide defect itself is solid.
2. B-001: did the rickroll URL come from pretraining memory or from a
   search result? Step-1 search results were not checked for the URL.
3. Reviewer B open question stands: do terminal `click[buy now]` actions
   complete a purchase, or does the run end before the env responds?
   No post-buy observation exists in any file.
4. A-016's finding-hash transcription error suggests the A-file hashes
   were hand-copied; all other 24 matched, so this looks isolated.
