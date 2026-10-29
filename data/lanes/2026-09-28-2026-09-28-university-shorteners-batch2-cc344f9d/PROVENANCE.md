# Provenance

Lane ingested 2026-10-09 (UTC) from legacy
evidence/2026-09-28-university-shorteners-batch2/ (now
evidence/remove-2026-09-28-university-shorteners-batch2/; artifacts in
data/lanes/2026-09-28-university-shorteners-batch2/).

Export batch: data/records/1b5e6afc3c90458bbf1055c3d211e694
(20 records, all tagged {"lane": "2026-09-28-university-shorteners-batch2"}).

## Records

- source_7b153ae86c30486ca5f6d7f85d7b4dee — source: https://goto.unm.edu/vbudg+
- observation_0943dafad5f14359a197656697d8cedd — web.capture of the vbudg stats page (verbatim bytes in artifact_2457bc119d164c4d9b698037e483049f)
- observation_dc4a9d49e0de4bb09f1cb1ed59201583 — infra.shortcut: https://goto.unm.edu/vbudg → https://go-unm.my.salesforce-sites.com/events/targetX_eventsb__events#/esr?eid=a12TO000008O2H3YAK (control: 4 hits, no agent markers)
- observation_1bcfb1e584074813916a35363729b5d4 — reachability.check: https://2dd.pl/ (blocked, Cloudflare challenge)
- observation_b0dcdf78cb394cd1a87cfc6fe348040f — reachability.check: https://da.gd/ (200, no public stats surface)
- observation_290e7a03b42b4d3b9a851b73a42f9a59 — reachability.check: https://fooabc.com/ (dns_failure, host dead)
- observation_9851840aadc34c6cbbc4a80d7d5f4d6a — reachability.check: https://go.aim.edu/ (blocked, 403)
- observation_739e258bbffe42089e3147cc440cb116 — reachability.check: https://goto.ucr.edu/KB0011332+ (200, stats login-walled)
- observation_3453070f91de4cb7b7058a33416549d5 — reachability.check: https://is.gd/ (blocked, 403 for non-browser UA)
- observation_acb1ffa6ddab4bfd991e33a83bd0bd41 — reachability.check: https://lnk.mcla.edu/ (blocked, 403 campus firewall)
- observation_1ffd3d9f35b34c15a6c9cbca5f73e043 — reachability.check: https://mlc-wels.edu/ (200, not a shortener)

Pre-ingest dedup (2026-10-09): 10 fuzzy key-term matches against the corpus —
0 hits (fresh corpus, Phase 3 rebuild). Within-batch: 10 distinct target keys,
no duplicates.

Known source precision gap: the 8 negative probes carry date-only time
(2026-09-28); observed_at is midnight UTC with time_basis legacy_documented
and a time_precision tag. Only the vbudg probe logged an intraday time
(~04:05 CDT).
