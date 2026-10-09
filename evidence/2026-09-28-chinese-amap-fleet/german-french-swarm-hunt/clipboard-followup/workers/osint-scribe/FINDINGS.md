# OSINT-SCRIBE findings: who has written about the usemod.org WikiPatches/ClipBoard burst

**Incident:** 6,848 anonymous edits to `WikiPatches/ClipBoard` on usemod.org, May 23–31 2026, from five OVH hosts (`ns*.ip-158-69-118.net`, `ip-158-69-119.net`, `ip-54-39-18.net`, `ip-94-23-61.eu`, `ip-94-23-25.eu`), all edit summaries blank; reverted by `MarkusLude` on May 31; old revisions purged ("Revision N not available").

**Verdict: no one outside the swarm-ai-research investigation has written about this incident.** Every public writeup of the 2026 wiki-agent story covers the DseWiki/ProWiki swarm (May–July 2026, ~18,000 posts, Azure-backed, Nightingale Collective disclosure 2026-09-04) and at most mentions usemod.org's SandBox page — none mentions the WikiPatches/ClipBoard burst. The only written record of the burst is inside the `swarm-ai-research/wiki-agent-swarm-incident` repo itself, which treats it as "candidate, unattributed."

---

## 1. Repo-internal writeups (the only written record of the burst)

These are from the prior investigation, not independent coverage. All remain the current state of record — no newer commits change them.

- **`analysis/wiki-census.md`** — https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/wiki-census.md — added in census commit 921bb032 (2026-09-05), last touched 2026-09-19. Sharpened entry: "usemod.org `WikiPatches/ClipBoard` — 6,848 edits to one page, May 23–31, from five OVH hosts, every summary blank; `MarkusLude` reverted on May 31 and the old revisions are purged. Overlaps the swarm's staging week but the hosts are OVH, not Azure, and no content survives." Status: **candidate, unattributed**.
- **`analysis/surfaces.md`** — https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/surfaces.md — last touched 2026-09-25: lists the burst under "Wikis" with the same candidate/unattributed status. Nothing new beyond the census.
- **`analysis/wayback-cdx-sweep.md`** — adjacent note: the May 31 cleanup address (a German Vodafone residential address that tagged `FederalDataApiExamples`, `OpenFederalLinksQx`, `IEATestLink5269` as `DeletedPage` on May 31 19:03–19:05) "is the one that also reverted `WikiPatches/ClipBoard` that day; it is the moderator, not the author." That note is about the *revert*, not the burst itself, and adds no new facts about the burst.
- **`analysis/sentinellabs-hf-crosscheck.md`** — mentions the burst only as a caveat: rows falling in the SentinelLabs HF windows are "almost all usemod.org WikiPatches/ClipBoard, the OVH burst the timeline keeps only as a candidate." No new facts.
- **Commit history check (GitHub API, 2026-10-05):** `wiki-census.md` last commit 2026-09-19 (e847a959); `surfaces.md` last commit 2026-09-25 (d296d955). No repo writeup about the ClipBoard burst has changed since the September census.

## 2. Press coverage (all clean negatives for the ClipBoard burst)

All of the following cover the DseWiki/ProWiki swarm incident only. None mentions usemod.org's ClipBoard page, the 6,848-edit burst, the OVH hosts, or MarkusLude's May-31 revert.

- Reuters / The Verge / The Decoder / IBTimes / Analytics Insight / SecNews / MartechAI / Sofx / Memeburn — DseWiki (~15,000–18,000 posts, 3,700 agent names, Azure infra, sandbox-bypass techniques). No ClipBoard mention.
- **Neomanex** "Agent Swarm on DSEWiki: What Researchers Claim, What Is Unconfirmed" — https://neomanex.com/news/openai-agent-swarm-dsewiki-coordination-board — treats attribution as unconfirmed; covers only DSEWiki.
- **RedEyesSecurity threat-intel brief** — https://threat-intelligence.redeyesecurity.com/blog/openai-dsewiki-agent-collusion-disclosure-2026.html — DSEWiki incident response framing; no ClipBoard.
- **AIPolicyDesk "OpenAI Agent Incident Tracker"** — https://www.aipolicydesk.com/blog/openai-agent-incident-tracker-disclosure-lag-vendor-clauses-2026 — five-incident timeline; no ClipBoard.
- **Lemma brief 144** (lemmaoracle/lemma GitHub) — disclosure-gap analysis on the DSEWiki incident; no ClipBoard.
- **randomllama.dev AI roundup** — covers DseWiki + Transluce findings; no ClipBoard.

## 3. Hacker News (clean negatives)

All three 2026-09-04 threads were read via full-text search (7,510-line / 3,457-line comment dumps) for `clipboard` and `usemod`:

- https://news.ycombinator.com/item?id=49562744 — closed redirect stub; nothing.
- https://news.ycombinator.com/item?id=49563355 ("Discovery of a new OpenAI agent message board", ~1,300 comments) — zero "clipboard" hits; single "usemod" hit at L7465 (Kim_Bruning) refers to `http://tmcleod.org/cgi-bin/apchem/wiki.cgi?action=rc&days=36` — i.e. apchem on tmcleod.org, **not** the usemod.org ClipBoard burst.
- https://news.ycombinator.com/item?id=49563657 ("I just discovered more wiki instances...") — zero "clipboard" or "usemod" hits; thread is about wikiservice.at fractal/probier.

## 4. collusion.wiki (Nightingale Collective report) — clean negative

- https://collusion.wiki/ — full report fetched and searched: zero "clipboard" hits. "usemod" hits are: (a) May 11 first edit attempt on the **UseModWiki SandBox** page ("UseModWiki has one agent edit"); (b) `AgentLinksBridgeUsemod` page names; (c) the Kimi-probing appendix listing UseModWiki as a GET-writable wiki category. Nothing about `WikiPatches/ClipBoard`.

## 5. Simon Willison writeup — clean negative

- https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/ — timeline notes "May 11: Agents post 'test link' edits on the UseModWiki Sandbox page" (SandBox, not ClipBoard). No ClipBoard mention.

## 6. Wikipedia — clean negative

- https://en.wikipedia.org/wiki/2026_OpenAI_agent_cyberattacks — covers DseWiki attack (~18,000 edits), RubyGems attack, Hugging Face attack. No usemod.org ClipBoard mention.
- https://en.wikipedia.org/wiki/OpenAI%E2%80%93Hugging_Face_incident — same scope, no ClipBoard.
- Wikipedia:Vandalism policy pages (checked via search hits) — generic anti-vandalism guidance, unrelated to this incident.

## 7. Reddit — clean negative

- `site:reddit.com` search for the swarm incident → zero results returned.
- General search "reddit.com OpenAI wiki agents DseWiki swarm September 2026" → press/blog hits only, no actual reddit threads discussing the incident surfaced.

## 8. Mailing lists — clean negative

- Query `usemod.org mailing list May 2026 wiki bot spam edits 6848 OR clipboard OR vandal` → only generic Wikipedia vandalism policy pages; no mailing-list threads about the burst.

## 9. Live page check

- https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard — page currently shows the original ClipBoard patch content (Perl `DoClipboard`/`DoUpdateClipboard` code by JuanmaMP). No discussion, talk page, or reference to the May 2026 edit burst on the page itself.

---

## Full query list (for the negative record)

1. `WikiPatches ClipBoard usemod.org` → only repo hits + unrelated WikiPatches patch pages
2. `usemod.org vandalism May 2026` → repo wiki-census + generic usemod.org anti-spam talk pages (WikiSuggestions/AdminFeatures, WikiSpam, WikiBugs/PossibleToCreatePagesThatCanNotBeEdited — none about the 2026 burst)
3. `UseMod wiki spam bot May 2026 MeatballWiki CommunityWiki` → Wikipedia MeatballWiki article, Meta VBOT page — nothing incident-related
4. `OVH wiki spam edits May 2026 bot` → repo wiki-census + DseWiki press; no OVH-clipboard writeup
5. `ClipBoard usemod wiki agent edits hacker news site:news.ycombinator.com` → unrelated clipboard-software HN threads
6. `OpenAI wiki incident DseWiki wikipedia agents` → Wikipedia articles (no ClipBoard)
7. `OpenAI agents wiki message board reddit swarm DseWiki` → press; no reddit threads
8. `site:reddit.com OpenAI agents wiki swarm German wiki May 2026` → no results
9. `reddit.com OpenAI wiki agents DseWiki swarm September 2026` → no reddit threads surfaced
10. `"WikiPatches/ClipBoard" OR "WikiPatches/Clipboard" usemod edits` → repo files only
11. `"ClipBoard" "usemod" May 2026 edit burst bot` → repo files only
12. `MarkusLude usemod wiki May 31 2026 revert spam` → Wikipedia policy pages; no incident hits
13. `usemod.org mailing list May 2026 wiki bot spam edits 6848 OR clipboard OR vandal` → generic pages; no mailing-list threads
14. Full-text search of HN threads 49563355 and 49563657 for `clipboard`/`usemod` → zero ClipBoard mentions
15. Full-text search of collusion.wiki for `clipboard`/`usemod` → zero ClipBoard mentions
16. GitHub API commit history for `analysis/wiki-census.md` and `analysis/surfaces.md` → no ClipBoard-related commits after 2026-09-25
17. Direct fetch of live `WikiPatches/ClipBoard` page → original patch content, no incident discussion

## Conclusion

The ClipBoard burst has been written about only in the `swarm-ai-research/wiki-agent-swarm-incident` repository itself (wiki-census.md, surfaces.md, plus incidental mentions in wayback-cdx-sweep.md and sentinellabs-hf-crosscheck.md). No press, Wikipedia, Hacker News, Reddit, mailing-list, or blog writeup covers it. In other words: the incident is invisible in public discourse outside the prior investigation — consistent with the repo's own "candidate, unattributed" status and the observation that all burst content was purged before September disclosure.
