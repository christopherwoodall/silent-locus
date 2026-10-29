# Hunt lane 1 — libraries.io metadata mirror — 2026-09-27/28

**Verdict: libraries.io is a PARTIAL but VERBATIM mirror of the campaign.**
It did not follow RubyGems' yanks. 303 of 560 queried campaign names (54.1%)
still have live project pages, and 202 of those retain the full poisoned
`<meta name="go-import">` description byte-for-byte.

## Coverage census

Full name census: 557 unique names from `data/gem-pins-batch{1..4}.txt` plus 3
IOC names absent from the pin files (`tryf3zz`, `wandsworthprobe1778551714`,
`q--00cfmapjson726`) verified by direct fetch. Raw data:
`hidden_files/lane1/census_html.jsonl` (560 records, zero gaps).

| cohort | found | miss |
|---|---|---|
| total | 303 (54.1%) | 257 |
| with verbatim go-import description | 202 | — |
| found, non-go-import description (canary words: `x`, `tmp`, `probe`, `output`) | 90 | — |

## The time-freeze finding

Joining the census against `published_at` from the Elastic
`diffend_harvest` records shows libraries.io is a **snapshot frozen mid-burst**,
not a live mirror:

| publish hour (UTC) | found | miss |
|---|---|---|
| 2026-05-11 (all day, rehearsal) | 42 | 0 (100%) |
| 2026-05-12 01:00 | 68 | 3 (96%) |
| 2026-05-12 02:00 | 121 | 149 (45%) |
| 2026-05-12 03:00 | 66 | 105 (39%) |

Everything published before ~02:00 UTC May 12 was captured; the mirror's
RubyGems sync evidently ran mid-burst and never picked up the rest (or the
yanks beat its later syncs). Net: an independent, timestamped, third-party
copy of the campaign's first ~3 hours, frozen in amber.

## Verbatim-match verification

libraries.io descriptions are byte-identical to our Diffend-harvested
go-import payloads. Example — ES `hit` record `matched_string` for `tryf3zz`:

```
rubygems.org/api/v1/gems/tryf3zz.yaml hg https://r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarWeekView.aspx%3FM%3D1%26WN%3D4%26CID%3D0%26OT%3D%26C%3D-1%26MR%3D0%26DL%3D0%26ACT%3DLater%26DD%3D2026%26txtonly%3D1%23calendar
```

libraries.io `og:description` for the same gem renders the identical string
inside `<meta name="go-import" content="...">`. Same for `southwarkssrfhack`
(`fossil https://moderngov.southwark.gov.uk`) and `uxjinalamb2`
(`hg https://r.jina.ai/http://moderngov.lambeth.gov.uk/...`).

## All 8 IOC names verified live

| gem | libraries.io URL | shows |
|---|---|---|
| tryf3zz | https://libraries.io/rubygems/tryf3zz | full go-import tag (hg → Wandsworth via r.jina.ai) |
| southwarkssrfhack | https://libraries.io/rubygems/southwarkssrfhack | full go-import tag (fossil → Southwark) |
| londonyardtestabc | https://libraries.io/rubygems/londonyardtestabc | `tmp` (matches canary description) |
| southfetchprobe42 | https://libraries.io/rubygems/southfetchprobe42 | `probe` |
| wandsworthprobe1778551714 | https://libraries.io/rubygems/wandsworthprobe1778551714 | `<meta name=go-import content=HI>` |
| zzsouthrunnerb | https://libraries.io/rubygems/zzsouthrunnerb | `docs helper` |
| uxjinalamb2 | https://libraries.io/rubygems/uxjinalamb2 | full go-import tag (hg → Lambeth via r.jina.ai) |
| q--00cfmapjson726 (June-18 wave) | https://libraries.io/rubygems/q--00cfmapjson726 | `Reference to public dataset for maps and statistics.` + **homepage field = `https://www.sec.gov/files/county.json`** (payload link preserved in a second field) |

## Retained-payload statistics (202 go-import descriptions)

- VCS values: hg 107, mod 34, fossil 24, git 17, bzr 11, svn 7 — same
  distribution shape as the corpus (hg-dominant, fake `mod` present).
- Target domains: r.jina.ai 123, moderngov.lambeth.gov.uk 67,
  democracy.wandsworth.gov.uk 54, www.digitizationguidelines.gov 34
  (the `zzfadgivar*` rehearsal family's FADGI PDF target — already in the IOC
  pack, corroborated here), moderngov.southwark.gov.uk 13, s.jina.ai 3.
- Family retention skew: `zz*` 61/13 found, `proxy` 5/0, `probe*` 6/35 —
  consistent with the time-freeze (early families fully captured).

## Method notes

- `https://libraries.io/api/rubygems/{name}` works **without** an API key but
  is rate-limited: `x-ratelimit-limit: 10`, `retry-after` ~676s. ~500 fast
  requests tripped it; 24 records were initially misclassified as misses
  from 429s and had to be purged and re-queried.
- The HTML project pages (`https://libraries.io/rubygems/{name}`) are NOT
  rate-limited the same way; the full census ran against HTML at 2× workers,
  1s spacing, parsing `og:description`. Watch for `IncompleteRead`
  mid-transfer drops — the og:description tag sits in `<head>`, so partial
  bodies still parse (flagged `partial: true`).
- libraries.io **site search and API search require login / API key** —
  no broad `go-import` enumeration possible without credentials (not pursued:
  no logins per lane rules). Name-driven census was the viable path.
- `/tmp` was wiped mid-run (497-record census lost); all working files now
  live in `hidden_files/lane1/` (persistent). Scripts: `census.py` (API),
  `census_html.py` (HTML, sharded, resume-safe).

## Bottom line for the hunt

libraries.io is the best surviving public copy of the campaign's opening
hours — 300 pages RubyGems can't yank, with payload text intact. It adds no
new gems beyond our corpus, but it is an independent, citable, third-party
witness to the go-import mechanism, and the only mirror found so far that
kept the June-18 wave's SEC payload link (in the homepage field).
