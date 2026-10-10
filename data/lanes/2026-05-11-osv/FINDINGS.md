# Findings — 2026-05-11 OSV sweep

OBSERVED: 717 of 1,284 swept campaign gems were present in Diffend
(first-publish 2026-05-11 19:40 → 2026-05-12 07:47 UTC); 566 were absent
on all passes (one more, `slvhg151`, was deduped against an existing
richer record).

OBSERVED: present gems carry `go-import` mechanism notes (vcs=unknown,
396; vcs=hg, 8) and `jina-laundered` (229) / `empty-summary` (262)
markers, matching the rubygems-goimport-campaign profile.

UPSTREAM: 7 campaign gems have OSV `MAL-*` advisories (all published
2026-07-07, CWE-506 embedded malicious code): zzjinavcsgit
(MAL-2026-9952), zzjinavcsbzr (MAL-2026-9950), probejiqptzco
(MAL-2026-8427), uxjinalamb2 (MAL-2026-9062), wandsworthprobe1778551714
(MAL-2026-9296), prx1b49033905 (MAL-2026-8456), trya1zz (MAL-2026-9003).

OBSERVED: the July-7 XSS/SSTI wave has zero advisories anywhere across
3,000 reviewed rubygems malware advisories — the least-covered wave.

UPSTREAM: GHSA-9j48-x3c3-mrp2 — RubyGems legacy API-key leak via improper
CDN cache config (introduced 2016-10-10, fixed 2026-07-09, keys revoked
2026-07-23, CVSS 7.2–7.3, affects gem < 3.2.0). Not in OSV (404 on
`/v1/vulns` during Lane 19).

INFERENCE: the retry pass changed 324 gems from absent to present,
so single-pass absence in this sweep is not proof a gem never existed —
only the final merged view is safe to cite.
