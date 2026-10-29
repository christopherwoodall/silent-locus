# Findings — urlquery marker sweep

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## Sweep design (OBSERVED)

- Source: urlquery.net public report corpus, read-only, via `uq.py search`
  (Secure Vault surrogate auth). No submissions.
- Sweep v1: 15 queries; v2: 19 queries (corrected quoted/explicit-AND
  syntax); v3: 1 query; pagination: 4 requests.
- Continuation 2026-09-29: full pagination of unscoped `"exploitgym"`
  (32 pages, offsets 30..960). `total_hits` stayed 967 on every page.
- Honest gap: 966/967 distinct report ids captured. The off-0 page returns
  29 rows (not 30); a probe at offset 966 returned an id already seen on
  off-960 (result-window drift). The 1 remaining hit is not addressable via
  stable pagination.

## Bulk: 966 unscoped-"exploitgym" hits (OBSERVED)

- evidence_grade: low for all 966.
- Match location: search-index only (captured HTML/JS text). Not verifiable
  via the public report API. This is a documented collection caveat, not a
  verification failure.
- Scan time range: 2026-05-27T07:25:18Z to 2026-09-28T14:17:49Z.
- Verdict: no verifiable ExploitGym incident traffic in the 966 captured
  hits. Per-report rows preserved in `events.jsonl`; aggregated here (one
  coverage claim) rather than 966 near-identical records.

## Curated: 9 graded findings (OBSERVED)

| report | marker | grade | verdict |
|---|---|---|---|
| c1140981-53c9-4e64-8771-c3bbd0027e5c | cybergym | context-only | Fabricated openai.com internal path probe (404 via Cloudflare). Curiosity probe, not incident traffic. |
| 63b73840-181b-41f4-8d2b-804ff6ca0efa | catflag | low | EDM tracker redirect; match not locatable via public API. Cannot tie to ExploitGym. |
| 807da9fb-f7c3-4789-96e9-8ed9737350a4 | cybergym | low | benchgecko.ai benchmark table mention. Not incident traffic. |
| cc030ec6-81c9-47a6-88fd-319b63b57a35 | cybergym | benign | SnackOnAI newsletter clickthrough to cybergym.io. Legitimate. |
| 28cc5c3b-4440-4701-a582-f16424637336 | cybergym | benign | Same newsletter wave; public CyberGym GitHub repo scan. |
| aeaedada-2f59-4f13-883b-6e4345bddc5e | cybergym | benign | japan.forum-incyber.com forum homepage; generic mention. Predates the incident. |
| 21b1c8af-6d95-4932-af58-d1f28e664cbe | restart_server | benign | Cronicle job-scheduler login page; ordinary ops UI text. |
| 5292d8cb-800b-4caf-8ee8-71ccd503ba7b | restart_server | benign | Splunk login page on squat/test domain; generic ops text. |
| 18d4e2a9-5c66-459c-ab09-060b74d964bc | restart_server | benign | Japanese AI support tool; generic text. |

## Marker term status (Factum `infra.ioc`)

- `exploitgym`: noisy — 966 low-grade hits, none verifiable.
- `cybergym`: noisy — 5 hits, all benign/context-only/low.
- `catflag`: candidate — 1 low-grade hit.
- `restart_server`: retired — 3 benign hits; refuted as a controller-traffic
  marker (generic ops UI text everywhere).

## Cross-lane note

The bare marker `exploitgym` is new to Factum. The corpus already holds
repo-path terms (`mpn/exploitgym`, `xiv/exploitgym`, ...) from the
2022-08-09-github-forensics lane — different entities (fork paths), not
dupes. Edge building across lanes on the bare term is a separate pass.
