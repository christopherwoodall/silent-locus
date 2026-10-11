# PROVENANCE — lane `2026-10-11-hf-traj-swenext`

## Source

- Dataset: `TIGER-Lab/SWE-Next-SFT-Trajectories`
  (SWE-Next SFT Trajectories, TIGER-Lab; SFT rollouts for the SWE-Next paper,
  arXiv 2603.20691, authors Jiarong Liang et al.).
- Local bytes: `evidence/hf-trajectories/raw/tiger-lab-swe-next-sft-trajectories/SWE_Next_SFT_Trajectories.jsonl`
  (215,812,925 bytes, 3,693 rows, sha256
  `0af4fc6c85d955f828cda73ce447e66e7d26350f64ec994bc48b7d6b28ac8867` —
  matches `SHA256SUMS-restored.txt`).
- Retrieval: curl from HuggingFace, 2026-10-08T11:50:53Z, rev
  `e378a60ddd7050fe9519a31a4d41d4872eeec6ac`.
- Retrieval anomaly (pre-existing, documented in `SHA256SUMS-restored.txt`):
  the 2026-10-07 pull captured 197,571,616 bytes / ~2,473 rows; the
  2026-10-08 restore captured 215,812,925 bytes / 3,693 rows. The upstream
  dataset changed between those dates. This lane uses the restored file
  (matches the HF card: 3,693 rows). A prior `dataset.snapshot` record
  (lane `hf-trajectories-audit`) records the old row_count 2473 — kept, not
  re-submitted.

## Method

- Streamed the JSONL line by line (script
  `data/lanes/2026-10-11-hf-traj-swenext/.work/extract_swenext.py`).
  The 206 MB file was never loaded into memory.
- Parsed assistant messages for `<function=NAME>...</function>` blocks and
  `<parameter=NAME>VALUE</parameter>` pairs. Parameter names were restricted
  to identifier tokens (`[A-Za-z_][A-Za-z0-9_]*`); 54 non-conforming tags
  were counted as malformed rather than aggregated (behavioral finding, not
  parser noise — the model itself writes broken XML-ish tool attempts).
- Aggregated: function-name frequency, per-function parameter distributions,
  full-corpus `execute_bash` first-command tokens (second pass, exact),
  `<parameter=path>` value frequencies, system-prompt variants, `finish`
  summaries.
- Submitted as 7 aggregated `intel.behavior` observation records
  (aggregation lane: 3,693 rows, no 1:1 ingest). No edges. No claims.
- Raw aggregates kept in
  `data/lanes/2026-10-11-hf-traj-swenext/.work/aggregates.json` and
  `bash_tokens.json` (not submitted; analysis byproducts).

## Model attribution

The dataset card says rollouts come from "expert agent rollouts" without
naming models. The released `SWE-Next-7B` / `SWE-Next-14B` models are
downstream products of this corpus, not the rollout models. No model can be
verified from the source docs → records carry `model=unverified`.

## Tags (every record)

`lane=2026-10-11-hf-traj-swenext`, `harness=swe-next`,
`source_dataset=tiger-lab-swe-next-sft-trajectories`, `model=unverified`,
`grade=OBSERVED`, `indicator=<category>`.

## Corpus coverage note

- Rows scanned: 3,693 / 3,693 (0 malformed JSON rows).
- Role counts: system 3,693 (1 prompt variant), user 3,692 (row index 3657 has
  system/assistant/tool turns only, no user message — observed in bytes),
  assistant 100,595, tool 96,902.

## Raw source removal (2026-10-11)
Behavioral extraction complete. All extractable signals ingested into Factum.
Raw source files removed from evidence/hf-trajectories/ after verification.
