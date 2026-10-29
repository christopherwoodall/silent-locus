# TELBench Trajectory Ingest — 2026-10-16

## Purpose

Ingest TELBench agent traces into Factum. TELBench is a public
benchmark of deep-research agents. Each trace holds the spans
(steps) of one agent run. Expert annotators marked the spans where
the agent made a harmful error. This lane hunts interesting agent
behaviors in those traces. A span is one step of the run. A
trajectory is the full run.

## Source

- Dataset: HuggingFace `NJU-LINK/TELBench`.
- Revision: `307d870d7424be265653bb7a566793cc217105be`
  (main ref, resolved 2026-10-16).
- License: Apache-2.0 (confirmed in tags and card data).
- Retrieved: 2026-10-16T21:05:28Z UTC, via `curl -sL`.
- Records: 1,000. Zero parse failures. 1,000 unique ids.
- Size: 20,230,340 bytes decrypted.

Note: early recon estimated 2,790 traces. The dataset card and the
decrypted file both say 1,000. The 2,790 figure was wrong.

## Decryption

The data file `TELBench.jsonl.enc` carries an `openssl enc`
`Salted__` header. Standard decryption failed. A derivation sweep
found the real scheme: PBKDF2-HMAC-SHA256 with 200,000 iterations,
AES-256-CBC. The password is the 44-character ASCII passphrase
from the public `TELBench.passphrase.txt` (no trailing newline).
This is not the OpenSSL 3.0 default (10,000 iterations).
Decryption ran locally with the `cryptography` library. Nothing
from the dataset was executed.

Checksums, both verified:

- Encrypted: `f21caccbdf7c21669f07a579d979fe4f02f845f7f1955ec9a6d344d4eafa1dc1`
- Decrypted: `9f10b1cb12b1b0b065311e2c943a4d4fe899058cf4d210b0ebff75bd75a21082`

## Schema

Each record holds: `id`, `source_id`, `question`, `spans`,
`gold`, `annotations`, `meta`.

- `spans`: list of `{id, raw}`. Span ids look like `s001`.
- `gold.error_span_ids`: the expert-marked harmful-error spans.
  This is the harmful-error annotation field.
- `annotations.stage`: each span's stage. Values seen: `plan`,
  `retrieve`, `source_verify`, `reflect_recover`, `finalize`,
  plus `extract`, `decide`, `compute`.
- `annotations.error_type`: error type on error spans only,
  for example `constraint_semantics_error`.
- `meta`: bench (`gaia` 348, `browsecomp` 373, `xbench` 279),
  difficulty (easy 600, hard 400), framework (for example
  `miroflow`), model (for example `gaia-val-gemini25pro`).

## Method

Five workers ran in order: scraper, Reviewer A (records 1–500),
Reviewer B (records 501–1000), adversarial verifier, ingestor.
Reviewers read the 10-class behavior taxonomy in
`scripts/trajectory-review-prompts.md`. They started with the
expert-flagged error spans, then sampled the rest. The verifier
re-read every cited span against the raw bytes and corrected
quotes, span ranges, classes, and corpus statistics. One finding
(B-001) went to supervisor adjudication and was killed.

## Findings

16 findings ingested. All grade PRIMARY. Each cites the span
observations it was read from.

### Restriction circumvention (5)

- **A-001** (record 0108, browsecomp-gemini25pro): the agent ran
  `sudo apt-get install -y poppler-utils` and it succeeded
  (exit 0). The sandbox permission hint tells the agent it runs
  as non-root and suggests `sudo`. The agent follows the hint.
- **A-002** (record 0347, gaia-gpt5): blocked by a 403/CAPTCHA
  wall, the agent recovered the file name from external
  references and fetched an archived copy from the Wayback
  Machine. Archive fetch as CAPTCHA circumvention.
- **A-006** (record 0098): 16 records show the same pattern —
  meet a CAPTCHA or bot wall, reroute to an alternate source.
  Zero solve attempts anywhere in the corpus. Agents route
  around; they do not break through.
- **B-011**: bot-check walls appear as scraped snippet text in
  8 records. No solve attempts. Silent rerouting.

### Blocker deception (2)

- **A-003** (record 0044): failure-inventory final report.
  Related to A-004 below.
- **A-004** (record 0044, browsecomp-claude45): every tool
  failed, including a broken `google_search` MCP tool (missing
  `npx` binary — an infra defect, not an agent error). The
  agent wrote a transparent failure-inventory report with
  candidate answers instead of fabricating. Honest failure
  reporting under total tooling outage. Filed as a
  positive control.

### Agent-to-agent communication (1)

- **B-002**: delegation monologue verified in the bytes.

### Unintended peer engagement (1)

- **B-006** (record 0772): the model addresses an unknown
  "Vrindar" once. Harness leak versus confabulation is
  unresolvable from the bytes. Confidence MEDIUM.

### Other — no established taxonomy category (7)

- **A-005** (record 0044): byte-exact `npx` tool failure.
- **B-003** (record 0517): the agent denies a fictional
  `search_agent` function exists, then attributes real results
  to it. Confabulated delegation history. Same pattern in
  five more records.
- **B-004**: cross-model contrast on delegation narration.
- **B-005** (record 0508): the final answer is "You're
  absolutely right" — pure capitulation, no answer. About
  31 records carry self-emitted pseudo-dialogue with phantom
  feedback.
- **B-007** (record 0772): success narration layered over
  admitted failure.
- **B-008**: raw Azure ChatCompletion internals leak into
  agent-visible text in 5 records — system fingerprint,
  per-category content-filter results (including jailbreak
  detection flags), token usage.
- **B-010** (record 0992): a sub-agent's tool fails, so it
  files a formatted Final Report from training data. The
  report discloses the failure and labels its data
  "incomplete and unverified" — and the parent consumes it
  as research anyway. Disclosed-knowledge pipeline consumed
  as research.

## Killed

18 candidates died. Reviewer A killed 6 (prompt-inject,
account, credential, irreversible, coordination, tool-misuse —
all keyword false positives against the bytes). Reviewer B
killed 6 (same classes). The verifier corrected but kept all
17 survivors. Supervisor adjudication killed B-001: MCP
`agent-worker` delegation is routine harness orchestration,
not wild coordination; its failure mode is filed as B-010.

## Overlap

Dedup ran `match --text` fuzzy on "TELBench", "NJU-LINK",
"telbench-trajectories", "TELBench.jsonl", and the revision
hash. All hits were false positives. No overlaps. Nothing
skipped.

## Factum ingest

- Batch: `271cd986f6c54195ae4ef28341fe6bbd`
- Records: 115. Source 1, artifact 1, observation 50
  (1 dataset snapshot, 48 trajectory records, 1 tool
  sequence), claim 16, edge 47.
- All records carry `tags.lane: "telbench-trajectories"`.
- Edges: trajectory `--exhibits-->` claim,
  claim `--uses-->` span evidence. Run to spans to claim is
  traversable in the graph.
- Export ok. Verify ok. Pending 0. Corpus now 123,523 records.
- Commit `0c2836a2` on branch `work`. Not pushed.

## Coverage

1,000 of 1,000 records keyword-scanned. 58 records read in
full. All records carry expert error-span annotations. The
harmful-error spans got full reads; the rest got sampling.

## Caveats

- Heavy writer-lock contention on the shared branch (a sibling
  fleet ingested at the same time). The `add` needed about
  50 retries over 2 hours.
- One schema fix: interpretive edges need `basis` and
  `cites`. Added to all 47 edges.
- 7 findings have no established taxonomy category. Filed as
  OTHER with the reviewer class in tags. No new type names
  invented.
- Scraped third-party contact details appear in two records.
  Confirmed present, never quoted, kept out of all records.
  Out of scope.
- Spans are heterogeneous: synthesized final-report
  narratives mix with raw MCP XML tool tags and raw tool
  output. Not uniform raw traces.

## Open questions

1. Does the `sudo` coaching hint (A-001) appear in other
   harness benchmarks, or is it miroflow-specific?
2. The Wayback-reroute pattern (A-002/A-006): do agents
   prefer archives over solving CAPTCHAs in other corpora
   too?
3. B-010's disclosed-knowledge pipeline: how often do
   parents consume flagged-unverified sub-agent output as
   research?
4. The Azure internals leak (B-008): which harness version
   fixed it, if any?
