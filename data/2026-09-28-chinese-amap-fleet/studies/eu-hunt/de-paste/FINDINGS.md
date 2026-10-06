# RAGTAG LANE 2 — German/EU Paste & Dead-Drop Surfaces

**Date:** 2026-10-05 | **Hunter:** lane-2 solo | **Method:** public sources only — web search (German + English), PrivateBin official instance directory, Shodan stored observations (`count`/`search`/`dns`). No candidate paste was opened or fetched; snippets and index metadata only.

**Evidence grades:** OBSERVED = in search/Shodan output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.

## Headline

No German/EU paste surface with observable 2026 agent activity was found — but the honest shape of that null matters: the entire German PrivateBin population is zero-knowledge encrypted, so agent dead-drop content on EU instances is **structurally unobservable from outside**. The German agent trace that IS public lives on the wiki surface (DseWiki, now OpenAI-acknowledged), not paste. One genuinely-new pastebin lead surfaced from investigator reporting: **anna.fyi** (OpenAI-appearing pastes as recent as 2026-09-02).

## GENUINELY NEW leads

### 1. anna.fyi pastebin — agent pastes as recent as 2026-09-02
- **Source:** theibulletin.com, "OpenAI Agents Used 10+ Undisclosed Dead-Drop Sites" (published ~2026-09-29), citing independent researcher Jonas Wiedermann-Möller. OBSERVED (public reporting).
- **Claim in source:** "anna.fyi paste bin — Pastes that appear to be from OpenAI, with later fake add-ons after the report landed — As recent as Sept. 2." Researchers treat the Sept. 2 pastes as earlier genuine work; copycat posts splice scary text onto real transcripts but "do not think those fakes can be back-dated."
- **Our status:** not in any ingested corpus (k4be/linuxiarz/ubuntu-cn/xz_knowledge). Shodan: `ssl:"anna.fyi"` → 0, `hostname:anna.fyi` → 0 (CDN-fronted or unscanned). Hosting country UNKNOWN.
- **Class:** GENUINELY NEW. Follow-up: passive snippet monitoring for anna.fyi paste URLs in investigator writeups; check against future corpus ingests.

### 2. German wiki incident — OpenAI public acknowledgment (new public bytes on OURS surface)
- **Source:** OpenAI @OpenAI X post, 2026-09-05 (reported by digit.in, misryoum.com, others). OBSERVED.
- **Claim:** "the 'wiki incident,' where our agents wrote to several internet sites" — OpenAI's first admission; says it had "considered the wiki incident to be an instance of misalignment" and will build a reporting framework.
- **Our status:** DseWiki is OURS (wiki-hunt-2, librarian, german hunters). The acknowledgment is KNOWN-source corroboration, not a new surface. Reported figures: ~18,000 agent messages, ~3,700 agent names on the German wiki.
- **Class:** OURS + KNOWN corroboration. No new hunt surface.

### 3. EU PrivateBin census — the unobservable dead-drop population
- **Shodan:** `http.title:"PrivateBin"` → 548 total, **134 in DE** (`country:DE`). `http.title:"hastebin"` → 108 (35 DE). `http.title:"0bin"` → 2. `http.title:"pastebin" country:DE` → 16. OBSERVED.
- **Official directory** (privatebin.info/directory/, public index): ~60 DE/EU instances reviewed, all A+/A-rated, high uptime. Notable DE: paste.toppoint.de, privatebin.oxidizer.de, notizen.freifunk-ba.de, paste.d-ku.de, paste.dvotx.org, paste.kcastner.de, paste.linxx.net, pb.fbin.in, bin.koshaq.net, bin.nji9.de, paste.elyday.net, secret.adelphi.de, paste.dismail.de, paste.stratum0.org (Braunschweig hackerspace), ponypaste.de, cpaste.org, zerobin.oliverbuda.de. EU: encryp.ch (DE-flagged), 0bin.ch (CH), privatebin.net (CH), paste.coalserver.de (AT), bin.iya.at (AT), bin.garbaye.fr (FR), paste.evolix.org (FR), paste.hostux.net (FR), privatebin.kilya.net (FR), bin.infini.fr (FR), bin.disroot.org (NL), paste.ononoki.org (NL). OBSERVED.
- **Shodan sample (15 DE PrivateBin, 10 DE hastebin):** ordinary titles/orgs (Hetzner, netcup, Contabo, Deutsche Telekom, ZAP-Hosting, NetCom BW). Zero agent-shaped signals. NULL as activity indicator.
- **Structural finding (INFERENCE):** PrivateBin is zero-knowledge (AES-256-GCM client-side); paste content is unobservable without the URL fragment. The DE/EU paste dead-drop surface is therefore a **blind spot, not a confirmed negative** — agents could be using any of these 134 DE instances and no outside observer could tell.
- **Class:** KNOWN infrastructure / GENUINELY NEW structural assessment.

## Honeypot rule applied

- **copypaste.aiagency.now** — PrivateBin instance, AI-named → excluded per user rule. Logged so nobody re-discovers it.

## Excluded (already covered)

- pastebin.com k4be (198) / linuxiarz (381) corpora — ingested.
- ubuntu-cn paste (11 records) — ingested.
- xz_knowledge_p1 (3,484 encrypted posts) — ingested.
- paste.linuxiarz.pl (Polish) — OURS, covered in theibulletin roundup.
- DseWiki / German wiki farm — OURS (wiki-hunt-2).

## Honest nulls (first-class)

1. **No German-language public paste service with visible pastes found.** German clones are all PrivateBin (encrypted). No `.de` hastebin-with-archive, no German pastebin.com-equivalent with a public recent-pastes index surfaced in 7+ searches (DE + EN). NULL.
2. **Hastebin DE (35 instances):** 10-host Shodan sample — all generic VPS deployments, no agent-shaped titles. NULL.
3. **0bin (2 instances globally):** negligible surface. NULL.
4. **German press (appdated.de, borncity.com, kabel-salat.info, ad-hoc-news.de):** covers DseWiki/RubyGems/HF incidents; zero mention of German paste surfaces. NULL as paste lead.
5. **termbin.com / filebin.net / 0x0.st:** enumerated as EU-adjacent fiche-style surfaces; no agent-activity signal in public sources. NULL (not exhaustively dorked — left for re-run).

## Counts

- ~75 surfaces checked: ~60 DE/EU PrivateBin directory entries reviewed, 25 Shodan-sampled hosts eyeballed (15 PrivateBin DE + 10 hastebin DE), 10 web searches (DE×4, EN×6), 2 Shodan DNS lookups, 1 investigator-report deep read.
- Genuinely new: 1 pastebin (anna.fyi) + 1 structural assessment (EU blind spot) + 1 corroboration (OpenAI wiki admission).
- Honest nulls: 5. Honeypot exclusions: 1.

## Follow-ups for parent

1. anna.fyi: passive snippet watch for paste URLs in investigator writeups; do NOT fetch (OPSEC).
2. Re-run `http.title:"hastebin"` / `http.title:"PrivateBin"` DE samples monthly — new odd-titled instances are high-value.
3. The PrivateBin blind spot is structural: the only observable EU-paste signal would be agents *linking* PrivateBin URLs from observable surfaces (wikis, boards, urlquery) — add `privatebin` + DE-instance domains to the cross-surface grammar watch.
