# Gem metadata deep dive — go-import injection campaign — 2026-09-27

Source: `data/gem-ioc-log.jsonl` (357 successful `diffend_harvest` rows),
`data/gem-pins-diffend.txt` (608 pins). Context:
`notes/rubygems-rescan-2026-09-27.md`. Static analysis only; nothing executed.

**Coverage caveats.** 250 of 357 rows carry a parseable `<meta name="go-import">`
tag; 107 do not — of those, 37 rows have no metadata captured at all
(harvester gap — includes headline gems `tryf3zz`, `oaisurveytestzz`,
`lambprobe4344`, `zzjinavcsgit`, `wandsworthprobe1778551714`,
`oaitest1778473828`; their tags were verified separately via direct Diffend
fetches), and ~70 are plain canaries (`x`, `test`, `tmp`, `abc`, `foo`,
`summary`, `probe`, `output`, `demo yard load`). Some pins appear twice in
the log (duplicate harvest rows, e.g. `tryf3zz 0.0.1` once empty, once
tagged). Counts below are row-level unless noted.

## 1. Go-import tag inventory

Canonical form: `<meta name="go-import" content="<import-prefix> <vcs> <repo-url>">`.
Field split: **description 189 / summary 63** — the actor prefers `description`.

Import prefix is near-universal `rubygems.org/api/v1/gems/<name>.yaml`
(the RubyGems API URL, used as a fake Go import path). Exceptions:

| Gem | Prefix | Note |
|---|---|---|
| `southgoinj1778551435` | `rubygems.org/gems/southgoinj1778551435` | no `/api/v1`, no `.yaml` |
| `lambproxyx` | `rubygems.org/gems/lambproxyx` | same |
| `htmlmetaproxyzz` | `rubygems.org/gems/htmlmetaproxyzz` | same; name says it all |
| `southprobe1778555189` | `rubygems.org/api/v1/gems/southprobe` | truncated — doesn't match gem name |
| `goproxylondonx` 0.0.5 | `rubygems.org/api/v1/gems/goproxylondonx.json` | `.json` not `.yaml` |
| `wandsworthprobe1778551714` 0.0.2 | `HI` | minimal probe — prefix AND url are just `HI` |

VCS distribution (250 tags): **hg 150, fossil 33, mod 30, bzr 13, git 12, svn 11**.
`mod` is not a real VCS — parser-behavior test (see §5).

## 2. Target clustering

Repo URLs after un-laundering `r.jina.ai`:

| Target | Tags | Notes |
|---|---|---|
| `moderngov.lambeth.gov.uk` (via jina) | 48 | mgCalendar*.aspx, mgWebService.asmx |
| `democracy.wandsworth.gov.uk` (via jina) | 46 | same stack |
| `moderngov.lambeth.gov.uk` (direct) | 40 | |
| `democracy.wandsworth.gov.uk` (direct) | 31 | |
| `moderngov.southwark.gov.uk` (via jina) | 21 | |
| `www.digitizationguidelines.gov` (FADGI PDF, via jina) | 15 | rehearsal families `zzfadgivar*`/`zzpdfvar*` |
| `www.digitizationguidelines.gov` (direct) | 12 | |
| jina→example.com (null target) | 9 | control group — `v*`, `chatoaitest*`, `lambfetch001`, `pwnp999` |
| jina (mangled inner URL) | 9 | `v*zzgbqvirfx` parser battery |
| `s.jina.ai` (Jina **search**, not reader) | 9 | `s.jina.ai/lambeth`, `s.jina.ai/wandsworth January 2026` — search-grounded path |
| `moderngov.southwark.gov.uk` (direct) | 4 | |
| `www.marinajacks.com` (via jina) | 2 | random benign 3rd-party: a restaurant catering PDF |
| `20.49.140.101` (direct) | 1 | **raw IP** — `southwarkssrfhack3` → `/mgWebService.asmx/GetMeetings` |
| `lbs-tm-prod.trafficmanager.net` (direct) | 1 | Azure Traffic Manager — `southwarkssrfhack4` → same SOAP path |
| `www.southwark.gov.uk`, `moderngov.southwark.gov.uk.` (trailing dot) | 1+1 | DNS edge cases |

Proxy split overall: **r.jina.ai reader 151 / direct 91 / s.jina.ai search 9**.
The direct (non-laundered) tags are not sloppy — they include the SSRF ladder
and the DNS oddities, i.e. deliberate A/B against the proxy.

## 3. VCS × family and VCS × target matrices

### By name-family

| family | hg | fossil | mod | bzr | git | svn |
|---|---|---|---|---|---|---|
| try*zz | 18 | 0 | 0 | 0 | 0 | 0 |
| *fetch* | 12 | 0 | 0 | 0 | 0 | 0 |
| dlx* | 11 | 0 | 0 | 0 | 0 | 0 |
| *probe* | 5 | 0 | 0 | 0 | 0 | 0 |
| zz* | 35 | 0 | 0 | 1 | 1 | 1 |
| oai* | 16 | 6 | 0 | 5 | 5 | 3 |
| chatoai* | 8 | 1 | 0 | 1 | 0 | 1 |
| lamb* | 15 | 4 | 4 | 1 | 2 | 1 |
| sln* | 3 | 4 | 0 | 4 | 1 | 3 |
| south* | 4 | 6 | 3 | 1 | 1 | 0 |
| wands* | 6 | 0 | 1 | 0 | 0 | 0 |
| *hack* | 2 | 1 | 0 | 0 | 1 | 1 |
| *root* | 1 | 5 | 0 | 0 | 0 | 0 |
| v* (`v*zzgbqvirfx`) | 0 | 0 | 19 | 0 | 0 | 0 |
| london* / sprobe* / other | 14 | 6 | 3 | 0 | 1 | 1 |

Pattern: **hg is the default** — the pure-fuzz families (`try*zz`, `dlx*`,
`*fetch*`, `*probe*`, `zz*`) are near-exclusively hg. The **VCS matrix is
exercised by the named families** (`oai*`, `sln*`, `south*`, `lamb*`,
`*root*`) — fossil/bzr/git/svn appear almost only there. `mod` belongs to
the `v*` parser battery plus the `*inj`/`*mod*`-named gems.

### By target (selected)

- FADGI PDF: hg-only (24/24 direct+jina) — fossil never touches it.
- Wandsworth via jina: hg 39 of 46 — the jina-laundered workhorse path.
- Southwark via jina: most VCS-diverse (hg 10, fossil 8, mod 1, bzr 1, svn 1).
- `s.jina.ai` search: spread across all six VCS values — the search path got
  the full matrix.

## 4. Timeline

Epoch nonces in 39 names (36 distinct) decode cleanly and sit minutes before
their Diffend index time — verified with `date -d @<epoch> -u`:

| Name | Epoch → UTC | Diff indexed |
|---|---|---|
| `oaitest1778473828` | 1778473828 → 2026-05-11T04:30:28Z | 04:42 |
| `wandsworthprobe1778551714` | 1778551714 → 2026-05-12T02:08:34Z | 02:51 |
| `southgoinj1778551435` | 02:03:55Z | 02:10 |
| `southmodinj1778552871` | 02:27:51Z | 02:35 |
| `hacksvn1778554764` | 02:59:24Z | 03:08 |
| `chatoaifetch177855388228` | 1778553882 + seq `28` → 02:44:42Z | 02:50 |
| `newhackhg1778556006` | 1778556006 → 2026-05-12T03:20:06Z | (burst tail) |

Epoch range overall: 2026-05-11T04:30:28Z → 2026-05-12T03:20:06Z. The
`chatoaifetch*` 12-digit nonces are 10-digit epoch + 2-digit sequence.

Diff-timestamp minute histogram (version rows):

- **Rehearsal:** May 11 04:42 (`oaitest1778473828`); 13:29–14:28 cluster
  (`zzfadgivar*`, `zzpdfvar*`, `zzjinavcs*` — FADGI targets, VCS-name matrix)
- **Evening trickle:** 18:16, 19:17, 20:35
- **Main burst:** May 12 01:27 → 03:32, peaks 02:06–02:51 and 03:07–03:19
- **Tail:** 07:55–07:56

The script generated names at publish time; Diffend indexed minutes later.
Non-epoch nonces (`lambprobe4344`, `hgprobe23760`, `testoai4182477`) are
random, not timestamps. `hgprobe*` versions are nonces too (`0.0.459341`).

## 5. Anomalies

1. **`southwarkssrfhack` — the SSRF ladder** (fossil→hg across 0.0.2–0.0.5):
   bare `http://moderngov.southwark.gov.uk` → **raw IP**
   `http://20.49.140.101/mgWebService.asmx/GetMeetings` → Azure
   `http://lbs-tm-prod.trafficmanager.net/mgWebService.asmx/GetMeetings` →
   full `https://moderngov.southwark.gov.uk/mgWebService.asmx/GetMeetings`.
   Domain → IP → cloud-infra → SOAP path: a deliberate SSRF-probe escalation.
   (`lambethssrfhack` exists but its metadata wasn't captured — harvester gap.)
2. **`v*zzgbqvirfx` — URL-parser differential battery** (all `mod` VCS, all via
   r.jina.ai): `http:%2f%2f`, `http://///`, `http:\\//`, `http:/\\/`,
   `http:` (no slashes), `?url=` param form, `%252F` double-encoding, `:80`
   port, `%3Ffoo=` encoded query, `example.com` null targets. Tests how
   downstream URL parsers normalize the repo URL.
3. **`dlxprobe*` — WAF/encoding battery vs modern.gov**: path traversal
   (`mgCalendarMonthView.aspx/../mgCalendarMonthView.aspx?M=1`),
   double-encoded query (`%253fM%253d1`), encoded `?` (`%3fM%3d1`),
   `/foo%3fM=1`, plus direct `mgWebService.asmx/GetMeetings` SOAP targeting
   with encoded params.
4. **Query-param fuzzing** on `mgCalendarMonthView.aspx`: `?M=1&Y=2026`,
   `?M=1%26DD=2026`, `?GL=1&bcr=1&M=1&Y=2026#`, `?M=1\\&amp\\;Y=2026`
   (backslash-escaped entity), `?DD=2026-01-01`, `%23` fragments, `?x=`.
5. **Version-iteration on the injection itself**: `goproxylondonx`
   0.0.1 `test` → 0.0.4 broken tag (`AA < meta name="go-import"
   content="rubygems.org/api/v1/gems` — truncated) → 0.0.5 full tag with
   `.json` prefix. They watched how the summary rendered and adjusted.
   `wandsworthprobe1778551714`: 0.0.1 `x` → 0.0.2 `HI` (escalating minimal
   HTML probes).
6. **Non-rubygems prefixes** (`southgoinj`, `lambproxyx`, `htmlmetaproxyzz`):
   `rubygems.org/gems/<name>` without `/api/v1` or `.yaml` — the import
   prefix itself is a variable under test.
7. **`oaipmxktcwywo`**: repo URL is `lat2search1` — garbage/non-URL, parser
   robustness probe.
8. **Document-library targets**: `wprox-c217-1fossil` →
   `democracy.wandsworth.gov.uk/documents/s124875/Cabinet%20report%20FHF.pdf`;
   `slvfossil308` → `moderngov.lambeth.gov.uk/documents/s1234/a` — the
   attachments path, not just the calendar.
9. **DNS edge cases**: `moderngov.southwark.gov.uk.` (trailing dot),
   `moderngov.lambeth.gov.uk:80`, `moderngov.lambeth.gov.uk//`.

## Read: what the actor was actually testing

This is a **registry-metadata rendering probe with an SSRF reconnaissance
kicker**, run as a single automated script on May 11–12, 2026:

1. **Core question**: which downstream consumers (registry pages, mirrors,
   diff viewers like Diffend, Go module proxies) render gem
   `summary`/`description` as raw HTML — and when they hit a `go-import`
   meta tag, what URL do they resolve and fetch? The canary URLs are
   distinctive (council calendar pages) so any inbound hit is attributable.
2. **The test matrix**: {import-prefix shape} × {6 VCS values} × {proxy,
   direct, search} × {target} × {URL encoding}. `hg` is the control; the
   named families sweep the VCS axis; `v*`/`dlxprobe*` sweep the parser axis.
3. **The SSRF ladder** (`southwarkssrfhack2→5`) is the sharp end: if any
   consumer fetches the repo URL server-side, the actor learns whether it
   follows to bare domains, raw IPs, cloud hostnames, and SOAP endpoints —
   classic SSRF filter-mapping.
4. **r.jina.ai is the observation post**: laundering through the reader
   proxy means the actor can watch Jina's fetch logs (or their own
   redirector) for hits without exposing origin infra; the direct-URL arm
   is the A/B control.
5. The FADGI PDF rehearsal (May 11 afternoon) was the dry run; the council
   burst was the main event. The whole thing was yanked within hours —
   consistent with a probe, not a persistence play.

Raw per-row data: `data/gem-ioc-log.jsonl` (`record_kind=diffend_harvest`,
`meta_summary`/`meta_description` fields). Full tag table is derivable with
the regexes in §1.
