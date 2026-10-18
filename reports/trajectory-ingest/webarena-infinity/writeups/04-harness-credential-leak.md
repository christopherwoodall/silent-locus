# WebArena Infinity: an API token persisted in trajectory metadata

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

A credential-like API token (prefixed `ak-`) and an organization identifier sit in plain text inside `result.json` error strings in at least two kimi trajectories. This is harness-side secret handling, not agent behavior: the token rode along in an API error message, and the benchmark persisted the message into the shipped corpus. Counting unit: 1 verified finding (RB-008), 2 observed instances, of 21 verified findings total.

Note on evidence handling: the token value and the organization identifier are deliberately withheld from this writeup. They were confirmed present in raw bytes, never copied into any working file, and the raw bytes are untouched.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: Reviewer B enumerated all 40 result.json error trajectories and read the kimi 429-error cases in full.
- Counting unit: n = 1 finding; 2 observed instances (task_e17, task_e20). n does NOT count the tokens — no value is reproduced anywhere in this report.

## 3. What happened

In `raw/kimi/elation-prescriptions/task_e17/result.json`, the errors array opens with a 305-character string: "Step 0: API error after 2 attempts: Error code: 429 - ..." whose embedded server message contains the account's organization identifier and a credential-shaped `ak-` prefixed token value, followed by "is suspended due to insufficient balance". The harness ran inference, hit a rate-limit/quota error, captured the provider's error text verbatim, and stored it in the trajectory metadata that ships with the dataset. The sibling trajectory task_e20 shows the same pattern.

## 4. Evidence

- **RB-008**, trajectory `kimi/elation-prescriptions/task_e17`, step 0, `result.json` errors[0]. Quote (token and org id withheld): "result.json errors[0] (305-char string): 'Step 0: API error after 2 attempts: Error code: 429 - {"error": {"message": "Your account <org-id> <ak- TOKEN> is suspended due to insufficient balance..."}}'. Credential-like ak- prefixed token value present in the stored error string; same pattern in sibling task_e20 result.json. Token value and org identifier deliberately withheld from this record."
- Files: `raw/kimi/elation-prescriptions/task_e17/history.json` (sha256 `ff21f6e1…`), `raw/kimi/elation-prescriptions/task_e17/result.json` (sha256 `4ad3a634…`). Sibling: `raw/kimi/elation-prescriptions/task_e20/result.json`.
- The token value and org identifier were verified in raw bytes and are not reproduced in any writeup, finding record, or working file.

## 5. Novelty

This is a new byte-verified instance of dataset secret-contamination, not a first discovery of the mechanism. Secret leakage into logs and persisted artifacts is a known infrastructure failure class. The internal-corpus overlap check found zero overlap. What this adds: a concrete contaminated corpus (public, mit-licensed, 2,329 trajectories) with byte pointers to the contaminated records — actionable for dataset hygiene, not for agent-TTP analysis. Filed as infrastructure, not as agent behavior.

## 6. Why it matters

Public trajectory corpora are training data. A credential-shaped token persisted in metadata is one scrape away from entering a training set, a vector index, or a retrieval cache — where it becomes far harder to remove. The error string also reveals operational facts (which account, quota state). The fix is trivial and one-directional: sanitize provider error text before persisting. Anyone redistributing or fine-tuning on this revision should know the two records exist so they can scrub them.

## 7. Uncertainties

- Is the `ak-` value a live credential or a revoked/test token? Cannot be established from the bytes. The writeup withholds it either way — a suspended-account token can still be a valid identifier and the same pattern can recur with live keys.
- Was the token the benchmark operator's own inference key? Most likely (it appears in the operator's inference error path), but this is an inference, not an observed fact.
- The full-corpus extent is unknown: only task_e17 and task_e20 were confirmed. A full regex sweep for `ak-` across all result.json files is an open gap.
- Per house rules, the raw bytes were not altered — no redaction was applied to the local copies. The finding flags the pattern; cleanup of the public dataset is the operator's call.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; no demonstrated credential use; the value was not replayed or tested). Cyberattack: None.
- Near-miss translation: the same persistence path with a live, funded key would publish a working credential into a public dataset. The demonstrated weakness is the persistence pipeline (unsanitized provider error text stored in shipped metadata), not any agent action.
- Disposition: we did not replay the error, test the token, or attempt any use of it. Read-only analysis. Fix owner: `task_author`/`environment` (sanitize error strings before persisting trajectory metadata).
