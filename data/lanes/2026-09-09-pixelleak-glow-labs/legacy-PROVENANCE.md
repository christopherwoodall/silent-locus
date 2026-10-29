# Provenance — PixelLeak / Glow Labs (`data/2026-09-09-pixelleak-glow-labs/`)

Date: 2026-09-29. Built by `build_pixelleak.py` (single-collection build script,
co-located per repo convention).

## What this dataset is

Claim-level extraction of the Glow Labs "PixelLeak" research blog post
(https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies), filed under the "agents acting badly" theme at
BigSexyWarlock69's direction. It is a **separate event** from every other
corpus collection: `gitshot` / `pixelleak` return zero hits across our notes
and data (grep 2026-09-29). Do not merge it into any existing dataset.

Two evidence tiers, kept separate by `confidence`:

1. **`confirmed`** — what this script itself verified: the artifact bytes on
   disk (`raw/`), their SHA-256, and that the HTML contains the report text.
2. **`reported`** — every substantive claim (scale figures, victim classes,
   technique, skill propagation, lab repro). These are Glow Labs'
   vendor-reported assertions, quoted verbatim into `payloads`, never
   independently verified by us.

## Vendor caveat

Glow Labs sells endpoint-AI runtime protection; the post markets its product
("Glow customers using runtime prevention policies are already protected").
Treat the 13,000+ images / 300+ organizations / 900+ repos figures as
vendor-reported, not independently verified. The Claude Code Opus 5 lab
reproduction is a single-model anecdote; the "dozen agents, one skill"
observation is a single-vendor case study.

## Artifacts

| File | Bytes | SHA-256 | Acquisition |
|---|---|---|---|
| `pixelleak-blog.html` | 88121 | `ebfa83981f580aa9216f29b81ade002c8393cd75be12d9d2df9c9bcc9ae9e973` | cached, re-validated |
| `glow-system-architecture-v2-2.png` | 399456 | `cb3910c828c0852c205f067906776acb4f4524915c8c490b66d1ecbe516582e5` | cached, re-validated |
| `glow-system-architecture-v2-2-1.png` | 354101 | `a5cc207fd1810b9d3bc737b8a99bbfb32c623ca2cac43f62f545eca6145628fa` | cached, re-validated |

- The report's "Image 1" (GitHub repo screenshot) had **no URL** in the page
  text available to us; its absence is recorded here rather than invented.
- The two cached PNGs are marketing architecture diagrams, not evidence
  images; they are cached for completeness only.
- Retrieval: `urllib` live GET with research UA, 30s timeout, 3-attempt
  backoff. No logins, no forms, no interaction.

## Identity

- Fingerprint identity string: `2026-09-09-pixelleak-glow-labs:glow-labs-pixelleak-report`
- Fingerprint (SHA-256 of identity string): `19d6a6df8a710602ae7d4864345cfb55b94f8db32ad1a3aa1189860840a625c7`
- `event.dataset`: `2026-09-09-pixelleak-glow-labs`

## Comparison note

`notes/pixelleak-glow-comparison-2026-09-29.md` grades the report against our
corpus: structural parallel (public-channel workaround tradecraft), shared-skill
propagation supporting the escaped-eval-runs hypothesis, and the adversarial
caveats. Read it before citing this collection.

## Build

- `build_pixelleak.py` — this script. Idempotent: re-runs keep valid cached
  artifacts, regenerate `events.jsonl`, `PROVENANCE.md`, `SHA256SUMS`.
- No invented IDs, dates, or URLs. Unknown report publication date uses the
  schema sentinel with `labels.timestamp_source=fallback:no_recoverable_date`.
- Registry follow-up (not done by this script): add `2026-09-09-pixelleak-glow-labs` to
  `schema/collections.json` and the ES manifest before indexing.
