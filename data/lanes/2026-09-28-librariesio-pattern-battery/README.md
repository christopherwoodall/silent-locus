# 2026-09-28-librariesio-pattern-battery: libraries.io mirror battery of the gem-hunt campaign (2,698 names checked)

**Lane status:** ingested into Factum 2026-10-09. Legacy directory renamed to
`evidence/remove-2026-09-28-librariesio-pattern-battery/`.

## What this lane did

On 2026-09-28 a grammar battery ran against libraries.io's RubyGems mirror.
It checked 2,698 campaign-related package names with direct project-page fetches
and mechanism-marker greps over descriptions. No login or API key was used.

| Battery | Checked | Found live |
|---|---|---|
| `try[a-z][0-9]zz` unseen combos | 231 | 0 |
| JFrog grammar names | 648 | 455 |
| JFrog non-grammar rest | 1,819 | 1,154 |
| **Total** | **2,698** | **1,609** |

1,191 of the live pages carry go-import payloads in their descriptions.

## Key results

- libraries.io is a partial but verbatim mirror of the campaign (report
  `observation_80bec6869b9c4972a98108fd0449f096`).
- July-7 XSS/SSRF/tar/YAML red-team wave: 55 gems fully mirrored, atom-dated
  2026-07-07 03:30–06:15 UTC. Gem `apexblack-evidence-1783394610` admits the
  API-key mechanism (report `observation_c6dac38553584d96a1f5b5bb69d566d1`).
- oai echo-rig family: 123 gems dated 2026-05-11 09:50–10:35 UTC; go-import
  tags pointed at HTTP echo services to verify the fetch fires. Webhook.site
  callback `oaihx7579061` on May 11 — the webhook dead-drop lineage starts
  here, not in July (reports `observation_04be81941b78488698b425430b22acd3`,
  dead drop `observation_54c16d6cf4b244428d38706e6882259d`).
- Timeline pushed back: May 8 (Drive targets), May 9 (XSS+go-import hybrid),
  May 11 (echo rig rehearsal), May 12 (main burst), June 18 (link-posting),
  July 7 (red-team) (reports `observation_2e2cf223435f4bec8e864755a7a92841`,
  `observation_ce75dad860304f7da0e32eb297bde6d5`).
- June-18 wave: 55 gems (`00proxy`/`00prx`/`-00` families), innocuous
  descriptions (report `observation_73bf6f07c0044a70a840d184cde8fe73`).
- tryzz namespace exhausted: 0/231 unseen combos (report
  `observation_4f96d285e0a1408c94b41d612fac3087`).
- libraries.io exposes no author field anywhere; 45 "Testing …" description
  markers found (report `observation_d0f27a648031415c8883a07fed7ec18b`).
- Sweep negative: zero hits for `web_hooks`, `oast.online`, `A000`, `ZZEND`
  across 1,912 descriptions — the southpxdatapp6pi zlib+base64 dead-drop is a
  Diffend-bytes-only technique (report `observation_be2085d3bc134de7b240031105cab044`;
  IOCs `observation_648b610a79e7452aaeb9c6ec705962bd`,
  `observation_c9b7ef1e82f640d78d355894f6bd4778`,
  `observation_e39a80a05de3402b9597c392e81a19b2`,
  `observation_b0f9cccb879f44018a6b958a49f95f33`).

## Caveats

- libraries.io is a partial mirror: 1,115/3,027 names missing (May-12 burst
  time-freeze effect).
- "Testing " description markers are operator-written labels, not author metadata.
- `versions.atom` `<published>` entries are the version publish dates used.
- Broad pattern search across all of libraries.io needs login/API credentials
  (not pursued). The oai family per the July-18 advisory is 206 names vs 141
  in the JFrog CSV; the delta list is not in hand.

## Files

- `raw/gem-hunt-pattern-battery-2026-09-28.md` — the full battery note (source).
- `LEGACY_PROVENANCE.md` — provenance as recorded before ingest.
- `events.jsonl`, `SHA256SUMS` — legacy lane records, kept as reference.
- `PROVENANCE.md`, `FINDINGS.md` — lane-level working documents.
