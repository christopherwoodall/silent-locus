# Other operators — persona-mimic hunt (2026-10-04)

Modeled two hypothetical operators from real precedent and hunted where THEY would leave traces.
Method: urlquery htmx batch (scripted, polite) + urlscan search API + Google-indexed scanner report pages.

## INFRA STATUS — read first

VM egress was **fully down** for the entire session (~23:24 CDT → end, 2026-10-04):
`urlquery.net`, `api.urlquery.net`, `urlscan.io`, `huggingface.co` all time out at the
egress proxy (20–60s timeouts, `curl` exit 28). Not host-specific — even the normally-working
HuggingFace route failed. Consequences:

- The 10-query urlquery-htmx batch (`/tmp/mimic/run_opA_htmx.py`, 6s between queries, tool
  delay 5s) could not run — every fetch failed. **Re-run it when egress recovers.**
- Authenticated `uq.py recent` (metronome clustering input) timed out twice.
- urlscan search API unreachable from the VM (independently key-gated anyway — see below).
- `browser.open` on the htmx endpoint returned empty (204); runtime barred retrying that route.

Evidence below therefore comes from **Google-indexed `urlquery.net/report/<uuid>` pages**
(via `browser.search`), whose "Related reports" tables give timestamps + neighboring
submissions. Findings marked [pending-egress] need the live API to confirm/extend.

---

## OPERATOR A — vuln-assessment swarm (tronzap-style precedent)

Known shape: systematic SSTI/RCE exploit-test matrix
(template-engine × bypass-variant naming: `k-ext-ssti`, `c-rc-php`, `o-rc-{nl,dollar,semi}`,
`calc` PoCs, `e0-ev2` eval series, `chk2.html`), run through localhost.run tunnels against
tronzap.com's full estate (dash/api/bo/dev/staging), submitted via urlscan API,
~40 scans in 2hr bursts. Different actor from our Amap operator.

### Hunt results

- **Open web: NEGATIVE.** `"k-ext-ssti" OR "e0-ev2" OR "eval-stdin"` → zero hits anywhere
  (no GitHub, no blogs, no writeups). Operator-internal labels, as expected — the signal
  lives in scanner DBs, not the open web.
- **Google-indexed urlscan results: NEGATIVE.** `site:urlscan.io tronzap` → nothing;
  `urlscan.io "dash.tronzap.com" OR "api.tronzap.com"` → nothing (only TronZap's own
  gitbook docs describing the estate). The known campaign's ~40 scans are not Google-indexed
  (unlisted/private visibility, or simply uncrawled).
- **Google-indexed urlquery reports: NEGATIVE.** `site:urlquery.net/report "calc.html" OR
  "chk2.html"` → none; `site:urlquery.net/report ssti exploit template injection` → none;
  `site:urlquery.net/report tronzap` → none. Consistent with the known campaign using
  urlscan only, not urlquery.
- **Context (not attribution):** tronzap.com is a TRON energy-rental service
  (dashboard `dash.tronzap.com`, API `api.tronzap.com` per their gitbook); ScamMinder
  rates tronzap.com 10/100 ("Scam"). The vuln-assessment target is itself a shady
  crypto service — worth remembering when modeling motive, not a lead by itself.
- **No NEW campaign with the same matrix shape found.** The naming grammar
  (`<engine>-<class>-<variant>`, `calc`/`chk2` PoC pages, `e0-ev2` eval series) is
  distinctive enough that a second campaign would be recognizable in urlscan search —
  **that check is [pending-egress] + needs a urlscan API key** (see Delegation).

### Delegation need (Operator A / urlscan)

urlscan's search API is key-gated (401 without a key); no urlscan connector/skill exists.
To hunt the matrix on other targets, an eligible agent needs to run, with a urlscan API key:
`GET https://urlscan.io/api/v1/search/?q=page.url%3A%22ssti%22%20OR%20page.url%3A%22calc.html%22%20OR%20page.url%3A%22chk2.html%22%20OR%20page.url%3A%22rc-php%22&size=100`
then cluster hits by `page.domain`, looking for a second target with the
`<engine>-<class>-<variant>` / `calc` / `e0-ev2` naming shape in a tight time burst.
(Live-browser fallback: urlscan.io/search/ is JS-driven.)

---

## OPERATOR B — detection/verification swarm (jmail.world-style precedent)

Known: 72 metronomic urlquery submissions (3-min cadence, 4hrs) auditing jmail.world
(forum/drive abused as phishing-redirector farm), 12 routed through cachedview.nl
archive-aggregator as fetch proxy, probing the target's own search with known-bad URLs
+ watch-phrase `seekers+of+decay`.

### B-1. The seekers campaign is BIGGER than the known 72

Google-indexed urlquery reports extend it in both directions:

**Google-oracle probes of the same watch phrase** (predates the September jmail bursts):
- `www.google.ca/search?q="seekers+of+decay"&udm=50` — 2026-07-08, 2026-07-10
  (also `%22seekers%20of%20decay%22` variant, 2026-07-10 12:03)
- `www.google.co.nz/search?q="seekers+of+decay"&udm=50` — 2026-07-09, 2026-07-11
- `www.google.im/search?q="seekers+of+decay"&udm=50` — July 2026 (dateless in snippet)
- `www.google.es/search?q="seekers+of+decay"&udm=50` — undated, same batch family
- `www.google.ru/search?q="seekers+of+decay"&udm=50` — 2026-09-03 14:58
- Report pages: https://urlquery.net/report/d24fdc14-0f05-40d6-9082-5c2da4daaa8c
  (google.ru), https://www.urlquery.net/report/f1d97eb1-cba4-4ad3-9090-45950dda0f88
  (google.ca), https://urlquery.net/report/ba8ff9d7-61d9-4ae2-b07c-f56ff9cb4ddb
  (google.co.nz), https://urlquery.net/report/2df7f3fd-1aac-4947-9325-9afef944b44f
  (google.im), https://urlquery.net/report/5fd2ea8a-d9f6-4bba-89fa-06f50350d8af
  (google.es)

`udm=50` = **Google AI Mode** (confirmed: kevinleary.net search-operators reference,
github.com/hiddenwaffle/udm50, Fortinet community doc). The operator asks AI Mode about
the canary phrase — a second oracle alongside the target's own search. The phrase was in
the operator's playbook by **July 2026**, ~2 months before the September jmail bursts.

**jmail.world seekers probes** (indexed report pages, UTC):
- 2026-09-05 17:57–18:00 — `jmail.world/person/appointment-dermnet?q=seekers+of+decay`,
  `jmail.world/thread/EFTA02287726?q=https%3A%2F%2Flivetraffic.net%2Flogin%3Frefer%3D119334`
- 2026-09-09 15:50–15:56 — `person?page=117`, `person?page=38`, `thread/EFTA02335749`
- 2026-09-12 03:54–03:55 — `person/philip-levine-baron-corp`
- 2026-09-15 00:27–00:45 — `person/craig-martin`, `sent/page/33`, `drive/vol00011-efta02536562-pdf`,
  `drive/item/EFTA00017193.pdf`, `drive/vol00011-efta02332522-pdf`
- 2026-09-17 20:08–20:09 — `thread/65001b8b4211528e5ed045d0254aad95`
- 2026-09-22 09:05–09:12 and 15:32–15:33 — `person?page=64`, `promotions/page/54`,
  `thread/81bb7832e0bf965de401fc4a6b12b864`
- 2026-09-23 23:24 — `person?page=78`
- 2026-09-24 01:35–01:38 — `person/jeff-fuller-mc2mm`, `drive/vol00010-efta00220819-pdf`
- 2026-09-26 22:59–23:00 — `person/meister-todd`
- Report pages: https://urlquery.net/report/6ca811d6-d33d-4133-b429-2f1cd546bac5
  (09-05), https://urlquery.net/report/13e93e39-da26-4cc1-bebe-e1a4c9aca12a
  (09-09), https://urlquery.net/report/7762cc3d-1575-4eba-956d-18dca9765702
  (09-15), https://urlquery.net/report/2a06faee-0af0-46f6-9eda-f79fbea6b672
  (09-22), https://urlquery.net/report/cce3bf10-a097-40b3-8dcc-a0f794dc85e9
  (09-23), https://urlquery.net/report/0f0999f1-dc53-4318-bdff-e4f504593a61
  (09-24), https://urlquery.net/report/6327e602-f0bb-4274-962b-b3275f2734a9
  (09-26)

**Shape notes (metadata tells the story):**
- Multiple bursts across 2026-09-05 → 09-26 (3 weeks), not one 4hr window. The known
  "72 submissions / 3-min cadence / 4hrs" is one burst; the campaign runs repeated bursts.
- Within-burst spacing ~2–5 min (e.g. 09-15: 00:32, 00:34, 00:37, 00:42, 00:45;
  09-09: 15:50, 15:52, 15:52, 15:55, 15:56) — consistent with the known 3-min metronome.
- Probe alternation: `q=seekers+of+decay` alternates with `q=<known-bad redirector URL>`
  (`https://www.followlike.net/?r=19384926`, `https://www.followlike.info/?r=19384926`,
  `https://livetraffic.net/login?refer=119334`) across jmail paths
  (`person/`, `thread/`, `drive/`, `promotions/`, `sent/`). The audit checks BOTH the
  canary phrase AND known-bad URLs against the target's own search — detection loop:
  is the redirector farm still indexed/serving?
- Neighboring submissions in each burst: `appwrite.io/verify-email` / `/reset` links
  (TDS up to 26), random `.vip`/`.shop`/`.date` spam domains, phishing verify chains —
  the operator submits a mixed queue; the jmail probes are the metronomic spine.
- Seekers probes trip TDS=2 (the farm content fires Threat Detection Systems).

### B-2. NEW — the `udm=50` SEO-indexation verification swarm (misfit → lead)

Same `&udm=50` (AI Mode) submission grammar, interleaved in the SAME report batches as
the seekers probes — but the queries target spam pages, e.g.:
`www.google.ru/search?q=Content+maker+online%3A+https%3A%2F%2Fbacklink-generator-tool.github.io%2Fbacklink-generator-tool%2Fdemo%2Fsmart-backlink-automation-platform-for-websites.html%3Fhttps%253A%252F%252F...%252Forganic-engagement-exchange-2026.html&udm=50`
— i.e. asking AI Mode about a spam page to check whether it got indexed.

- **Domains:** backlink-generator-tool.github.io, traffic2archive.github.io,
  BoostExchangeNow.github.io, BacklinkMaker.github.io, SocialBoostExchange.github.io,
  autolinkbooster.blogspot.com, prolinkbuildertool.blogspot.com,
  backlinkpulse.blogspot.com, rankboosterbacklinks.blogspot.com,
  quicklinkbuilder.blogspot.com, index-boost-tool.blogspot.com.
- **Google country-domain rotation:** .co.nz (2026-01-11, 01-13, 01-22), .ca/.im (July),
  .ru/.es (2026-09-03). Running since at least **January 2026**.
- **cachedview.nl tie-in:** the `index-boost-tool.blogspot.com` urlquery report
  (https://urlquery.net/report/ede7b468-0905-4451-b6d3-2837a2be1a2a) has `cachedview.nl`
  in its Host Summary (first seen 2025-12-18, last 2026-06-04) alongside
  `traffic-exchange.github.io` and `backlink-generator-tool.github.io` (3 host alerts) —
  the archive-aggregator-as-oracle tradecraft appears in this swarm too.
- **Assessment:** either the same operator's second business (blackhat-SEO indexation
  checks) or a different operator reusing the `udm=50` oracle grammar. Shared submission
  batches + shared cachedview.nl usage lean same-operator. Either way this is a NEW
  detection/verification swarm beyond the known jmail.world one. Scope kept to
  agents/swarms — no human attribution attempted.

### B-3. Phishing-redirector audit via Google `/url` chains

The same batches submit `google.*/url?q=<rand>&…&url=amp/<phish-domain>/…/<base64-email>`
URLs — feeding Google-redirect-abusing phishing chains to urlquery's sandbox to capture
the full redirect chain (detection/verification of live phishing infra):

- `…&url=amp/blitz…co­m/sys/ccs/o3ioaBdijBrgB3LkqCUGqxST/YWhvbGxhbmRAc2x1cnBtYWlsLm5ldA==`
  → base64 decodes to `aholland@slurpmail.net`
- `…&url=amp/antitrustlawcenter.org/dayo/available/YXNobGVlLmhvZGdlQGpvaG5zdG9uZ3JvdXAuY2E=`
  → `ashlee.hodge@johnstongroup.ca`
- `…&url=amp/phillydj.com/gbadun/uqILDQrXlwLFfXjPN41Xmzn4/amh1YmVydEBobWVwYXJ0cy5jb20=`
  → (same email-in-redirect grammar)
- `…&url=amp/mapleleafreborns.com/heishers/cRFYv3HbKJLV1oXKjZq6UgAj/eHF0ZWFjaGVybG9nc0BtZHJjLm9yZw==`
  → `xqteacherlogs@mdrc.org`
- `maps.google.ca/url?q=https%3A%2F%2Ftaiwanmid.com%2Fweb%2Fbrowser%2F&…#?defvwerwfer=c2RyZW5uZW5AZXhhY3RzY2llbmNlcy5jb20=`
  (base64 email as fragment param)

Same operator family (shared batches with the seekers probes). The victim emails are
phishing-kit redirect parameters, recorded here as infrastructure metadata only.

### B-4. Archive-oracle-as-fetch-proxy usage

- **cachedview.nl:** known 12 in the jmail burst; ALSO used by the B-2 SEO swarm
  (index-boost-tool.blogspot.com report). Archive-aggregator-as-oracle is shared
  tradecraft across both swarms — treat as an operator-family marker.
- **archive.ph / archive.is / archive.today as submitted URLs:** only benign-looking
  clusters found — `archive.is/www.bloomberg.com/...` paywall-dodge submissions
  2026-09-21–24 from one IP (185.14.97.131, AS56655 Gigahost), TDS 1–3, plus old
  one-offs (imgur 2024-10, shilapatra 2025-05). No agent-swarm shape; noted as a
  possible lead (clustered, single IP, 4 days) but likely human news archiving.
  Report: https://urlquery.net/report/5ca4e99c-48b6-4180-990f-eb6ff1117b4e
- **Megalodon, ghostarchive:** zero indexed urlquery submissions.

### B-5. Metronome clustering on OTHER single targets — [pending-egress]

Blocked by the outage. Ready method: `uq.py recent --limit 200` → group by host →
interval analysis → flag low-CV regular cadences against a single host. The indexed
data already shows the jmail bursts at 2–5 min spacing; the live run will confirm the
cadence precisely and surface any other metronomic single-target audits.

---

## Summary for the parent

1. **Operator A:** no new campaign found; honest negatives on open web, Google-indexed
   urlscan, and Google-indexed urlquery. The urlscan-API matrix hunt needs a urlscan API
   key + recovered egress (exact query + delegation spec above).
2. **Operator B:** the known jmail.world audit is one campaign of a larger operator
   family: seekers watch-phrase probes run Jul→Sep 2026 across jmail.world's own search,
   Google AI Mode (`udm=50`), with known-bad-URL alternation and cachedview.nl proxying.
   **New lead:** a `udm=50` SEO-indexation verification swarm (Jan→Sep 2026, 11+ spam
   domains, rotating Google country domains, cachedview.nl usage) interleaved in the same
   submission batches — likely the same operator's second lane. Plus a phishing-redirector
   audit lane submitting Google `/url` → AMP-cache → base64-email redirect chains.
3. **Pending when egress recovers:** `/tmp/mimic/run_opA_htmx.py` (10 polite htmx queries:
   ssti, rc-php, eval-stdin, calc.html, chk2.html, k-ext-ssti, e0-ev2, o-rc-, c-rc-,
   tronzap) and the `uq.py recent` metronome clustering.
