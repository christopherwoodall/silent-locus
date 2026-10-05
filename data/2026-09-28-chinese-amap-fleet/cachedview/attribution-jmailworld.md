# Attribution: the jmail.world audit campaign (2026-10-05)

**Scope correction up front:** the "72-report run (Oct 4 23:54 → Oct 5 03:58 UTC)" from
`new-fleets/FINDINGS.md` is a *slice* of a much larger campaign. Full htmx history pull
(`jmail.world`, 17 offsets, 872 unique reports): **Oct 2 12:05 → Oct 5 04:13 UTC, ~64 hours,
median gap 3.0 min, essentially continuous** (three pauses: 52 min, 230 min, 107 min).
Earlier probes with identical payloads on Sep 6 / 14 / 17 / 18 / 22 (via web-search-visible
urlquery reports) — same actor warming up.

## 1. What the campaign is

**Target: jmail.world = "Jmail", the Epstein-files archive** (Wikipedia: browser-based archive
of the Epstein Files Transparency Act releases, Gmail-style UI by Riley Walz / Luke Igel;
450M projected visits). The path grammar is the site's own namespace:
`/thread/EFTA<N>` (email threads), `/drive/vol<N>-efta<N>-pdf`, `/thread/<hex32>`,
`/person/<name>`, `/promotions/page/N`, `/topic/damage-control`, `/jotify/playlist/favorites`,
`/search`, `/calendar`.

**Workload: redirect/abuse audit of the site's `?q=` search.** Every submission appends `?q=`
with one of 6 fixed payloads (or occasionally no `q`, 34 index-page submissions):

| Payload | n (of 872) | Notes |
|---|---|---|
| `https://livetraffic.net/login?refer=119334` | 157 | affiliate ID 119334 |
| `https://2pink.org/dang-ky?ref=119334` | 141 | same affiliate ID |
| `https://www.followlike.net/?r=19384926` | 139 | affiliate ID 19384926 |
| `https://www.followlike.info/?r=19384926` | 137 | same ID |
| `seekers+of+decay` | 135 | unidentified watch-phrase / case codename |
| `http://folllike.com/?19384926` | 129 | same ID (typosquat of followlike) |

Payload choice is **uniform-random, not rotating** (autocorrelation flat at ~0.16 for all
periods 1–12; first-40 sequence shows no cycle). All 60 direct-URL scans in the 72-sample
fired urlquery's analyzer (TDS=2) — expected, since the query string carries known-bad URLs.
67/72 final URLs == submit URL: **the site does not redirect on `?q=`** (one slug
canonicalization: `steven-sinofsky-` → `steven-sinofsky-psylo`). So the audit's apparent
finding so far: no open-redirect on the probed pages, at least as urlquery's scanner sees it.

Two readings of intent (unresolved): (a) a **threat researcher** checking whether a
high-traffic site (450M visits) has been compromised to inject affiliate-kit redirects;
(b) the **kit operator themselves** verifying their injected placements are still live
(the payloads carry *their own* affiliate IDs — 19384926, 119334). The `seekers+of+decay`
phrase searches the archive for that string — likely the investigator's case codename;
no phishing-world meaning found (web hits are only this campaign's own urlquery reports).

## 2. Submitter fingerprint (72 full records via authenticated API)

- **UA: exactly 1** across all 72 —
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0`
  = urlquery's **default scanner UA**. The submitter set no custom UA.
- **Settings: all defaults.** `desktop`, `public`, empty referer, no cookies, no tags
  (18 reports carry urlquery's *auto* `pdf` tag — not submitter-applied), version 0,
  status done. Single exit node `qguvgzjxzsgb3vs` for all 72 (urlquery infra routing).
- **No submitter-side grammar at all**: no nonce params, no tag grammar, no custom UA.
  This is the sharpest contrast with our Amap operator (bursty, `uq` tag grammar, varied
  UAs incl. experiments).

## 3. Timing: serialized drip, not a metronome

Second-precision completion times (full records) for the 72-slice:
median gap **2.68 min**, mean 3.45, stdev 3.20; histogram: 3-min (39), 2-min (9),
0-to-1-min (7), then a tail to 24 min. **Seven negative gaps** (down to −56 s):
scan N+1 completed *before* scan N. A strictly serialized submit→wait→submit loop cannot
produce that; the consistent model is a **timer-fired loop (~every 3 min) or
submit→wait-with-timeout**, where slow scans overrun and complete out of order
(e.g. four completions inside 22 s at 00:33:07–00:33:29 — queued scans flushing).
Longer gaps (7–24 min) cluster after cachedview submissions.

Campaign-wide (872, minute precision): median 3.00 min, p90 7.0 min, three real pauses
(52 / 230 / 107 min). Otherwise unbroken 24/7 for 64 h — **no human manually submits at
1-per-3-min for 64 hours. Automation is certain.**

## 4. cachedview.nl: 103/872 (~12%), all four days

Submissions shaped `cachedview.nl/#https://jmail.world/...?q=...`. Critical technical
point: **the `#fragment` never leaves the browser** — urlquery scans only the cachedview.nl
shell page (final URL = cachedview.nl or `about:privatebrowsing`, DOM 232 bytes,
`times_seen=61`, `resource_available=False`). These 103 scans check *nothing* about the
target. Either the submitter misunderstands cachedview (believes submitting the proxy URL
archives/checks the target), or it's a ritual "consult the archive oracle" step.
Distribution: present from the first hour (Oct 2 15:13), median spacing 6 submissions,
but 20 back-to-back pairs — not a strict every-Nth rule. No correlation with path type
or payload (EFTA/hex32/vol-pdf/person all represented; payloads mixed).

## 5. Comparison with known shapes

| Dimension | jmail auditor | Our Amap operator | Tronzap (urlscan) |
|---|---|---|---|
| Cadence | serialized ~1/3 min, 64 h | bursty, multi/min | bursty parallel |
| Submitter grammar | none (defaults) | `uq` tags, varied UAs | test-matrix naming |
| UA | 1× urlquery default | varied incl. experiments | n/a |
| TTP family | audit/verify (detection) | collect/exfiltrate | vuln-test matrix |
| Target | jmail.world (Epstein archive) | Amap/IDPH/AIHW | tronzap.com (crypto) |
| Runtime | 64 h continuous | months, intermittent | Sep 5–Oct 4 |

**Not our operator** (no shared grammar/infra/TTP). **Not tronzap-shaped** (serialized
drip vs bursty parallelism). It is its own actor: a standing audit loop, active since
at least Sep 6.

## 6. Verdict

**Programmatic — certain** (64 h at 1-per-3-min sustained, uniform-random payload
selection, pre-scraped URL list, timer-loop timing signature).

- **Human's script / cron — most likely (~2:1).** Rigid cadence, all-default settings,
  fixed payload kit with `random.choice`-style selection, no agent tells anywhere in the
  data, Sep small-probes → Oct full-campaign matches human test-then-launch. The three
  pauses fit operator restarts or 429 backoffs. The cachedview fragment-misunderstanding
  is a very human-scripter mistake.
- **AI agent — possible, not indicated.** For: exploratory URL picks (specific person
  pages, `/topic/damage-control`, `/jotify/playlist/favorites`, `/calendar?types=travel`
  suggest browsing-driven discovery); cachedview-as-archive-oracle is an agent-ish
  reasoning step; Sep→Oct escalation fits agent iteration. Against: cadence too rigid
  for a think-then-act loop, 64 h is very long for one agent session, zero prompt-like
  or verbose artifacts in URLs, defaults everywhere.
- **Commercial scanner (phishing-detection vendor) — unlikely.** Vendors scan broad
  feeds with custom infra; a 64-hour single-site search-box audit with fixed affiliate
  IDs is a targeted investigation, not vendor-shaped.

## 7. What would settle it

1. **urlquery submission logs** (source IP constancy, API-key vs web-form submission)
   — not exposed in report records; urlquery staff only. This is the single highest-value
   discriminator.
2. **Submission-side (not scan-completion) timestamps at sub-minute precision** —
   timer-fired vs reactive loop.
3. **Campaign status after 04:13 UTC Oct 5** — still running or stopped clean?
   (Collection gap: htmx throttled after the pull; authenticated search 429'd.)
4. **jmail.world server-side logs** for the `?q=` hits — moot for attribution (requests
   come from urlquery's scanner, not the submitter), but would confirm what the audit
   actually found (reflected? indexed?).
5. **Identifying "seekers of decay"** — researcher codename vs threat-actor phrase.

## 8. Collection notes & gaps

- Full records for the 72-slice pulled via authenticated `uq.py report` (all 72 OK,
  ~30 KB each); cached ephemerally at `/tmp/jmail_full/` — re-pullable, not archived.
- htmx history: 17 offsets (0–850), 872 unique; throttled after offset 850 (network
  errors), so **pre-Oct-2 history is incomplete** — Sep 6/14/17/18/22 probes known only
  from web-search-visible urlquery reports.
- Authenticated `uq.py search` returned **429** after the 72-report pull (rate limit);
  campaign status after 2026-10-05T04:13Z is unknown.
- New watch item for the hunt: recurring audit actor with a fixed affiliate-kit payload
  set — worth a standing `jmail.world` / `seekers+of+decay` / `19384926` / `119334`
  watch; if the payload kit appears against other domains, the actor is expanding
  target coverage.
