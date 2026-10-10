# Certificate Transparency sweep — tunnel services & amap (2026-10-04)

Surface: CT logs via crt.sh. Goal: find undiscovered agent/swarm fleets via
bulk-issuance shapes (many certs, short windows, non-random naming grammars).
Known context (excluded from "new"): Chinese Amap-map data-collection fleet on
`<hex>.lhr.life` (localhost.run) tunnels, `uqscan=<word><date>` tags, Jan–Oct 2026.

Raw query dumps (JSON, kept on the collecting VM in /tmp; re-fetchable):
- `/tmp/ct_lhrlife.json` — `%.lhr.life` (286 rows)
- `/tmp/ct_cf.json` — `%.trycloudflare.com` (5,000 rows — crt.sh JSON row cap)
- `/tmp/ct_ngrok.json` — `%.ngrok.io` (4,909 rows)
- `/tmp/ct_ts.json` — `%.tailscale.com` (4,997 rows)
- `/tmp/ct_amapdot.json` — `%.amap.com` (1,223 rows)

## 0. crt.sh machine interface (per 2026-10-04 collection doctrine)

Page source of `https://crt.sh/` fetched (5,897 bytes). The frontend is a plain
HTML 4.01 GET form (`<FORM name="search_form" method="GET">`) with ONE inline
script (39 chars: `document.search_form.q.focus();`). **There are no XHR/fetch/
htmx/JS endpoints** — the machine interface IS the form's GET target:

- `GET https://crt.sh/?q=<LIKE-pattern>&output=json` — `%` wildcards;
  `%.example.com` = subdomains; a bare `foo` also substring-matches.
- `output=` variants: `json` (used here), `atom`, `csv` (not exercised).
- Known but not exercised: `exclude=expired`.
- Quirks observed 2026-10-04: JSON hard-caps at **5,000 rows** (exact 5,000 on
  trycloudflare); heavy queries 502 (amap.com once, recovered on retry) or time
  out entirely (broad `%amap%`, 3 attempts); transient 404s on first attempt of a
  new query. Pacing 8–15 s between queries + a browser User-Agent kept it alive.
  Each JSON row carries a `result_count` field (values 1–3 observed) whose meaning
  is undocumented — not interpreted here.

## 1. `%.lhr.life` — 286 rows, 115 unique names (2020-04-22 → 2026-10-03)

- 112 `<14-hex>.lhr.life` tunnel certs + 3 base names (`lhr.life`, `localhost.run`,
  `dev.localhost.run`). **Zero agent-harness naming** anywhere in CNs/SANs — no
  `uq`, `agent`, `fleet`, `swarm`, `harness`, `probe` tokens; labels are pure
  lowercase hex, all exactly 14 chars (localhost.run's standard random SSH-tunnel
  subdomain format).
- Issuance shape: sparse, 1–4/day typical; mini-bursts 2025-02-22 (7) and Aug 2026
  (9, spread across the month, LE YE1/YE2/YR1/YR2 + 2 ZeroSSL — organic, no
  single-day burst). Issuers: ~85% Let's Encrypt (full intermediate rotation:
  R3/E5/E6/R11/E7/E8/R10/R13/R12/YE1/YR1/YR2/YE2), ZeroSSL (15 rows / 9 unique
  names), Amazon (base names only), DigiCert (2020 apex only).
- Verdict on fleet provisioning: **no burst, no naming grammar → no fleet shape.**

### 1a. KEY ANOMALY — known fleet subdomains are absent from CT (lead, not negative)

Our repo holds **83 distinct `<hex>.lhr.life` subdomains** from the fleet's
urlquery reports (e.g. `117316201a4b6d.lhr.life` seen 2026-10-04,
`4971ea21124a89.lhr.life` seen 2026-08-23). **0 of 83 appear in CT.**
Exact-match verification (crt.sh `?q=<name>&output=json`):
- `01b17695d6b838.lhr.life` → `[]`
- `02e18ab88f2ece.lhr.life` → `[]`
- `05f62f53cd7fd2.lhr.life` → `[]`
- `1140d08703ca02.lhr.life` → `[]` (after one curl retry)
- Control `0418f1e395a48e.lhr.life` (from the wildcard result set) → 1 cert,
  proving exact-match works and the zeros are real.

**Mechanism found (explains the absence — structural, not evasion):**
localhost.run terminates tunnel TLS at its edge with a wildcard `*.lhr.life`
cert (Amazon ACM, CN=`localhost.run`, SAN=`*.lhr.life`, renewed ~annually
2020 → 2026-05-31; `*.dev.lhr.life` on CN=`dev.localhost.run`). Per-tunnel
subdomains never need individual certs — the fleet's HTTPS rides the service
wildcard. The 112 individually-issued per-subdomain certs are a *different
population* (tunnel users who self-issued certs for their own subdomains).

Consequence: **CT is structurally blind to this fleet's tunnel provisioning.**
First-seen dates for the fleet's tunnels cannot be recovered from CT. urlquery
report dates (Jan–Oct 2026 per writeup-lhr-life.md) remain the timeline source.

### 1b. LEAD — ZeroSSL-issued per-subdomain certs, incl. 3 in the last 3 days

9 unique tunnel names carry ZeroSSL certs (not LE): 2023-08-17, 2024-05-01,
2024-06-13, 2024-06-29, **2026-08-14 `efa9eb3bda1df5`, 2026-08-20
`967f1af7dfd915`, 2026-10-02 `deab0fff603d04`, 2026-10-03 `0418f1e395a48e`,
2026-10-03 `92f1f5cd378431`**. ZeroSSL issuance is programmatic (API-driven),
anomalous vs the normal LE flow. **Zero overlap with the 83 known fleet names.**
Someone is scripting cert issuance for localhost.run tunnel subdomains right
now. Recommended cross-lane check: urlquery/DNS/ping for these 9 names.

## 2. `%amap%` (broad identity-substring) — QUERY FAILED, documented

Attempted 3×: curl exit 28 (timeout) at 90 s and 170 s; once returned HTTP 502
in ~19 s. crt.sh's backend cannot serve this query. **Not a clean negative —
unanswerable via this path.** Scoped alternative `%.amap.com` used instead ( §3).

## 3. `%.amap.com` — 1,223 rows, 37 unique SANs — CLEAN NEGATIVE

All legitimate AutoNavi/Alibaba first-party infra: `*.amap.com`,
`*.apiinit/*.apilocate/*.aps/*.autolr/*.cms/*.et-api/*.gxd/*.innovation/
*.insight-api/*.lbp/*.manage/*.pre/*.publish/*.restapi/*.srp/*.tb/*.testing/
*.traffic/*.vs/*.yuntu.amap.com`, plus `restapi`, `apilocate`, `pcookie`,
`trafficubi-kuo.online.amap.com`, `sentry.aosdev.amap.com`, `hostmaster@amap.com`.
Issuers 99% GlobalSign OV (Alibaba's CA); legacy strays: DigiCert, WoSign,
TrustAsia, Symantec, GoDaddy, GeoTrust, StartCom. No third-party or
operator-looking names on amap.com. (Note: query was `%.amap.com`, subdomains;
apex `amap.com` appears in SANs.)

## 4. Other tunnel services

### 4a. `%.trycloudflare.com` — 5,000 rows (JSON ROW CAP HIT), 159 unique CNs
- Word-salad Quick Tunnel hostnames (`acid-federal-buys-spine.trycloudflare.com`),
  ~99% ZeroSSL. **Burst: 99 certs on 2021-06-13 + 44 on 2021-06-14** — a
  fleet-provisioning-shaped event, but June 2021 (historical, not new).
- Newest cert 2021-07-24; **nothing after mid-2021** — Cloudflare moved to edge
  wildcard termination; per-tunnel trycloudflare certs are dead. Clean negative
  for 2026 activity. Caveat: result set truncated at the 5,000-row cap; the
  unique-name analysis covers the returned sample.

### 4b. `%.ngrok.io` — 4,909 rows, 1,933 unique CNs
- All `<8-hex>.ngrok.io` (ngrok's legacy random format), ~98% Let's Encrypt X3/X1.
- **Newest cert 2019-08-31** — per-tunnel ngrok.io certs ended 2019 (ngrok moved
  to `*.ngrok.io` wildcard). Clean negative for anything recent.

### 4c. `%.localhost.run` — covered by §1
- Only the Amazon wildcard `*.lhr.life` (CN=`localhost.run`) + `*.dev.lhr.life`
  (CN=`dev.localhost.run`). No per-tunnel names. Consistent with §1a mechanism.

### 4d. `%.tailscale.com` — 4,997 rows, 177 unique SANs — CLEAN NEGATIVE
- All Tailscale corporate infra: derp1–24 relays (`derp3-sin`, `derp10-sea`,
  `derp1-nyc`…), `api`, `login`, `controlplane`, `pkgs`, `githook`. Newest
  2023-06-26. **Tailscale node/machine certs come from Tailscale's internal CA
  and are NOT publicly logged** — structural CT blind spot for tailnet nodes,
  same class of limitation as §1a.

## Verdicts

| Query | Verdict |
|---|---|
| `%.lhr.life` | No fleet shape (sparse, random-hex only). **2 leads:** (a) all 83 known fleet tunnels absent from CT — explained by `*.lhr.life` edge wildcard (CT blind spot, mechanism verified); (b) 9 ZeroSSL-issued tunnel-subdomain certs, 3 in last 3 days, zero fleet overlap — active programmatic issuance by unknown party |
| `%amap%` | Failed 3× (2 timeouts, 1 502) — unanswerable, not a negative |
| `%.amap.com` | Clean negative — all Alibaba/AutoNavi first-party |
| `%.trycloudflare.com` | Historical 2021-06-13/14 burst (99+44 certs, ZeroSSL word-salad names); dead since 2021-07-24 — clean negative for 2026 |
| `%.ngrok.io` | Dead since 2019-08-31 — clean negative |
| `%.localhost.run` | Wildcard-only — consistent with lhr.life finding |
| `%.tailscale.com` | Corporate infra only; node certs not publicly logged — clean negative |

**Bottom line:** No undiscovered 2026 agent/swarm fleet found in CT on this
surface. The surface's main yield is structural: both localhost.run and
Tailscale terminate tunnel TLS behind service wildcards / private CAs, so CT
cannot see fleet tunnel provisioning at all — absence of certs is expected and
must not be read as absence of activity. The one live lead is the ZeroSSL
programmatic issuance on `*.lhr.life` subdomains (§1b).
