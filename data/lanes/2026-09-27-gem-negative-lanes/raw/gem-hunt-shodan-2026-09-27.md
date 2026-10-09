# HUNT LANE 17 — Shodan
Date: 2026-09-27
Task: internet-wide scan data on the campaign's infrastructure footprint — host lookup for
20.49.140.101, search for `http.html:"go-import"`, hosts referencing council modern.gov
domains / r.jina.ai.

## Tool status (honest)

- **Shodan host pages** (`shodan.io/host/<ip>`): PUBLIC, no login — full banner/cert data retrieved.
- **Shodan search UI** (`shodan.io/search?query=...`): fetch timed out at the worker level
  (RECV_TIMEOUT, upstream fetch failure). Per lane rules this was NOT retried, so the
  `http.html:"go-import"` search and the council/r.jina.ai host searches are **unexecuted**.
  The Shodan search API requires an API key; no account was created per instructions.
- **DNS note**: local resolver returns 198.18.253.23 / 198.18.253.24 (RFC 2544 benchmark space)
  for r.jina.ai / s.jina.ai — almost certainly sandbox egress interception, not the real
  addresses. Not pursued; treat as unreliable.

## Finding 1 — 20.49.140.101 host page (SUCCESS)
URL: https://www.shodan.io/host/20.49.140.101

- **Device**: Microsoft Azure Application Gateway v2.
- **Open ports**: 80/tcp, 443/tcp, 4443/tcp — all return `HTTP/1.1 404 Not Found`
  via `Server: Microsoft-Azure-Application-Gateway/v2` (scans dated Sep 24–26, 2026).
- **TLS certificates observed**:
  - 443: CN=dev.southwark.gov.uk, O=London Borough of Brent, Entrust-issued (2023–2024 validity window
    on the captured cert); SANs: dev.southwark.gov.uk, www.dev.southwark.gov.uk, devlocaloffer,
    devpropertylicensing, devschools, devcypdirectory, devforms, devsafeguarding, devmy.
  - 4443: CN=geomap.southwark.gov.uk, Sectigo-issued Dec 2025 – Jan 2027.
- **No campaign markers**: no go-import content, no beacon strings, no anomalous banners.
  This is a plain council Azure front door.

**Interpretation**: Shodan independently corroborates the urlscan finding — 20.49.140.101 is
genuinely Southwark council's Azure-hosted estate (gateway + council certs). The SSRF ladder's
raw IP in the campaign payloads was **real target infrastructure, not attacker infrastructure
and not a decoy**. The campaign pointed its tooling at the victim's own front door.

## Finding 2 — go-import host search (BLOCKED, not executed)
- `http.html:"go-import"` via the Shodan web search UI: fetch timed out; not retried per rules.
- Requires: Shodan account / API key for the search API.
- **Recommendation for parent**: this is the one Shodan query worth running with credentials —
  it would enumerate every internet host currently serving a `<meta name="go-import">` tag,
  i.e. the live set of go-import confusion endpoints (legit + campaign-shaped).

## Finding 3 — council / r.jina.ai host searches (BLOCKED, not executed)
- Same search-UI dependency; not executed. r.jina.ai IPs could not be reliably resolved
  from this environment (see DNS note).

## Bottom line for the parent
1. Shodan host pages are open and useful: the 20.49.140.101 lookup is a clean,
   independently-verifiable confirmation that the campaign's SSRF target IP is the
   victim's own Azure estate.
2. The high-value Shodan work (internet-wide `http.html:"go-import"` enumeration) needs
   an API key — flagged as the single Shodan action worth credentialed follow-up.
3. No attacker infrastructure surfaced: the campaign left no Shodan-visible hosts of its own
   in what was reachable without credentials.
