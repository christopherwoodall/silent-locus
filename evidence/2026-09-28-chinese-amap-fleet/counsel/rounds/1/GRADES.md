# COUNSEL — Round 1 Grading Record

*Chair: Hunter S. Thompson (campaign-trail). Filed 2026-10-05 ~08:15 UTC.*
*Method: 10 hunting lanes, 20 peer-grade files, every finding graded by ≥2 personas on the charter rubric (Novelty / Evidence / Actionability / Verdict). The grade files in `grades/` are the primary record; this file is the Chair's rollup, tie-breaks, and final dispositions.*

## Scoreboard

| Persona | Lane | Findings | Grader A | Grader B | Chair disposition |
|---|---|---|---|---|---|
| wizard | `?page=` discriminator family | 9 | archivist: 0K/4W/0KILL | conspiracist: 7K/2W/0KILL | KEEP w/ wounds; ESCALATE mechanism |
| nerd | ODIN Fleet | 15 | conspiracist: 15K | archivist: 15K | KEEP report; **KILL the lead** (debunked null) |
| jock | fresh-inbox re-sweep | 7 | conspiracist: 7K | nerd: 5K | KEEP all; ESCALATE IP correction |
| cheerleader | live campaign | 8 | jock: 7K/1W | nerd: KEEP headline, 2W | KEEP; ESCALATE live findings |
| adversary | red-team the leads | 5 targets | jock: kills stand | cheerleader: concur 5/5 | KEEP all; kills ADOPTED |
| artist | msgboard.dev | 6 | cheerleader: 5K/1W | adversary: 5K/1W | KEEP 1–5; WOUND 6 (truncated, re-file) |
| thug | infra corroboration | 26 | adversary: 2K/4W/3KILL | artist: 22K/4W/0KILL | **TIE-BROKEN** (see below) |
| clown | njxzgz + crooked msgboard | 7 | thug: K/W mix | artist: 3K/1W/3KILL-conf | KEEP mechanics; WOUND intent |
| archivist | litterbox + audits | 11 | thug: K/W mix | clown: graded | KEEP; litterbox verdict stands |
| conspiracist | venue constellation | 9 dots | clown: graded | archivist: KEEP, 2W | KEEP w/ 2 wounds |

K = KEEP, W = WOUNDED. Kill counts below are Chair-final.

## Chair's tie-break: the Thug's "agent-infra LEADs" vs the Adversary's kills

The Adversary killed 62.234.187.97 and the jina-lookalike "agent infra" hypothesis on three grounds: (a) base rate — personal devs run identical stacks; (b) corpus-contrary — 96k tag-sweep reader events touch ONLY official endpoints, never bespoke mirrors; (c) README-norm — httpbun self-hosting is the documented norm. The Thug's new data (Shodan uniqueness counts, cert details, sibling hosts, the RETN imposter) is genuine but ORTHOGONAL — it never engages (a), (b), or (c). The Artist graded the observations clean (22 KEEP) while wounding only adjectives, which does not answer the kill grounds either.

**Ruling:** the noun "agent-infra" is KILLED for 62.234.187.97, jina.orz.fit, jina.qingchuan.cloud, and relay.woaifei.com. The *observations* survive WOUNDED as watchlist infra oddities: the orz.fit farm's second node (43.173.89.2, GENUINELY NEW), the qingchuan four-IP cartography incl. Kingsoft Beijing Open WebUI box, and the RETN 139.45.201.13 "Jina AI" self-signed imposter cert on an exposed BMC. Upgrade condition: agent-traffic co-occurrence or a second independent pivot. Until then, do not cite as agent-linked. Convention fix adopted: Shodan-stored records are PUBLIC SOURCE, not OBSERVED.

## The 14 kills (Chair-final, all evidenced)

1. **`/xss-osint-insert` as agent double-submit** — dead. urlquery's own date fields: 2026-07-31T12:19:33Z and 12:32:29Z (13 min apart, not "same minute 2026-08-08"). Layer confusion: two urlquery *scans* of an inbox page (5 GETs, alert_count 0, zero captured webhook requests) read as two webhook *submissions*. Nothing ever POSTed. Dead-drop-diver FINDINGS.md amended.
2. **`?r=<19-digit>` as operator grammar** — dead. Both nonces decode to ns-timestamps 2026-06-21 19:40:00Z and 19:46:16Z, 6 minutes apart; any two such timestamps share 15+ leading digits. The `178207` prefix is what time looks like. Cache-buster, one human's June-21 session.
3. **62.234.187.97 as agent infra** — dead. "New API" is a 48k-star open-source LLM gateway; the box is a hobbyist Tencent VPS (default nginx test page, EOL tag, old CVEs). Zero corpus hits in 688k events.
4. **jina-reader lookalikes as agent infra** — dead. Personal AI-dev domains; agents in 96k events use only official reader endpoints. Watchlist only.
5. **ODIN Fleet lead** — dead by the vendor's own About section. 4Players' commercial game-server hosting; the mention was Docker Hub marketing copy. Naming correction logged: no `fourplayers/openclaw` GitHub repo exists (it's `4Players/openclaw-docker`). Landmine flagged: `neversight/learn-skills.dev` hosts a file named `odin-agent-skills` (about the game product — will confuse someone later).
6. **178.63.67.106 as operator infra** — dead. It's webhook.site's own host IP / a urlquery Hetzner scan-pool node (report `c9104bb8`: target IP .106 vs exit IP .153 — different fields). The "same infra as the fleet inbox" framing conflated target-resolution with scan-exit. CONTEXT.md and IP_LOG amended.
7. **Litterbox as live dead-drop surface** — dead. 68 reports, epoch-nonce activity confined to Apr 19–May 10, last report Jul 27 (an .apk, human-kit-shaped). Historical one-off cluster.
8. **"11 live webhook.site inboxes"** — unreconciled figure, killed as a claim. Only 4 confirmed ALIVE (newest beacon 03:05Z).
9. **anhui-famous as new** — killed by the bytes; already in ALL_LINKS.md and the grammarian's catalog.
10. **Corridor theory** (njxzgz = Nanjing–Xuzhou–Ganzhou) — killed by its own author: all 24 scans pin ONE Amap POI.
11. **Random-nonce theory** (njxzgz) — killed on grammar match + venue correlation + zero hits in 590k oai-traces / 96k tag-sweep.
12. **Greeting-loop-as-heartbeat** — killed (0–1s gaps, single 4-min session).
13. **Message-length steganography** (msgboard.dev) — killed; the surviving observation (char-vs-byte fuzz calibration, `extra-probe-marker`) kept as genuinely new byte detail.
14. **"Labels ran dry" narrative** — falsified by `uqm=1/2/3` and `uqattempt=0/1` tag grammars at 02:13–02:30Z (Nerd's wound-turned-find). Campaign was still tagging at 02:30Z.

## Wounds carried forward (not kills)

- letss.win → unattributed infra oddity (agent-linkage dead; Ncat proxy points human/pentester).
- Clown's fragment dead-drop *intent* ("talking to the scan log") — mechanics airtight, intent honest INFERENCE.
- Wizard's family framing — mechanism family proven, grammar family not; `?x=0` is a lead, not a member; `?run=` downgraded to KNOWN (tracker).
- Cheerleader's cadence narrative — burst timestamps are receipts, "operator-shift rhythm" is story.
- Conspiracist DOT 3: linuxiarz ×22 count has 14 unaccounted pastes; bullfincher "4 hits / 2026-02-26" needs paste IDs or stays rumor.
- Artist finding 6: truncated mid-word ("Rel") — re-file before citing.

## Honest nulls honored (first-class)

ODIN Fleet (debunked), litterbox-as-live-surface, beeceptor frozen since May 20, pipedream-infra frozen since May 4 (RETRACTED Round 2: our own infra-sweep bytes show 2026-07-10, 2026-08-10, and 2026-09-03 hits, plus an in-window 2026-05-04 hit), no follow-up scans of the fresh inbox, `?page=header3` siblings (no header1/header2), msgboard.dev corpus absence (0 hits), 0 "odin"/"4players" in 688k events, 0 urlquery reports for odin.4players.io.

## Corrections to the record (applied)

- CONTEXT.md: fresh-inbox IP framing; xss-osint-insert entry; `?r=` entry; Tencent entry.
- Dead-drop-diver FINDINGS.md: SHAPE-3 (dates, layer), SHAPE-4 (retired as grammar).
- IP_LOG.md: 178.63.67.106 precision fix; 62.234.187.97 + jina lookalikes downgraded from LEAD; letss.win downgraded; 5 new watchlist IPs appended.
