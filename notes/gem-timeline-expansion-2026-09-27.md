# Gem campaign: burst timeline + actor expansion — 2026-09-27

Two-part analysis of the May 11–12, 2026 go-import meta-tag injection campaign
(555 gems / 608 version pins, yanked from rubygems.org, recovered via Diffend).

**Provenance:** independent collection (Christopher's screenshots + our Diffend
pull). NOT part of the SwarmTraces dataset.

**Coverage note:** timeline analysis below is built from 385/608 harvested pins
(379 unique gem-version records w/ Diffend "Last diff" timestamps) as of
~22:30 UTC 2026-09-27; the bulk harvest was still running. Hour-level totals
marked [full] come from the complete Diffend enumeration in
`notes/rubygems-rescan-2026-09-27.md` (555 gems); minute-level structure is from
the partial harvest and is representative but incomplete.

---

## PART A — Burst timeline (May 11–12, 2026, UTC)

### Phase 0 — Rehearsal, May 11 (30 gems, 33 version records)

| Time (UTC) | Gems | What |
|---|---|---|
| 04:42 | `oaitest1778473828` (0.0.1, 0.0.2) | First touch. Single gem, epoch-suffixed name (epoch 04:30:28Z → published 04:42, ~12 min lead). Two versions in the same minute — immediate republish test. |
| 13:29–13:34 | `zzfadgivar00`–`13` | "fadgi variant" numbered series. Published ~2/min, order shuffled (00, 03, 01, 07, 04, 08, 12, 05, 09, 13, 11…). |
| 13:35–13:38 | `zzpdfvar01`–`15` | "pdf variant" numbered series, same shuffled-batch pattern. |
| 13:39 | `zzjinavcs{git,hg,svn,bzr}` | All four VCS values in ONE minute. The actor literally names **jina** + VCS in the gem name — the {proxy}×{VCS} test matrix, rehearsed in naming before the main burst puts it in payloads. |
| 14:23 | `pathpkg94321zz` (0.1.0/0.1.1/0.1.2) | Unusual 0.1.x version scheme; three versions same minute. |
| 14:28 | `testoai4182477` | Last rehearsal gem. |

Read: the rehearsal tests (1) epoch-suffixed naming, (2) numbered `var` series
publishing, (3) the VCS matrix, (4) multi-version republishing. The `zzjinavcs*`
names are the tell — "jina" enters the actor's vocabulary here, 11 hours before
the main burst launders payload URLs through `r.jina.ai`.

### Phase 1 — Evening bridge, May 11 18:16 → 20:35 (3 gems)

| Time (UTC) | Gem |
|---|---|
| 18:16 | `southextractproxy2026` |
| 19:17 | `wandsworthproxyabcabc` (0.0.1, 0.0.2) |
| 20:35 | `zzzltestfoobarxyz` (0.0.1, 0.0.2) |

One gem roughly per hour, each a place/proxy-flavored name, two with immediate
same-minute version bumps. This looks like placement/visibility checks —
publish one, confirm it indexes, move on — during the 11-hour gap between
rehearsal and main burst.

### Phase 2 — Main burst, May 12 01:34 → 07:56 [full: 516 gems]

Hour buckets [full enumeration]:

| Hour (UTC) | Gems |
|---|---|
| 01:00 | ~66 (partial: 66) |
| 02:00 | **271** |
| 03:00 | ~104 (partial: 104) |
| 07:00 | 2 (tail) |

5-minute cadence (partial data, shape representative): ramp 01:35 (8) →
01:50/01:55 (17/22 per bucket) → sustained 02:05–02:45 (11–25/bucket) →
second wind 03:05–03:20 (15–29/bucket) → dead until 07:55 (2).

Inter-arrival in the 01:00–04:00 window: **median gap 0s** (249 of 337 gaps
under 60s; mean 22s). Multiple gems publish per minute for three straight
hours — fully automated batch publishing, not manual.

### Family ordering — which families first?

First-seen per family (main burst):

| Time (UTC) | Family | First gem |
|---|---|---|
| 01:38 | *probe*/proxy* | `probervdgcosw` |
| 01:39 | london* | `londonproxytestabc1778549587` |
| 01:41 | *fetch* | `gexpfetchxyz` |
| 01:42 | lamb* | `lambethscraper1778549610` |
| 01:46 | *hack* | `testgemhack1778550021` |
| 01:49 | other | `slntestrootabc` |
| 02:34 | chatoaifetch* | `chatoaifetch177855288717` |
| 03:06 | vcs-named | `dlxprobe1` |
| 03:11 | try[a-z][0-9]zz | `trya1zz` |
| 03:13 | wandshack* | `wandshack8` |

The opening wave (01:38–01:49) fires **six families interleaved within 11
minutes** — probe/proxy, london, fetch, lamb, hack, misc. Families do NOT
publish sequentially; the names were pre-generated as one batch and uploaded
in shuffled/parallel order (within-family numeric series like
`zzfadgivar00–13` / `dlxprobe1–23` are also time-shuffled, though minute
resolution limits sub-minute ordering claims).

Two exceptions to the interleave:
- **`try[a-z][0-9]zz` is the last family** (03:11–03:32), and its letter
  groups ARE time-sequential: trya* (03:11) → tryb* (03:18) → tryd* (03:24)
  → trye* (03:24) → tryf* (03:32). The generator walked the alphabet as it
  published. (No tryc* in harvested data yet — may be in unharvested pins.)
- **`chatoaifetch*` arrives as a block** at 02:34+ (12-digit suffixes =
  10-digit epoch + 2-digit suffix; suffixes 17, 28, 30, 36, 41, 42, 69, 78,
  94 — spread, not a counter; reads as random).

The burst **opens and closes on oai***: rehearsal starts with
`oaitest1778473828` (May 11 04:42); the final two gems are `oaijanla` and
`oaisurveytestzz` (May 12 07:55–07:56).

### Epoch nonces: name-generation → publish lead time

10-digit epochs embedded in names verified via `date -d @<epoch> -u`
(e.g. 1778551714 → 2026-05-12T02:08:34Z; 1778473828 → 2026-05-11T04:30:28Z;
1778553882 → 2026-05-12T02:44:42Z). Diffend "Last diff" minus name epoch:

- Median lead: **6.5 min** (n=43, range ~5–22 min; one 42-min outlier on a
  0.0.2 republish).
- Names are generated minutes — not hours — before publish. The pipeline is:
  generate name (epoch-stamped) → build gem → publish → Diffend snapshots,
  all inside ~6 minutes. Tight automation loop.

### Version bumps: iterative testing, not just pairs

Most multi-version gems bump 0.0.1→0.0.2 in the same minute (publish,
tweak, republish). Two cases show **iterative** behavior spread over time:
- `probejiqptzco`: 0.0.1 (01:38) → 0.0.2 (01:53) → 0.0.3 (01:56) →
  0.0.4/0.0.5/0.0.6 (02:11). Six versions over 33 min — publish, observe,
  adjust, repeat.
- `wandsworthprobe1778551714`: 0.0.1 (02:16) → 0.0.2 (02:51, 35 min later).
  The 0.0.2 summary is the minimal probe `<meta name=go-import content=HI>`
  (0.0.1's summary was `x`) — the actor dialing the payload down to the
  smallest possible injection.

### Tooling read (Part A summary)

1. **Pre-generated name batches, parallel/shuffled upload** — families
   interleave within minutes; numeric series are time-shuffled.
2. **~6-minute generate→publish loop**, fully automated (median 0s
   inter-arrival in the peak window).
3. **Rehearsal → bridge → burst** phasing: single-gem test (04:42) →
   variable/VCS matrix rehearsal (13:29–14:28) → sparse placement checks
   (18:16–20:35) → flood (01:34–03:32) → two-gem tail (07:55).
4. **Sequential generator visible once**: the try[a-z][0-9]zz family's
   letter groups publish in alphabetical order — the one place the
   generation order leaks through the shuffle.
5. **Iterative payload tuning** on at least two gems (probejiqptzco,
   wandsworthprobe1778551714).

---

## PART B — Actor expansion on Diffend

Behavioral fingerprints used: epoch-suffixed names, go-import meta tags in
summary/description, canary `x=1` lib contents, single-letter authors,
1980-01-02 faked dates, zz/oai/probe/dlx/fetch families, rubygems_version
3.6.7. All Diffend access was read-only GETs at ~1.2s pace.

### B1 — rgscan_s4_* / rgslice-authz-*: NOT the same actor (correction)

The task brief carried the rescan's loose "same actor family" phrasing for the
`rgscan_s4_*` upload/yank-integrity-testing gems. Direct fingerprint comparison
refutes it:

| Fingerprint | May campaign | rgscan_s4_20260317235101 | rgslice-authz-one-031726 |
|---|---|---|---|
| Diffend URL | https://my.diffend.io/gems/tryf3zz/0.0.1 | https://my.diffend.io/gems/rgscan_s4_20260317235101/0.0.1 | https://my.diffend.io/gems/rgslice-authz-one-031726/0.0.1 |
| Authors | single letters (`x`,`a`,`z`) | `Security Scanner` | `rgscanone031726` |
| Date | 1980-01-02 (faked) | 2026-03-17 (real) | 2026-03-17 (real) |
| Summary | go-import meta tag | "RubyGems security slice S4 benign test gem" | "…security testing gem" |
| Description | go-import / `x` | "Benign gem for authorized upload/yank integrity testing" | "temporary gem for authorized security testing" |
| Email | — | scanner@example.com | ae1dbmxom9o5x5@sharebot.net |
| go-import | yes (269/391 harvested) | no | no |
| rubygems_version | 3.6.7 | 3.4.20 | — |

Verdict: a **different, benign actor** doing authorized upload/yank integrity
testing (Mar 17–18, 2026). It shares only the *behavior* (publish → yank),
which is why the rescan cited it as evidence that yanked gems persist on
Diffend — not the actor. The timestamp-in-name convention is superficially
similar (`rgscan_s4_20260317235101` = human-readable datetime) but the format
differs from the campaign's epoch nonces.

### B2 — Other live "probe" families: all different actors

- **qoderprobe-gem-20260828** (Aug 28): author `qoderprobe`, real date
  2026-08-28, summary "probe", description "security probe gem". No go-import.
  https://my.diffend.io/gems/qoderprobe-gem-20260828
- **atlas_qa_handoff_20260528230548** (May 28): author `Atlas QA`, real date,
  "Payload-only encrypted same-day QA handoff snapshot". No go-import, no
  x=1, rubygems_version 3.3.15. A real QA team's artifact.
  https://my.diffend.io/gems/atlas_qa_handoff_20260528230548
- **byteprobe-{5m,20m,50m,100m,200m,300m,400m}-<hex>** (Sep 20, author
  `probe`): size/bandwidth probes — Diffend refuses to render ("exceeds the
  maximum displayable size"). Different purpose, different actor.
- **qa-authz-probe\*** / **qa-scope-probe-\*** (Aug 24, author `qa`),
  **apex-hijack-probe-a1** (Jul 7, author `audit`): small families (≤3 gems),
  distinct authors/naming; no campaign fingerprints per rescan triage.

### B3 — Full Diffend sweep: no second campaign

16 search terms (probe, zz, oai, fetch, hack, scan, jina, fossil, vcs, dlx,
test, 999, root, lamb, south, wandsworth) × up to 15 result pages, 663 unique
gems with "Last diff" dates, bucketed by month:

| Month | Gems | Reading |
|---|---|---|
| May 2026 | 367 | **the campaign** |
| Sep 2026 | 81 | legit gems (aws-sdk-*, gitlab-*, davinci test kits…) + byteprobe family |
| Aug 2026 | 32 | legit + qa-authz/qoderprobe families |
| Jun 2026 | 11 | legit (google-apis-*, lambda-*) |
| Jul 2026 | 10 | legit + apex-hijack-probe-a1 |
| Mar 2026 | 8 | legit + rgscan pair |
| all other months | 1–6 each | background legit matches |

- **Zero** epoch-suffixed (10-digit) names outside May 2026.
- **Zero** `try[a-z][0-9]zz` names outside May 2026.
- Jan–Apr 2026 window: only legit gems + the rgscan pair + `bridge-key-9993`
  (SEO spam, rescan-classified).

**Conclusion: one actor, one campaign.** No other burst on Diffend matches the
behavioral fingerprints. The actor operated May 11–12, 2026 and (by this
evidence) has not run a second campaign under these conventions.

### B4 — Bonus: the "jina"-in-name subfamily (main burst)

The `jina` search term surfaced 9 campaign gems beyond the rescan's family
table — the actor embeds the proxy name in gem names during the main burst,
not just in the rehearsal's `zzjinavcs*`:

| Gem | Last diff (UTC) |
|---|---|
| `zgitjina64499a` | May 12, 02:12 |
| `uxjinawands2` | May 12, 02:14 |
| `uxjinasouth2` | May 12, 02:14 |
| `uxjinalamb2` | May 12, 02:15 |
| `zgitjina55da35` | May 12, 02:19 |
| `xjinasouth1` | May 12, 02:28 |
| `southhgjina245` | May 12, 02:38 |
| `wandjinamod36977` | May 12, 03:06 |
| `rootjina18601` | May 12, 03:13 |

Patterns: `ux+jina+{lamb,south,wands}+2` (the three boroughs again),
`z+git+jina+alnum`, `wand+jina+mod` (`mod` = the fake VCS value),
`south+hg+jina`, `root+jina` ("root" was on Christopher's tracked word-part
list). All May 12, 02:12–03:13 — interleaved with the main burst, same as
everything else.

### Part B summary

1. **rgscan_s4_* is a different actor** — benign integrity tester; the
   "same actor" premise is corrected.
2. **All other live probe families are different actors** (verified by
   author/date/payload fingerprints where renderable).
3. **No second campaign exists on Diffend** by these fingerprints — 663-gem
   sweep, month-bucketed, zero epoch-suffixed or try*zz names outside May 2026.
4. **New subfamily**: 9 "jina"-in-name campaign gems in the main burst
   (02:12–03:13), extending the borough × VCS × proxy matrix into names.

## Provenance (this note)

- Timeline: `data/gem-ioc-log.jsonl` (diffend_harvest records, Diffend "Last
  diff" timestamps) + epoch verification via `date -d @<epoch> -u`.
- Analysis scratch: `/tmp/timeline_data.json`, `/tmp/timeline_dedup.json`.
- Expansion sweep: `/tmp/sweep3.py` → `/tmp/expansion_names3.json` (663 gems);
  log `/tmp/sweep3.log`. Read-only GETs, ~1.2s pacing, no logins, no POSTs.
- Coverage: timeline built from 385/608 harvested pins (harvest in flight at
  analysis time); sweep is complete.
