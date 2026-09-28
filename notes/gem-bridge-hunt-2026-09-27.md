# Bridge analysis: gem campaign vs frozen urlquery hunt — 2026-09-27

**Question from Christopher:** "Anything connected to our other dataset?"
**Hunt source (READ-ONLY, frozen):** `/home/hatch/workspace/muse-home/projects/urlquery-api-hunt/`
(359 IOC rows, 1,275 graph nodes / 2,550-node Elastic export, 51,643 unified reports — nothing written there.)
**Gem source:** `data/gem-ioc-log.jsonl` (336 gem names, 199 payload URLs, 9 domains) + `notes/rubygems-rescan-2026-09-27.md`.

## Headline verdict

**The frozen hunt already contains this exact campaign.** Lane 5 (2026-09-25) investigated the
May-12 gem wave and absorbed it into the hunt's graph: 7 gem IOC nodes, an incident node, and a
technique node. The 2026-09-27 Diffend rescan independently re-derived the same campaign and
quantified it far beyond lane 5's partial view (555 gems / 608 pins vs lane 5's handful of probe
gems + the disputed "2,090" public-record figure).

On the corpus itself (hunt's 51,643 urlquery reports vs the gem payloads): **zero literal
URL/domain/token overlap.** The connections are tradecraft-level (shared toolkit conventions),
not infrastructure-level (no shared hosts, inboxes, slugs, or targets). Verdict per connection
below.

## 1. The hunt absorbed the gem campaign first (meta-finding)

Frozen graph nodes (in `artifacts/dataset/elastic/graph-nodes-2026-09-25-v1.ndjson`):

| node_id | what it is |
|---|---|
| `ioc-lane5-dlxprobe4` | gem-package: dlxprobe4, go-import canary probe |
| `ioc-lane5-wandsworthprobe1778551714` | gem-package: epoch-suffixed probe gem |
| `ioc-lane5-slnprobe-cluster` | gem-package: slnprobe14–26 cluster |
| `ioc-lane5-slnleaker5` | gem-package: "leaker" variant |
| `ioc-lane5-southpxdatapp6pi` | gem-package: webhook dead-drop variant |
| `ioc-lane5-zzsouthrunner` | gem-package |
| `ioc-lane5-sec-proxy-gems` | gem-package group |
| `inc-rubygems-oai` | incident: "RubyGems 2,090+ 'oai' publish wave" |
| `tech-lane5-goimport-canary` | technique: "go-import meta-tag canary packages" |

So the hunt's *only* go-import / council-targeting knowledge comes from lane 5's own
investigation of this campaign — it is the same campaign observed twice, not a bridge between
two independent observations. Anyone reading the hunt's graph should know `inc-rubygems-oai`
and the lane-5 gem nodes describe the Diffend corpus.

**Lane 5 vs Lane D, resolved:** Lane D (2026-09-26) declared "DEAD — no bridge" and corrected
the 2,090 count — but it checked the *live* compact index, from which yanked gems are removed.
The Diffend evidence overturns its "wave does not exist" conclusion while keeping its count
correction for the live index: the wave existed, was yanked, and Diffend retained it. Our
enumeration: 555 gems / 608 pins (611-line pin file incl. header), not 2,090 — the origin of
the 2,090 figure remains unexplained (possibly npm/PyPI, other name families, or erroneous).

**Coverage gap:** our 608-pin set includes lane 5's sln (32), southpx (1), southrunner (3),
pwnp999 (1) families, but NOT `sec-proxy-gems`, `slnleaker*`, `yardbreaker*`, `exfiltest*`
(0 hits each in `data/gem-pins-diffend.txt`). Those likely belong to the public record's
June-18 wave or differently-named families — not yet pulled from Diffend.

## 2. Per-connection verdicts

### a. r.jina.ai reader-proxy laundering — PATTERN-LEVEL BRIDGE (confirmed)
- Hunt: `r.jina.ai` domain IOC, **618 reports** (+246 proxy-domain rows); carried URLs include
  `r.jina.ai/http://api.allorigins.win/raw?url=` (proxy chains) and
  `pure.md/r.jina.ai/http://www.sec.gov/files/county.json`.
- Gems: `r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarWeekView.aspx?...`,
  `r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarMonthView.aspx?M=1&DD=2026`,
  plus 10+ `r.jina.ai/http://example.com...` placeholder variants; also `s.jina.ai` references.
- **Literal carried-URL overlap: none.** Same laundering convention, disjoint target sets.
  Verdict: shared tradecraft, not shared infrastructure.

### b. Council targets (Wandsworth / Lambeth / Southwark) — GEM-EXCLUSIVE
- Grep over all 51,643 hunt reports: `wandsworth` 0, `lambeth` 0, `southwark` 0,
  `modern.gov` 0, `go-import` 0, `dlxprobe` 0, `tryf3zz`/`trye3zz` 0,
  `r.jina.ai/http://democracy` 0.
- The UK-council calendar targeting exists only in the gem campaign. No hunt campaign
  targets these councils.

### c. SEC `county.json` — HUNT YES, OUR GEMS NO (lane 5's gem-SEC claim unverified)
- Hunt: `https://www.sec.gov/files/county.json` (90 reports), vanderbi.lt slugs
  (`maallraw260618`, `countrf260623c`), `pure.md/r.jina.ai/http://www.sec.gov/files/county.json`.
- Our 608-pin gem corpus: **zero** `sec.gov` URLs in any payload.
- Lane 5's note attributes SEC-chasing to the public record's June-18 wave (83 gems, via
  r.jina.ai / Google Translate / Jira chains) — that wave is **not** in our Diffend pull
  (May 11–12 only). Status: public-record-only, unverified from our data. Do not cite as a
  confirmed bridge.

### d. `example.com` placeholder sink — GEM-SIDE CONFIRMED, HUNT-SIDE NOT IN IOC SET
- Gems: 10+ payload variants (`https://r.jina.ai/http://example.com`,
  `https://r.jina.ai/http://example.com%23`, double-encoded variants) — the actor tests
  placeholder/sink URLs through the same injection path.
- Hunt IOC rows: **zero** `example.com` entries. Lane 5's note claims hunt-side
  itty.bitty.site LZMA pages scrub sinks to literal `example.com`, but it is not codified
  as an IOC. Weak/unverified bridge.

### e. Epoch-suffix artifact naming — CONVENTION-LEVEL BRIDGE (confirmed, different windows)
- Gems: `wandsworthprobe1778551714` → 2026-05-12 02:08 UTC; `proxyzz1778548845` →
  2026-05-12 01:20 UTC; `chatoaifetch*` 12-digit epoch+seq suffixes.
- Hunt: ntfy topics `oai1781965813`, `oaimic1781974645`, `tabx1781967972`,
  `rb1782012062tfkhj`, `cross1781797021`, `a115r1781964433` → **2026-06-18 – 06-21**.
- Same naming convention (~5.5 weeks apart), no shared epoch values. Convention-level only.
  Note: the hunt's June-18 ntfy epoch coincides with the public record's June-18 gem wave
  date — circumstantial, not evidence.

### f. `zz` tokens — CONVENTION-LEVEL ONLY, zero literal overlap
- Hunt: `zzmasscounty*`, `zzcounty1vhve` (YOURLS slugs), `zzuq…` (timing-probe pages) — in
  report bodies/notes, not IOC rows.
- Gems: 96 of 336 names contain `zz` (`try[a-z][0-9]zz` ×29, `zzjinavcs*`, `zzfadgivar*`,
  `v12zzgbqvirfx`…).
- No shared literal token. Both use `zz` as a namespace/prefix marker.

### g. Gem names/packages in hunt corpus — ZERO
- 51,643 reports grepped for gem names, `rubygems`, `go-import`: zero hits (confirms lane 5's
  earlier grep). No hunt report references the gem campaign's packages.

### h. Hardcoded-IP SSRF tradecraft — GEM-SIDE ONLY (notable)
- `southwarkssrfhack3` go-import payload: `hg http://20.49.140.101/mgWebService.asmx/GetMeetings`
  — the actor hardcoded the resolved Azure IP of the Southwark ModernGov host, bypassing DNS.
  The gem name itself declares the intent (`ssrfhack`). No hunt-side equivalent checked;
  hunt IOC rows contain no IP-literal target URLs of this form.

### i. `s.jina.ai` (Jina search API) — GEM-SIDE ONLY
- Present in gem payload references; zero hunt IOC rows.

## 3. Overall picture

Three layers, keep them distinct:

1. **Same campaign, observed twice:** the frozen hunt's lane-5 nodes (`inc-rubygems-oai`,
   7 gem IOCs, `tech-lane5-goimport-canary`) ARE the Diffend gem campaign. The rescan's
   contribution is quantification (555 gems / 608 pins, burst timing, full payload
   inventory) and the download path (Diffend diff → reconstructed `.gem` tarballs).
2. **Shared tradecraft, different operations:** r.jina.ai laundering, epoch-suffix naming,
   `zz` namespacing, `?x=` cache-busting appear in both corpora with disjoint targets,
   disjoint identifiers, and disjoint time windows (May 12 gems vs June 18–21 hunt beacons).
   Consistent with a common operator toolkit or playbook, not with shared infrastructure.
3. **Unverified public-record claims:** the "2,090 packages," the June-18 SEC-chasing wave,
   and the OpenAI-agent attribution (rubyhack.ai / Nightingale Collective) all rest on the
   public record, not on our Diffend pull. Our data neither confirms nor refutes them.

## 4. Open threads / recommended next pulls

- Pull the June-18 wave from Diffend (names per public record: `slnleaker*`, `yardbreaker*`,
  `exfiltest*`, sec-proxy families) to test the SEC-`county.json` bridge claim directly.
- Diffend indexes npm/PyPI too — check whether the campaign extends beyond RubyGems
  (the unexplained 2,090 figure may live there).
- The `20.49.140.101` hardcoded-IP payload and the `southwarkssrfhack*` family deserve a
  dedicated SSRF-angle writeup; check whether other pins hardcode IPs.
- `v12zzgbqvirfx`-style suffixed tokens and `s.jina.ai` references are unexamined —
  fold into the metadata fingerprint pass.
- If the hunt is ever unfrozen: annotate `inc-rubygems-oai` with the Diffend quantification
  (555/608, burst timeline) — do NOT merge the corpora; provenance stays separate per
  Christopher's correction (gem corpus is our own Diffend pull, not SwarmTraces data).
