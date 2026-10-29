# Probe results — workbench-161.248.63.110 (2026-10-23)

Target: https://161.248.63.110:443 (Cairn-family "自动化渗透测试工作台", AS215355, ALICE NETWORKS LTD)
Worker: passive fieldwork lane. Method: curl GET only, TLS verification skipped (IP-literal host), polite ~3s between requests.
Root page previously captured: silent-locus/data/lanes/india-cert-in/raw/discovery/pentest_wb_161.248.63.110_root.html

## 1. Liveness

- GET https://161.248.63.110:443/ → **200** at 2026-10-23T14:10:53Z. Host is LIVE.

## 2. Endpoint probe results

All probed GET-only, one at a time, 2026-10-23T14:11–14:12Z. No 401/403, no credential prompt, no session/login requirement encountered.

| Endpoint | HTTP | Auth gate | Notes |
|---|---|---|---|
| /logs | 200 | none | **byte-identical to root page** (SPA index.html fallback) |
| /api/logs | 404 | n/a | not found |
| /history | 200 | none | **byte-identical to root page** |
| /api/history | 404 | n/a | not found |
| /projects | 200 | none | **byte-identical to root page** |
| /api/projects | 404 | n/a | not found |
| /tasks | 200 | none | **byte-identical to root page** |
| /api/tasks | 404 | n/a | not found |
| /runs | 200 | none | **byte-identical to root page** |
| /api/runs | 404 | n/a | not found |

Key finding: all five 200 responses are the same 4,618-byte HTML document — sha256 a58eed50376f5a018673e018811eb367027abd059c0c613b63a2143f, md5 3bc55ee449c9b9eac6c9995491603bd0 — identical to GET `/`. This is a React single-page app whose server serves index.html for all non-API routes. **No server-rendered log, history, task, project, or run content was reachable via GET on the common surface list.**

## 3. What was pulled

Directory: `silent-locus/data/lanes/india-cert-in/raw/workbench-161.248.63.110/logs/`

Each file is 4,618 bytes; each has a matching `.PROVENANCE.txt` (URL, UTC retrieval time, curl method, identity note) and `.sha256`.

- logs-20261023T141149Z.html
- history-20261023T141157Z.html
- projects-20261023T141202Z.html
- tasks-20261023T141207Z.html
- runs-20261023T141213Z.html

No response exceeded the 5MB cap; no truncation was needed.

## 4. Content notes (page shell only)

The 4,618-byte shell contains no logs, no data, no credentials, no human-identifying content (no names, emails, billing — grep found zero email-like strings). Structural observations recorded for the analysis lane:

- `<title>自动化渗透测试工作台</title>`; meta description: "面向已获授权目标的自动化渗透测试与安全评估工作台" (automated pentest and security-assessment workbench for authorized targets).
- React SPA; boot splash; theme key `localStorage["cairn.theme.preference"]` — client code uses the "cairn" name.
- Entry bundle: `/assets/index-30P0W08I.js`; stylesheet: `/assets/index-1r_Fpo0j.css`. **NOT fetched** — kept as a lead for the analysis lane, out of this probe's scope.
- Any real log/history content would load client-side via the bundle's internal API calls (no such route is exposed on the common GET list).

## 5. Stop conditions / threads stopped

- **No stop conditions were triggered.** No 401/403, no login screen, no credential prompt, no human-identifying content, no third-party victim data encountered.
- No endpoint beyond the assigned common list was guessed, fuzzed, or requested. No JS-bundle API routes were fetched or enumerated.
- If the analysis lane wants to continue: candidate leads are the client bundle (`/assets/index-30P0W08I.js`) to enumerate the app's internal API routes, and the bundle-sourced routes it uses to fetch log/history data. Expect auth gates there; further work should be scoped by the parent.

## 6. Anomalies

None observed at the HTTP level. The only notable behavior is the blanket index.html fallback for all non-API GET routes (typical SPA hosting), and 404 on all /api/* guesses.

## 7. Files produced

- This report: `silent-locus/data/lanes/india-cert-in/raw/workbench-161.248.63.110/probe-results-2026-10-23.md`
- Evidence: `silent-locus/data/lanes/india-cert-in/raw/workbench-161.248.63.110/logs/` (5 × HTML + 5 × PROVENANCE.txt + 5 × sha256)
