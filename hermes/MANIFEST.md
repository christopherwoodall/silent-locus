# Hermes hunt profile — MANIFEST

One line per file. All scanners ship disabled. No secrets in this tree.

## Root

- `README.md` — What the profile is, layout, how to load it, how to enable a scanner, /hunt toggle behavior, standing exclusions.
- `soul.md` — Profile persona and operating doctrine: direct, evidence-first, human-present hunting.
- `MANIFEST.md` — This file list.

## Skills (playbooks)

- `skills/hunt-methodology.md` — PRIMARY/SECONDARY grading and novelty checks against corpus, lists, and tracker.
- `skills/evidence-capture.md` — Provenance triple, cache everything, never redact evidence files.
- `skills/scanner-ops.md` — Enable/disable procedure, confidence caps, quota guards, fail-closed defaults.
- `skills/triage.md` — Pattern match versus confirmed behavior; never bulk-dismiss LOW hits.
- `skills/ingest-notes.md` — Hermes Postgres catalog record shape; Factum named only as the current silent-locus store.

## Tools (standalone scanners, all disabled by default)

- `tools/_common.py` — Shared helpers: config load, enabled gate, provenance-triple writer, display-text redaction.
- `tools/config.json` — Per-scanner config: enabled flags, rate limits, quota guards, confidence caps, env-var key names only.
- `tools/run.py` — Runner: `list` shows scanners and caps; `run <scanner>` refuses disabled scanners with no network call.
- `tools/urlquery.py` — urlquery search scanner; hits grade SECONDARY.
- `tools/urlscan.py` — urlscan search scanner; hits grade SECONDARY (third-party scan metadata).
- `tools/prcomment.py` — GitHub PR-comment behavior scanner; pattern matches only, grade SECONDARY.
- `tools/shodan.py` — Shodan count-delta scanner; emits only on large or sustained deltas, grade SECONDARY.
- `tools/crtsh.py` — crt.sh certificate scanner; grade SECONDARY.
- `tools/wayback.py` — Wayback CDX scanner; grade SECONDARY.
- `tools/iocfeeds.py` — OTX indicator feed scanner; first run seeds seen state silently, grade SECONDARY.
- `tools/intel_slot5.py` — Intel blog watch (reader plus direct fallback); new items are "new to inventory".
- `tools/telegraph.py` — telegra.ph page watch; title plus content hash only, no author tracking.
- `tools/FALSE-POSITIVES.md` — Known false-positive classes per scanner.

## Workspace (skeleton, no real data)

- `workspace/raw/README.md` — Raw captures live here, each with .PROVENANCE.txt and .sha256.
- `workspace/state/README.md` — Scanner state lives here (seen sets, baselines, quota state).
- `workspace/reports/README.md` — Reports live here; outward-facing reports carry no GitHub links.
- `workspace/lists/README.md` — Lists live here; config targets are the scope, and editing them is a TIER-B ship event.
