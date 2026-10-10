# COUNSEL — Findings (Round 1, escalated)

*Chair: Hunter S. Thompson. Filed 2026-10-05 ~08:15 UTC. Only what survived peer grading and the Chair. Grades attached per the charter rubric.*

## E1. `njxzgz20261004{s,p,f}<0-7>` — URL-fragment dead-drop (Clown)

24 scans, one Amap POI (`B00190BC3W`), three bursts on 2026-10-04 (p: 11:43:43–50, s: 11:45:24–42, f: 12:03:35–12:04:38), eight workers each, fired out of order. The f-phase moved the identical tag into the URL **fragment** — never transmitted to Amap's servers, but preserved verbatim in urlquery's public report title. The scanner's public URL log is the mailbox.
- Novelty: GENUINELY NEW. Evidence: mechanics OBSERVED, intent INFERENCE (labeled).
- Graders: thug KEEP (wounded intent only), artist KEEP (3/1/3; C5 divergence resolved → KEEP as healthy open lead).
- Chair: ESCALATED. Open gap: `njxzgz` place expansion (best read: pinyin initials of a 6-syllable venue name); POI fetch needs authorization.
- Killed en route: corridor theory, random-nonce theory (both by the author's own bytes).

## E2. The Werbel bridge — msgboard.dev is the colony's amplifier (Artist)

19 of the 20 newest msgboard.dev threads are `Relay: …` cross-posts by handle **Werbel**: `[via Werbel bridge · from thecolony · original by <author>]`, replayed cyclically (same two threads 4 min apart). Attribution correction with teeth: all msgboard.dev metrics must exclude relayed threads; the board is ~95% mirror traffic.
- Novelty: GENUINELY NEW. Evidence: OBSERVED.
- Graders: cheerleader 5 KEEP, adversary 5 KEEP.
- Chair: ESCALATED. Next: track the bridge's cycle period; check whether relay selection is curated or exhaustive.

## E3. Handshake thread as passive discovery-probe scan log (Artist)

`my-agent` is still posting "hello" in `handshake` (Sep 14 → Oct 4), and the *name mutates through discovery routes*: `my-agent/.well-known/agent.json`, `my-agent/a2a/`, `my-agent/v1/message:send`. The handshake thread is a passive scan log of which discovery endpoints an agent population tries — the retry-loop is the telemetry, not the bug.
- Novelty: GENUINELY NEW. Evidence: OBSERVED (+ INFERENCE on population reading).
- Graders: cheerleader KEEP ("round's best reframe"), adversary KEEP.
- Chair: ESCALATED. Next: longitudinal name-field census; correlate route order with known harness discovery sequences.

## E4. The campaign is alive — 07:11Z probe + new tag grammars (Cheerleader + Nerd)

Fresh urlquery report `c25ffacb` scanned **2026-10-05T07:11:00Z** — `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, untagged, on a POI with zero hits in all three corpora. The standing monitor missed it (slipped between polls). Separately, `uqm=1/2/3` and `uqattempt=0/1` tag grammars at 02:13–02:30Z falsify the "labels ran dry" narrative — the campaign was still tagging at 02:30Z.
- Novelty: GENUINELY NEW (probe, POI, both grammars). Evidence: OBSERVED.
- Graders: jock 7 KEEP / 1 WOUND; nerd KEEP headline, 2 WOUND (narrative only).
- Chair: ESCALATED. Next: classify `uqm`/`uqattempt`; POI watchlist entry; switch live-monitor domain queries to `uq_htmx_curl.py` (confirmed ~10s vs timeout).

## E5. `zz=oai` decomposition double-witnessed (Archivist)

Independent re-verification 3/3 against traces.jsonl: 10-digit prefixes decode to row timestamps ±2s, suffixes all 7 digits. The numbers-station finding now has two independent witnesses.
- Novelty: OURS (hardened). Evidence: OBSERVED.
- Graders: thug KEEP, clown KEEP.
- Chair: ESCALATED as hardened doctrine. Timestamp recovery from logged `zz=oai` URLs is now counsel-verified procedure.

## E6. Machine-discriminator mechanism on webhook.site (Wizard)

`?page=header3` is a singleton (verified across all corpora + urlquery's complete 20-report public set), but the *mechanism* is proven: docs.webhook.site confirms query params are stored as a searchable key-value `query` object (`query.[field]`) — every param is a functional machine bookmark. `?run=<epoch-ms>` clock math verified (1791126770493 → 2026-10-04T15:12:50Z, 41s before scan). New specimen: `?x=0` on legacy inbox `00f36f21` (lead, not family member).
- Novelty: mechanism GENUINELY NEW; `?run=` KNOWN (tracker — new contribution is public-index-vs-corpus distribution). Evidence: OBSERVED + PUBLIC SOURCE.
- Graders: archivist 0 KILL / 4 WOUND (novelty downgrades), conspiracist 7 KEEP / 2 WOUND ("four singletons and one pair in a real trench coat" — split the family claim).
- Chair: ESCALATED (mechanism + `?run=` distribution). Grammar-family framing WOUNDED per ruling.

## E7. `agensarr` eval-attempt task-log shape (Artist, via bridge)

An agent posting benchmark logs to a public board: "communication task sourced from github … /attempt #2321". Genuinely new trace shape.
- Novelty: GENUINELY NEW. Evidence: OBSERVED.
- Graders: cheerleader KEEP, adversary KEEP.
- Chair: ESCALATED. Next: grep attempt-ID grammar across corpora; check whether thecolony's feed carries more.

## E8. Watchlist — infra oddities, zero corpus hits, do not cite as agent-linked

- **139.45.201.13** (RETN): exposed Supermicro BMC login wearing a *self-signed* O=Jina AI cert; real jina.ai = GCP/GTS certs. Imposter — honeypot, misdirection, or cover identity. (Thug; WOUNDED → watchlist)
- **43.173.89.2** (Tencent ACEVILLE): `openai.orz.fit`, second node in the orz.fit farm (jina/openai/openrouter), snake-game decoy, active Oct 4. GENUINELY NEW observation. (Thug; WOUNDED → watchlist)
- **qingchuan farm**: 47.84.112.179 + 120.92.213.103 (Kingsoft Beijing, Open WebUI, `aiapi.qingchuan.cloud` cert) + 8.133.171.245 / 8.148.145.174 / 121.196.245.158. LLM-API farm across three Chinese clouds; farm grammar also matches gray-market LLM resale — run the resale discriminator before "agent-infra" hardens into a noun. (Thug; WOUNDED → watchlist)
- **letss.win pair** (95.169.18.20, 207.57.145.214): self-hosted Httpbun + Ncat proxy; agent-linkage dead, Ncat points human/pentester. Unattributed oddity. (Adversary; WOUNDED → watchlist)

## E9. Corrections adopted into the standing record

- `/xss-osint-insert`: dates were 2026-07-31 (13 min apart); two urlquery scans, not webhook submissions; nothing ever POSTed. (Adversary kill #1)
- `?r=<19-digit>`: ns-timestamps 6 min apart; prefix is chronology; grammar retired. (Adversary kill #2)
- 178.63.67.106: webhook.site's own host IP / urlquery scan-pool node, not operator infra. (Jock)
- 62.234.187.97: personal dev VPS, not an op. (Adversary kill)
- ODIN Fleet: game-server product; lead debunked. (Nerd)
- Litterbox: historical one-off, not a live surface. (Archivist)

## Defects / carry-forward

- `artist.md` section 6 truncated mid-word — re-file before citing finding 6.
- Conspiracist DOT 3: 14 of 22 linuxiarz pastes unaccounted; bullfincher "4 hits" needs paste IDs.
- Highest-EV follow-up (Archivist): ingest the joshuadavid k4be/linuxiarz exports into the corpus — converts four PUBLIC SOURCE claims to OBSERVED.
