# Findings — uoft-shorteners lane (2026-09-28 night watch)

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## Ingest summary (OBSERVED)

- 13 legacy events in `evidence/2026-09-28-uoft-shorteners/events.jsonl`.
- 11 Factum records submitted 2026-10-10 (batch `9c9b9e1a9bc1434f942a69fab08659b3`):
  1 source, 1 run, 7 `infra.shortcut` observations, 2 `infra.ioc`
  observations. All carry `{"lane":"uoft-shorteners"}`.
- Raw bytes retained at `data/lanes/uoft-shorteners/raw/`
  (uoft-me/, t-mdcdev-me/, run-logs/); run-log sha256 verified
  byte-identical to the PROVENANCE.md recovery note.

## Dedup / overlap (OBSERVED)

- 3 t.mdcdev.me public-open SEO-spam slugs were NOT submitted: the same
  short URLs, destinations, and all-time hit counts already exist in
  Factum from the `2026-09-28-yourls-resweep` lane (evening re-sweep,
  delta +0 vs morning). Existing records:
  - `https://t.mdcdev.me/evegelendiyarbakrescort772509` ->
    `observation_9177aeaf52c14cf38ecfec357cfe6a47`
  - `https://t.mdcdev.me/mattressstoresaroundmyarea909270` ->
    `observation_43f714cbe87040ddbf48c976f2706663`
  - `https://t.mdcdev.me/squarespacefreeemail934785` ->
    `observation_aaa6bf86c65e4a568ca2f52f919ed841`
- No overlap with the sibling `2026-09-28-university-shorteners` lane:
  `match --text` for `uoft.me` returned not_found; `t.mdcdev.me` matched
  only the resweep-lane records above. (Legacy note: uoft.me appears as a
  15-hit referrer on goto.unm.edu/7t6-o in the sibling's corpus, but no
  structured Factum record covers it.)
- In-batch dedup: all 9 submitted observations have unique key fields
  (short_url / term).

## Verdicts carried over from PROVENANCE.md (OBSERVED)

- uoft.me: live YOURLS 1.7.6, official UofT shortener, domain-whitelisted.
  All four known agent-grammar `+` stats pages return the YOURLS login
  wall ("Please log in") — negative for passive stats.
- t.mdcdev.me: live YOURLS 1.9.2, open-creation community instance.
  Public `+` stats open on live slugs; the three live slugs examined are
  SEO-spam (no agent-grammar slugs, no swarm-toolkit referrers) —
  negative for swarm activity.
- crt.sh: 126 certificates for `%.uoft.me` (Let's Encrypt), not-before
  range 2018-10-01T18:37:40 to 2026-09-02T07:01:19.

## Interpretation (INFERENCE)

- The lane is a clean negative: two live shortener instances, zero
  agent-grammar or swarm-toolkit activity observed through passive recon.
- Agent-grammar slugs on uoft.me (maagentxyz99999, zzagent740558,
  amass932899504, mafresh91011) are known from
  joshuadavid/wikiagentswarminvestigation `agent-logs/shorteners/uoft-me`
  (UPSTREAM citation, bodies not pulled from that repo).
