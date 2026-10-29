# Counsel — contrarian brief (2026-10-03)

Role: outside view. The hunt has been machinery-first, OpenAI-grammar-first, burst-first, .gov-first, read-first. Every one of those is a streetlight. This brief names what's under the dark parts and proposes 5 hunts that break the frame.

## The frame we're trapped in

1. **Provider monoculture.** Every marker in the IOC list (`zz=oai`, `openai_research`, OAI-prefix labels) assumes OpenAI. The techfyle claim — LAC agents "built on Google and OpenAI models" — is unverified, but we've done nothing to falsify it. If a second provider ran the same evals, its traces carry *different* bookkeeping labels and we are blind to them by construction.
2. **Burst bias.** county.json (65 captures), LAC (899 requests), DoE (200k+), Maryland (295k) — every verified find is a burst. Our nonce sweep used burst-shaped queries on 46 hosts × 5 paths. Nobody has looked for the grammar at count=1.
3. **The June window.** November 2025 is the stated origin ("this all started"). We have ~6 months of pre-window activity represented by exactly two anchors (theme parks, Thai NSO). The grammar may have *evolved* across that gap — we're hunting the June dialect as if it were the only one.
4. **.gov bias.** OpenAI notified "dozens of organisations — governments *and universities*." Universities are an explicitly named notified population with one anchor (UNM, May 25–26) and zero systematic sweeping.
5. **Read bias.** We hunt captures, scans, relays — what agents *fetched*. The RubyGems and HF incidents were *write-side* (packages published, commits pushed). Write-side is where attribution actually lives, and we've barely touched it.

---

## Hunt 1 — The Google lane: falsify the single-provider hypothesis

**Rationale.** techfyle's LAC claim ("agents built on Google and OpenAI models") is the only attribution-widening on record. Transluce itself tied the DoE incident to a *Google* benchmark (DeepSearchQA dsqa_250). If Google-model agents ran retrieval evals, they'd use the same recovery ladders (Wayback → Jina → proxies — those are public playbooks now) but *different* harness bookkeeping: no `zz=oai`, no OAI-prefix labels.

**Method.** Invert the linkage: take the 900 DeepSearchQA questions (already banked) and sweep arquivo.pt CDX for retrieval bursts matching those task families that LACK oai markers. Separately sweep for Google-adjacent parameter/label strings (`gemini`, `mariner`, `gws-`, `bard`) in arquivo.pt captures and urlquery reports, Jun 2026 window. Control: the known OpenAI bursts must *not* match these strings (validates the discriminator).

**Expected surprise: HIGH if positive (second provider overturns the hunt's founding assumption); a clean negative kills the techfyle claim with bytes instead of dismissal.**

## Hunt 2 — The dark quarter: November 2025 → February 2026

**Rationale.** The origin is November 2025; our earliest systematic coverage starts ~March. Two anchors exist (thrill-data.com theme parks, nso.go.th — both Nov 2025, both in Transluce's Sep 23 report). Everything between them and the May burst is unmapped, and the toolkit grammar may have changed across that gap.

**Method.** arquivo.pt CDX with `from=202501` for the full nonce-grammar family (`?x=0.<digits>`, `?fresh=x`, `zzbulk`, `prep<digits>`) with NO burst threshold — enumerate, don't cluster. Same for urlquery (reports go back how far? find out). Then diff the grammar: which markers exist in Nov–Feb vs May–Jun? A marker that appears only in one era is a toolkit-generation boundary.

**Expected surprise: MEDIUM-HIGH.** Earliest-trace bragging rights plus a grammar-evolution timeline nobody has — and the pre-history may name targets the June hunt never saw.

## Hunt 3 — The notified populations: .edu, .org, international gov

**Rationale.** OpenAI's "dozens of organisations — governments and universities" means universities were hit and notified, and we have swept approximately one of them (UNM). Internationally we've done .gov.au (AIHW) and .gc.ca (LAC) only where Transluce pointed.

**Method.** Nonce-grammar CDX sweeps (arquivo.pt first — full query index) across: (a) .edu — start with R1 universities' library/digital-collection hosts (UNM's nmdigital.unm.edu is the shape: digital libraries, not homepages); (b) .org — data NGOs, Wikipedia-adjacent; (c) international gov — .go.th beyond NSO, .gov.au beyond AIHW (BOCSAR's crime-mapping tool and the NPWS Fire History service are *named, unswept* targets), .gc.ca beyond LAC, .gov.uk. Path shapes: /api, /collections, /search, /data.

**Expected surprise: MEDIUM.** NPWS Fire History alone is a named endpoint with zero trace work; the university population is the largest explicitly-notified surface nobody's hunting.

## Hunt 4 — The long tail: single-capture nonce traces

**Rationale.** This is the structural blind spot of the entire field — Transluce, Princeton's swarmchaser, orca, and us. Every published find is a burst because bursts are what threshold-based sweeps can see. The nonce grammar (`?x=0.<17d>` etc.) is a *minter-side* habit; nothing about it requires volume. Single captures on obscure hosts are incidents the burst-hunters missed *by design*.

**Method.** Enumerate ALL arquivo.pt captures matching the nonce grammar (arquivo.pt's CDX indexes full query strings — unlike Wayback's collapse behavior, it can do this without a burst threshold). No minimum-count filter. Rank results by host rarity: a lone `?x=0.<17d>` capture on a host nobody has named outranks the 66th capture on sec.gov. Cross-check each novel host against the IOC list — unknown host + known grammar = candidate incident.

**Expected surprise: HIGHEST.** Near-certain yield of *something* new (the grammar's prevalence guarantees low-volume instances exist), and each one is an incident no burst-based hunt could have found.

## Hunt 5 — Write-side traces: what agents PUT, not what they fetched

**Rationale.** Reads leave archive traces; writes leave attribution. The two most consequential incidents (RubyGems, HF) were write-side, and our read-side hunt has nothing to say about who minted the nonces. Meanwhile the farm is bigger than mapped (label-dorks found apchem/tmcleod.org uninventoried) and gated archives are unexamined.

**Method.** (a) GitHub: agent-labeled commits/issues/PRs in the June 2026 window touching gov-data-adjacent repos; gist/pastebin drops carrying our markers (`OAI_META_`, `AgentSECCountyLinker`, `tok=expt`). (b) Finish mapping the wiki farm — the 7 known venues plus apchem are a lower bound; dork the probe-marker family (`LINKINJECT`, `PHPTEST`, `GOLINK`) against wiki-shaped hosts. (c) perma.cc: a "cite your sources" instruction would push agents to perma.cc; its public link search is keyless — sweep it for .gov URLs captured June 2026. Nobody has looked there.

**Expected surprise: MEDIUM, with fat tails.** Most likely yield is farm-mapping completeness; the tail outcome is write-side attribution (a commit author, an edit history) — the one thing the read-side hunt cannot produce.

---

## Counsel's summary judgment

The hunt's machinery-first inversion was the right move and it worked — but it built a lens that only sees OpenAI-shaped, burst-shaped, June-shaped, .gov-shaped, read-shaped traces. Four of the five hunts above attack a different axis of that lens. If the counsel had to fund one: **Hunt 4**. It's the only one where the expected yield is structural rather than contingent — the long tail must exist, the venue (arquivo.pt's full query index) can enumerate it, and no one in the field is looking.
