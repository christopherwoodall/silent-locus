# Ladder candidates — PROBE REPORT

2026-10-03. Read-only curl probes (21 requests, all logged in
`data/probe-log.jsonl`, rerunnable via `probe.py`). Honest zeros throughout.

## 1. jqp.vercel.app — server-side jq fetch+transform proxy

- **Live and working.** Homepage: "jqp is a free serverless proxy that lets
  you request data from remote sources, filter it using jq-web, and receive
  the filtered response." Grammar from its README:
  `https://jqp.vercel.app/api/v0?url=<encoded>&jq=<encoded>`.
- **Verified against the SEC incident target:** one read-only fetch of
  `https://www.sec.gov/files/county.json` through `?url=…&jq=keys`
  returned HTTP 200 with the array keys `[0..27]`. The audit-bench report
  of agents using jqp against this exact file is technically plausible.
- **No public history.** `/api/history`, `/history`, `/recent`,
  `/api/recent`, `/gallery` all 404; no login form; no listing hints on the
  homepage. It is serverless (Vercel) — requests exist only in the
  operator's private Vercel logs.
- **Verdict: NOT a trace source.** Confirmed working relay, publish-by-default
  status: no. Its URL grammar (`url=…&jq=…`) remains a dorkable fingerprint
  if jqp-wrapped links ever surface elsewhere (e.g. in wiki recipe pages).

## 2. bitily.in /admin — YOURLS shortener

- **`/admin` is login-gated today.** HTTP 200 serves the YOURLS 1.9.3-dev
  login page ("Please log in", username/password form). No link listings
  without credentials.
- Root `https://bitily.in/` and `https://bitily.in/MYLABI/` both return a
  literal 11-byte "Hello world" — the public front is a stub.
- The audit-bench claim of a "searchable /admin panel" does not hold as of
  2026-10-03 (it may have been open at incident-report time; unverifiable now).
- **Verdict: NOT a trace source** via any public route found. Escalation
  would require credentials, which is out of scope.

## 3. s.jina.ai — Jina search API

- Root returns: "Authentication is required to use this endpoint. Please
  provide a valid API key via Authorization header." Key-gated.
- `jina.ai/reader` is marketing/docs only; the single "trending" match is
  a `trending_up` rate-limit icon, not a query log. No public query logs,
  trending queries, or stats anywhere found.
- **Verdict: NOT a trace source.** (Incident-era note: r.jina.ai was keyless
  in May–June 2026; s.jina.ai's gating is a later state.)

## 4. Exa (exa.ai) — commercial search/fetch API

- `exa.ai/search` is the "Exa Agent" web UI; its Recents panel says "Sign in
  to see your history" — per-account, login-gated. `/recent`, `/trending`,
  `/playground` all 404. No public telemetry, logs, or query listings.
- **Verdict: NOT a trace source.** One verification probe, as tasked.

## 5. tinyurl.com — shortener

- Homepage is a marketing page; no recent-link listings, public index, or
  link directory found. Expected: shorteners do not publish target lists.
- **Verdict: NOT a trace source.** One check, as tasked.

## Bottom line

All five candidates are **usable-as-relays but not scannable-as-trace-sources**:
no public history, logs, or listings on any of them. The skill-ladders lane
stands validated (the ladders are real and the jqp↔county.json link checks
out technically), but the probe set adds no new searchable surface. The
highest-EV trace sources remain the publish-by-default archives already in
the probe set (Wayback CDX/SPN, archive.today, arquivo.pt, Ghost Archive,
Megalodon) plus urlquery.net/urlscan.io.
