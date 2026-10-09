# FINDINGS — old shared IOC wordlist → Wikipedia sweep

Date: 2026-10-07 (UTC)
Lane: wikipedia-edit-hunt-2026-10-06 / wordlist-wiki-sweep
Source wordlist: `~/workspace/silent-locus/ioc-wordlist/wordlist.json`
(status=active; 3,822 terms total)

## Scope

1,148 Wikipedia-plausible terms retained from launcher_toolkit, relay,
dead_drop, eval and target categories (`search-terms.json`, built
2026-10-07T00:45:00Z). Dropped: question terms (2,608 eval-question texts),
long digests, bare IPs/CIDRs, raw exploit probes, SQLi/XSS/SSTI
URL-encoded payloads (`dropped-terms.json`).

Method: `insource:"<term>"` phrase search per term per wiki via
`action=query&list=search&srnamespace=*` (curl, >=5.2s pacing, 3 attempts).
Three special-char terms (`${7*7}`, `oai[0-9]+`, `zz=oai[0-9]+`) searched as
`insource:/.../` regex instead — CirrusSearch phrase mode mangles them into
wildcard-ish queries with giant false-positive sets (see CORRECTIONS.md).

Wikis searched (9): en, commons, meta, incubator, test, test2, simple, bg,
www.mediawiki.org.

## Coverage

| wiki | terms searched / 1,148 | status |
|---|---|---|
| en.wikipedia.org | 1,148 | complete |
| commons.wikimedia.org | 1,148 | complete |
| meta.wikimedia.org | 1,148 | complete |
| incubator.wikimedia.org | 1,148 | complete |
| test.wikipedia.org | 1,148 | complete |
| test2.wikipedia.org | 1,148 | complete |
| simple.wikipedia.org | 1,148 | complete |
| bg.wikipedia.org | 1,148 | complete |
| www.mediawiki.org | 1,148 | complete (3 terms fetched with srlimit=1 after repeated IncompleteRead on full payloads; totalhits only) |

Total raw captures: 10,332 insource-*.json (1,148 x 9 wikis) under `raw/<wiki>/`
(old-format zero-padded captures from the first sweep generation were
re-fetched in the corrected format; mediawiki.org's 103 stale captures
re-run during gap-fill).

## Verdict: CLEAN NEGATIVE

No wordlist term was found reused on Wikipedia surfaces in any
agent-shaped or incident-shaped context. Specifically:

- **Zero temp-account matches**: no `~2026-` / `~2025-` account pages among
  any candidate sample titles (1,148 captures with hits > 0 scanned on
  complete data). One near-miss: `{{replyto|~2025-35207-32}}` in a
  mediawiki.org accessibility-feedback archive next to a catbox.moe image
  link — a human replying to a 2025 temp user's feedback, pre-incident.
  Graded NOISE.
- **Zero Lifeval matches**: no case-insensitive `lifeval` in any sample
  title or snippet.
- **Zero `zz=oai<digits>` grammar hits**: the regex search returned 0 on
  all 9 wikis.
- The 1,148 captures with totalhits > 0 break down as generic web noise:
  archive domains (web.archive.org, archive.today, archive.li, arquivo.pt),
  github.com, httpbin.org, file-host URLs in file descriptions, government
  data portals (bea.gov, aihw.gov.au, kansasmemory.gov), COIBot link-report
  pages, and generic code words (`retry`, `fId`, `html_content`).

## Graded candidates of interest (all resolved NOISE)

| term | wiki | context | grade | reason |
|---|---|---|---|---|
| `webhook.site` | commons | User talk:Paq Long — JS snippet with `webhook.site.<hex>` URL | NOISE | named account, self-posted on own talk page, 2026-01-03 — predates incident; human webhook experiment |
| `${7*7}` | test | User talk:BF Testing | NOISE | 2022-06-23 SSTI filter-test section by named user; predates incident 4 years |
| `#../../etc/passwd` | test | User talk:CONFIQ | NOISE | single 2026-01-13 revision by MrBOTinja; predates incident |
| `file=/etc/passwd`, `#../../etc/passwd` | commons | User talk:HIDDENCATI | NOISE | 2019 page content |
| `oai[0-9]+` (regex) | all | coincidental `oai`+digits in URL slugs, ref names (woai1=WOAI TV, Soai2001) | NOISE | no `zz=oai<digits>` grammar present; see CORRECTIONS.md |
| `oai-` | all | ~25k hits/wiki | NOISE | OAI-PMH metadata protocol references |
| `zz_prefix` | en, simple | Template:ISO 15924 script codes | NOISE | `zz` = unassigned script code, not agent grammar |
| `OAIResearchMar26` | en | article "OpenAI–HuggingFace incident" | NOISE | encyclopedic article about a different incident |
| `httpbin.org` | test | K15/K22/K24/K26 citation-test pages | NOISE | "test phab:T113596" pages, 2022, InternetArchiveBot |
| `httpbin.org/redirect-to` | en | User:John Vandenberg/test T113596 | NOISE | WMF dev test page |
| `httpbin.org` | meta | User:John wick 2222 | NOISE | GitHub Actions workflow snippet |
| `httpbin.org` | mediawiki.org | User:Harej/PublicSuffixList; Arabic tech community page | NOISE | WMF dev + code snippet |
| `0x0.st` | commons/meta/mediawiki.org | file descriptions, steward archives, gadget talk | NOISE | image-host references, 2022-era |
| `exploitgym` | bg | Потребител:Alexandar Shopov/sandbox/ChatGPT | NOISE | named human admin's ChatGPT sandbox |
| `usemod.org` | meta/incubator | Interwiki map, Usemod logo file | NOISE | interwiki infrastructure; cross-lane ref only (EUROSWARM lead is separate) |
| `wikiservice.at`, `wikiservice.at/dse/wiki.cgi` | commons/meta | User:DavidSchmitt, User:Anthere archives | RECORD ONLY | reviewer-killed linkage (dse); retained as evidence, no shared-harness claim |

## Reviewer notes

- Kill authority exercised on: dse cross-corpus linkage (retained as
  record only, no operator/harness claim), M5 fetch-oracle gloss (not
  applicable to this sweep), consecutive-UID geometry (not applicable).
- No new agent-shaped claims are made in this report; nothing required
  killing because nothing cleared the bar.

## Limitations (honest)

1. `insource:` searches current page content only — sandboxes get cleaned,
   so historical revisions are not covered. (Same blind spot as the
   vocab/ngram sweeps; revision-history grep was applied to primary
   sandbox pages in the lane's earlier work.)
2. Only 9 wikis searched; the other ~900 Wikimedia wikis were not swept.
3. `srlimit=50` — sample titles/snippets reflect top-50 results per
   term; grading scanned samples, not all hits, for giant-count terms
   (those were auto-graded NOISE only when the term was a generic web
   domain/URL with unambiguous organic context).
4. Search index lag: CirrusSearch may miss very recent edits.

## Provenance

- Term list: `search-terms.json` (1,148 terms, built from
  ioc-wordlist/wordlist.json status=active).
- Raw captures: `raw/<wiki>/insource-<n>.json` with `_sweep` envelope
  (term, category, fetched_utc, http_status) + full API response.
- Collection scripts: `sweep_resume.py`, `gapfill.py` (curl-equivalent
  urllib, >=5.2s pacing, 3 attempts, 60s timeout).
- Corrections: `CORRECTIONS.md` (special-char query mangling).
- Graded: 2026-10-07 by sweep completion coordinator; all kills/NOISE
  grades evidence-bound per lane reviewer rules.
