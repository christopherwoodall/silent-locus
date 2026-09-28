# PROVENANCE — university-shorteners-batch3 dataset

## Scope

Batch 3 (workstream B, 2026-09-28) sweeps NEW venues only — batches 1 and 2
(`data/university-shorteners/`, `data/university-shorteners-batch2/`) are
untouched. Source of candidates: (1) `go.uvm.edu` (University of Vermont
YOURLS) surfaced via a public URL-shortener blocklist (hagezi/dns-blocklists
issues) plus search-engine-indexed `~` preview pages; (2) three more blocklist
edu/community candidates (`go.sjf.edu`, `s.wnmu.edu`, `linktest.lse.ac.uk`);
(3) `test.yourls.org` (official YOURLS test instance, from Brausepulver's
`5_new_yourls_instances.md`); (4) `1aas.com` community YOURLS (web search).

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+` stats pages, `~`
  preview pages, front pages.
- Never: shortening/action/API-write endpoints, logins, form submissions,
  counter increments, mass target fetching, challenge solving.
- Slug sources: search-engine-indexed `~` pages (`-4s0q~`, `tgmtq~`) and
  UVM public docs / press (`xc26` from a 2026-09-26 news article;
  `may3`, `vtpitchchallenge`, `myuvm`, `sublet`, `phcourses`, `vk62t` from
  UVM KB/press pages — checked live, recorded in progress.log, not indexed).
  No slugs were guessed.
- Login-walled `+` stats (1aas.com) recorded and not bypassed.
  403/DNS-dead/retired hosts recorded as-is.

## Key finding / caveat

go.uvm.edu's PUBLIC stats pages expose traffic statistics and traffic
LOCATION only — the "Traffic Sources" (referrers) section is owner-only
(per UVM's own KB article `url-shortener-go-uvm-edu`, updated 2026-04-09,
which lists referrers under "View link statistics" requiring NetID+Duo).
So go.uvm.edu CONFIRMS the public-`+`-stats surface on a fourth university
instance but CANNOT leak the agent proxy-stack referrer fingerprint. It is
indexed as a control (public-stats venue, zero agent markers), not as a
fingerprint hit.

## Contents

- `go-uvm-edu/-4s0q_stats_2026-09-28.txt` — indexed `~` preview page slug,
  2013 library link, 266 hits all-time, zero markers.
- `go-uvm-edu/tgmtq_stats_2026-09-28.txt` — indexed `~` preview page slug,
  2013 security-blog link, 334 hits all-time, zero markers.
- `go-uvm-edu/xc26_stats_2026-09-28.txt` — freshest public slug found
  (created 2026-09-24), team-store link, 1 hit, zero markers.
- `negative-probes/*.txt` — 5 documented negatives.
- `university-shorteners-batch3.jsonl` — 3 Elastic-ready docs (the 3 UVM hits).
- `pattern-sweep.json` — per-file pattern-family sweep (all families empty).
- `SHA256SUMS` — checksums of every file above.
- `progress.log` — resumable run log.

## Elastic

Index `university-shorteners-batch3`, canonical shared schema
(notes/gems-es-mapping.json), `labels.shortener.scope` = university.
Negatives are documented here and in the notes report, not in Elastic
(same convention as batches 1 and 2).

## Guards honored

Read-only research only. No submissions/uploads/accounts/logins/posts/
counter increments/payload execution. Agents/infrastructure traces only —
no operator identity, registrant details, or person-focused attribution.
No credentials reproduced. No absolute home-directory paths in logs/docs.
