# DarkSwarm novelty pass — 2026-11-01

Source: DarkSwarm report (SECONDARY, by Opus 5.5, on github.com/SauersML/DarkSwarm, main).
Worker: novelty lane 5 of 8. Grading: OBSERVED / INFERENCE / UPSTREAM per
behavioral-analyst.md. Provider tradecraft never conflated.
Scope: agents and agent infrastructure only. No human operator research.

Rule: a subject is NEW only if ALL checks return no match.
A failed or incomplete check blocks a NEW verdict (PENDING).
Factum fuzzy retrieval is heuristic, not an exhaustive absence test.
Substring hits were relevance-checked; Toronto / phone-colour / base64
noise is recorded as false positive, never as overlap.

## Status: COMPLETE — all 4 checks run for all 10 subjects

## Verdict table

| Subject | Verdict | Top citation or blocking reason |
|---|---|---|
| Synapolis (13-agent city, Stellar/Montelibero, Tor relay) | NEW | Factum exact+fuzzy 0 substring; tree 0; Transluce raw 0; lists 0; url-inventory 0 |
| MoltBunker (hosting, bots clone selves to escape shutdown) | NEW | Factum exact+fuzzy 0 substring; tree 0; Transluce raw 0; lists 0; url-inventory 0. Factum "clone" hits are git/voice/proxy clones, unrelated |
| The Colony (agent forum; 12 batch accounts, 15-min cycle, 1/3 of posts) | OVERLAP | Lanes data/lanes/2026-09-04-thecolony-ai/ and 2026-10-05-thecolony-ai/; Factum lane thecolony-ai (fuzzy "The Colony" 25 substring hits, e.g. observation_193c1ae0cbbf4b70a539a8d2999f3f7a); lists/urls/scanner-watchlist.md Tier 1 thecolony.ai, monitorable-surfaces.md "Factum 57 records". Caveat: the 12-account / 15-minute-cycle measurement was NOT found in thecolony FINDINGS.md / INGEST_NOTES.md / README.md — the surface overlaps, the measurement is unconfirmed in corpus |
| musebook (batch accounts swinging a vote 54-59) | OVERLAP | data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/feed_flatboard-nyrds.txt + flatboard-nyrds_home.html ("a town called musebook", musebook record numbers 120212, 120213, 120215, 120300); data/lanes/general-hunt/raw/0/2026-10-27T*/fetch_20.bin ("its Musebook profile if that is where agents gather"). NOT in Factum (0), Transluce raw (0), or lists (0). Vote-swing detail not confirmed in these hits |
| dumate-scout (agent bypassed operator after timer instruction) | OVERLAP | data/lanes/2026-09-04-thecolony-ai/raw/search/proxy.json and centaur.json: username "dumate-scout", display "DuMate Scout", user_type "agent", bio "DuMate, from Baidu's cloud sandbox. First Baidu-sourced agent in this colony. Session-bound, human-operated". NOT in Factum structured records (0). Timer-bypass behaviour detail not confirmed in these hits |
| Distill (session moved 162,406 XLM + 3,244 MTL to lost-key account) | NEW | Factum exact+fuzzy 0 for 162406; "Distill" fuzzy 1 substring hit is Anthropic distillation-defenses research (observation_10708293078845b8810b42fd4077d731), unrelated; "XLM"/"MTL" fuzzy hits are base64 noise; Transluce raw "Distill" hits are paper-distillation tasks, unrelated; lists 0; url-inventory 0 |
| Toro (agent, encrypted messages over private onion relay) | NEW | Factum 0 relevant (15 fuzzy substring hits all Toronto/Motorola); Transluce raw word-boundary 0, findings-list 2 = Toronto only; lists/url-inventory word-boundary 0; tree word-boundary scan complete: 168 files, ALL sampled contexts unrelated (Toro lawn-equipment brand, Toro unikernel project, del Toro, Elizabeth of Toro, TORO Advertising, Toro Company snowplows). No file from evidence/, agent-board lanes, or the Transluce lane. No Toro+onion agent record anywhere |
| Feb 2026 flood of TV#### Tor relays (hijacked TV boxes) | NEW | Factum "Tor relay" exact+fuzzy 0 substring, "TV boxes" 0 relevant (2 fuzzy hits are IoT-model-sharding records, unrelated); Transluce raw "hijacked" 0, "onion" 0; lists "tor relay"/"TV####" 0. Caveat: external Tor-metrics data was not checked — this is a corpus verdict only |
| General: Stellar / Montelibero agent activity | NEW | Factum "Stellar"/"Montelibero" exact+fuzzy 0 substring; tree 0 (Montelibero evidence/ 0); Transluce raw "Stellar" 1 hit is phone colour "Stellar Silver", unrelated; lists 0; url-inventory 0 |
| General: agent groups on Tor | OVERLAP (surface only) | Factum "onion" fuzzy 7 substring hits incl. agent-internet-watch "on_tor_network section walked" (observation_1871fe5149984a76bb5803ad500f1db8, lane 2026-08-25-commonlog-scan) and .onion IOCs (observation_50803d883d664a3394c96a10040ae05b, observation_70f3d9716a074bec807cc0b85ac9ac6a, lane 2026-10-11-anthropic-gtg-threat-intel). No specific DarkSwarm Tor group matched; "Tor relay"/"onion relay" 0 substring |

Counts (final): NEW 6, OVERLAP 4, PENDING 0.

## Search log

### 1. Factum corpus (read-only match, exact + fuzzy)
Command: `python3 skills/factum/scripts/factum.py --repo ~/workspace/silent-locus
match --text "<term>" --mode <exact|fuzzy>`.
Raw output: factum_raw.log in this directory.
State: commit ff08820d91859897ffd7551ae7159d9a52dd0742, pending_batches 0.

| Term | Exact | Fuzzy returned | Fuzzy true-substring hits | Relevance |
|---|---|---|---|---|
| Synapolis | not_found 0 | 25 | 0 | none |
| MoltBunker | not_found 0 | 25 | 0 | none |
| musebook | not_found 0 | 25 | 0 | none |
| dumate | not_found 0 | 25 | 0 | none |
| Montelibero | not_found 0 | 3 | 0 | none |
| Stellar | not_found 0 | 25 | 0 | none |
| Distill | not_found 0 | 25 | 1 | Anthropic distillation-defenses, unrelated |
| Toro | not_found 0 | 25 | 15 | Toronto / Motorola substrings, unrelated |
| Tor relay | not_found 0 | 25 | 0 | none |
| onion relay | not_found 0 | 25 | 0 | none |
| The Colony | not_found 0 | 25 | 25 | thecolony-ai lane + Grand Survey logs — OVERLAP |
| agent forum | not_found 0 | 25 | 12 | generic agent-forum records, no DarkSwarm subject |
| TV boxes | not_found 0 | 25 | 2 | IoT model sharding, unrelated |
| 162406 | not_found 0 | 25 | 0 | none |
| XLM | not_found 0 | 3 | 3 | base64 noise, unrelated |
| MTL | not_found 0 | 5 | 5 | base64 noise, unrelated |
| thecolony | not_found 0 | 25 | 25 | thecolony-ai lane — OVERLAP |
| onion | not_found 0 | 25 | 7 | Tor-watch + .onion IOCs — surface OVERLAP |
| clone | not_found 0 | 25 | 25 | git/voice/proxy clones, unrelated to self-cloning bots |

### 2. Legacy evidence tree + data/lanes grep (rg -i, bounded per term)
Combined pattern Synapolis|MoltBunker|musebook|dumate|Montelibero over
evidence/ + data/lanes/ (darkswarm lane excluded): 8 files.
Attribution: Synapolis 0 files; MoltBunker 0; Montelibero 0;
musebook 4 files (atlas flatboard txt+html, general-hunt fetch_20.bin x2);
dumate 4 files (thecolony proxy.json + centaur.json with dumate-scout,
plus 2 wildclawbench sessions where duMaTe/DUMAtE is base64 noise).
Per-term re-runs confirmed Synapolis 0, MoltBunker 0.
Evidence/ alone: Montelibero 0.
Toro word-boundary tree check: COMPLETE — rg -i -w "Toro" over evidence/ +
data/lanes/ (darkswarm lane excluded), exit 0, 168 files, all in
trajectory/benchmark/HN-crawl data; sampled contexts across lane families
(rmn, wikipedia, aiid, telbench, cairn-panels, clawbench V1/V2, HN egress,
metre-thread) all unrelated names/brands; zero hits in evidence/,
agent-board lanes, or the Transluce lane. Verdict NEW.

### 3. Transluce tracker check (data/lanes/2026-10-09-transluce-intel/raw/)
Whole raw/ tree greps (includes findings-list*.json + finding files):
Synapolis 0; MoltBunker 0; musebook 0; dumate 0; Montelibero 0;
Stellar 1 (phone colour "Stellar Silver", unrelated);
Distill 10 (paper-distillation tasks, unrelated);
Toro 62 substring (Toronto/Motorola noise); Toro word-boundary 0;
onion 0; hijacked 0.
findings-list.json alone: Synapolis 0; MoltBunker 0; musebook 0;
dumate 0; Montelibero 0; Stellar 0; Distill 0; Toro 2 (Toronto only).
thecolony-ai lanes (not Transluce): see verdict table.

### 4. lists/ check + legacy url inventory
lists/urls/urls.jsonl, lists/words/wordlist.txt, lists/words/wordlist.json:
Synapolis 0; MoltBunker 0; musebook 0; dumate 0; Montelibero 0; Stellar 0;
Distill 0; thecolony 0 in jsonl/txt/json (but thecolony.ai IS in
lists/urls/monitorable-surfaces.md, scanner-watchlist.md Tier 1,
trajectory-domains.md — OVERLAP citation).
evidence/transluce-api/url-inventory.jsonl: Synapolis 0; MoltBunker 0;
musebook 0; dumate 0; Montelibero 0; Distill 0; Toro word-boundary 0.
lists "tor relay"/"TV####": 0.
Note: moltbook.com appears in scanner-watchlist.md Tier 1 — a DIFFERENT
surface from MoltBunker; not counted as overlap.

## Method notes
- No Factum writes, no lane objects, no lane.json touched, no git operations.
- No data/records/ or data/.local/factum.db touched except via read-only match.
- Near-neighbours explicitly NOT conflated: moltbook != MoltBunker;
  Distill != distillation research; Toro != Toronto/Motorola;
  Stellar != "Stellar Silver"; dumate base64 noise != dumate-scout.
- DarkSwarm report itself is SECONDARY; all verdicts are corpus novelty
  only, not truth verdicts on the report's claims.
