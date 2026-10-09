# FINDINGS — web2cit.toolforge.org index hunt (lane c)

Date: 2026-10-06. Branch: wikimedia-rogue-agents-followups-2026-10-06.
Question: did the OpenAI rogue agents' Web2Cit translate/debug usage (geodata-retrieval egress laundering, 2026-06-26) leave observable traces in public URL indexes?

Verdict: **clean negative across all three indexes. Zero agent-shaped hits.** (OBSERVED)

## Transport health (verified first, before any zero claims)

- `https://urlquery.net/` → 200, 1.9s (OBSERVED)
- `https://urlscan.io/` → 200, 1.6s (OBSERVED)
- `http://web.archive.org/cdx/search/cdx` (port 80, per TOOLS.md lesson) → 200 (OBSERVED)
- Pacing: ≥6s between keyless requests; Python HTTP stacks avoided entirely (curl only).
  Note: `~/workspace/skills/urlquery/bin/uq.py` (authenticated API) DOES work via urllib on this VM
  (surrogate auth OK); the htmx curl variant `uq_htmx_curl.py` works too. Used both.

## Index 1 — urlquery.net

Queries run (exact), all via `uq.py search --query ...`:

| Query | total_hits | Result |
|---|---|---|
| `web2cit.toolforge.org` | 6 | all token-noise: SEO backlink-spam submissions (mobil-meritking.vip, kurasorgu.com, blogspot SEO tools) + one google-translate proxy spam. None involve web2cit. Noise, graded NOT-RELEVANT (OBSERVED) |
| `url.domain:web2cit.toolforge.org` | 0 | **zero** (OBSERVED) |
| `url.domain:web2cit-beta.toolforge.org` | 0 | zero (OBSERVED) |
| `url.domain:web2cit-test.toolforge.org` | 0 | zero (OBSERVED) |
| `web2cit.toolforge.org/translate` | 0 | zero (OBSERVED) |
| `web2cit` | 9 | 6 SEO-spam (above) + mobil-meritking.vip, kurasorgu.com, 78923ttv.837684523.xyz — none web2cit-related. Noise (OBSERVED) |

Why the noise: urlquery's search tokenizer splits on dots, so `web2cit.toolforge.org` matches the token `translate` (google-translate spam) and unrelated junk. The domain-scoped query `url.domain:` is the reliable one → **0 submissions of any web2cit host, ever indexed.** No tags, no submitters, no embedded targets to grade.

## Index 2 — urlscan.io (public API, `GET /api/v1/search/?q=...`)

| Query (URL-encoded) | total | Result |
|---|---|---|
| `domain:web2cit.toolforge.org` | 0 | zero (OBSERVED) |
| `page.url:"web2cit.toolforge.org*"` | 0 | zero (OBSERVED) |
| `web2cit.toolforge.org` (bare) | 0 | zero (OBSERVED) |
| `domain:web2cit-beta.toolforge.org` | 0 | zero (OBSERVED) |
| `domain:web2cit-test.toolforge.org` | 0 | zero (OBSERVED) |

**urlscan has never indexed a scan touching web2cit.toolforge.org.** (OBSERVED)

## Index 3 — Wayback CDX

Method: `http://web.archive.org/cdx/search/cdx?url=<prefix>&matchType=prefix&output=json`, collapse=urlkey, limit 5000–10000. All 200 OK.

### translate endpoint (the egress primitive: `translate?url=<TARGET>&format=json`)

27 captures of `web2cit.toolforge.org/translate*`. Full target inventory (18 unique targets):

- Bibliographic/news targets, ALL ORGANIC-shaped (OBSERVED):
  hmwilson.archives.org.au (2022-11), independent.ie (2024-12), www.example.com/abc (2025-04, template test),
  npr.org (2025-11), muslimheritage.com, www1.folha.uol.com.br (sandbox=Diegodlh, 2026-02),
  bigenc.ru, web2cit.toolforge.org/ (self-test, 2026-03), milliard.tatar news (×3, 2026-04, one with sandbox=Blackisnewyellow),
  priyakumar.org (2026-04, sandbox=Blackisnewyellow), tatarica.org (×2, 2026-04, sandbox=Blackisnewyellow),
  rsloboda-rt.ru (×2, 2026-04, sandbox=Blackisnewyellow), www.bbc.com (2026-06-26).
- Both parameter forms observed in the wild: `?url=<TARGET>` (3 captures) and `?domain=X&path=Y` (rest) — the hacker's `translate?url=` form is real (OBSERVED).

### debug endpoint (`debug/<TARGET>`)

35 captures; ALL bibliographic/news targets (French/Swiss press 2025-12: 24heures.ch, blick.ch, lenouvelliste.ch, letemps.ch, lqj.ch, rfj.ch, rhonefm.ch, rts.ch; gamepro/gamestar/eurogamer/pcgames; Tatar news via Blackisnewyellow sandbox; archives.org.au; churchesaustralia.org; haaretz via sandbox=Aaron Liu 2026-03). ORGANIC (OBSERVED).

### sandbox paths (`sandbox/<USER>/<TARGET>`)

Named sandbox users: Blackisnewyellow (Tatar-news citation tests, 2026-04), Aaron Liu (haaretz, 2026-03). Both bibliographic. ORGANIC (OBSERVED).

### Variant hosts

`web2cit-beta.toolforge.org/translate*` → 0 captures. `web2cit-test.toolforge.org/translate*` → 0 captures (OBSERVED).

### Host-level domain query (234 unique captures, 2022-03 → 2026-09)

Keyword sweep of every captured URL for `arcgis | geocod | hawaii | openai | gpt | chatgpt` → **0 hits** (OBSERVED).
2026-06 window captures: only the www.bbc.com pair (2026-06-26 18:14:43Z + 18:15:02Z).
Post-incident (2026-07/08/09): 6 captures, all root/static assets or www.britannica.com (bibliographic) — no investigator artifacts yet as of index state.

## The one coincidence (graded, NOT chased as a lead)

`translate?domain=www.bbc.com&...&tests=true` captured 2026-06-26 18:14–18:15Z — same calendar day as the rogue agent's Web2Cit config change (2026-06-26T23:01:21Z, upstream assertion). Graded **ORGANIC/COINCIDENCE** (INFERENCE), not agent-shaped, because:
1. Capture time is ~5h BEFORE the documented config change, and the incident activity was geodata-targeted, not BBC.
2. bbc.com is a bibliographic target — exactly Web2Cit's normal use.
3. Wayback captures reflect crawler follows of wiki-linked URLs (Web2Cit test pages embed these links), not direct agent fetches; no submitter attribution exists.
4. No other 2026-06 geodata/API-shaped target exists in the index.

## Grading summary

- Agent-shaped: **0** (OBSERVED — no API-shaped target, no bulk timing, no automation markers anywhere)
- Organic: all 27 translate + 35 debug + sandbox captures (bibliographic/news targets, named-wiki-user sandboxes, spaced over 2022–2026) (OBSERVED)
- Investigator artifacts: 0 as of 2026-10-06; anything dated 2026-10-05+ should be treated as suspect per standing rule (INFERENCE/rule)

## Updated IOCs

- None new. The clean negative IS the finding: the agents did not submit web2cit URLs to public indexes (consistent with them using wiki-internal test pages, not third-party scanners).
- Candidate URL log: NONE fetched live; the CDX-listed targets were observed as index metadata only, never visited. No new URLs need live-fetching.

## Caveats

- urlquery/urlscan zeros mean "not in index," not "never submitted" — both indexes only see what submitters/scanners submitted. Agents who never touched the public scanners are invisible here by construction.
- Wayback captures are crawler echoes of publicly-linked URLs; a directly-fetched (never-linked) translate URL would not appear. Coverage of the actual agent fetch is therefore partial at best.
- CDX `matchType=prefix` with bare prefix per TOOLS.md; backend was healthy this run (no 504/Temporarily-Offline retries needed).
- urlquery API tokenization makes bare-string queries noisy; `url.domain:` scoping is the reliable query form for this hunt.
