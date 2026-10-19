# FALSE-POSITIVES — Lane 10: Shodan harness scanner

This file lists the noise the Shodan harness scanner will see. A
banner-count change is not evidence of malicious activity until it
is corroborated: new panels must be profiled (open vs login-gated),
and Counsel must clear the host before any deeper collection.

## Count volatility (the dominant noise)

Shodan re-scans on its own schedule. A count of 223 today can be 210
or 240 tomorrow with no real-world change: hosts go dark, DHCP
reassigns IPs, Shodan's own coverage shifts. Small deltas (+/- 10%)
are normal churn. Treat them as coverage notes, not findings. Large
or sustained deltas deserve a look.

## Product fingerprint false positives

`product:"Hermes Agent"` fires on renamed and localized builds
("ATUM Sovereign", "Meccano Agent", "Hermix Agent", Chinese/Korean/
Russian titles). Some of these are forks, demos, or unrelated
software that shares a banner string. The 2026-10-19 hunt found 23
fetched pages that were not panels at all (a French landing-page
farm, a security-company site, a Wix business page). A count
includes these until a profile pass excludes them.

## Honeypots and research scanners

Security researchers run honeypots that mimic agent panels, and
Shodan itself is a scanner. A new banner may be a honeypot, a
researcher's intentionally exposed instance, or a red-team range.
An open panel is not proof of crime. The hunt scope is agents and
agent infrastructure; Counsel grades each host before any claim.

## Shodan API limitations

`/shodan/host/search` returns empty on the current plan, so this
module tracks counts only. A count change cannot name the new or
departed hosts. Do not claim "N new panels appeared" with host
detail you do not have. The hit records the delta and the query;
host-level attribution requires the search endpoint or a
follow-up `/shodan/host/{ip}` pass.

The Hermes product set is partial (4,200 of ~5,499 banners seen;
pagination stopped ~page 41). Counts for that query understate the
true exposure. Note the gap; do not treat the count as complete.

## Login-gated vs open

Most panels in the inventory are login-gated (2,648 of 3,354 in the
2026-10-19 hunt). A count change dominated by login-gated hosts is
less urgent than one dominated by open dashboards. The count query
cannot distinguish them; the profile pass can.

## Triage rule

Keep a hit only if the count delta is large (>10%), sustained across
two runs, or concentrated in a query tied to an active investigation.
Small churn is logged, not alerted. Every count-change hit needs a
follow-up profile pass before any maliciousness claim.
