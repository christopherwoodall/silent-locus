# MANIFEST — integrated analysis, July 2026 RubyGems spike set

## Deliverables (this directory)

- REPORT.md — integrated analysis (742 lines).
- findings.json — 22 numbered findings with grade and evidence paths.
- adversarial-review.md — NO-SHIP draft review plus disposition of all 20 fixes.
- verifier-report.md — SHIP-WITH-FIXES verification plus ship-time refresh.
- live-urls-refreshed-20261027.txt — 49 artifact URLs at ship time.
- live-version-dates-20261027.json — version publish dates and per-version
  downloads for the 23 live gems, fetched for REPORT.md §3.2.
- MANIFEST.md (this file), SHA256SUMS.

## Audit trail (working/, not deliverables)

- working/linguist.md, working/cryptologist.md, working/verdict-survivor.md,
  working/shell-phenomenon.md, working/open-questions-gaps.md — lane notes.
- working/adversarial-review-draft.md — full 509-line NO-SHIP draft.
- working/verifier-report-draft.md — full verifier draft.

## Sources integrated (read-only; none modified by this swarm)

- reports/rubygems-july-spike-review/REPORT.md + findings.json (prior review).
- reports/rubygems-july-spike-review/live-check-20261027/ (first census).
- reports/rubygems-july-spike-review/live-check-help-20261027/ (helper census).
- reports/rubygems-july-spike-review/live-check-reconciled-20261027/
  (reconciled census + tombstone-diffend-pairs.json).
- reports/ruby-sus-gems-export-v2.json (3,036-row full-sweep export).
- data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv
  (operator-uploaded 533-row July spike CSV).
- Live RubyGems versions endpoint (version dates, §3.2) and Diffend refresh
  (jrjackson backfill, §3) — fetched read-only for this report.

## Rules observed

- Read-only GET/HEAD only. No POST, no login, no sessions, no accounts.
- No payload executed. No callback URL fetched. Internal metadata-address URI never fetched.
- No credential-shaped value and no full canary token in any deliverable (shapes + counts only).
- No Factum writes. No Transluce or other report submissions.
- No other worker's files touched. No push (parent pushes and delivers).
- ASD-STE100 style in REPORT.md: short sentences, simple words, terms defined on first use.
