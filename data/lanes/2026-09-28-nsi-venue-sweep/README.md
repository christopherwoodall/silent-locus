# nsi-venue-sweep

National-stats venue pattern sweep, lane run 2026-09-28.

Question: does the swarm drink from other national statistical institute
endpoints beyond the known ones (Vietnam GSO PX-Web, Iceland PX-Web, UK ONS,
US Census/DataUSA)?

Method: corpus domain census over 679 unique domains, read-only live probes
of candidate API roots, bounded negative sweeps. See PROVENANCE.md.

Result: 12 legacy events ingested into Factum (2026-10-09):

- 7 `infra.ioc` (category domain, status active): stats API task venues —
  datasets.cbs.nl, unctadstat-api.unctad.org, site-test.nsi.bg (corpus venue
  plus live-header venue-model refinement), tigerweb.geo.census.gov,
  api.usaspending.gov, pxweb.gso.gov.vn. All tagged
  `{"lane": "nsi-venue-sweep"}`, grade OBSERVED (refinement record INFERENCE).
- 2 `reachability.check`: live read-only probes, GET, outcome response,
  HTTP 200 — datasets.cbs.nl OData root, UNCTADstat reportMetadata endpoint.
- 3 `intel.report` (lab swarm-hunt): bounded negatives — zero corpus hits
  for other national PX-Web deployments (8 hosts), zero new jina-laundered
  stats venues, zero headline-economics API hits (9 checked).

Source bytes preserved: PROVENANCE.md, SHA256SUMS, build_dataset.py,
events.jsonl (moved from evidence/2026-09-28-nsi-venue-sweep/).

Factum record IDs:
- obs-00 observation_b0ac6506f69b473fbb521adaf36a3bca (datasets.cbs.nl venue)
- obs-01 observation_e2720f030f324d10a71b7768dd8beb62 (CBS probe)
- obs-02 observation_18b22683cc6e4849a9d4425d7a24b12d (UNCTADstat venue)
- obs-03 observation_bab607936611440ba7d46a4c93c7d914 (UNCTADstat probe)
- obs-04 observation_2572a455f47f4eb389169ff6b6a5563e (site-test.nsi.bg venue)
- obs-05 observation_5e4cf85f11374550afe2c1cffac4b7e2 (venue-model refinement, INFERENCE)
- obs-06 observation_0fb2d505424343ada7584a21afb434be (tigerweb venue)
- obs-07 observation_cb0e394918ff4ebdb7d1a1b5a84e63c2 (usaspending venue)
- obs-08 observation_cff9f55df3694910913d32eb39a36775 (pxweb.gso.gov.vn)
- obs-09 observation_f4144a5efe3a4ecb8f5660b25bf3ed12 (PX-Web negative)
- obs-10 observation_7f710beb58f7497db96af540fd979f02 (jina negative)
- obs-11 observation_4afbe45070a248509e673d8467b28312 (headline-APIs negative)

Lane ID: lane_3898163249ab47a8935d38418681ba23.
