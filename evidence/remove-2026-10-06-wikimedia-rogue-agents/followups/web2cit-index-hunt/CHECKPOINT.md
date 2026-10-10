# CHECKPOINT — web2cit-index-hunt (lane c)

Status: LANE COMPLETE 2026-10-06. Findings in FINDINGS.md. Branch: wikimedia-rogue-agents-followups-2026-10-06.

## Done

1. Transport health verified (urlquery.net 200, urlscan.io 200, wayback CDX port-80 200).
2. urlquery.net: bare + domain-scoped + variant-host queries (6 queries) → 0 genuine web2cit submissions.
3. urlscan.io: 5 queries (domain:, page.url:, bare, 2 variant hosts) → all total=0.
4. Wayback CDX: translate* (27 captures), debug* (35), sandbox*, variant hosts (0), host-level domain query (234 captures, keyword sweep for arcgis/geocod/hawaii/openai/gpt/chatgpt = 0).
5. All targets graded organic; the 2026-06-26 bbc.com coincidence documented and graded coincidence.
6. Never live-fetched any candidate URL; nothing redacted; grades on every claim.

## Raw evidence kept (ephemeral, /tmp — re-runnable)

- /tmp/web2cit_cdx_translate.json — translate* prefix CDX dump (27 captures)
- /tmp/web2cit_cdx_all.json — host domain CDX dump (234 unique captures)

## What's next (if the lane is re-opened)

1. **Post-disclosure re-sweep** (investigator-artifact watch): anything dated 2026-10-05+ on these endpoints is suspect (observer-in-the-data rule).
2. **Cross-lane join**: Meta-Wiki Web2Cit/data namespace API pass (sibling lane) — other configs targeting non-bibliographic domains would corroborate the fetch-oracle detection rule; this index lane stays clean regardless.
3. **urlquery date-scoped re-query** if the index grows: `date:[2026-06-20 TO 2026-07-10]` scoping on `url.domain:web2cit.toolforge.org`.

## Exact resume commands

```bash
# transport health
curl -sS -m 20 -o /dev/null -w "%{http_code}\n" https://urlquery.net/ ; \
curl -sS -m 20 -o /dev/null -w "%{http_code}\n" https://urlscan.io/ ; \
curl -sS -m 20 -o /dev/null -w "%{http_code}\n" "http://web.archive.org/cdx/search/cdx?url=example.com&limit=1&output=json"

# urlquery (authenticated; 6s pacing)
cd ~/workspace/silent-locus
python3 ~/workspace/skills/urlquery/bin/uq.py search --query "url.domain:web2cit.toolforge.org" --limit 50
python3 ~/workspace/skills/urlquery/bin/uq.py search --query "url.domain:web2cit.toolforge.org" --limit 50 --offset 50
# date-scoped variant:
python3 ~/workspace/skills/urlquery/bin/uq.py search --query "url.domain:web2cit.toolforge.org date:[2026-06-20 TO 2026-07-10]" --limit 50

# urlscan.io (6s pacing)
curl -sS -m 30 "https://urlscan.io/api/v1/search/?q=domain%3Aweb2cit.toolforge.org&size=100" -H "Accept: application/json"
curl -sS -m 30 "https://urlscan.io/api/v1/search/?q=page.url%3A%22web2cit.toolforge.org*%22&size=100" -H "Accept: application/json"

# Wayback CDX (port 80, bare prefix; 8s pacing)
curl -sS -m 60 "http://web.archive.org/cdx/search/cdx?url=web2cit.toolforge.org/translate&matchType=prefix&output=json&fl=timestamp,original,statuscode&collapse=urlkey&limit=5000" -o /tmp/web2cit_cdx_translate.json
curl -sS -m 60 "http://web.archive.org/cdx/search/cdx?url=web2cit.toolforge.org/debug&matchType=prefix&output=json&fl=timestamp,original&collapse=urlkey&limit=2000"
curl -sS -m 90 "http://web.archive.org/cdx/search/cdx?url=web2cit.toolforge.org&matchType=domain&output=json&fl=timestamp,original&collapse=urlkey&limit=10000" -o /tmp/web2cit_cdx_all.json
```

## Open questions for parent

- None blocking. The clean negative stands: agent-shaped hits = 0 across all three indexes as of 2026-10-06.
