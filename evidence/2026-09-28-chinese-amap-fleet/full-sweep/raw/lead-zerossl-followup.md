# ZeroSSL lead follow-up — programmatic cert issuance on `<14-hex>.lhr.life` (2026-10-05)

Deepens `cert-transparency.md` §1b. Raw evidence: `ct_zerossl_certspotter_2026-10-05.json`
(CertSpotter dump, 41 records, this dir).

## 0. Source notes — crt.sh was down; CertSpotter used instead

- crt.sh `?q=%.lhr.life&output=json` attempted 6× over ~40 min (2026-10-05 ~05:01–05:28 UTC):
  2× curl timeout (120 s, 180 s), 4× HTTP 502 (nginx, fast-fail by the end).
  Narrow queries (`q=0%.lhr.life`, `exclude=expired`) also 502 — backend-wide outage,
  not query-weight. **The 4 pre-2026 ZeroSSL names from the §1b sweep could not be
  re-verified or named; re-fetch when crt.sh recovers.** Do not treat this as a negative.
- Fallback (documented for reuse, per collection doctrine): **CertSpotter keyless API**
  `GET https://api.certspotter.com/v1/issuances?domain=<d>&include_subdomains=true&expand=dns_names&expand=issuer`
  — no key, browser UA, ~35–55 s per call. Pagination via `Link: <...?after=<id>...>; rel="next"`
  (header path is relative AND drops `/v1` — re-prefix it). Records: `id`, `tbs_sha256`,
  `cert_sha256`, `dns_names`, `pubkey_sha256`, `not_before`, `not_after`, `revoked`,
  `issuer{name}`. **Dedupe by `tbs_sha256`**: each CT-log submission is a separate record
  (same cert appears 2–3×). History depth limited: page 2 (`after=`) returned `[]` —
  for `lhr.life` coverage starts 2026-05-31. Not a substitute for crt.sh on old certs.
- urlquery keyless htmx via **curl, not `uq_htmx.py`**: python `urllib` dies in the
  proxy CONNECT tunnel on this VM (same egress-proxy class of failure as the HF
  `httpx2` issue in TOOLS.md); curl handles the proxy fine. Exact call used:
  `curl -H "HX-Request: true" -H "Accept: text/html" -H "HX-Current-URL: https://urlquery.net/search?q=<q>" "https://urlquery.net/api/htmx/search/?q=<q>&limit=25&offset=0"`
  with browser UA, 5–6 s pacing (first 2 calls in a batch timed out once, succeeded on retry).

## 1. ZeroSSL tunnel-name table (CertSpotter window: 2026-05-31 → 2026-10-03)

Deduped by `tbs_sha256`. All names are bare `<14-hex>.lhr.life` (single SAN each).

| first seen | name | ZeroSSL certs | intermediate(s) | also issued by |
|---|---|---|---|---|
| 2026-08-14 | `efa9eb3bda1df5` | 1 | ZeroSSL RSA DV SSL CA 2 | — |
| 2026-08-20 | `967f1af7dfd915` | 1 | ZeroSSL RSA DV SSL CA 2 | — |
| 2026-09-10 | `a7bfa19dd56391` | 1 | ZeroSSL RSA DV SSL CA 2 | — (NEW vs §1b) |
| 2026-09-22 | `ca990e9a89525d` | 1 | ZeroSSL RSA DV SSL CA 2 | — (NEW vs §1b) |
| 2026-10-02 | `deab0fff603d04` | **2** | ZeroSSL **ECC** DV SSL CA 2 **+** ZeroSSL RSA DV SSL CA 2 | — |
| 2026-10-03 | `0418f1e395a48e` | **2** | ZeroSSL **ECC** DV SSL CA 2 **+** ZeroSSL RSA DV SSL CA 2 | — |
| 2026-10-03 | `92f1f5cd378431` | 1 | ZeroSSL RSA DV SSL CA 2 | Let's Encrypt YR2 (2026-10-02, day before) |

Plus 4 older ZeroSSL names from the §1b crt.sh sweep (first-seen 2023-08-17, 2024-05-01,
2026-06-13, 2024-06-29) — **names not recovered** (crt.sh down; outside CertSpotter window).
Minimum distinct ZeroSSL tunnel names overall: **11** (7 verified here + 4 from §1b).

Adjacent multi-CA names in the same window (not ZeroSSL, but same programmatic shape):
- `93ca25e80716ce` (2026-10-03): **3 distinct certs, 3 CAs, 1 day** — LE YE2 + LE YR1 + SSL.com TLS Issuing RSA CA R1.
- `1338981620088f` (2026-09-22): 3 distinct LE certs (YE2 + 2× YR1), 1 day.
- `4fee6c798907e5` (2026-09-15): 2 distinct LE YE1 certs, 1 day.
- `deab0fff603d04`, `0418f1e395a48e`: dual RSA+ECC ZeroSSL same-day (see table).

## 2. urlquery lookups (keyless htmx, 2026-10-05)

All 8 names searched (`--limit 25` equivalent): **0 reports each** — `efa9eb3bda1df5`,
`967f1af7dfd915`, `deab0fff603d04`, `0418f1e395a48e`, `92f1f5cd378431`, `a7bfa19dd56391`,
`ca990e9a89525d`, `93ca25e80716ce`. (Endpoint returned literal "No reports found".)
Local corpus check: 0 hits for all names across `events.jsonl`, `urlscan-lhr/`, `raw/`
(the amap-fleet `events.jsonl` contains no `lhr.life` at all — it is the amap.com corpus).
Web search for the two Oct names: no indexed-web hits.

## 3. DNS / HTTPS liveness — INCONCLUSIVE (VM egress limitation, not a negative)

- This VM's egress proxy intercepts DNS (`dig <name>.lhr.life` → `198.18.0.20x`, RFC-2544
  benchmark range) and HTTPS is proxied (CONNECT via `fd8b:4f84:7d32:99::1`).
- One transient probe returned `HTTP 502` with body `no tunnel` (localhost.run edge's
  dead-tunnel response); all subsequent probes (incl. a known-fleet control tunnel seen
  in urlquery 2026-10-04) returned `http=000` connection failures. Signal is proxy
  flakiness, not tunnel state. **Liveness cannot be determined from this VM — needs an
  off-proxy vantage point.** Recorded as unanswered, not as "tunnels are dead".

## 4. Assessment

**Single actor vs many:** the October cluster points to ONE actor running cert-automation
experiments: dual RSA+ECC ZeroSSL issuance on `deab0fff603d04` (Oct 2) and `0418f1e395a48e`
(Oct 3) is the same distinctive fingerprint on consecutive days; `93ca25e80716ce` got
three different CAs in one day (Oct 3); `92f1f5cd378431` switched LE→ZeroSSL overnight.
The Aug–Sep ZeroSSL certs (RSA only, ~1–2/week, no bursts) look like the same pipeline in
an earlier config — ECC intermediates appear only from Oct 2 (tooling/config change).
The 2023–2024 ZeroSSL names (4, unrecovered) show the behavior is years old, not new.

**Timing:** steady trickle, not a fleet-provisioning burst. ~1 ZeroSSL cert per 1–2 weeks
Aug→Oct 2026. No single-day mass issuance.

**Grammar/marker overlap with fleet tradecraft:** NONE. Names are uniform random 14-hex
(char distribution flat across 0-9a-f; leading chars spread) — localhost.run's own
assignment format, identical to the fleet's tunnel names in form but sharing zero
actual names. No `uqscan=`, `uqcors`, epoch-nonce, or any agent-harness tokens anywhere
in CNs/SANs. **Zero overlap with the 78 known fleet tunnel names** extracted from
`writeup-lhr-life.md`.

**Fleet-adjacent vs independent: INDEPENDENT (evidence-weighted).**
For fleet-adjacent: same tunnel service, same 14-hex name format.
Against: (a) 0/78 name overlap; (b) 0 urlquery reports for all 8 checked names — the
fleet's tunnels DO get submitted to urlquery (that is where the 78 names come from), so
a ZeroSSL name with zero reports was never scanned, i.e. never part of the fleet's
scanning pipeline; (c) the fleet rides localhost.run's `*.lhr.life` edge wildcard and
has no need for per-subdomain certs (§1a mechanism) — per-subdomain issuance is a
different population by construction; (d) the multi-CA/RSA+ECC experimentation shape
matches someone testing ACME client tooling, not fleet provisioning.
No positive evidence links the ZeroSSL issuer to the Amap fleet operator.

## 5. Verdict

Someone has been programmatically issuing real (ZeroSSL/LE/SSL.com) certificates for
random localhost.run tunnel subdomains since at least 2023, currently ~1–2/week, with an
October 2026 escalation into multi-key-type (RSA+ECC) and multi-CA experimentation on
individual tunnel names. It is a distinct, independent actor from the Chinese Amap fleet —
same parking lot, different car. The lead stays open as a phenomenon (active, ongoing),
but it is NOT fleet infrastructure on current evidence.

## 6. Open questions

1. The 4 pre-2026 ZeroSSL names (first-seen 2023-08-17, 2024-05-01, 2024-06-13, 2024-06-29
   per §1b) — re-fetch `%.lhr.life` from crt.sh once its backend recovers; check whether
   they show the same dual-issuance/multi-CA fingerprints.
2. Liveness: are any of the 7 recent ZeroSSL tunnels currently up? Requires probing from
   a non-proxied vantage point (this VM's egress cannot answer it).
3. Attribution: CT exposes no ZeroSSL account info; the API-driven issuer is not
   publicly attributable from certificate metadata alone. (Hunt scope is agents/swarms —
   no operator-identity pursuit regardless.)
4. Is the Oct 2–3 cluster (dual RSA+ECC ×2 names, LE→ZeroSSL switch, 3-CA name) one
   actor's single test run? Timing says likely; unproven.
5. `uq_htmx.py` is broken on proxied VMs (urllib CONNECT timeout) — the curl form in §0
   is the working keyless path; worth patching the script or documenting the workaround
   in the urlquery skill.
