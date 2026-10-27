configs:
- config_name: default
  data_files:
  - path: run-log.json
    split: train
---
language:
- en
license: cc-by-nc-4.0
tags:
- ai-agents
- benchmark
- evaluation
- agent-evaluation
- llm-agents
- trustworthy-ai
- product-review
- c2pa
pretty_name: Hlido AI Agent Benchmark
size_categories:
- n<1K
task_categories:
- other
---

# Hlido AI Agent Benchmark

<!-- last-updated: 2026-04-14 | agents: 10 -->

**Independent, cryptographically-attested evaluations of AI agents and products.**

Hlido reviews AI agents the way Rotten Tomatoes reviews films — independent verdicts with proof, one clear score, and no sponsored rankings. This dataset is the machine-readable output of those reviews.

Every run is:
- Executed autonomously by the Hlido testing pipeline
- Cryptographically signed using C2PA (Coalition for Content Provenance and Authenticity)
- Scored using Hlido's proprietary two-layer evaluation model

**Website:** [hlido.eu](https://hlido.eu)  
**Methodology:** [hlido.eu/methodology](https://hlido.eu/methodology/)  
**Updated:** Daily (automated pipeline)

> © 2026 Hlido. The Laddoo Score, scoring methodology, tier system, and evaluation framework are proprietary. See licence and terms below.

---

## What's in this dataset

`run-log.json` — the full review ledger. Each entry is one Hlido pipeline run.

### Schema

| Field | Type | Description |
|---|---|---|
| `runId` | string | Unique run identifier |
| `domain` | string | Domain tested (e.g. `getbaton.dev`) |
| `url` | string | Entry URL used for the review |
| `startedAt` | ISO 8601 | When the pipeline run began |
| `finishedAt` | ISO 8601 | When the pipeline run completed |
| `score` | number \| null | Engine surface score (0–100). Null if run incomplete. |
| `tier` | string \| null | Engine tier label |
| `laddooScore` | number \| null | Hlido Laddoo Score (0–100) — final composite score |
| `laddooTier` | string \| null | VITAL / STEADY / FADING / FLATLINE |
| `pagesVisited` | array | Each page crawled: url, type, blocked |
| `blockersHit` | array | Blockers encountered: type, action taken, confidence |
| `claimsTested` | number | Number of marketing claims evaluated |
| `claimsVerified` | number | Claims that held up under testing |
| `errors` | number | Pipeline errors during run |
| `c2paSigned` | boolean | Whether artifacts were C2PA-signed |
| `t1Confidence` | string | High / Medium / Low — proportion of product surface testable |
| `testTier` | string | Tier 1 UI Auto / Tier 2 Guided Manual / Tier 3 Custom |
| `loggedAt` | ISO 8601 | When the record was written |
| `note` | string | Notes on blockers, anomalies, or methodology context |

---

## Scoring Overview

Hlido uses a proprietary two-layer scoring model. Full methodology is published at [hlido.eu/methodology](https://hlido.eu/methodology/).

### Layer 1 — Engine Score

Automated measurement of the public web surface across six dimensions: product clarity, feature depth, trust signals, claim verification, user experience, and pricing transparency.

The engine score reflects what an independent observer can verify from the public surface without login or payment.

### Layer 2 — Hlido Laddoo Score

Hlido's independent editorial assessment of the product across four dimensions:

- **Strategic Alpha** — Does it solve a real problem in a differentiated way?
- **Craft & Soul** — Is the overall product experience excellent?
- **Execution Grit** — Does the product deliver on its core promise?
- **Value Signal** — Is pricing fair and transparent relative to its category?

The exact weights and blending formula are proprietary and not disclosed in this dataset.

**Laddoo tiers:** VITAL (90–100) · STEADY (70–89) · FADING (40–69) · FLATLINE (0–39)

### Login Walls and Tier Confidence

A product behind a login wall is not automatically scored lower on product quality. The engine score reflects what could be verified publicly; the editorial Laddoo Score assesses the product on its own merits. All reviews carry a confidence label (T1 High / Medium / Low) and a note on how much of the surface was testable.

---

## Evidence & Attestation

Each reviewed agent has a corresponding proof bundle (stored privately at Hlido):
- Screen recording of the review session (MP4)
- Timestamped screenshots of key moments (PNG)
- `attestation.json` — structured metadata: domain, claims tested, blockers, scores
- All artifacts C2PA-signed (PS256, DigiCert timestamp authority)

C2PA signing means the video and screenshots carry a cryptographically verifiable chain of custody — provably captured by Hlido, provably unmodified. Proof bundles are available to reviewed agents on request.

---

## How to use this dataset

```python
import json, urllib.request

url = "https://huggingface.co/datasets/hlido-eu/agent-benchmark/resolve/main/run-log.json"
with urllib.request.urlopen(url) as r:
    data = json.load(r)

runs = data["runs"]

# Filter to scored runs only
scored = [r for r in runs if r.get("laddooScore") is not None]

# Sort by Laddoo Score
top = sorted(scored, key=lambda x: x["laddooScore"], reverse=True)
for r in top[:10]:
    print(f"{r['domain']:30} {r['laddooScore']:3}/100  {r.get('laddooTier','')}")
```

---

## Licence & Terms

This dataset is released under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

You may:
- Use and share the data for **non-commercial research, journalism, and personal projects** with attribution
- Cite Hlido in academic papers and public analysis

You may **not**:
- Use this data to build a competing AI agent evaluation or scoring product
- Reproduce, replicate, or adapt the Hlido scoring methodology, Laddoo Score formula, or tier system in any commercial product
- Represent Hlido scores as your own without clear attribution
- Train commercial models on this data without written permission

For commercial licensing, API access, or bulk data: [hlido.eu](https://hlido.eu)

**Attribution:** "Hlido AI Agent Benchmark, hlido.eu"

---

## Citation

```bibtex
@misc{hlido2026benchmark,
  title   = {Hlido AI Agent Benchmark},
  author  = {Hlido},
  year    = {2026},
  url     = {https://huggingface.co/datasets/hlido-eu/agent-benchmark},
  note    = {Independent, cryptographically-attested AI agent evaluations. Laddoo Score and methodology are proprietary. Updated daily.}
}
```

---

## Contact

[hlido.eu](https://hlido.eu) — submit an agent for review, request a T2 deep evaluation, or enquire about commercial data licensing.
