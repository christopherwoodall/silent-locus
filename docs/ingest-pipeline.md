# Ingest Pipeline: Holistic View

Date: 2026-10-19
Purpose: Board-level description of the hunt's data pipeline — sources,
detection, processing, storage, and output.

## The Pipeline in One Picture

```
SOURCES → DETECTION → COLLECTION → REVIEW → STORAGE → OUTPUT
   ↓          ↓            ↓           ↓         ↓         ↓
Blogs    IOCs/words   Crawlers    Counsel   Factum    Reports
Shodan   Tag grammar  Fleets      Red team  Raw dirs  Filings
URLQuery Custom rules  Scanners    Grading   URL inv.  Writeups
Traject.                                      Wordlist
arXiv
```

## 1. Sources

Where raw signal comes from.

| Source | What | How |
|--------|------|-----|
| **Shodan** | Exposed agent-harness panels (Cairn, Strix, Hermes) | API queries on title/html markers |
| **URLQuery** | Agent activity in scan reports | htmx endpoint, tag-grammar searches |
| **Transluce** | Agent incident findings tracker | Daily API pull, ingest-on-arrival |
| **Blogs** | Threat intel (NorForge, Gambit Security, etc.) | Manual monitoring, linked in reports |
| **Trajectory corpora** | Agent behavior datasets (HuggingFace) | Fleet ingest: download → review → Factum |
| **arXiv** | Papers with agent fingerprints | Keyword/pattern sweeps |

## 2. Detection

How we know what to look at.

### IOCs (Indicators of Compromise)

Structured markers stored as `infra.ioc` records in Factum. Each has:
- **Term**: the searchable string (domain, IP, tag, hash)
- **Category**: what kind of indicator (proxy, dead-drop, shortener, etc.)
- **Provenance**: where it was first seen
- **Status**: active, retired, or noisy

### Word List

`lists/words/wordlist.txt` — active search terms, one per line.
`lists/words/wordlist.json` — metadata superset (includes noisy/retired).

Terms come from: trajectory analysis, blog reports, fleet discoveries.
Noisy terms stay in JSON but leave the active list.

### Tag Grammar

Fleet-specific URL parameters that mark agent activity:
- `uqscan=`, `uqframe=` — urlquery fleet markers
- `zz=` — OpenAI provider marker
- `oai*` — OpenAI toolkit tags

These are high-signal because they're machine-generated, not human.

### Custom Rules

Detection logic with documented false-positive analysis. Each rule has:
- Description of what it catches
- Known FP sources
- Mitigations
- Corroboration threshold for MEDIUM/HIGH grading

Example: the `creator-ip` rule (webhook.site creator IP from token metadata)
documents that researchers also create inboxes, and mitigates by requiring
fleet-indicator context.

### Blog Monitoring

Threat intel blogs (NorForge, etc.) are monitored for new TTPs, clusters,
and infrastructure. Findings feed back into IOCs and word list.

## 3. Collection

How we pull the data.

### Crawlers (Single-Script Pipeline)

**Pattern**: Linear modular pipeline, not agent-spawning. One Python script,
modules run in sequence, state file tracks progress.

Example: `swarm-infra-crawler.py`
1. **Harvest** — search urlquery for fleet markers, extract inbox UUIDs
2. **Creator** — GET token metadata per inbox → creator IP + UA → classify
3. **Pivot** — invert to creator-IP → inbox clusters

Passive only: GET requests, no POSTs, no logins. Polite delays.

### Scanners (Orchestrated Modules)

**Pattern**: `scanners-orchestrator.py` runs modules in `scripts/scanners/`:
- `crtsh.py` — certificate transparency
- `ntfy.py` — ntfy.sh topics
- `urlscan.py` — urlscan.io
- `wayback.py` — Wayback Machine
- `packages.py` — npm/PyPI/RubyGems
- `urlquery.py` — URLQuery

Each module is independent. The orchestrator coordinates and dedups.

### Dynamic Agents (Fleets)

**Pattern**: Coordinator spawns workers, each with a character/role.
Workers run in parallel lanes, return results to coordinator.

Example: Cairn hunt fleet
- **Sextant** — query refinement
- **Harbor** — host enumeration
- **Lantern** — passive panel profiling
- **Babel** — linguist/target analysis
- **Cipher** — cryptologist (encoded content)
- **Red** — adversarial reviewer (kills false positives)
- **Counsel** — clearance gate (MALICIOUS/BENIGN/UNDETERMINED)
- **Ledger** — ingest + reporting

Standing composition: every fleet includes a linguist, a cryptologist,
and an adversarial reviewer.

### Key Differences

| | Crawler | Scanner | Fleet |
|---|---|---|---|
| Pattern | Linear pipeline | Orchestrated modules | Coordinator + workers |
| Parallel? | No (sequential) | Partial | Yes (full) |
| State | File-based | File-based | Agent-managed |
| Best for | Focused harvests | Multi-source sweeps | Complex investigations |

## 4. Review

How we separate signal from noise.

### Counsel Gate

A hard gate before deep collection. Each host/finding gets:
- **MALICIOUS** — proceed to log mining
- **BENIGN** — documented, no further action
- **UNDETERMINED** — held, needs more evidence

No log scraping on UNDETERMINED or BENIGN. This is absolute.

### Adversarial Review (Red Team)

Every finding is attacked:
- Is it a honeypot?
- Is it a demo or test?
- Is it the operator's own infrastructure?
- Does the evidence support the claim?

Nothing ships until Red can't kill it.

### Grading

Every claim is graded:
- **OBSERVED** — directly seen in evidence
- **INFERENCE** — reasoned from evidence
- **UPSTREAM** — from a cited external source

### Novelty Check

Before calling anything NEW:
1. Search Factum corpus
2. Search legacy internal corpus
3. Query Transluce findings
4. Check `lists/` inventories

Novelty is unestablished until all checks complete.

## 5. Storage

Where it all lives.

### Factum (Structured)

The system of record. 217,302 records across 107 lanes (2026-10-19).

Record types:
- **observation** — what was seen (105k)
- **edge** — relationships between records (96k)
- **artifact** — file references (2.5k)
- **source** — provenance anchors (485)
- **claim** — graded assertions (434)

Every record carries a lane tag. Immutable evidence; metadata editable.

### Raw Directories (Unstructured)

`data/lanes/<lane>/raw/` — original bytes with provenance triples:
- The data file
- `.sha256` hash
- `.PROVENANCE.txt` (source URL, retrieval time, method)

Evidence is never deleted, never redacted.

### URL Inventory

`lists/urls/urls.jsonl` — canonical operational URL list (510 URLs).
`lists/urls/activity-hosts.md` — curated activity-hosting endpoints.
`lists/urls/trajectory-domains.md` — 48 interesting domains from trajectories.

### Word List

`lists/words/wordlist.txt` — active terms.
`lists/words/wordlist.json` — full metadata.

## 6. Output

What comes out.

| Output | Audience | Status |
|--------|----------|--------|
| **Reports** | Internal | `reports/trajectory-ingest/<corpus>/REPORT.md` |
| **Transluce filings** | External | Frozen — queued for freeze lift |
| **Writeups** | External | Transluce-style, per behavior family |
| **Evidence logs** | Internal | URLs + sha256 + timestamps |
| **Graphs** | Both | Target sectors, timelines, geolocation |

## Pipeline Health

- **Throughput**: Single-writer Factum lock is the bottleneck (~6 min per full load)
- **Reliability**: VM reboots ~hourly; durable patterns (state files, JSONL appends) survive
- **Coverage**: 107 lanes, 217k records, growing via fleet ingests
- **Quality**: Counsel gate + Red team + novelty checks on every finding
