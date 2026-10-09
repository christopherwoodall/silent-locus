# HTMX-FIX verification — OBSERVED grade

Date: 2026-10-06 (CDT) / probes run 2026-10-07 00:13–00:15 UTC via curl through VM egress proxy, ≥5s pacing.

**Verdict: the sweep's bug claim REPRODUCES and the fix is found.** The old pattern
`GET /api/htmx/search/?q=<query>&limit=<n>&offset=0` with no headers returns **204 No Content**
even for queries with many known results. A single header — `HX-Current-URL` — flips it to
**200 with report rows**. `HX-Request: true` alone does NOT fix it (contrary to the sweep's
suggestion that "HX-Request emulation headers" were needed). `HX-Current-URL` alone is
sufficient; `HX-Request` adds nothing.

Note: row counts are counted as occurrences of `href="/report/<uuid>"` (each report row
renders exactly one such link in its URL cell). Each curl ran with a different fresh
timestamp, so row counts differ slightly between probes (21 vs 23) — the table reflects
observed values per probe.

## Probe table

| probe # | headers sent | HTTP code | body bytes | report rows found |
|---|---|---|---|---|
| 1 | (none) | 204 | 0 | 0 |
| 2 | `HX-Request: true` | 204 | 0 | 0 |
| 3 | `HX-Request: true` + `HX-Current-URL: https://urlquery.net/search?q=webhook.site` | 200 | 118178 | 21 |
| 3b | `HX-Current-URL: https://urlquery.net/search?q=webhook.site` only | 200 | 136540 | 23 |
| 4 | `User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36` + `Accept: text/html` only | 204 | 0 | 0 |
| 5 (neg ctrl) | (none), q=zzz-no-such-term-xyz | 204 | 0 | 0 |
| 6 (neg ctrl) | `HX-Current-URL: https://urlquery.net/search?q=zzz-no-such-term-xyz`, q=zzz-no-such-term-xyz | 200 | 1202 | 0 ("No reports found") |

Minimal header set: **exactly one header — `HX-Current-URL: <the /search page URL>`**.
UA spoofing and `HX-Request` are unnecessary.

## Working curl command (verbatim)

```sh
curl -sS -o out.html -w "%{http_code} %{size_download}\n" \
  -H "HX-Current-URL: https://urlquery.net/search?q=webhook.site" \
  "https://urlquery.net/api/htmx/search/?q=webhook.site&limit=24&offset=0"
```

Response headers on the winning probe confirm the htmx wire contract is back:
`Hx-Push-Url: /search?q=webhook.site&view=&type=reports`, `Hx-Trigger-After-Swap: reInitFB`,
`Content-Type: text/html; charset=utf-8`. The body is the report table `<div>` + a
`<script>` block, ready for htmx swap — not an empty shell.
Full sanitized `curl -v` output appended to `../raw/probe-log.txt`.
