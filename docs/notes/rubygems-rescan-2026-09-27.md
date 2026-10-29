# RubyGems rescan — 2026-09-27

> **Provenance (2026-09-27, per Christopher):** the gem corpus documented
> here is our own **independent Diffend-sourced collection** — the May
> 11–12, 2026 RubyGems go-import meta-tag injection campaign, recovered
> from my.diffend.io. It is **NOT part of the SwarmTraces dataset** and
> is not claimed as one. SwarmTraces records are referenced below only
> as a comparison corpus for bridge checks (all negative).

## Source identification (NEW)

Christopher identified the screenshot source: **https://my.diffend.io/gems** —
**Diffend**, the Mend (formerly WhiteSource) Supply Chain Defender gem
version-diff index. The screenshots' "Last diff" cards and "Mend Software"
footer match exactly (the screenshot's "Merad" was a misread of "Mend").

Diffend indexes RubyGems (plus npm/PyPI) packages and renders per-version
diffs. Critically, **it retains gems that were later yanked from
rubygems.org** — which is why every screenshot name 404s on the live
RubyGems compact index and API but resolves on Diffend.

## The May 11–12, 2026 burst — quantified

Full Diffend enumeration (13 search terms: zz, probe, wandsworth, lamb,
south, london, oai, hack, root, fossil, 999, dlx, fetch; all result pages;
1,277 unique gems) finds a single coordinated campaign:

- **Pre-burst rehearsal:** 39 gems, May 11, 2026 04:42–14:31 UTC
  (`oaitest1778473828`, `zzfadgivar00–13`, `zzpdfvar00–15`,
  `zzjinavcs{fossil,hg,svn,bzr,git}`, `pathpkg94321zz`, `testoai4182477`,
  `zz-oai-test12`)
- **Main burst:** 516 gems, May 11, 2026 18:16 → May 12, 2026 07:56 UTC
- **Peak:** 01:00–03:59 UTC May 12 accounts for 510 of the 516
  (02:00 hour alone: 271 gems)
- **Versions:** 555 gems → 608 version pins; 40 multi-version gems
  (mostly 0.0.1→0.0.2 pairs; `probejiqptzco` 0.0.1–0.0.6,
  `goproxylondonx` 0.0.1–0.0.5, `oaifetchgemugkejy`/`southnewsprobe1778550995`/
  `southfetchprobe42` 0.0.1–0.0.3, `pathpkg94321zz` 0.1.0–0.1.2)

"Last diff" on Diffend is the version's index/diff time, i.e. effectively
the publish time. Epoch-suffixed names self-timestamp: e.g.
`wandsworthprobe1778551714` → 1778551714 = 2026-05-12T02:08:34Z, first
version diffed 02:16; `chatoaifetch177855388228` = epoch 1778553882
(02:44:42Z) + 2-digit sequence "28".

### Burst families (main burst, 516)

| Family | Count | Notes |
|---|---|---|
| try[a-z][0-9]zz | 29 | trya1–5, tryb0–4, tryd0–4, trye0–4, tryf0–8; all 0.0.1, 03:32 |
| oai* | 68 | oaijfossil*, oaijbzravdemr, oailme, oaivcstest*, oaifetchgemugkejy (3 versions), oaisurveytestzz |
| lamb* | 68 | lambfetch002–006, lamhack*, londonyardtestabc is london* |
| south* | 44 | southprobe*, southwarkssrfhack(+2–5), southwarkhack*, southproxy{hg,bzr,svn,fossil}, southip1, southmeet*, southrobots, southdot, southnews-payload1-35329 |
| vcs-named / sprobe* | 30 | southproxy{hg,bzr,svn,fossil}, sprobe{hg,svn,fossil,bzr}z, dlxprobe0–23 |
| *hack* | 21 | hacksvn*, newhack{git,hg,svn}*, wandshack0–9 |
| chatoaifetch* | 19 | 12-digit suffixes = 10-digit epoch + 2-digit seq |
| wandsworth* | 13 | wandsworthprobe*, wandsworthproxy*, wandshack* |
| london* | 5 | londonprobe*, londonproxytestabc*, londontestphjoxf, goproxylondonx |
| other campaign | ~219 | councilfetch*, fetchrootx*, extfetchedwand<epoch>, dnsfetchabc12, docfetchxyz, designfetchdemo, dlxlast, agentoaitestabc123, aaaresultfetchx, eiljanlambpfwo, fosscallamb, fmtsouthprox, fooaid503724d, gexpfetchxyz, gozzz, asdf-zzzz, caljanzzjcq, civic-lambda-proxy, southextractproxy2026, … |

Single-version 0.0.1 gems dominate; the 40 multi-version cases are
enumerated in the Versions bullet above (full per-gem version lists in
`/tmp/diffend_versions.jsonl`).

## Campaign characterization: go-import meta-tag injection probes

Sampled metadata (26 gems across families) shows a systematic pattern. The
payload lives in the gem `summary`/`description` fields as an HTML
`<meta name="go-import">` tag — the tag Go tooling uses for module-proxy
discovery (`content="<import-prefix> <vcs> <repo-url>"`):

- `oaisurveytestzz` summary:
  `<meta name="go-import" content="rubygems.org/api/v1/gems/oaisurveytestzz.yaml`
  `fossil https://r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarMonthView.aspx?M=1&DD=2026">`
- `lambprobe4344` description+summary:
  `<meta name="go-import" content="rubygems.org/api/v1/gems/lambprobe4344.yaml`
  `hg https://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx%23">`
- `tryf3zz` summary: `... tryf3zz.yaml hg https://r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarWeekView.aspx%3F…%26DD%3D2026…%23calendar">`
- `southwarkssrfhack` summary: `... fossil https://moderngov.southwark.gov.uk` (direct, no proxy)
- `wandsworthprobe1778551714` 0.0.2 summary: `"<meta name=go-import content=HI>"` (minimal probe; 0.0.1 was `x`)
- `agentoaitestabc123` description: `... mod https://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx` ("mod" is not a real VCS — parser-behavior test)

VCS values exercised: **hg, fossil, git, mod, bzr, svn** — matching the
vcs-named gem families (`southproxyhg/bzr/svn/fossil`, `sprobehgz/svnz/fossilz/bzrz`,
`newhackgit/hg/svn*`, `zzjinavcs*`).

Repo URLs point at **UK council democracy sites** (all London boroughs,
all running the modern.gov/democracy meeting-calendar stack):
- `democracy.wandsworth.gov.uk` (Wandsworth)
- `moderngov.lambeth.gov.uk` (Lambeth)
- `moderngov.southwark.gov.uk` (Southwark)
- `www.digitizationguidelines.gov/...FADGITechnicalGuidelines...pdf` (FADGI — matches `zzfadgivar*`/`zzpdfvar*` names)

Most (not all) repo URLs are laundered through **`https://r.jina.ai/http://…`**
(the Jina reader proxy); some are direct, one double-URL-encoded
(`wandshack3`).

Canary contents: `lib/x.rb` containing `x=1` or empty; `authors: ["a"]`
(or `x`, `z`, `abc`, `DL`, `news`, `pt`); `date: 1980-01-02` (faked);
`rubygems_version: 3.6.7`. Plain (non-injection) gems use summaries like
`x`, `test`, `tmp`, `foo`, `abc`, `output`, `test2`.

Read: one actor's automated **metadata-injection / SSRF-adjacent probe
campaign** — testing whether gem `summary`/`description` fields are
rendered as raw HTML by downstream consumers (registry, mirrors, diff
viewers, Go module proxies), using UK council calendar pages as
distinctive canary URLs. The gem names themselves are the test matrix:
{place, oai, chat} × {probe, proxy, fetch, hack} × {hg, svn, bzr, fossil, git}.

## How Diffend serves contents (task 2)

- **No `.gem` downloads.** No download button, link, or API observed
  anywhere on gem/version/diff pages (grep for `download` on version
  pages: zero hits; the only form is "Compare gem versions" → POST
  `/gems/diffs`, which requests a new diff render, not a file).
- **Only rendered diffs** — but the diffs are **server-rendered diff2html
  with complete file contents**: every version page
  (`/gems/<name>/<version>`) embeds the full unified diff against empty,
  and pair pages (`/gems/<name>/<v1>/<v2>`) embed the complete
  inter-version diff. Files seen: `checksums.yaml`, `metadata` (full
  `Gem::Specification` YAML), `data/<files>`.
- **Full contents are recoverable** from read-only GETs at normal pace:
  proven by `scripts/harvest_diffend.py` (see Pipeline), which
  reconstructs valid `.gem` tarballs from the rendered diffs (pilot:
  5/5 gems incl. a 2-version gem with diff application).

No yank indicator is shown on Diffend pages — yanked gems simply persist
in its index.

## Why rubygems.org 404s (task 3)

The gems were **yanked from rubygems.org**. Evidence:

1. Every tested screenshot name 404s on both the compact index
   (`/names`) and the version API — yanked gems are removed from both.
2. Diffend (which snapshots gems at publish time) still has them with
   May 2026 diff timestamps.
3. The same actor family does explicit upload/yank testing: the
   currently-live `rgscan_s4_20260317235101` (author "Security Scanner")
   is described as "Benign gem for authorized upload/yank integrity
   testing version 2".
4. Diffend is not a different source — its metadata (rubygems_version
   3.6.7, `rubygems.org/api/v1/gems/<name>.yaml` import prefixes in the
   injections) confirms these gems were published to rubygems.org first.

## Pipeline: fetch_gems.py → harvest_diffend.py (task 4)

`fetch_gems.py`'s `https://rubygems.org/downloads/<name>-<version>.gem`
approach **cannot work** for this campaign (yanked → 404). New method:

**`scripts/harvest_diffend.py`** — same CLI contract as `fetch_gems.py`
(`--names`, `--pin-file` with `name==version` lines, `--pilot`,
`--i-reviewed-manifest` cap at 600). For each pin it walks
`my.diffend.io/gems/<name>` → version diff pages → reconstructs
`.gem` tarballs (metadata.gz + data.tar.gz + checksums.yaml) into
`data/raw/gems/`, and appends provenance to `data/gem-ioc-log.jsonl`
(record_kind `diffend_harvest`, with `diff_url`, `meta_summary`,
`meta_description`, `meta_authors`). Reconstructed gems are layout-valid
but **not byte-identical** to the originals (gzip members re-compressed);
the original `checksums.yaml` is preserved in the log. Verified:
pilot 5/5 → `mine_gems.py` processes the reconstructed gems cleanly
(tar-member read + text grep only, per its safety rules).

**Target list:** `data/gem-pins-diffend.txt` — **608 pins**
(`name==version`, one per line; 555 gems, 40 multi-version). Working
download method: there is no bulk .gem endpoint on either source
(rubygems.org 404s: yanked; Diffend: diffs only). The per-version
Diffend diff pages (recorded as `diff_url` in the log —
e.g. `https://my.diffend.io/gems/tryf3zz/0.0.1`) are the working
"download URLs"; run
`python3 scripts/harvest_diffend.py --pin-file data/gem-pins-diffend.txt --i-reviewed-manifest`
to materialize them into `data/raw/gems/` (~608 gems × ~2 requests at
~1s pace ≈ 25–30 min).

**Gap noted:** `mine_gems.py` scans data-file contents only, not
`metadata` — but this campaign's payload is in `summary`/`description`.
`harvest_diffend.py` captures those fields into the log; a metadata-field
fingerprint pass is still TODO for the parent pipeline.

## Bridge check (task 5)

- **r.jina.ai — PATTERN-LEVEL BRIDGE, confirmed.** The reader-proxy
  laundering convention (`https://r.jina.ai/http://<target>`) in the gem
  injections is identical to the hunt's documented r.jina.ai IOC usage
  (618 reports, 2026-05-01–09-18; e.g.
  `https://r.jina.ai/http://api.allorigins.win/raw?url=`). Same
  tradecraft convention, different operation (registry metadata
  injection vs agent URL-scanning). Not actor attribution — the
  convention is public and widely reused.
- **Council URLs** (`democracy.wandsworth.gov.uk`,
  `moderngov.lambeth.gov.uk`, `moderngov.southwark.gov.uk`): zero hits in
  hunt iocs.csv, zero in all 189,579 SwarmTraces records.
- **go-import**: zero in SwarmTraces; not a hunt IOC.
- **Gem names** (`tryf3zz`, `wandsworthprobe*`, `lambprobe*`, …): zero in
  SwarmTraces; zero in hunt IOCs.
- **Epoch nonces / zz-tokens** from gem contents: `x=1`/empty canaries
  carry no IOCs.

## Currently-live generated families (for contrast)

From the rubygems.org compact index (2026-09-27), still present and
unrelated to the May burst: `byteprobe-{5m,…,400m}-<hex>` (author
`probe`, 2026-09-20), `qa-authz-probe*`/`qa-scope-probe-*` (author `qa`,
2026-08-24), `qoderprobe-gem-20260828` (2026-08-28, incl. an
`onmouseover` injection in one version's author string),
`apex-hijack-probe-a1` (author `audit`, 2026-07-07),
`rgscan_s4_*`/`rgslice-authz-*` (upload/yank integrity testing,
2026-03-17/18), `atlas_qa_handoff_20260528230548` ("Payload-only
encrypted same-day QA handoff snapshot", 2026-05-28),
`auth-loop-debug-artifact-20260306013047` (2026-03-06). None share
naming, authors, or payloads with the May campaign.

Unrelated junk found via the "999" term: `bridge-key-9993` (2026-04-12)
is SEO spam — its README is a "curated web" link farm routed through
`proxmox.turboaccess.net/go?url=…&src=rubygems-209` redirect links.
Not part of the campaign.

## Verdict

- Lane D's narrow 2026-09-26 verdict ("oai in current rubygems.org
  names is dead") **stands** — it tested the live index correctly.
- The broader RubyGems lane is **reopened and resolved**: the screenshot
  burst is a real, ~555-gem, yanked go-import-injection probe campaign
  (May 11–12, 2026), recovered in full via Diffend. Its only corpus
  bridge is the shared r.jina.ai laundering convention (pattern-level,
  not actor-level). No evidence connects it to the SwarmTraces agent
  corpus beyond that.

## Provenance

- Diffend enumeration: `/tmp/diffend_enum2.jsonl` (1,277 gems, 13 terms)
- Burst set: `/tmp/burst_names.json` + pre-burst list in
  `/tmp/diffend_versions.jsonl` job
- Harvester: `scripts/harvest_diffend.py`; pilot verified 2026-09-27
- Metadata sample: `/tmp/meta_sample2.jsonl`
- Read-only GETs only, ~1–1.2s pacing, no logins, no POSTs.
