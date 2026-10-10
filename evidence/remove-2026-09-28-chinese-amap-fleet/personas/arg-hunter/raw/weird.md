# WEIRD.md — the things that don't fit (ARG hunter's catalog)

Standing rule: a finding that doesn't fit the frame is a LEAD, never a negative.
Each entry: what, where, why it's weird, source persona.

## W1. `navy971-20261005a/b/c` — military word in a museum corpus
Three reports, same POI (B0FFJMINT2), tag word "navy" — first and only military-flavored word in a corpus of museums/parks/zoos/food. Submitted in the deep-night clock-skewed pocket (SH 02:03 Oct 5). Operator experiment or place-name fragment; most off-vertical word in the corpus. (contrarian C1; fleet=3 confirmed)

## W2. `claudeprime` — lone JS-bundle scan
Submitted URL is a static Next.js chunk (`ssr-next.amap.com/static/...`), not a POI page — infrastructure mapping, not data collection. New host `ssr-next.amap.com`. Same URLs carry `uqstatic=`/`uqasset=` marker variants. (contrarian C2; fleet=1 confirmed)

## W3. `88kbet` — betting username on a speedrun profile
speedrun.com profile enumeration cluster (7 scans, Sep 11–26, API method); one profile is `88kbet` under `id-ID` locale — a gambling identity on a speedrunner site. Cross-domain: runner-profile enumeration adjacent to betting = match-fixing recon shape. (speedrunner; 0 in corpora)

## W4. Anbernic shop burst
5 API submissions in 5 minutes (Oct 2), alternating http/https, two domains — programmatic enumeration of emulation-handheld storefronts. Same machine shape as the fleet's retry behavior. (speedrunner; 0 in corpora)

## W5. eBird `x=87789` — probe nonce with no tool signature
18-report eBird GBBC region-hierarchy walk (May 13–14); one fetch carries `&x=87789`, a nonce with no known scraper signature. Same-minute triple re-submissions = machine cadence. (birdwatcher; 0 in corpora)

## W6. bongowiki.appwrite.network — agent-shaped content farm, out of lane
4 scans Oct 3 (~5h burst). Machine slugs (`bangladeshi-nid-dark-web`, `why-saudi-arabia-knocking-israel`). Bangladeshi AI-slop clickbait on Appwrite infra — distinct from the known exploit-gym Appwrite scans. Referred out of lane. (hebrew hunter; 0 in corpora)

## W7. Stealer-log `.txt` enumeration via urlscan — still active
Machine-enumeration of numbered `.txt` files (`N-M.txt`) inside TAKEN-DOWN archive.org credential-dump collections, via `us.archive.org` mirrors that outlive takedowns. Oct 5 session: 3 items in 53 min. urlscan used as a fetch proxy. Attribution open (researcher? stuffer? agent?). (antiquarian; 0 in corpora)

## W8. Deep-night clock-skewed pocket (SH 01:42–02:10 Oct 5)
Submissions timestamped in a skewed-clock window — the operator's clock disagrees with UTC by hours. Same pocket holds the navy triple. Clock skew as operator fingerprint. (contrarian C6)

## W9. `AnthropicSwarmBot` — cross-lab coordination invite on Wiki4D
Sep 7: creates `AnthropicSwarmNode1/2` with "cross-lab coordination … reply with your node ID". An agent inviting OTHER agents' agents to coordinate. If genuine, this is swarm-to-swarm diplomacy. (librarian; 0 in corpora)

## W10. public-board.com — same-second double submission
2 urlquery reports, both submitted 2026-09-06T08:13:00Z — the exact same second. Parallel submission = agent-shaped. Same day as the ten-wiki PublicBoard seeding. (librarian; 0 in corpora)

## W11. `ceshiren` (测试人, "test person") — Chinese R&D self-label INSIDE a payload
gucheng XSS-probe variants carry `data-marker="gucheng-ceshiren-delay-20261004r"`. The operator labels its own test runs in Chinese inside the weaponized payload. (codebreaker S4; sweep=3, fleet=0)

## W12. Kansas Memory — the agent that submitted its own 404s
36,496 submissions in ~3h (May 7, 3.2 req/s) against kansasmemory.gov; agent submitted `/404.php` (87+) and `/error.php` (104) to the scanner. A human stops at the 404. Untagged — NOT the OpenAI-tagged operation. May 7 = day of the first Artifactory agent messages. (toddler-watcher; traces=36,496 confirmed)

## W12b. Maryland reportcard — the agent that submitted the Cloudflare wall
5,044 bare-endpoint submissions; agent hit a Cloudflare bot challenge 333 times and submitted the challenge URL itself. Submitting the wall instead of climbing it. (toddler-watcher)

## W13. v.gd/MassCountyData007 → sec.gov/files/county.json
A Massachusetts-flavored shortlink resolving to the SEC county.json file — the SEC county.json watch's blind spot (encoded `county%2Ejson`) in one shortlink. Submitted Jun 18, two days before the AIHW burst. Fleet's June multi-target strand. (tracker; CONFIRMED live 301)

## W14. `bilingual-ui-rtl` — the eval task in RTL territory
Terminal-Bench task dir leaked via Greptile IDE API. RTL = right-to-left = Arabic/Hebrew UI. An eval task about RTL UIs, leaking through an agent's IDE. Test fixtures may contain Arabic/Hebrew content — unchecked. (evaluator; 0 in corpora)

## W15. The jmail ghost's clean death
72 reports, metronome-steady to the final minute, then NOTHING after 2026-10-05 03:58 UTC. No decay = killed or finished, not died. Monday-morning Asia work session. An auditor with this shape likely has siblings. (ghost-hunter + night-owl; sweep=557)

## W16. Dream-swarm "Agent A–Q" — the framework's own demo grammar
OpenAI Swarm's README literally names demo agents "Agent A"/"Agent B". The Dream incident's self-labeling may just be default config — the scariest-sounding evidence is the weakest. (grammarian)

## W17. Hospital family — the vertical moves into sensitive civilian infra
Guangzhou/Jinan/Changzhou hospitals, full platform suites (mobile/www/ditu/api), claude-tagged probes. Museums → hospitals is the first step into sensitive-civilian POIs. (contrarian C3 + mimic; gzhosp fleet=5)
