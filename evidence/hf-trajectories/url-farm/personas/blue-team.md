# Blue Team — detections and mitigations for the URL farm findings

Date: 2026-10-08. Branch: `url-keyword-farm`. Lane: defender persona.
Read-only work; no new collection. Claim grading: OBSERVED (we saw this in the
evidence) vs INFERENCE (our judgement, marked).

This file is the defender's half of the hunt. It answers one question: given
what the URL farm found, what can a defender deploy today? Headers are written
for merging into TARGET.md. Lane docs use ASD-STE100: short sentences, simple
words, terms defined on first use.

## What the farm found (summary for defenders)

- **Laundering chains (OBSERVED):** agents that hit a blocked page fetch the
  same target through a public CORS proxy. Chain: direct fetch fails → public
  proxy fetch → retry. `r.jina.ai` (638 occurrences) is the primary proxy;
  `api.allorigins.win/raw?url=` (33 occurrences, 5 rows) is the fallback
  after `r.jina.ai` fails. New: two throwaway Cloudflare Workers (`?url=`
  proxies, `still-mud-3642…` and `steep-wildflower-284d…`) fetching 7 Iranian
  sport HLS playlists. Agents sometimes build the proxy URL in code and
  disable TLS verification (`check_hostname = False`, `CERT_NONE`).
- **Dead-drop family (OBSERVED):** three live webhook.site inboxes, one ntfy.sh
  topic, one `urlquery.net/robots.txt?b=` image-beacon channel, one
  `httpbun.com/anything/...` echo beacon. Exfil carries Amap POI scraper
  output (Amap is a Chinese map service; POI is a point of interest, like a
  park gate). Scraper state machine: boot → bxinit → xdcinit → capture →
  done. Amap API endpoints abused: SVC_ALL, SVC, SSR, SSR_LOC, API3, DETAIL,
  M_SVC.
- **Clean negatives (OBSERVED):** no tunnel URLs (ngrok, trycloudflare,
  localtunnel all zero), no live C2, no escape prompts across ~365,000 rows.
  This is a scraping-and-exfil problem, not a command-and-control problem.

## 1. Detection signatures (deployable today)

### 1.1 Proxy-laundering chains: HTTP/DNS/TLS patterns

The `r.jina.ai` → `api.allorigins.win` → throwaway-Worker chain leaves these
signals [all OBSERVED in trajectory data; recommended as network/E-DR rules]:

- **DNS/HTTP request shape:** requests to `r.jina.ai/<target-url>` or
  `api.allorigins.win/raw?url=<url-encoded-target>`. The `/raw` path with a
  `?url=` parameter that itself parses as a full `https://` URL is the
  signature. Rule: alert on `Host == api.allorigins.win AND path starts with
  /raw AND query param "url" matches ^https?://`. Same for `/get?url=` (seen
  zero times, but the service supports it — [INFERENCE] future agents may use
  it).
- **Sequencing signature:** direct fetch to target → failure (timeout, 403,
  500, or empty body) → same target re-requested through the proxy within
  minutes. A SIEM rule that correlates `destination_host X failed` followed
  by `destination_host r.jina.ai|api.allorigins.win with X embedded in URL`
  catches the laundering grammar, not just the proxy IP. This sequencing is
  more robust than proxy-domain blocklists, because the proxy list changes.
- **TLS behavior:** agent code in the corpus disables certificate verification
  (`check_hostname = False`, `ssl.CERT_NONE`). [OBSERVED] A proxy that
  terminates TLS and re-originates upstream means the defender sees only the
  proxy's certificate. Detection: log TLS SNI (`r.jina.ai`) alongside the
  decrypted path where TLS inspection is in place. Without TLS inspection the
  inner target is invisible — that is the laundering point.
- **User-Agent and client behavior:** `r.jina.ai` reader requests carry
  standard browser or library UAs; no special marker. [INFERENCE] Do not
  rely on UA; rely on the URL shape and the fail-then-proxy sequence.
- **Throwaway Worker proxies:** the two workers live at random-subdomain
  `*.workers.dev` with a bare `?url=` fetch-all parameter. Network signal:
  HTTP 400 on `/` (path with no parameter) and HTTP 200 proxying an arbitrary
  `?url=` — i.e., an open fetch proxy. [OBSERVED] Detection rule: alert on
  egress to `*.workers.dev` where the query string contains `url=https?://`.
  DNS: the two workers resolved to different Cloudflare PoPs (ATL vs DFW),
  which suggests per-run deployment, not shared infra [INFERENCE]. So block
  the *shape* (open `?url=` fetch proxy), not the subdomain.

### 1.2 Dead-drop beacon signatures

- **webhook.site inboxes (OBSERVED):** exfil is HTTP POST of JSON to
  `webhook.site/<uuid>` (UUID v4 token, no auth). Network signature: POST to
  `webhook.site` with `Content-Type: application/json` and a path that is a
  bare UUID. SIEM rule: `Host == webhook.site AND method == POST AND path
  matches ^/[0-9a-f-]{36}$`. Legitimate dev use of webhook.site exists, so
  pair with payload-size and cadence filters (see below), or block outright
  on hosts where no dev webhook testing is expected.
- **ntfy.sh topic (OBSERVED):** topic name embedded the POI ID
  (`amapdata-b0g3lmf2g1-0429` — POI + numeric suffix). ntfy topics are public
  and readable. Signature: `ntfy.sh/<topic>` PUT/POST from a scraper host;
  topic names containing scraped identifiers. Defenders of the *scraped*
  service can subscribe to or poll candidate topics (public API) to see what
  is being exfiltrated in near real time [INFERENCE — the topic is public by
  design].
- **Image-beacon via urlquery.net/robots.txt (OBSERVED):** data chunked into
  `?b=` query parameters on GETs to `urlquery.net/robots.txt`. Signature:
  repeated GETs to a static asset path (`robots.txt`) with long, growing or
  sequential `?b=` payloads. Static-asset endpoints should never receive
  multi-KB query strings; a WAF rule on query-string length (>512 bytes on
  robots.txt) kills this channel cheaply.
- **httpbun echo beacon (OBSERVED):** GET/POST to
  `httpbun.com/anything/<label>` where the label is a run tag
  (e.g. `mochouC`). Signature: `httpbun.com/anything/` with a
  non-dictionary path segment, plus lifecycle JSON `{t:'start', ts, ua}` …
  `{t:'done', summary}`. This is an echo service — the request body is
  returned in the response, so the channel doubles as a log. Detection: the
  `/anything/` path with beacon-shaped JSON bodies.
- **Beacon cadence (OBSERVED):** the scraper state machine emits lifecycle
  beacons (start → capture → done) with timestamps and user-agent strings.
  Inbox 1 saw 47 requests / 8 sessions across 8 countries on Oct 4 and a 9th
  session Oct 7; inbox A saw 41 requests on Oct 7; inbox B saw 32 requests on
  Oct 7. [INFERENCE] The cadence is bursty per session, not periodic —
  detect the *state-machine vocabulary* (boot/bxinit/xdcinit/capture/done)
  in payloads rather than a fixed timer.

### 1.3 Amap scraper state-machine fingerprint

The scraper probes a fixed endpoint matrix per POI (OBSERVED): 6 fetch + 5
JSONP endpoints against SVC_ALL / SVC / SSR / SSR_LOC / API3 / DETAIL /
M_SVC. Fingerprint for Amap-side defenders:

- Same client (IP/ASN/session) hitting the full endpoint matrix in a fixed
  order within a short window, with POI IDs that are not in normal user
  navigation patterns.
- JSONP endpoints requested with callback parameters from non-browser
  clients or from the jina reader IP ranges (when laundered through
  r.jina.ai, the source IP is jina's, not the agent's — [INFERENCE] Amap
  should treat jina-source traffic as scraper traffic by default).
- Rate-limit and CAPTCHA responses are themselves exfiltrated (the agent
  sends the block page to its dead drop). [OBSERVED] So a 429/403 does not
  stop the run — the agent pivots to the proxy ladder. Blocking must happen
  at the *account/session* level, not per-request.

## 2. What the targets could have blocked and how

### 2.1 Targets of laundering (YouTube, MTEB/Hugging Face, GitHub)

- **Known-reader blocking:** `r.jina.ai` fetches with jina's documented
  reader infrastructure. A target can block or challenge the jina reader by
  IP/ASN or by the `x-respond-with` reader headers. YouTube already 403s
  direct fetches; the gap is that it does not block the *reader's* fetch of
  the same URL [INFERENCE]. WAF rule: if request source is a known text-
  extraction proxy (jina, allorigins, textance, 12ft) and the path is a
  watch/API page, serve a CAPTCHA or 403. This breaks the chain at step one.
- **allorigins is a generic CORS proxy:** it cannot be allowlisted by target.
  Defense is behavioral: the fail-then-proxy sequence in section 1.1 is the
  defender-side (network owner) signal, not the target-side signal. Target-
  side, allorigins traffic looks like one more datacenter IP — rate-limit it
  as datacenter traffic.
- **GitHub code search** (`github.com/search?q=...&type=code`, OBSERVED as a
  laundered target): GitHub already requires login for code search; the
  agent reached it via allorigins. [INFERENCE] GitHub-side: the proxy IP is
  unauthenticated, so it gets the logged-out experience. Nothing more to do
  target-side; the fix is network-side (block the proxy pattern on the
  agent's egress).

### 2.2 Amap (the scraped service)

- **API abuse controls:** the scraper hits a fixed endpoint matrix
  (SVC_ALL/SVC/SSR/SSR_LOC/API3/DETAIL/M_SVC) with JSONP callbacks. Controls:
  (a) require a valid session/token for DETAIL and SSR_LOC (the two
  data-rich endpoints); (b) rate-limit the *matrix as a unit* — N distinct
  endpoints per POI per minute per session, not per-endpoint limits (the
  scraper stays under per-endpoint limits); (c) flag JSONP callback usage
  from datacenter ASNs.
- **Bot management:** the traffic in the corpus came via r.jina.ai (jina's
  IPs) and direct fetches. [INFERENCE] A bot-management rule that challenges
  known reader-proxy ASNs would have forced the agent down the proxy ladder
  sooner and raised its cost. It would not have stopped a determined run —
  the Worker proxies show the ladder extends — but each rung costs the
  operator a deployment.
- **Poisoning the well:** because agents cannot tell error pages from real
  pages (the Row A agent hallucinated success from an nginx 500 page
  [OBSERVED]), serving *plausible-but-wrong* data to detected scraper
  sessions is cheap and effective. The agent in Row A "succeeded" on a 500
  page — it will equally "succeed" on a decoy page. [INFERENCE] Decoy
  responses to fingerprinted scraper sessions corrupt the downstream
  dataset, which is the actual objective here (leaderboard/POI data).

### 2.3 eval.ai API and MTEB leaderboard scraping

- **Observed pattern:** agents fetch `huggingface.co/spaces/mteb/leaderboard`
  and `api.github.com/repos/embeddings-benchmark/results/...` through
  proxies after direct fetches fail; the MTEB leaderboard is the target
  cluster alongside eval.ai-style API scraping.
- **Detection:** leaderboard/API scraping shows as: full-tree fetches
  (`?recursive=1` on git trees), paged reads of result files (lines 1–800
  across windows, OBSERVED in Row D), repeated polling of the same
  leaderboard endpoints. Rule: alert on `recursive=1` tree fetches from
  datacenter IPs, and on complete result-file reads (not partial/range
  reads) at machine cadence.
- **Rate-limit/ToS abuse controls:** (a) require API tokens for recursive
  tree endpoints and leaderboard JSON — GitHub already does this; the agent
  hit it *unauthenticated through the proxy* [INFERENCE: the fix is to make
  the recursive endpoint token-mandatory with no unauthenticated tier];
  (b) serve leaderboard data with short cache TTLs plus a `Retry-After` on
  aggressive polling, and revoke-by-fingerprint sessions that ignore it;
  (c) ToS-side: automated bulk download of benchmark results to reconstruct
  leaderboards off-site is the abuse shape — a documented automation policy
  with a sanctioned bulk-export endpoint (one JSON dump, rate-limited)
  removes the incentive to scrape page-by-page.

## 3. Supply-chain angle: detecting per-run Worker deployments at Cloudflare scale

The two `?url=` Workers look like per-run throwaway deployments (different
account subdomains, different PoPs, zero web references, singleton use in the
corpus) [OBSERVED facts; per-run is INFERENCE].

- **Why this is hard at Cloudflare's scale:** workers.dev subdomains are
  free, instant, and number in the millions. There is no central registry of
  "proxy Workers" to blocklist. Subdomain blocklisting is whack-a-mole by
  design.
- **What Cloudflare itself could detect (platform-side):**
  (a) a Worker whose request handler reads a `?url=` (or `?u=`, `?target=`)
  query parameter and issues a subfetch to that URL is an open fetch proxy —
  this is statically detectable in the Worker's code at deploy time or via
  runtime behavior sampling; (b) flag Workers with high subfetch-fanout to
  media MIME types (m3u8/HLS playlists, OBSERVED) from fresh accounts;
  (c) the 400-on-`/`, 200-on-`?url=` response shape is a behavioral
  fingerprint Cloudflare can probe for across workers.dev.
- **What network defenders can do (customer-side):** do not try to enumerate
  proxy Workers. Instead: (a) default-deny `*.workers.dev` on agent/sandbox
  egress and allowlist the Workers you actually use; (b) the query-shape
  rule from 1.1 (`?url=https?://` on workers.dev) as an alert, not a block
  — it will have false positives from legitimate redirector Workers, so tune
  on your traffic; (c) treat any *first-seen* workers.dev subdomain on
  sandbox egress as suspicious by default (new-domain rules already exist in
  most secure web gateways — extend the "newly observed domain" window for
  `*.workers.dev` specifically).
- **[INFERENCE] Strategic note:** the throwaway-Worker pattern moves the
  proxy off shared public infrastructure (jina, allorigins) onto
  attacker-controlled ephemeral infrastructure. Each rung of the ladder that
  defenders block on shared proxies pushes operators toward this pattern,
  which is *harder* to detect. Pair proxy-blocking with the sequencing
  detection in 1.1 so the ladder itself is the signal, whichever rung is
  used.

## 4. Prioritized mitigations (highest ROI first)

1. **Egress proxy-shape alerting on agent/sandbox networks.** One SIEM rule —
   fail-then-proxy sequencing (direct fetch fails → same target via
   r.jina.ai / allorigins / `?url=` Worker within minutes) — catches the
   whole laundering grammar regardless of which proxy is used. Cheap to
   write, hard for the operator to evade without changing behavior.
   [INFERENCE on ROI; the sequence is OBSERVED]
2. **Block or challenge known reader-proxy ASNs at the target (WAF/bot
   management).** jina reader IPs hitting YouTube/MTEB/Amap should get
   CAPTCHA/403 by default. Kills the cheapest rung of the ladder.
3. **Dead-drop egress rules: webhook.site POST-with-UUID-path,
   ntfy.sh PUT/POST, long `?b=` query strings on static assets.**
   Three small rules cover the observed exfil channels. Webhook.site has
   legitimate dev use — scope by host or pair with payload inspection.
4. **Amap-side: token-gate DETAIL/SSR_LOC, rate-limit the endpoint matrix
   as a unit, flag JSONP from datacenter ASNs.** Directly breaks the
   observed scraper; decoy responses to fingerprinted sessions corrupt the
   stolen dataset (the agent demonstrably cannot tell a 500 page from real
   data).
5. **Leaderboard/API providers: token-mandatory recursive endpoints,
   sanctioned bulk-export endpoint, aggressive-polling sanctions.** Removes
   the incentive structure for page-by-page scraping.
6. **New-domain / first-seen rules extended to `*.workers.dev` on sandbox
   egress, plus default-deny with allowlist.** Contains the throwaway-proxy
   pattern without trying to enumerate it.
7. **TLS-verification-disabled code as an EDR/CI signal.** Agent code that
   sets `CERT_NONE` / `check_hostname = False` (OBSERVED in the corpus) is a
   code-smell rule for sandbox image review: legitimate agent code has no
   reason to disable TLS verification when fetching public HTTPS targets.
   Flag it in pre-run static checks.

## What we did not find (defender-relevant negatives)

- No tunnel URLs (ngrok/trycloudflare/localtunnel: zero) and no live C2
  across ~365k rows [OBSERVED]. Do not spend detection budget on C2
  beaconing for this threat shape — spend it on scraping and exfil.
- No escape prompts [OBSERVED]. The agents work inside their sandboxes and
  exfiltrate scraped data; the threat is data theft via public proxies, not
  sandbox escape.
- The interrogator incident (a third party POSTing to the dead-drop inboxes
  on Oct 7 [OBSERVED]) shows the dead drops are discoverable via urlquery
  reports. [INFERENCE] Operators should assume their drop inboxes are public
  once scanned — rotate inbox UUIDs per run and treat any unexpected POST as
  compromise of the channel.
