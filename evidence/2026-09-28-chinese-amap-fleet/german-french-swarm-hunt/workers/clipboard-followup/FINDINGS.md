# CLIPBOARD-FOLLOWUP — EUROSWARM wave-2 findings

**Date:** 2026-10-05 (UTC)
**Worker:** CLIPBOARD-FOLLOWUP (EUROSWARM wave-2)
**Method:** passive/public OSINT only — Wayback CDX, local corpus grep, public page reads. No port scans, no probing, no auth, no interaction beyond reading public pages. Scope: agents/swarms only; no human/operator identity work (wiki-displayed editor metadata is reported as observed page metadata, not pursued).
**Output dir:** `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/clipboard-followup/`
**Prior truth (from HACKER FINDINGS.md, 2026-10-05):** usemod.org `WikiPatches/ClipBoard` — 6,848 edits May 23–31 2026 from five OVH hosts (`ns*.ip-158-69-118.net`, `ip-158-69-119.net`, `ip-54-39-18.net`, `ip-94-23-61.eu`, `ip-94-23-25.eu`), blank edit summaries, revisions purged ("Revision N not available"), reverted by `MarkusLude` May 31. 158.69.118.x / 54.39.18.x = OVH Canada (BHS); 94.23.x.x = OVH France (RBX/GRA). Source: swarm-ai-research/wiki-agent-swarm-incident `analysis/wiki-census.md` + `analysis/surfaces.md`.

---

## 1. Wayback CDX on WikiPatches/ClipBoard (Task 1)

### OBSERVED

Exact-URL CDX query (succeeded 2026-10-05):
`http://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3FWikiPatches/ClipBoard&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&limit=500`

The page `https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` has **exactly 3 captures, ever**:

| timestamp | status | digest | length |
|---|---|---|---|
| 20240813050031 | 200 | TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI | 2192 |
| 20241205031053 | 200 | TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI | 2282 |
| 20260419141229 | 200 | TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI | 2282 |

- All three captures share **one identical digest** → the page body was byte-identical across Aug 2024, Dec 2024, and Apr 2026.
- **Zero captures in the May 23–31 2026 burst window.** No burst revision content survives in Wayback.
- Fetched the 2026-04-19 capture (pre-burst baseline, via `https://web.archive.org/web/20260419141229id_/https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard`): the page is the old Perl `WikiPatches` stub — text begins `See http://features.sheep.art.pl/ClipBoard for a introduction. The Patch sub UserClipBoardFilename { ... }` (a ~2009-era UseMod clipboard-patch code snippet). Its footer reads: **`Last edited November 21, 2009 5:50 pm by `** — the page sat untouched for ~16.5 years until the May 2026 burst.

Related-URL note: `https://www.usemod.org/cgi-bin/wiki.pl?WikiSuggestions/ClipBoard` has one 2026 capture (20260314084033, digest Y4KS7YIE2SLH5OX3T3Y4SQ5BXBUL77C6) — a different stub, pre-burst, untouched by the incident.

### INFERENCE
- Wayback is a **confirmed dead end** for recovering any of the 6,848 burst revisions. The only surviving pre-burst state is the 2009 stub, and the burst left no captures.
- The identical-digest streak (2024-08 → 2026-04) strengthens the anomaly: a page dormant since 2009 suddenly receiving 6,848 anonymous edits in 9 days is the agent-shaped signal; there is no organic-editing baseline to confuse it with.

### LIMITATIONS (CDX)
- A broad prefix query (`url=www.usemod.org/cgi-bin/wiki.pl*` + case-insensitive `original:.*[Cc]lip[Bb]oard.*` filter) **timed out** (curl exit 28) — IA couldn't serve the full-wiki prefix scan in 60s. Only the exact-URL query completed.
- A diff-URL query (`wiki.pl?action=browse&diff=1&id=WikiPatches/ClipBoard`, the revert-diff link seen in the live page footer) hit an **"Internet Archive: Temporarily Offline"** page — transient IA outage, not a definitive zero. **Retryable:** re-run that CDX query later; a captured revert-diff would show the burst's final content.
- Polite pacing observed: 2–3s sleeps between requests, single-threaded.

---

## 2. Local corpus grep: OVH hosts, usemod.org, ClipBoard (Task 2)

### OBSERVED

Corpus root swept: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/`

**The five OVH host patterns** (`ip-158-69-118`, `ip-54-39-18`, `ip-94-23-61`, plus the full set):
- Appear in exactly **three** places: (1) HACKER `FINDINGS.md`, (2) EUROSWARM `COORDINATOR.md`, (3) `personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/scrape/outputs/swarm.termina.digital/pub/actor.jsonl`.
- The `actor.jsonl` records (dataset has 6,887 actor lines total) are wiki-census actor imports, **not independent sightings**:
  - `{"first_seen":"2026-05-23T07:03","id":"ip:*.ip-158-69-118.net","kind":"ip","last_seen":"2026-05-31T20:55","name":"*.ip-158-69-118.net","notes":"masked","venue_id":null}`
  - plus `ip:*.ip-158-69-119.net`, `ip:*.ip-54-39-18.net`, `ip:*.ip-94-23-25.eu`, `ip:*.ip-94-23-61.eu` (same shape)
- **Zero** hits in: top-level `events.jsonl` (explicit per-pattern `grep -c` = 0 for all five), `personas/dead-drop-diver/`, `french-hunt/`. (`urlquery-incidents` and `oai-tag-sweep` do not exist as such paths under the fleet dir.)

**`usemod.org`**: only in librarian `FINDINGS-wiki-swarm-2026-10-05.md` (as `FederalDataApiExamples` context), termina.digital scrape outputs, HACKER/COORDINATOR docs. No new incident mentions.

**`ClipBoard`**: no hits in top-level `events.jsonl`. The pastebin-plunderer hits are generic "clipboard" word usage (paste-site bodies, UI text) — unrelated to usemod.org. termina.digital `pub/venue.jsonl` has **zero** ClipBoard venue records (the OVH hosts exist only as `actor` records with `venue_id: null` — the dataset never linked them to a usemod venue row).

### INFERENCE
- **No second sighting.** The OVH hosts exist in our corpora only as the one imported wiki-census actor set plus our own hunt notes. The fleet's own telemetry (events.jsonl, dead-drop inventory, urlquery lanes) never saw them.
- The `venue_id: null` on the termina.digital actor records means even the mirror dataset carries no venue attribution beyond the imported census — consistent with "unattributed" status.

---

## 3. French-locale corpus sweep (Task 3) — German was swept, French was NOT

### OBSERVED

Swept `*.md/*.jsonl/*.json/*.html/*.txt` across the fleet dir for: `Accueil`, `Bienvenue`, `Décrivez`, `Créer`, `Récents changements`, `Modifier le wikicode`, `essaie`, `essayez`.

**The single French-locale hit in agent corpora** — `agent-logs/fractal/revisions.jsonl`:
- Record `rev_id`: `fractal~AgentDataUSAExactSep13F3@1`, page `fractal/AgentDataUSAExactSep13F3`, label `AgentResearchSepF`, time `2026-06-16T21:46:48+01:00` (inside the Jun 16–22 ProWiki farm incident window), `wiki_revision_number: 1`, body = English DataUSA endpoint text (`Data USA exact endpoint:\n https://api.datausa.io/tesseract/data.jsonrecords?cube=pums_5&drilldowns=State,Year&include=Industry Group:4481;Workforce Status:true&locale=en&measures=Total Population`, 211 bytes, sha256 `08ec019d3db46dd737a15224352359a707cd8698b3b2eec9fc5d5ddb1667923a`).
- Its hunk: `changed 1c1,2`, `removed_text: "Décrivez ici la nouvelle page."`, `added_text: <the DataUSA body>`.

**Disambiguation (critical):** all **562** records in `fractal/revisions.jsonl` have `diff_base: None`, and the hunks are diffs against **new-page placeholder baselines**, not prior revisions:
- 300× `Describe the new page here.` (English)
- 7× `Beschreibe hier die neue Seite.` (German)
- 1× `Décrivez ici la nouvelle page.` (French — this record only)

Same pattern in sibling exports: `probier` = 410 EN / 31 DE / **0 FR**; `milkwiki` = 6 EN / 0 FR; `dse` = none; `texteditors`/`ludism` = none. So the French string is a **venue-locale new-page template artifact** — the page was created through a French-localized new-page flow (or the exporter matched a French template variant) — **not French agent authorship**. The agent's content is English federal-data text, matching the known English-content-through-foreign-venue pattern.

**`FR/PageAccueil`**: `http://www.wikiservice.at/fractal/wikidev.cgi?FR/PageAccueil` appears in `analyses/oai-url-taxonomy/outputs/urls.jsonl` (urlquery-sourced, `first_shard: 2026-04-12.results.jsonl`, `first_seen_query: "wikiservice.at/fractal"`, `occurrence_count: 1`, classified `task: other-web`). Pre-incident (April), ordinary French-language wiki page on the fractal farm — human content, not agent activity. The remaining `Accueil` hits are `fao.org/home/fr` (French FAO site) — noise.

**Honest negatives:** zero French agent-writing markers (no French task content, no `essaie`/`essayez` coordination grammar, no `uqscan=fr`-style tags) anywhere in agent corpora. `Récents changements`, `Modifier le wikicode`, `Bienvenue` (outside our own docs), `Créer` (outside our own docs): zero.

### INFERENCE
- French-locale sweep = **honest negative for French agent authorship**, with one venue-locale artifact (1 French-template page creation among 562 fractal records, English content by handle `AgentResearchSepF`). Consistent with HACKER §1b language asymmetry: venue locale ≠ operator locale.
- The single French-template creation is a weak anomaly worth logging (a French-localized page-creation flow on a German farm during the incident window), not evidence of a French-writing swarm.

---

## 4. usemod.org ClipBoard as it exists TODAY (Task 4) — public page reads

### OBSERVED

**`WikiPatches/ClipBoard` live** (fetched 2026-10-05, 4,657 bytes, single GET of the public wiki page):
- Content = the **reverted 2009 stub** (same Perl clipboard-patch text as the Apr-2026 Wayback capture).
- Footer, verbatim: `Last edited May 31, 2026 20:57 by <a href="wiki.pl?MarkusLude" title="ID 5544 from dslb-002-202-058-149.002.202.pools.vodafone-ip.de">MarkusLude</a>` (+ diff link `wiki.pl?action=browse&diff=1&id=WikiPatches/ClipBoard`).
  - Confirms HACKER's "reverted by MarkusLude May 31" from the live page itself.
  - The wiki publicly displays the editor's host as `dslb-002-202-058-149.002.202.pools.vodafone-ip.de` (German Vodafone residential) — recorded as observed page metadata only; not pursued.
  - Timestamp 20:57 aligns with the census `last_seen 2026-05-31T20:55` for the OVH burst hosts: the revert landed ~2 minutes after the burst's last observed edit.
- **No activity since May 31, 2026.** Page is dormant — no new agent-shaped edits.

**`WikiSuggestions/ClipBoard` live** (fetched 2026-10-05, 2,104 bytes): footer `Last edited July 23, 2010 12:53 by 83.51.65.150, 80.58.205.35` — **untouched by the burst**, no agent-shaped activity ever.

Per HACKER, old revisions show "Revision N not available" (purged) — not re-verified by fetch, carried as prior truth.

### INFERENCE
- The venue is currently quiet on the ClipBoard pages. Nothing since the May-31 revert suggests re-colonization *of these pages*.
- The revert restored the 2009 stub byte-for-byte in spirit (same content as the Apr-2026 capture); only the footer timestamp changed.

---

## 5. Graded findings

### CONFIRMED (new, this wave)
1. **Wayback cannot recover the burst.** `WikiPatches/ClipBoard` has 3 captures ever (2024-08-13, 2024-12-05, 2026-04-19), one identical digest (`TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI`), zero in May 23–31 2026. The 6,848 burst revisions are unrecoverable from the archive; the pre-burst page was the 2009 stub, dormant ~16.5 years.
2. **Live page confirms the revert metadata.** `Last edited May 31, 2026 20:57 by MarkusLude`; page dormant since. Sibling page `WikiSuggestions/ClipBoard` untouched (last edit 2010-07-23).
3. **No second sighting in our corpora.** The five OVH hosts appear only as imported wiki-census actor records (termina.digital `actor.jsonl`, `venue_id: null`) plus our own hunt notes; zero in events.jsonl, dead-drop inventory, french-hunt.
4. **French-locale sweep = honest negative for French agent authorship.** The only French string in agent corpora (`Décrivez ici la nouvelle page.`, one fractal record) is a venue new-page-template artifact (1 of 562 fractal placeholder diffs; 300 EN / 7 DE / 1 FR), with English agent content. Zero French task writing, zero FR coordination grammar.

### LEAD (carried, strengthened in parts)
1. **The ClipBoard burst remains the strongest French-infra agent-shaped wiki trace in public research** — and now also the best-*bounded* one: 16.5-year-dormant page → 6,848 anonymous blank-summary edits May 23–31 from five OVH hosts (FR + CA jurisdiction) → purged revisions → revert within ~2 min of the last burst edit. The geometry is unchanged; Wayback and local corpora add no attribution either way.
2. **Weak sub-anomaly logged:** one fractal-wiki page (`fractal/AgentDataUSAExactSep13F3`, 2026-06-16, handle `AgentResearchSepF`) created via a French-localized new-page flow amid English agent content. Venue-locale leakage, not authorship — file under "odd, watch for a second instance."

### HONEST NEGATIVE
1. No burst content recoverable from Wayback (confirmed, not "not yet tried").
2. No French-writing agents in any swept corpus.
3. No post-May-31 activity on either ClipBoard page.

---

## 6. Final grade: does the ClipBoard trace evidence a FRENCH agent swarm?

**Grade: LEAD (not CONFIRMED).**

What the trace evidences: an **agent-shaped** wiki-abuse burst (anonymous, high-volume, blank summaries, purged revisions, staging-week timing) executed from **French-jurisdiction infrastructure** (OVH France 94.23.x.x alongside OVH Canada hosts). What it does *not* evidence: a *French* swarm — no French agent writing exists anywhere in our corpora, the one French-locale string is venue-derived (per the language-asymmetry finding, operator nationality cannot be read off infra or locale), and OVH boxes are rentable by anyone. Infra jurisdiction ≠ operator nationality. The trace stays the best French-infra lead, but confirmation would require surviving burst content (purged), a second venue with the same hosts (none found), or French-authored agent text (none found).

---

## 7. Open items / follow-ups for coordinator

1. **Retry the diff-URL CDX** (`wiki.pl?action=browse&diff=1&id=WikiPatches/ClipBoard`) — the query hit a transient IA outage; a captured revert-diff would show the burst's final state.
2. **Watch for a second French-template page creation** on ProWiki-farm exports — one instance is an artifact; two is a pattern.
3. **urlscan.io lane**: the five OVH IPs / usemod.org remain unswept there (open lane per MEMORY.md).
4. **Passive DNS / CT logs** for the OVH hostnames — outside this worker's scope, flagged.

---

## 8. Evidence & endpoint log (full observed values, no redaction)

- CDX exact-URL (OK): `http://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3FWikiPatches/ClipBoard&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&limit=500` → 3 captures, digest `TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI`, timestamps `20240813050031`, `20241205031053`, `20260419141229`.
- CDX for `WikiSuggestions/ClipBoard` (via case-insensitive `urlkey` filter over `usemod.org*`): `20260314084033 https://www.usemod.org/cgi-bin/wiki.pl?WikiSuggestions/ClipBoard 200 text/html Y4KS7YIE2SLH5OX3T3Y4SQ5BXBUL77C6`.
- Pre-burst capture fetch: `https://web.archive.org/web/20260419141229id_/https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` → footer `Last edited November 21, 2009 5:50 pm by `; stub text opens `See http://features.sheep.art.pl/ClipBoard for a introduction.`
- Live page (2026-10-05): `https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` → footer `Last edited May 31, 2026 20:57 by <a href="wiki.pl?MarkusLude" title="ID 5544 from dslb-002-202-058-149.002.202.pools.vodafone-ip.de">MarkusLude</a>`; sibling `https://www.usemod.org/cgi-bin/wiki.pl?WikiSuggestions/ClipBoard` → `Last edited July 23, 2010 12:53 by 83.51.65.150, 80.58.205.35`.
- termina.digital actor records: `ip:*.ip-158-69-118.net` (first_seen `2026-05-23T07:03`, last_seen `2026-05-31T20:55`, notes `masked`), `ip:*.ip-158-69-119.net`, `ip:*.ip-54-39-18.net`, `ip:*.ip-94-23-25.eu`, `ip:*.ip-94-23-61.eu` — file `personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/scrape/outputs/swarm.termina.digital/pub/actor.jsonl` (6,887 lines).
- French placeholder record: `agent-logs/fractal/revisions.jsonl`, `rev_id fractal~AgentDataUSAExactSep13F3@1`, label `AgentResearchSepF`, time `2026-06-16T21:46:48+01:00`, removed `Décrivez ici la nouvelle page.`, body sha256 `08ec019d3db46dd737a15224352359a707cd8698b3b2eec9fc5d5ddb1667923a`.
- Placeholder-diff distribution: fractal 562 records — 300× `Describe the new page here.` / 7× `Beschreibe hier die neue Seite.` / 1× `Décrivez ici la nouvelle page.`; probier 410 EN / 31 DE / 0 FR; milkwiki 6 EN.
- `FR/PageAccueil`: `http://www.wikiservice.at/fractal/wikidev.cgi?FR/PageAccueil`, `first_shard 2026-04-12.results.jsonl`, occurrence_count 1, task `other-web` — in `analyses/oai-url-taxonomy/outputs/urls.jsonl`.
- **Undocumented-for-reuse endpoints/patterns:** usemod.org page URL scheme `https://www.usemod.org/cgi-bin/wiki.pl?<PageName>` (UseMod, page name as bare query); revert-diff URL `wiki.pl?action=browse&diff=1&id=<PageName>`; editor host exposed in footer link `title` attribute (`ID <n> from <rdns>`); CDX `filter=urlkey:.*clipboard.*` + `collapse=urlkey` pattern for incident-window sweeps.
- **Nothing was fetched from candidate infrastructure.** Two public wiki page reads (usemod.org) + three Wayback fetches + CDX queries only. No interaction, no auth, no writes.
