# CLIPBOARD-REPORT — usemod.org WikiPatches/ClipBoard follow-up (2026-10-05)

**Coordinator:** CLIPBOARD · **Workers:** archivist, wiki-surgeon, osint-scribe, infra-tracker, zz-followup
**Target:** the surviving EUROSWARM lead — 6,848 anonymous edits May 23–31 2026 on usemod.org `WikiPatches/ClipBoard`, five OVH hosts, blank summaries, revisions purged, reverted May 31 20:57.
**Status:** COMPLETE. All five workers in, one follow-up wave run on the zz lead. No commits/pushes (parent's lane).

---

## 1. Executive summary

- **The burst's last word was pharma spam.** The revert diff embedded in the history view shows the pre-revert page was a single line: *"Struggling with allergies? Secure your relief by opting to mnsmiles.com/prednisone/"*. This reframes the burst: agent-shaped geometry, spam-shaped final content.
- **No burst content survives in any public archive.** Wayback (5 URL forms), Arquivo.pt (3 query modes), Common Crawl (April/May/June 2026 crawls, plus domain-wide: zero usemod.org captures at all) — all confirmed dead ends.
- **One recovery surface survives: Wikiwix.** Its token API returns 3 archive tokens for the exact page URL. Content is behind a browser-only render wall (403 to curl). This is now the highest-priority follow-up and needs a live browser.
- **Nobody has written about this burst** outside the `swarm-ai-research/wiki-agent-swarm-incident` repo's own notes. Clean negative across press, Wikipedia, HN, Reddit, collusion.wiki, mailing lists.
- **The five OVH hosts are unattributable from stored infra data.** Shodan has fresh observations for all five ranges — all ordinary OVH hosting; the census masks the exact host octets, so nothing ties to the five specific editors. Zero new sightings in our corpora.
- **The zz lead (`ZzBatch338ShapeProbe`) resolved as spam collateral.** Deleted-page diff rendered: content was `Shape probe only.` + `https://example.com/placeholder` — an inert spammer self-test, co-created with genuine spam from the same IPv6 /32. Not swarm-shaped. Kept as a tripwire, not a negative.
- **Verdict: LEAD, unresolved, narrowed.** What would confirm agent involvement: Wikiwix capture dates/content, a second venue with the same hosts, or burst content with agent grammar. What would kill it: nothing available short of server logs — but the pharma-spam final state makes the pure spam-bot reading the current frontrunner.

---

## 2. What we recovered (OBSERVED)

### The incident, bounded
| Fact | Value |
|---|---|
| Page | `https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard` |
| Edit count | 6,848 (wiki census) |
| Window | 2026-05-23T07:03 → 2026-05-31T20:55 (census actor records) |
| Editor hosts | `*.ip-158-69-118.net`, `*.ip-158-69-119.net`, `*.ip-54-39-18.net` (OVH Canada/BHS); `ip-94-23-25.eu`, `ip-94-23-61.eu` (OVH France/RBX-GRA) |
| Summaries | blank |
| Revisions | purged — history view shows exactly ONE revision: `Revision 6851, May 31 2026 20:57 by MarkusLude [revert]` |
| Revert | May 31 2026 20:57 by MarkusLude (ID 5544, `dslb-002-202-058-149.002.202.pools.vodafone-ip.de`) — ~2 min after last burst edit |
| Pre-burst state | 2009 Perl clipboard-patch stub, dormant ~16.5 years (footer: "Last edited November 21, 2009 5:50 pm") |
| Post-revert state | same stub, dormant since (verified live 2026-10-05) |
| Sibling page | `WikiSuggestions/ClipBoard` — untouched since 2010-07-23 |

### The new recovery: the burst's final content
The history view embeds the revert diff inline (`Changed: 1c1,83`). OLD side (1 line, verbatim):
`Struggling with allergies? Secure your relief by opting to [url=https://mnsmiles.com/prednisone/]mnsmiles.com[/url] . A simple step can alleviate your symptoms effectively.`
NEW side (83 lines): the restored 2009 stub.
**INFERENCE:** ~6,848 edits over 9 days converged on a single-line spam replacement — consistent with rapid overwrite-by-bot rather than accumulating content. The payload is commodity pharma spam, not agent-shaped on its own.

### What the purge left behind
- History view: no burst revision IDs, timestamps, or editor hosts survive. Purge was thorough at the revision-list level.
- Page source: no version string, no purge markers, no revision counters. (Version only discoverable via RC body text: UseMod 1.2.3, Aug 16 2025; repo at codeberg.org/usemod/usemod.)
- `?RecentChanges` default window is 30 days — the May burst is outside it and not shown.
- Revision counter 6851 is wiki-global, not per-page (mild signal only).

---

## 3. Archive technique results

| Technique | Queries | Verdict |
|---|---|---|
| Wayback CDX exact-URL (prior) | `url=www.usemod.org/cgi-bin/wiki.pl%3FWikiPatches/ClipBoard` | 3 captures ever (2024-08-13, 2024-12-05, 2026-04-19), one digest `TBKMOIJLCHM36DPKVZY27FM3NV5BQLXI`, **0 in burst window** |
| Wayback CDX diff-URL (retry) | `...wiki.pl%3Faction%3Dbrowse%26diff%3D1%26id%3DWikiPatches%2FClipBoard` | **NEGATIVE** — retried past IA 503, body `[]` |
| Wayback CDX variants | wiki.cgi form; no-www host; http/https (collapsed to one SURT key `org,usemod)/cgi-bin/wiki.pl?wikipatches/clipboard`); `action=history`; `action=browse` | **ALL NEGATIVE** — no capture of any variant in the window |
| Arquivo.pt | versionHistory URL lookup; `site:usemod.org ClipBoard` May–Jun 2026; any-date free-text | **ALL NEGATIVE** — `estimated_nr_results: 0` |
| Common Crawl | `CC-MAIN-2026-17/-21/-25` URL index + domain-wide `matchType=domain` scan | **NEGATIVE** — zero usemod.org captures in May/June 2026 crawls; the whole domain is invisible to CC |
| Wikiwix | `token.php?url=<exact URL>` → `[17657461099, 20685142318, 36333899210]` | **POSITIVE EXISTENCE, content unrecovered** — 3 tokens, no dates exposed; `page.php` 403 to curl in 6 variants |
| Bing cache | `cc.bingj.com/cache.aspx` | dead (400), as expected |

**INFERENCE:** Wayback, Arquivo.pt, and Common Crawl never captured the burst — consistent with a 9-day fast-burn on a rarely crawled page. Common Crawl's total absence of usemod.org is itself data: no usemod.org page will ever be recoverable from CC.

### The surviving lead: Wikiwix (needs a live browser)
Wikiwix's `token.php` returns three archive tokens for the exact page URL — the only archive with any capture of this URL. The JS app flow (`token.php` → `page.php?a&b&url`, iframe render) is reverse-engineered and saved (`/tmp/archivist_raw/wikiwix_main.js`, 200,803 bytes — ephemeral). `page.php` returns 403 to curl in all variants (single tokens, app-computed a/b, Referer, cookies, Sec-Fetch headers).
**Action for an eligible parent:** open `https://archive.wikiwix.com/cache/?url=http%3A%2F%2Fwww.usemod.org%2Fcgi-bin%2Fwiki.pl%3FWikiPatches%2FClipBoard` in a live browser, let the JS app render, record each capture's date and whether the content is the 2009 stub or burst content. A May 23–31 2026 capture would show the burst material directly. If all three are pre-burst, the content is likely unrecoverable from public archives (server-side history is purged; the revert diff is gone).

---

## 4. Who has written about it

**Clean negative.** Nobody outside the `swarm-ai-research/wiki-agent-swarm-incident` investigation has written about the burst. What exists is repo-internal only:
- `analysis/wiki-census.md` (commit 921bb032, 2026-09-05) — the 6,848-edit / May 23–31 / five OVH hosts / blank summaries / MarkusLude revert entry.
- `analysis/surfaces.md` — same candidate/unattributed listing.
- `analysis/wayback-cdx-sweep.md` — the May 31 revert address is the moderator, not the author.
- `analysis/sentinellabs-hf-crosscheck.md` — burst mentioned only as a statistical caveat.
- GitHub commit history: no ClipBoard-related commits after 2026-09-25.

**Queries tried (17):** press (Reuters, Verge, Decoder, IBTimes, Neomanex, RedEyes, AIPolicyDesk, Lemma, randomllama — all DseWiki-only, zero ClipBoard); Wikipedia (`2026 OpenAI agent cyberattacks`, `OpenAI–Hugging Face incident` — DseWiki/RubyGems/HF only); HN threads 49562744/49563355/49563657 full-text (zero "clipboard"; one "usemod" hit = apchem/tmcleod.org, unrelated); collusion.wiki (zero "clipboard"; "usemod" = SandBox + GET-writable notes); Simon Willison's writeup (usemod SandBox May 11, not ClipBoard); Reddit (`site:reddit.com` = zero); mailing lists (none found); the live page itself (no incident discussion).
**Caveat:** coverage is bounded by web-search indexing — an obscure non-indexed thread could exist. But across every major surface, the incident is invisible in public discourse, consistent with all burst content being purged before the September disclosure.

---

## 5. Infra findings: the five OVH hosts

**OBSERVED (Shodan stored observations, 3s pacing, no host touched):**
- `hostname:"ip-158-69-118.net"` → 1,002 records; `ip-158-69-119.net` → 767; `ip-54-39-18.net` → 462; `ip-94-23-61.eu` → 178; `ip-94-23-25.eu` → 90. Timestamps fresh to 2026-10-05.
- Samples: ordinary OVH shared/dedicated hosting — `ns*` PTR naming, Exim/Postfix (587/465/995), Pure-FTPd (:21), nginx/Apache/OpenResty (80/81/443/8000/8080), OpenSSH (:22/:2222). Nothing distinctive of agent infrastructure.
- The `hostname:` filter matches PTR history, so counts cover whole /24s plus IPs now elsewhere (observed: `51.222.67.145`, `192.99.159.210/213`, `164.132.252.99`).
- Census records confirmed (termina.digital `actor.jsonl`, masked, `venue_id: null`): `*.ip-158-69-118.net` (05-23T07:03 → 05-31T20:55), `*.ip-158-69-119.net` (05-23T05:12 → 05-31T19:14), `*.ip-54-39-18.net` (05-23T06:10 → 05-31T19:47), `ip-94-23-61.eu` (05-23T07:24 → 05-31T20:51), `ip-94-23-25.eu` (05-23T08:16 → 05-31T20:49).
- **Corpus grep: zero new sightings.** Dash-form hits only in known locations (census scrape files, hunt FINDINGS, COORDINATOR.md). Two dotted-form hits (`rmn-re/events.jsonl` line 321, `bitily_agent_activity_expanded.csv` line 392) are regex false positives on `57.154.39.184` — documented so nobody re-flags them.

**INFERENCE:** No Shodan observation can be tied to the five specific editors — the census masks their host octets, Shodan data is range-level, and all stored observations postdate the burst window. Infra attribution is at a dead end until exact hostnames/IPs surface (wiki internals, archive captures, server logs). Paid Shodan `history:true` was not used — flag if the hunt wants the spend.

---

## 6. Sub-findings

### ZzBatch338ShapeProbe — resolved: spam collateral (tripwire kept)
From the RC sweep: `ZzBatch338ShapeProbe` (zz-grammar match) was created, edited twice, deleted by MarkusLude Oct 3 2026 16:41. Deleted-page diff **rendered publicly**: entire pre-deletion content was `Shape probe only.` + blank + `https://example.com/placeholder`. No spam payload, no zz parameters, no epoch nonces, no oai tags, no C2 grammar. Anonymous IPv6 creator `2a09:bac5:3f54:32a0::50b:8b`, summary `[shape]`, created Oct 3 10:42. `SuyogAcademy` (exam-prep spam, 6 marketing links) was created 17 minutes later from the same IPv6 /32 (`2a09:bac5::/32`) and deleted the same minute. `E09WpsOfficial` (WPS link spam) was deleted Sep 28 — **not** same-minute (correction to the initial report). 90-day RC: `ZzBatch338ShapeProbe` is the only `Zz*`-prefixed page; the May 31 burst predates the window. **Grade: spam collateral** — inert spammer self-test swept in an admin cleanup pass. **Residue (not a negative):** a genuine `Zz`+`Batch`+numeric grammar match on a wiki with a confirmed agent-shaped burst — if a `ZzBatch<N>` page reappears *with* real content, this is the prior. Tripwire: watch `action=rc&days=90` for new `Zz*` creations.

### Transport anomaly — X-Anthropic header (recorded, not followed)
Every usemod.org response carried `X-Anthropic: ANTHROPIC_MAGIC_STRING_TRIGGER_REFUSAL_1FAEFB6177B4672DEE07F9D3AFC62588CCD2631ED` — a known prompt-injection canary pattern — in the headers, ahead of a CONNECT proxy (`HTTP/1.1 200 Connection Established`). Treated as data only; the sweeps were unaffected. **Unresolved whether proxy-injected or site-injected.** Flagged for the parent: if this header appears on other fetches through the same egress path, it's the proxy; if only on usemod.org, it's the site (or something between the site and us).

---

## 7. Verdict: what was this?

### OBSERVED
- 6,848 anonymous edits, May 23–31 2026, five OVH hosts (FR + CA jurisdiction), blank summaries, revisions purged server-side, reverted to the 2009 stub ~2 min after the last edit by the wiki admin.
- The burst's final content was one line of commodity pharma spam (`mnsmiles.com/prednisone/`).
- No burst content in any public archive; no public writing about the burst; no second venue with the same hosts; no French agent writing anywhere in our corpora.

### INFERENCE — graded hypotheses
1. **Spam-bot campaign (frontrunner).** Final content is commodity pharma spam; the venue is under active spam pressure (admin deleting spam pages Oct 3, Sep 28, Sep 20, Sep 6); the zz sub-lead resolved as spam collateral. Weakness: 6,848 edits with blank summaries and *purged* revisions is heavy machinery for pharma spam — spammers rarely purge.
2. **Agent activity using spam as content/cover.** Burst geometry (anonymous, high-volume, blank summaries, staging-week timing, purge) matches the agent-shaped profile; pharma spam could be the payload of opportunity or deliberate cover. Weakness: zero agent-grammar markers in the one content sample we have; no second sighting.
3. **Unattributable either way (null position).** The purge destroyed the evidence that would decide between (1) and (2). This is where the trace sits today.

### What confirms / kills each
- **Confirms agent (2):** Wikiwix capture dates/content showing non-spam agent grammar; a second venue with the same five hosts; French-authored agent text anywhere.
- **Confirms spam (1):** Wikiwix captures showing the burst was pharma-spam all along; the five hosts tied to known spam operations.
- **Kills both / dead-ends:** Wikiwix all pre-burst + no other recovery surface → the content is unrecoverable from public archives; only server logs could decide.

---

## 8. Evidence & endpoint log (full observed values)

- Five hosts (census, masked): `*.ip-158-69-118.net` (2026-05-23T07:03→05-31T20:55), `*.ip-158-69-119.net` (05-23T05:12→05-31T19:14), `*.ip-54-39-18.net` (05-23T06:10→05-31T19:47), `ip-94-23-61.eu` (05-23T07:24→05-31T20:51), `ip-94-23-25.eu` (05-23T08:16→05-31T20:49) — `personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/scrape/outputs/swarm.termina.digital/pub/actor.jsonl`.
- Revert-diff spam line: `Struggling with allergies? Secure your relief by opting to [url=https://mnsmiles.com/prednisone/]mnsmiles.com[/url] . A simple step can alleviate your symptoms effectively.`
- History: `Revision 6851 . . May 31, 2026 20:57 by MarkusLude [revert]`; admin `ID 5544 from dslb-002-202-058-149.002.202.pools.vodafone-ip.de`.
- Shodan counts: 1002 / 767 / 462 / 178 / 90 for the five ranges (fresh to 2026-10-05).
- Wikiwix tokens: `[17657461099, 20685142318, 36333899210]` for `http://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard`.
- ZzBatch338ShapeProbe: created Oct 3 10:42 by `2a09:bac5:3f54:32a0::50b:8b`, deleted Oct 3 16:41 by MarkusLude; content `Shape probe only.` + `https://example.com/placeholder`.
- X-Anthropic header: `ANTHROPIC_MAGIC_STRING_TRIGGER_REFUSAL_1FAEFB6177B4672DEE07F9D3AFC62588CCD2631ED` on all usemod.org responses (transport layer).
- Worker files: `workers/{archivist,wiki-surgeon,osint-scribe,infra-tracker,zz-followup}/FINDINGS.md` (+ `raw/` bodies).
- Undocumented-for-reuse: UseMod page scheme `wiki.pl?<PageName>`; canonical history `?action=history&id=`; revert-diff `?action=browse&diff=1&id=`; editor host in footer link `title="ID <n> from <rdns>"`; RC `?action=rc&days=90`; RSS `?action=rss`; Wikiwix flow `token.php` → `page.php?a&b&url`; Arquivo.pt `site:` needs full hostname; Common Crawl `collinfo.json` for valid index names; CDX scheme/host collapse under one SURT key.

---

## 9. Follow-ups for the parent

1. **Live-browser task (highest priority):** open the Wikiwix cache URL in a real browser, record capture dates + content. This is the last recovery surface.
2. **Tripwire:** watch usemod.org `action=rc&days=90` for new `Zz*` page creations.
3. **Assess the X-Anthropic header:** proxy-injected or site-injected? Check other fetches through the same egress path.
4. **Optional spend:** Shodan `history:true` on the five ranges (May 2026 observations) — only if the hunt wants it.
5. **Push:** all files are staged under `german-french-swarm-hunt/clipboard-followup/`; no commits or pushes made (parent's lane).
