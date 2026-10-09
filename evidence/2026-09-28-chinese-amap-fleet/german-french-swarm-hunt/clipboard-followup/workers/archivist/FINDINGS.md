# ARCHIVIST — WikiPatches/ClipBoard Archive-Recovery Findings

**Lead:** usemod.org WikiPatches/ClipBoard — 6,848 anonymous edits May 23–31 2026, revisions purged server-side, reverted May 31 2026 20:57.
**Worker:** ARCHIVIST (archive recovery) for CLIPBOARD coordinator.
**Date of work:** 2026-10-05.
**Status:** COMPLETE. All five assigned techniques executed.

**Prior truth (not redone):** Wayback CDX exact-URL query for `www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` returned exactly 3 captures (20240813050031, 20241205031053, 20260419141229), one identical digest, ZERO in the burst window. Pre-burst 2009 stub already recovered.

**Pacing:** 2–3s between requests, single-threaded, curl. No writes, no interactions beyond reads.

---

## OBSERVED

### Technique 1 — Wayback CDX: diff-URL form (`action=browse&diff=1&id=WikiPatches/ClipBoard`)

**Query URL:**
`https://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3Faction%3Dbrowse%26diff%3D1%26id%3DWikiPatches%2FClipBoard&output=json&fl=timestamp,original,statuscode,digest&collapse=digest`

**Result:** HTTP 503 on first pass (IA transient outage, ~12:25 CDT). Retry try-1 → HTTP 200. Body: `[]` — zero captures.

**Verdict:** NEGATIVE. No archived revert-diff page exists in Wayback.

### Technique 2 — Wayback CDX: URL-variant forms

- **2a `wiki.cgi` variant** — Query: `https://web.archive.org/cdx/search/cdx?url=usemod.org/cgi-bin/wiki.cgi%3FWikiPatches%2FClipBoard&output=json&fl=timestamp,original,statuscode,digest&collapse=digest` → first pass HTTP 503, retry try-2 → HTTP 504, retry try-3 → HTTP 200, body `[]`. **NEGATIVE.**
- **2b `wiki.pl`, no-www host** — Query: `https://web.archive.org/cdx/search/cdx?url=usemod.org/cgi-bin/wiki.pl%3FWikiPatches%2FClipBoard&output=json&fl=timestamp,original,statuscode,digest&collapse=digest` → HTTP 503 on first pass. Superseded by 2c before retry: CDX normalizes scheme/host under one SURT key (see 2c). **NOT RETRIED (subsumed).**
- **2c http-vs-https variant** — Query: `https://web.archive.org/cdx/search/cdx?url=usemod.org/cgi-bin/wiki.pl%3FWikiPatches%2FClipBoard&matchType=exact&output=json&fl=timestamp,original,statuscode,digest,urlkey` → HTTP 200. Three captures, one urlkey `org,usemod)/cgi-bin/wiki.pl?wikipatches/clipboard`, digest `TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI` (all identical):
  - 20240813050031 — `https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` — 200
  - 20241205031053 — same — 200
  - 20260419141229 — same — 200
  CDX returned `https://www.usemod.org/...` as `original` for all three despite the scheme/host-agnostic query: scheme and www are collapsed into the same capture set. **NEGATIVE for burst window (no May 2026 capture in any scheme/host variant).**
- **2d `action=history&id=`** — Query: `https://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3Faction%3Dhistory%26id%3DWikiPatches%2FClipBoard&output=json&fl=timestamp,original,statuscode,digest&collapse=digest` → HTTP 200, body `[]`. **NEGATIVE.**
- **2e `action=browse&id=` (no diff)** — Query: `https://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3Faction%3Dbrowse%26id%3DWikiPatches%2FClipBoard&output=json&fl=timestamp,original,statuscode,digest&collapse=digest` → first pass HTTP 503, retry try-1 → HTTP 200, body `[]`. **NEGATIVE.**

**Verdict (Technique 2):** ALL NEGATIVE. Wayback holds no capture of any URL variant of this page in the burst window — not the page, not its history view, not a browse view, not a diff view.

### Technique 3 — Arquivo.pt

- **3a versionHistory** — Query: `https://arquivo.pt/textsearch?versionHistory=usemod.org%2Fcgi-bin%2Fwiki.pl%3FWikiPatches%2FClipBoard&maxItems=50` → HTTP 200, `estimated_nr_results: 0`, `response_items: []`. **NEGATIVE.**
- **3b `site:usemod.org` + ClipBoard, May–Jun 2026** — Query: `https://arquivo.pt/textsearch?q=site%3Ausemod.org+ClipBoard&from=2026-05-01&to=2026-06-30&maxItems=50` → HTTP 200, `estimated_nr_results: 0`, `response_items: []`. **NEGATIVE.**
- **3c any-date `usemod.org ClipBoard`** — Query: `https://arquivo.pt/textsearch?q=usemod.org%20ClipBoard&maxItems=20` → HTTP 200, `estimated_nr_results: 0`, `response_items: []`. **NEGATIVE.**

**Verdict (Technique 3):** ALL NEGATIVE. Arquivo.pt holds nothing for this URL/page at any date.

### Technique 4 — Common Crawl index API

First attempt used wrong index names (`CC-MAIN-2026-22`, `-24`, `-26`) → HTTP 404 `No index found for collection`. Corrected via `https://index.commoncrawl.org/collinfo.json` (HTTP 200; 128 indexes; latest 2026: `CC-MAIN-2026-39`; relevant window indexes: `CC-MAIN-2026-17` [crawl 2026-04-10→04-23], `CC-MAIN-2026-21` [2026-05-08→05-21], `CC-MAIN-2026-25` [2026-06-05→06-18]).

- Query `https://index.commoncrawl.org/CC-MAIN-2026-{17,21,25}-index?url=usemod.org%2Fcgi-bin%2Fwiki.pl%2AClipBoard%2A&output=json` → all HTTP 404 with body `{"message": "No Captures found for: usemod.org/cgi-bin/wiki.pl*ClipBoard"}`. **NEGATIVE for the page URL in all three crawls.**
- Domain-wide probe `https://index.commoncrawl.org/CC-MAIN-2026-21-index?url=usemod.org&matchType=domain&output=json&collapse=urlkey&filter=original%3A.%2A%5BCc%5Dlip%5BBb%5Doard.%2A` → HTTP 404 `{"message": "No Captures found for: usemod.org"}`. Same on `CC-MAIN-2026-25`. **Common Crawl captured NOTHING from the entire usemod.org domain in the May and June 2026 crawls.**
- One broad-filter attempt (`url=www.usemod.org/*` + regex filter) → HTTP 504 gateway timeout; superseded by the domain-scan negative.

**Verdict (Technique 4):** NEGATIVE. Common Crawl has zero usemod.org coverage in the relevant crawls; nothing from the domain exists to query.

### Technique 5 — Wikiwix

- `https://archive.wikiwix.com/cache/?url=http%3A%2F%2Fwww.usemod.org%2Fcgi-bin%2Fwiki.pl%3FWikiPatches%2FClipBoard` → HTTP 200, but body is a JS-app shell only (no server-rendered archive data). The classic dated-cache path `/cache/20260601000000/http://...` → HTTP 200, redirects to `/cache/index.html?t=20260601000000&url=...`, same JS shell.
- Inspected the app bundle (`static/js/main.2cb1b30d.js`, 200,803 bytes): the app resolves captures via `GET https://archive.wikiwix.com/cache/token.php?url=<url>` then renders via `page.php?a=<…>&b=<…>&url=<url>` in an iframe.
- **token.php query** → HTTP 200, body: `[17657461099,20685142318,36333899210]` — **THREE archive tokens exist for this exact URL.** This is a POSITIVE existence signal: Wikiwix holds archived copies of the page.
- `page.php` with each token (a=b=token), with the app's own computed a/b values (a=17912205352, b=-9508192272.666667), with Referer set, with cookies, and with browser-like Sec-Fetch headers → **HTTP 403 `Forbidden` in all 6 variants** from curl. Direct token path `/cache/17657461099` → HTTP 404.

**Verdict (Technique 5):** POSITIVE EXISTENCE, CONTENT UNRECOVERED VIA CURL. Wikiwix has 3 archived captures of the page (tokens 17657461099, 20685142318, 36333899210 — no dates exposed by token.php). The capture content is served only to the JS app / real browser; curl is blocked (403). **Needs a live-browser check**: open `https://archive.wikiwix.com/cache/?url=http%3A%2F%2Fwww.usemod.org%2Fcgi-bin%2Fwiki.pl%3FWikiPatches%2FClipBoard` in a real browser, let the app load the captures, and read the capture date(s) and page content. Capture dates will determine whether any of the 3 copies falls in May 23–31 2026.

### Technique 6 (bonus probe) — Bing cache

Query `https://cc.bingj.com/cache.aspx?q=usemod.org%2fcgi-bin%2fwiki.pl%3fWikiPatches%2fClipBoard&d=1&w=1` → HTTP 400 "Our services aren't available right now". Consistent with prior finding that search-engine caches are dead. **NEGATIVE/DEAD END.**

---

## INFERENCE

1. **Wayback, Arquivo.pt, and Common Crawl are all confirmed dead ends for the burst content.** Five URL forms × Wayback, two Arquivo.pt query modes plus a full-history versionHistory lookup, and Common Crawl URL + domain scans across the April/May/June 2026 crawls all return zero. The burst content was never archived by any of the three public web archives — consistent with a fast-burn campaign (9 days) on a niche wiki page that crawlers rarely visit.
2. **Wikiwix is the one surviving lead.** Three archive tokens exist for the exact page URL. If any token's capture date falls in May 23–31 2026, it would show the burst content (or the reverted stub, if captured later). Dates and content are currently behind a browser-only render wall.
3. **Common Crawl's total absence of usemod.org** (not just this page — the whole domain) is itself data: usemod.org is effectively invisible to CC's 2026 crawls, so no usemod.org page will ever be recoverable from CC.
4. Epistemic status: everything above is directly observed from tool output. The "Wikiwix holds captures" claim rests on token.php returning 3 numeric tokens for this exact URL — an existence signal, not content.

## Recommended follow-ups (for CLIPBOARD / parent)

- **Live-browser task (highest priority):** open the Wikiwix cache URL above in a real browser, let the JS app render, record each capture's date and whether the content is the 2009 stub or burst content. If a May 2026 capture exists, save the rendered page HTML.
- If Wikiwix yields nothing in-window: remaining recovery surfaces are server-side only (usemod.org's own page history is purged; the revert diff is gone) — the content is likely unrecoverable from public archives.

## Files / raw evidence

- Raw responses: `/tmp/archivist_raw/` (t1_diff.json, t2a_cgi.json, t2e_browse.json, t3a/b/c_arquivo_*.json, t4_cc*.json, cc_collinfo.json, t5*_wikiwix*, t6_bing.html) — ephemeral.
- Wikiwix app bundle: `/tmp/archivist_raw/wikiwix_main.js` (200,803 bytes) — key for reproducing the token.php/page.php flow.
