# Glossary: hunt jargon

One-line definitions for the terms used across the hunt. Each entry links
to where the concept is worked in the repo.

## Tradecraft

- **Dead drop** — a public inbox an agent writes to and an operator reads
  from: webhook.site UUID inboxes, Pipedream requestbins, ntfy topics,
  Discord/Slack/Telegram webhook URLs. The 20-year-old primitive at the
  center of the hunt.
  → `data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/why-these-sites/WHY-SITES.md`
- **Exfil primitive** — any outbound channel an agent could use: webhooks,
  pastes, file hosts, reader proxies, tunnels, email. "Egress" in the
  skill studies means *any* outbound web communication, including email.
- **Relay / reader proxy** — a fetch-by-proxy service that launders the
  origin IP and reshapes content: r.jina.ai (keyless), zread.ai,
  allorigins, translate.goog. Twenty-year-old mechanism; the
  markdown-for-LLMs tuning is the new refinement.
- **Exfil grammar** — the machine-generated structure *around* a
  primitive: query-param families, path templates, demux markers
  (`?m=<MARK>`), chunked sendBeacon sequences. The grammar discriminates
  operations; the primitive does not.
- **Beacon** — periodic check-in traffic: `?retry=3`, `?x=0/1/2`,
  `?v=<digits>` query shapes against a dead drop or tunnel host.

## Marker families

- **zz grammar** — `zz=oai<digits>`: `oai` + 10-digit epoch seconds + 7
  random digits. Prefix recovers collection time ±2s (verified 3/3).
  The launcher toolkit's nonce family; near-zero outside incident corpora.
- **Epoch nonces** — timestamps minted as nonces: 19-digit epoch-ns,
  `<label><epochms>`, `retry={epoch_ms}-{N}`. Zero time-API usage is
  itself a signal; nonces decode to session wall-clock.
- **oai tags** — `oai*` / `oai-` prefixed labels (tags, tunnel
  subdomains, params). Investigator self-naming also uses `oai-` —
  treat lane-3 `oai-*` strings as investigator-generated unless proven
  otherwise.
- **uqscan grammar** — `uqscan=<word><date><letter>` tag family and its
  lineage (`uqn` → `uqtag` → `mark=` → `uqscan` over ~10 months).
- **Eval fingerprint** — a verbatim-searchable phrase from a public eval
  question (e.g. a DeepSearchQA question fragment). Agents execute eval
  questions rather than pasting them, so fingerprints hunt *task-shaped*
  traffic, not text.
  → `collections/eval-questions/HUNT-QUERIES.md`

## Shapes and units

- **Agent-shaped** — matching known agent behavior/geometry (burst timing,
  machine cadence, nonce grammars) without confirmed attribution.
- **Swarm** — multiple agent instances operating with coordination
  (shared dead drops, plan inheritance, retry loops).
- **Fleet** — the incident unit in this corpus: a burst of agent-like
  activity attributed to one launcher/toolkit run (e.g. the Amap fleet).
- **Campaign** — sustained activity across fleets sharing tooling or
  infrastructure.
- **Lane** — an analyst workstream: `personas/<lane>/` (69 lanes) or
  `raw/lanes/` (9 lanes), each with `FINDINGS.md`/`CHASE.md`.

## Architecture

- **Destination** — where exfil goes: webhook.site, Discord, catbox.moe,
  r.jina.ai. Old tradecraft (10/14 CONFIRMED-OLD); old countermeasures
  apply.
- **Control plane** — the agent-invokable interface layer: MCP servers,
  vault APIs, tunnel brokers shipping MCP servers, crypto eSIM
  provisioning. The new attack surface; no old countermeasure exists.
- **Launcher / toolkit** — the common harness behind incidents: oai tags,
  zz/epoch grammars, jina laundering, webhook dead drops. Hunt the
  toolkit, not the campaign.
- **Sybil infrastructure** — machine-provisioned identity capacity:
  crypto-bought eSIMs, throwaway accounts, API-key resellers. Tripwire as
  provisioning, not as comms.

## Evidence grades (see `evidence-rules.md`)

- **OBSERVED / INFERENCE / upstream assertion** — the epistemic labels on
  every claim.
- **confirmed / agent-shaped-unconfirmed / lead** — strength grades.
- **watchlist-grade vs evidence-grade** — "live and interesting" vs
  "supports a claim about an operation". A complete verdict on its own.
- **Clean negative / weak negative / could-not-check** — the three kinds
  of "nothing found". Only the first is a zero.

## Corpus mechanics

- **Keep-all + annotate** — nothing is deleted; external overlap goes in
  per-report annotation sidecars and dataset-level provenance records.
- **Fingerprint** — SHA-256 of a collection's documented identity string;
  the join key across the corpus.
- **1970 sentinel** — `1970-01-01T00:00:00Z` with
  `labels.timestamp_source = "fallback:no_recoverable_date"`: event time
  unrecoverable. Exclude from time-series analysis.
- **record_kind** — the snake-case record class (98 in use: `wiki_event`,
  `webhook_deaddrop`, `null_read`, `corpus_grep_negative`, …).
  Registry in `schema/README.md`.
- **Rollup** — aggregate index layer; joins and consolidations live here,
  never in the canonical event stream.
