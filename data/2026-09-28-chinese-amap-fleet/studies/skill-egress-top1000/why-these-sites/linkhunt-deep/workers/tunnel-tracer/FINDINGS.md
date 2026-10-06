# TUNNEL-TRACER findings (2026-10-05)

Worker: tunnel-tracer. Method: passive/stored observations only — urlquery frozen
corpus, urlscan.io public search API, Shodan API (DNS + host search), local
corpus greps. **Neither tunnel endpoint was ever connected to, fetched, or
probed.** Full observed values below, no redaction. OBSERVED vs INFERENCE are
separated throughout.

---

## LEAD A — `morris-satellite-deferred-letters.trycloudflare.com`

### A1. The fingerprint rows (OBSERVED)

`silent-locus/collections/re-hunt-qa-fingerprints/data/hits.jsonl` lines
3863–3873 — 11 rows, all against one urlquery record:

| qid | fingerprint | matched_field | excerpt | record_id |
|---|---|---|---|---|
| dsqa_043 | WHO | url.original | `morris-satellite-deferred-letters.trycloudflare.com/apps/who-visits/?i=316697` | ec2fdfcd-e213-4d39-8ed3-fcf4adf457f0 |
| dsqa_079 | WHO | url.original | (same) | (same) |
| dsqa_497 | WHO | url.original | (same) | (same) |
| dsqa_632 | WHO | url.original | (same) | (same) |
| dsqa_696 | WHO | url.original | (same) | (same) |
| dsqa_701 | WHO | url.original | (same) | (same) |
| dsqa_720 | WHO | url.original | (same) | (same) |
| dsqa_738 | WHO | url.original | (same) | (same) |
| dsqa_826 | WHO | url.original | (same) | (same) |
| dsqa_861 | WHO | url.original | (same) | (same) |
| dsqa_873 | WHO | url.original | (same) | (same) |

All 11 rows share the identical excerpt and record_id.

### A2. Why the match fired (OBSERVED — mechanism)

- The "WHO" fingerprint comes from the DSQA question text: every one of the
  11 questions mentions WHO = World Health Organization (e.g. dsqa_043:
  "Of the countries that the WHO listed in 2017 as having 100% of their
  hospitals following national dementia standards, which country has had the
  greatest increase in life expectancy between 1950 and 2023 according to
  OurWorldInData.org?").
- `collect.py` (re-hunt-qa-fingerprints lane) matches with case-insensitive
  substring: `if fp_lower in url.casefold()` (line 485). The fingerprint
  "who" therefore matched the path segment **"who-visits"**.
- Correction to the prior truth in corpus-grepper FINDINGS.md §7: it is not
  3 questions (dsqa_043/079/497) — it is 11 — and the match is a
  case-insensitive collision between an acronym (WHO, World Health
  Organization) and the English word "who" in a URL path. It carries **zero
  DoE-task signal**.

### A3. The full urlquery record (OBSERVED)

Source: `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/raw/ua_anomaly.json.gz`,
report_id `ec2fdfcd-e213-4d39-8ed3-fcf4adf457f0` (query was
`date:[2026-09-19 TO 2026-09-25]`):

- `date`: 2026-09-24T13:15:40Z
- `submit.url.addr`: `morris-satellite-deferred-letters.trycloudflare.com/apps/who-visits/?i=316697`
- `final.url.addr`: same (no redirect)
- `final.title`: `Facebook`
- `ip.addr`: `104.16.230.132`; `ip.as`: `Cloudflare, Inc.`; `ip.country`: (empty)
- `tags`: `['meta', 'facebook', 'phishing', 'social']`
- `settings.useragent`: `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0`
- `settings.referer`: `''` (empty); `settings.cookies`: None; `settings.exit_node`: `31pu2ilhjrkmwpf`
- `final.dom`: size 0, mime `text/plain; charset=utf-8`, sha256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
  (= SHA-256 of the empty string — the captured body was empty)
- `stats.alert_count`: `{"ids": 0, "urlquery": 2, "analyzer": 3}`

INFERENCE: the tunnel served a Facebook phishing kit at `/apps/who-visits/`
(`who-visits` = the classic "who viewed my profile" lure). urlquery's own
classifier tagged it phishing/social/facebook; the scanner fetched a page
titled "Facebook" but got a zero-byte body back (kit did not render for the
scanner, or the body was emptied post-load).

### A4. urlscan.io stored observations (OBSERVED — public search API)

Three stored observations of the exact URL:

1. 2026-09-09T17:27:48.527Z — uuid `01a08736-10c1-75ff-92b7-7fbd30eae8e5` —
   title `Facebook`, status 200, ip `104.16.230.132` (Cloudflare), server
   `cloudflare`, mime `text/html`
2. 2026-09-24T13:01:31.981Z — uuid `01a0d381-a743-754e-b6ed-403df3a7cfe3` —
   title `Facebook`, status 200, ip `2606:4700::6810:e784` (Cloudflare),
   server `cloudflare`, mime `text/html`
3. 2026-09-26T11:32:45.750Z — uuid `01a0dd7c-acc0-7213-a171-5aa04aa21311` —
   title `Suspected Phishing | Cloudflare`, status 403, ip
   `104.16.231.132`, server `cloudflare`, mime `text/html`

(Full urlscan result-detail API is login-gated; per the passive-only rule only
the public search API was used.)

INFERENCE from the timeline: the same phishing page was live on Sep 9 and
Sep 24 (200 / "Facebook"), and by Sep 26 Cloudflare itself was serving a
"SUSPECTED PHISHING" 403 for the tunnel domain — Cloudflare flagged the
quick-tunnel hostname. The urlscan Sep-24 observation (13:01:31Z) sits ~14
minutes before our urlquery report (13:15:40Z): plausibly the same submission
being scanned by both services, not two independent submissions.

### A5. The `?i=316697` parameter (OBSERVED + INFERENCE)

- DSQA question IDs run dsqa_000–dsqa_899. `316697` matches no DSQA qid, and
  the string `316697` appears nowhere else in our corpora except the two
  derived hits files (re-hunt-qa-fingerprints and re-hunt-patterns, both
  referencing this same urlquery record).
- The tunnel hostname appears in no other corpus file either — the only
  matches across all of `~/workspace/silent-locus/` are these hits files and
  our own study notes (corpus-grepper FINDINGS.md, WHY-SITES.md).
- INFERENCE: `?i=316697` is most plausibly a phish-kit parameter (victim or
  campaign ID). No evidence ties it to any DSQA question, session, or eval.

### A6. dsqa_250 / DoE linkage (OBSERVED)

- dsqa_250 question text: "Using data from civilrightsdata.ed.gov for the
  2017-2018 school year, determine which of the following states - South
  Carolina, North Carolina, Georgia, or Virginia - had the highest ratio of
  full-time equivalent school counselors to students reported as victims of
  race-related harassment or bullying." Tags:
  `incident-match-doe-20260617`, `gov-data`, `gov-education`.
- dsqa_250 fingerprints: `["civilrightsdata.ed.gov", "South Carolina",
  "North Carolina", "Virginia"]` — none appears in the tunnel URL.
- Verdict: **no connection.** The LEAD A fingerprint hit is graded as
  fingerprint noise (weak lexical collision), not evidence of any DoE-eval
  linkage.

### A7. Shodan (OBSERVED)

- `shodan.py dns morris-satellite-deferred-letters.trycloudflare.com`:
  `{domain: null, tags: null, subdomains: null}`
- `shodan.py search 'hostname:morris-satellite-deferred-letters.trycloudflare.com'`: total 0, matches []
- Verdict: no stored Shodan observations. Expected for an ephemeral
  quick-tunnel hostname (INFERENCE: "morris-satellite-deferred-letters" is
  the random-adjective-noun-name grammar of cloudflared quick tunnels, not
  agent tradecraft).

### A8. Campaign-linkage assessment — LEAD A

- **Crimeware, not agent infrastructure (evidence grade: high).** A Facebook
  credential-phish kit behind a cloudflared quick tunnel; independently
  flagged by urlquery tags (`phishing`, `social`, `facebook`, 5 analyzer
  alerts) and by Cloudflare itself ("Suspected Phishing | Cloudflare" 403
  on Sep 26).
- **No link to any known swarm/agent campaign (evidence grade: high-negative
  by absence).** Zero appearances in any corpus outside our derived hits;
  the hostname's random-name grammar is standard quick-tunnel output; the
  urlquery submitter UA is stock Firefox (matching the UA sweep's finding
  that 9,979 recent reports carry only stock browser UAs).
- **DoE/dsqa_250 linkage: refuted** (A6) — the fingerprint match that seeded
  this lead is a false positive; corpus-grepper FINDINGS.md §7's framing
  ("carries a DoE-task fingerprint") should be downgraded to noise.

---

## LEAD B — `oai-scratchpad-cache-versioning-demo.ngrok.io`

### B1. What the log is (OBSERVED)

`.../personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/demo-scratchpad/run4.2.log`
(2,015 lines, 92,908 bytes):

- An OpenAI **Responses API** JSON log: response id
  `resp_0e17f9551f6cb925006aac9341b88087d1b653b0f542c56db1`, model
  `gpt-5.6-luna`, `created_at` 1789694785 = **2026-09-18T01:26:25Z**,
  `billing.payer: developer`.
- 30 `web_search_call` / `open_page` tool actions (the Responses API
  "web_search" tool — not public web search). 99 line-matches for
  `ngrok.io`.

### B2. What was being demoed (OBSERVED)

The tunnel served a **"Demo Messageboard"** — a mutable scratchpad
demonstrating that the OpenAI web.run page cache can hold a versioned
history of a site that only chatgpts can see:

- `?set-html=<urlencoded html>` writes the current revision of the
  scratchpad ("One mutable resource; many cache-addressed moments").
- `?page=N&run=4` (and fragment form `#page=N` per `populate_board.sh`)
  addresses historical revisions via the page cache ("The origin remembers
  only the present. The cache may remember the past.").
- Board copy is self-descriptive: "Hello, future cache archaeologists",
  "Five mutations of one scratchpad; five distinct URLs presented to the
  page cache", "An ignored query string has become an address for history".
- Sibling files: `creation.log` (Page 1 run, 2026-09-18T00:39–00:40Z; the
  demo site was "inaccessible to the web tool" at that moment),
  `run4.1.log` (another Responses API run, `created_at` 1789694716),
  `populate_board.sh` (writes 10 pages via `oai_fetch_url_live`
  against `BASE="https://oai-scratchpad-cache-versioning-demo.ngrok.io/demo"`),
  `scratchpad.py` (the server code), `scratchpad.db*` (sqlite state).
- URL aliases in the log: `/r1789841073_p45`, `/r1789841458_p71`,
  `/{RID}_p45` (epoch-nonce + page-number aliases, e.g. `r1789841073_p45`).

### B3. Provenance — whose run and whose tunnel (OBSERVED)

- The directory chain is
  `.../pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/`,
  whose `README.md` states: this is the **joshuadavid/wikiagentswarminvestigation**
  repository ("This repository was generated by me grabbing the
  full_wiki_logs.zip file from collusion.wiki and then asking Claude a
  million dumb questions"), shallow-cloned into our tree on 2026-10-05
  (directory mtime 07:33) for the lane-3 OSINT work.
- The README explicitly describes `./demo-scratchpad` as:
  *"A demonstration of how agents could use an ephemeral page and the openai
  web.run page cache to have a versioned history of a site that only
  chatgpts can see."*
- Verdict: **the tunnel is the investigator's OWN demo infrastructure**
  (their ngrok + `scratchpad.py` + `populate_board.sh`), and the logs are
  their own Responses API runs exercising it. It is not an unknown agent
  campaign's infrastructure, and the `oai-` prefix is the investigator's
  naming, not campaign tradecraft.

### B4. The `oai-` naming convention (OBSERVED)

- Full-tree grep for `oai-`-prefixed tunnel/hostname URLs across
  `~/workspace/silent-locus/` and `~/workspace/muse-home/projects/`: the
  **only** `oai-`-prefixed tunnel hostname anywhere is
  `oai-scratchpad-cache-versioning-demo.ngrok.io`, occurring solely in the
  demo-scratchpad files.
- No `oai-`-prefixed ngrok/trycloudflare/ngrok-free/loca.lt hostname exists
  in `urlquery-api-hunt/artifacts/raw/` either.
- Verdict: `oai-` is not a naming convention used by any campaign in our
  corpora — it is this one investigator's demo name.

### B5. Public-index resolvability (OBSERVED)

- urlscan.io public search API for
  `domain:oai-scratchpad-cache-versioning-demo.ngrok.io`: **total 0** — no
  stored observations.
- Shodan DNS: `{domain: null, tags: null, subdomains: null}`; Shodan host
  search `hostname:oai-scratchpad-cache-versioning-demo.ngrok.io`: total 0.
- Verdict: the tunnel has no stored presence in urlscan or Shodan (consistent
  with a short-lived investigator demo; ngrok hostnames only resolve while
  the tunnel is up).

### B6. Campaign-linkage assessment — LEAD B

- **Not a campaign lead at all (evidence grade: high).** The tunnel and logs
  are joshuadavid's own cache-pinning demonstration from the
  wikiagentswarminvestigation corpus — attributed by the README's own
  description and by the log format (OpenAI Responses API runs run by a
  developer against their own ngrok demo).
- The demo IS, however, a working artifact of the cache-pinning tradecraft
  the lane is studying: it shows the exact `?set-html=` / cache-addressed
  mechanism by which the swarm's `chatgpt-user` web.run channel could keep a
  versioned dead-drop history (cf. run1 README's repeat-hits-25m finding:
  the `web.run` 16-IP pool cache-pinning burst signature). Useful as a
  reference mechanism demo, not as attribution evidence.
- No link to any unknown campaign; do not cite the `oai-` prefix as swarm
  tradecraft.

---

## Still unknown

1. `?i=316697` — victim/session/campaign ID meaning of the phish-kit
   parameter (no corpus occurrence beyond this URL; would need the kit
   source, which we do not have and must not fetch live).
2. Who submitted the tunnel URL to urlquery (Sep 24) and urlscan (Sep 9,
   Sep 24, Sep 26) — submitter attribution is not in stored data; the
   urlquery UA sweep's definitive negative (only stock browser UAs across
   9,979 reports) applies.
3. Whether the Facebook phish kit behind LEAD A has any relation to the
   agent-incident corpora — currently zero overlap; it sits alongside the
   hunt scope only because a fingerprint engine tripped on it.
4. The origin operator of the cloudflared tunnel (ephemeral quick-tunnel;
   no stored records).

## Recommended note for lane owners

- Downgrade corpus-grepper FINDINGS.md §7: the "DoE-task fingerprint on a
  trycloudflare tunnel" is a false positive from case-insensitive substring
  matching of the 3-letter acronym WHO against the English word "who" in a
  URL path. The `re-hunt-qa-fingerprints` lane may want a minimum-token or
  word-boundary rule for short acronym fingerprints (WHO, DSO, RSC, etc. —
  187 pattern-log rows use fingerprint "WHO" alone).
- LEAD B is a provenance success story in reverse: the `oai-` tunnel is the
  *investigator's* artifact, and the run1 clone landing in our tree on
  2026-10-05 means `oai-*` strings in lane3 grep results should be treated
  as investigator self-generated unless proven otherwise.
