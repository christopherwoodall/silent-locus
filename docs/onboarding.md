# Onboarding: the silent-locus hunt

Welcome. This document is the fastest path from zero to productive in this
repository. It assumes you are technical but new to the project.

## What the hunt is

`silent-locus` is a forensics corpus and an active hunt for **public traces
of AI agents** — autonomous software agents leaving observable footprints on
the public internet: URL-scanner submissions, wiki edits, package-registry
injections, dead-drop inboxes, tunnel endpoints, shortener stats pages.

The working hypothesis (documented in the corpus, refined over the hunt):

> The incidents are **different runs of different evaluations that escaped**,
> linked by a **common launcher/toolkit** — not a shared payload, and not the
> same agents. Same provider, different agents, different evals.

The toolkit's fingerprints: `oai*` tags, `zz=oai` / epoch-nonce grammars,
reader-proxy laundering (r.jina.ai and cousins), webhook dead drops
(webhook.site, Pipedream, ntfy, Discord/Slack/Telegram webhooks).

Scope is **agents and agent infrastructure only**. Human/operator identity,
registrants, and social-profile attribution are out of scope — always.

## The core results so far

- **Top-1000 skill-egress scan** (`data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/INVESTIGATION-REPORT.md`):
  1,013 skill identities, 6,343 units scanned, 1,541 with egress hits.
  The dead-drop grammar now ships whole in single skills.
- **Thesis test** (`studies/skill-egress-top1000/why-these-sites/WHY-SITES.md`):
  10 of 14 egress destinations grade CONFIRMED-OLD (some literally the same
  product lineage, e.g. RequestBin 2012 → Pipedream 2019). The new part is the
  **agent-invokable control plane** (MCP vault invocation, crypto eSIMs,
  MCP-native tunnels) — not the destinations.
- **Link-hunt** (`why-these-sites/linkhunt-deep/LINKHUNT-DEEP.md`): live
  material plus four published corrections (a withdrawn false positive, two
  reframed leads, one corrected count). Corrections are logged, never erased.
- **AI Village join** (`data/2026-09-28-chinese-amap-fleet/village-join/VILLAGE-JOIN-2.md`):
  2025 village agents independently memorized the same exfil primitives as
  benevolent dev tooling — strongest support for the old-tradecraft thesis.
  Primitives are detection surface; **grammars** are the discriminating layer.
- **Eval-questions corpus** (`collections/eval-questions/`): 10,201 public
  eval questions with expected-source domains and verbatim fingerprint
  phrases, plus 50 ranked hunt queries.

## Repo layout (short version)

- `data/` — 71 event collections (`YYYY-MM-DD-<subject>`), each with
  `events.jsonl`, `PROVENANCE.md`, `SHA256SUMS`, `raw/`.
- `data/2026-09-28-chinese-amap-fleet/` — the active hunt workspace:
  `personas/` (69 analyst lanes), `raw/lanes/` (9 lanes), `studies/`,
  `METHODOLOGY.md` (the hunt manual), `LESSONS.md` (the findings log),
  `live-monitor/`, `infra-watchlist/`, `village-join/`, `slug-hunt.py`.
- `collections/eval-questions/` — the eval-question corpus and hunt queries.
- `schema/` — the record schema and collection-naming rules.
- `scripts/` — loaders, validators, builders.
- `ioc-wordlist/` — the shared IOC word list.
- `docs/` — this directory.

See [`repo-map.md`](repo-map.md) for the annotated tree.

## First three things to read

1. [`methodology.md`](methodology.md) — how the hunt works (distilled from
   the full manual). Read this before touching any data.
2. [`evidence-rules.md`](evidence-rules.md) — the evidence contract. The
   single most important rule: **never redact from evidence**.
3. [`../data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/INVESTIGATION-REPORT.md`](../data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/INVESTIGATION-REPORT.md)
   — the integrated 2026-10-05 investigation report. The current state of
   the hunt in one file.

## How to run a hunt lane

1. **Pick a lane or a lead.** Lanes live in
   `data/2026-09-28-chinese-amap-fleet/personas/<lane>/`. Each lane has a
   `FINDINGS.md` (or `CHASE.md`). New lanes get their own directory.
2. **Work passive-only.** Public OSINT: search APIs, public indexes,
   archived captures. Never probe suspicious infrastructure directly —
   no fetching candidate URLs, no submitting to scanners, no logins.
   (See [`methodology.md`](methodology.md) § OPSEC.)
3. **Write as you go.** Steps, rationale, evidence, caveats, complete URL
   lists — in the lane's `FINDINGS.md`, incrementally.
4. **Grade everything.** Every claim carries an epistemic label:
   `OBSERVED`, `INFERENCE`, or upstream assertion, plus a grade
   (confirmed / agent-shaped-unconfirmed / lead). See
   [`evidence-rules.md`](evidence-rules.md).
5. **File honest zeros.** A documented clean negative with stated coverage
   is a first-class result. "Could not check" is not a zero.
6. **Cross-reference before claiming.** Check the marker against the
   corpus and the IOC wordlist — collisions across unrelated contexts get
   their own investigation; disjoint grammars across corpora discriminate
   families.

## Key vocabulary

See [`glossary.md`](glossary.md). The thirty-second version: a **dead
drop** is a public inbox an agent writes to and an operator reads from;
an **exfil primitive** is any outbound channel (webhook, paste, relay,
tunnel); **grammars** (`zz=oai`, epoch nonces, `?m=` demux keys) are the
machine-generated tag families that discriminate operations; the
**control plane** (MCP servers, vault APIs) is the new attack surface,
distinct from the **destinations** (the old dead-drop sites).

## Toolchain

[`toolchain.md`](toolchain.md) covers the scripts and query surfaces:
`slug-hunt.py` (cross-archive slug presence), `uq.py` (urlquery search),
urlscan search API, Wayback CDX, the `hf-download` skill, and the
eval-questions `_tools/`.

## Rules that are not optional

- Agents and infrastructure only. Never pursue operator identity.
- Passive/public OSINT only. Log candidate URLs; never live-fetch them.
- Never redact from evidence. Full observed values stay in the files.
- Every claim graded: OBSERVED vs INFERENCE vs upstream assertion.
- Honest negatives are first-class. Document what you checked.
