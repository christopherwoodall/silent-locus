# COUNSEL JUDGE VERDICT — cairnwatch.py (lane 12) + surfacewatch.py (lane 13)

Date: 2026-10-20. Judge: counsel judge (hard gate). Verdict is final.

Both modules are designs, not yet built. Both ship disabled by default.

## Verdicts

- MODULE 1 cairnwatch.py — GO-WITH-CHANGES.
- MODULE 2 surfacewatch.py — GO-WITH-CHANGES.

Surfacewatch is NOT killed. The adversarial kill rested on a missing
in-repo target list. The operator's design brief enumerates 13 targets;
that objection is resolved. The adversarial reviewer's remaining demands
convert to binding build requirements (S1–S5). The list must be hardcoded
in the module source — a config-soft list or any target discovery at build
time re-triggers the kill.

## Standing scope (both modules)

- Passive GET only. Never POST, login, or interaction.
- Disabled by default. --dry-run performs zero network calls.
- Every recorded IP is classified via attach_ip_classification().
  Standing rule, BigSexyWarlock69.
- Evidence rule reconciliation: raw capture bytes keep full values with
  sensitivity annotated, never redacted. The 2026-10-19 carve-out governs
  scanner-emitted paths only: redact_secrets() applies to hits, error-log
  context, summaries/dedup keys, and state files — never to raw evidence.
- 2026-10-20 operator override: established fleet-infrastructure IPs are
  publishable. This does NOT relax the identity line generally.
  Worker/creator strings are recorded verbatim and never pivoted,
  enriched, or attributed.

## MODULE 1 — cairnwatch.py: binding constraints

Targets: 4 Counsel-cleared malicious Cairn panels.
185.242.245.159:8000, 31.56.206.187:8000, 31.57.47.29:8000,
31.59.92.155:8000.

1. Allowlist HARDCODED as frozenset in module source. Not config-soft.
   No --hosts override. No auto-discovery.
2. Per run: exactly 4 GETs to /projects. GET /projects/{id} only for
   unseen project IDs. Streaming reads, 2MB cap per response. Per-run
   byte budget ~10MB with abort on exceed.
3. No CookieJar, no auth headers. Redirects are not chased: 3xx or
   final-URL mismatch = degraded state, never a hit.
4. Content-type and JSON-shape validation before any diffing.
   Invalid payload = degraded state.
5. Pacing: >=2s between hosts, 30s timeout, max 1 retry, then the host
   is "dark" for the run. 429 = hard stop for that host in this run.
   Dark-host alert only after a documented N consecutive dark runs
   (N set and documented in the FALSE-POSITIVES doc).
6. Detection (diff by project id): new project (unseen id); status
   transition (carries from->to); worker heartbeat transition.
   Indicator names describe observed events only. No "malicious" in
   indicator names; no undefined terms (e.g. "Tier-1"). The
   malicious-verdict statement goes in dated provenance, not in names.
7. Heartbeat = transition semantics only: new worker id,
   resume-after-stale, stale-while-active. NEVER alert on advancing
   timestamps. Diff on worker-id set membership and status transitions,
   never timestamp deltas. Staleness threshold explicit: >=2x poll
   interval + skew margin. Use the word "heartbeat" only if the API
   names the field; else "worker timestamp advanced".
8. Grade PRIMARY for direct observations. Confidence set explicitly per
   detection rule and documented in the FALSE-POSITIVES doc.
9. State: projections + hashes only, never titles or detail bytes.
   Canonical JSON hashing. State load failure -> quarantine the corrupt
   file and re-baseline with zero hits. Writes via per-target tmp name
   + atomic rename; state version-stamped.
10. redact_secrets() added to _common, applied on all four output paths:
    hits, error-log context, summaries/dedup keys, state. Error context
    carries identifiers only, never content.
11. normalize() for detection only; never emit decoded variants.
    Decoded variants never enter hits, summaries, or state.
12. Worker/creator strings recorded verbatim; never pivoted, enriched,
    or attributed.
13. Document the shared-USER_AGENT OPSEC tradeoff in the module doc
    (fingerprintable; known standing tradeoff — do not rotate silently).
14. Register in orchestrator LANES as
    ("cairnwatch", "cairn-panel-watch", False).
15. Ship gate: FALSE-POSITIVES-cairnwatch.md exists and covers, per
    detection rule, the benign triggers and mitigations. No ship
    without it.

## MODULE 2 — surfacewatch.py: binding constraints

Targets (13, hardcoded): rel-ochre.vercel.app/api/canon,
room.trydemigod.com, inference.dahl.global, extract.paypercall.dev,
agenttavern.dev, public-agents.com, agentsboard.org/llms.txt,
agents-agents-agents.com/llms.txt, bboard.ai/llms.txt,
agentgateway.pythonanywhere.com/mcp.json, tantive.space/skill.md,
swarmmemo.com, messageboardforaiagents.com.

1. Target list HARDCODED as frozenset in module source (S1). Not
   config-soft. No --targets override. No target discovery. New targets
   require counsel review + operator word.
2. Per-target fetch contracts (S2): GET only; no CookieJar/auth headers;
   content-type validation before hashing; redirects not chased
   (3xx/final-URL mismatch = degraded); streaming 2MB cap per target;
   per-run byte budget ~10MB with abort; >=2s spacing; 30s timeout;
   max 1 retry; 429 = hard stop for that target in this run.
3. Normalized-extraction hashing (S3): canonical per-target extraction
   (volatile boilerplate stripped only where the target's fetch
   contract documents it), then canonical-bytes hashing. Hash-only
   change = PRIMARY-observed, MEDIUM max. normalize() for detection
   only; never emit decoded variants or page text.
4. Per-target gap semantics (S4): a failed/missing fetch is a gap —
   never a hit, never a clean negative. Gaps do not silently
   re-baseline. Per-target consecutive-gap tracking; gap alert only
   after a documented N.
5. Infrastructure-surfaces-only (S5): all 13 targets are public
   agent-infrastructure surfaces. The module fetches public pages only
   and performs no interaction.
6. Hits carry identifiers only: target, hash pair (old->new),
   observed_at. Never page bytes, titles, or decoded variants.
7. State: hashes/projections only, never page bytes or titles.
   Canonical hashing. Corrupt state -> quarantine + re-baseline with
   zero hits. Per-target tmp + atomic rename; version-stamped.
8. redact_secrets() on all four output paths (hits, error-log context,
   summaries/dedup keys, state). Error context: identifiers only.
9. Indicator names describe observed events only (e.g. content-hash
   changed). No "malicious", no undefined terms.
10. Document the shared-USER_AGENT OPSEC tradeoff in the module doc.
11. Register in orchestrator LANES as
    ("surfacewatch", "surface-watch", False). Disabled by default.
    --dry-run = zero network.
12. Ship gate: FALSE-POSITIVES-surfacewatch.md exists and covers, per
    rule, the benign triggers and mitigations. No ship without it.

## Build-time kill triggers (both)

- Target/host discovery or config-soft lists.
- Emitting decoded variants, page bytes, or titles in hits or state.
- Timestamp-delta heartbeat alerts (cairnwatch) or gap-as-hit
  (surfacewatch).
- Any POST/login/interaction, CookieJar/auth headers, or chased
  redirects.
- Missing FALSE-POSITIVES doc at ship.
