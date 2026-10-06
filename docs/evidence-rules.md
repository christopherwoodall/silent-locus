# Evidence rules: the contract

Every contributor — human or agent — works under this contract. It exists
so that a reader can trust any file in this repo without knowing who wrote
it.

## 1. Never redact from evidence

Evidence files keep **full observed values, always**. No `[REDACTED]`
placeholders, no `***` masking, no truncated tokens, no withheld octets —
even for keys, tokens, and webhook URLs.

If a value is sensitive, **annotate its sensitivity beside it** — do not
remove it. Example:

```
discord.com/api/webhooks/1404099194175619203/FktBiiN76dGTrk
(sensitivity: bearer token, observed in public corpus; document-only —
 never validate, call, or transmit)
```

Rationale: a redacted value is unverifiable and unmatchable. Future hunts
join on exact strings; masking destroys the join key. The values in this
corpus were observed in public systems; the annotation carries the care,
not the redaction.

Corrections to published claims are **logged, never erased**: the original
claim is preserved verbatim inside the retraction note, with the reason
and the evidence for the correction. See
`why-these-sites/CORRECTIONS-LOG.md` in the skill-egress study for the
template.

## 2. Epistemic labels: OBSERVED vs INFERENCE

Every substantive claim carries one of three labels:

| Label | Meaning | Example |
|---|---|---|
| **OBSERVED** | Bytes are present in the cited artifact. Verifiable by re-reading. | "The skill posts to `discord.com/api/webhooks/` at runtime (code at `raw/scan-d1.json:412`)." |
| **INFERENCE** | A reasoned linkage from observed facts. States its premises. | "The 9 urlscan observations are observer-side rescans (7 API submissions in 3 scripted bursts + 2 urlhaus auto-submissions), not operator beaconing." |
| **Upstream assertion** | Someone else's claim, cited, not independently verified. | "JFrog Security Research reports 3,022 GemStuffer packages (cited in PROVENANCE.md)." |

Rules:

- Never present an INFERENCE with OBSERVED language. "The tunnel is
  live" (observed: HTTP 200 on a stored observation) is not "the operator
  is active" (inference).
- Infrastructure facts stay OBSERVED; campaign/operator conclusions stay
  INFERENCE. This separation is load-bearing for the whole corpus.
- When new evidence changes a label, update the label and note what
  changed — don't silently upgrade.

## 3. Strength grades

On top of the label, findings carry a strength grade:

- **confirmed** — bytes present, independently re-verifiable.
- **agent-shaped-unconfirmed** — matches known agent behavior/geometry but
  unattributed (e.g. the usemod.org ClipBoard burst: agent-shaped, leading
  hypothesis spam-bot).
- **lead** — worth following, not yet characterized.
- **watchlist-grade** — live and interesting, not evidence of anything yet
  (e.g. a live Pipedream endpoint answering HTTP 400 to scans).
- **evidence-grade** — supports a claim about an operation.
- **clean negative** — checked with a working query path, documented
  coverage, nothing found. First-class result, same writeup rigor as a
  find.
- **could-not-check** — the query path failed. Not a negative. State what
  failed.

"Watchlist-grade, not evidence-grade" is a complete verdict. Use it.

## 4. How to cite

- **Corpus records:** collection slug + `events.jsonl` line or record
  fingerprint, e.g. `2026-05-12-webhook-deaddrops/events.jsonl`
  (fingerprint `abc123…`).
- **Raw artifacts:** repo-relative path + line/byte offset, e.g.
  `studies/skill-egress-top1000/raw/scan-d1.json:412`.
- **External sources:** full URL + retrieval date + what was observed.
  Archived captures: archive URL + capture timestamp.
- **Timestamps:** use the artifact's own event-time field; name the field
  you used. Never silently substitute normalization or retrieval times.
- **Counts:** cite what you pulled, not what a counter reported. Counts
  fluctuate between count-time and pull-time; the pulled set is the
  coverage, at pull time only.

## 5. Negatives and uncertainty

- File clean negatives with the same rigor as finds: what was checked,
  the query path, the coverage window, the date.
- Distinguish: **clean negative** (healthy transport, empty result),
  **weak negative** (limited window/coverage — e.g. urlscan's anonymous
  30-day search window), **could-not-check** (transport failed).
- Date every negative. A negative is only valid for its coverage window.
- A finding that doesn't fit the frame is a lead, never a negative.
  Misfits get their own investigation.

## 6. What "verified" means here

A claim is verified when an independent re-read of the cited artifact
reproduces it — not when a script exits 0. "The script ran" is process
evidence; the bytes are the evidence. Spot-check machine-generated
extractions against the raw artifact before citing them.

## 7. Scope guardrails (evidence-relevant)

- Agents and infrastructure only. No operator identity, registrant, or
  social-profile attribution — not in evidence, not in notes.
- Passive/public OSINT only. Evidence gathered by probing, fetching
  candidate URLs, or interacting with suspicious infrastructure is out of
  scope and must not be added.
- Decoded payloads are text evidence only. Never execute, never fetch
  onward, never submit anywhere.
