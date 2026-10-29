# FALSE-POSITIVES — Lane 8: crt.sh scanner

This file lists the noise the crt.sh scanner will see. A new cert is not
evidence of the fleet until it ties to the fleet's proxy domain
(`hysandbox.tencent-cloud.com` in the SAN list) or to Tencent-issued
agent-sandbox-like names.

## Noisy wildcard patterns

- `%hy3%` and `%hy4%` match a very large number of unrelated certs.
  "hy3" / "hy4" are short letter-number pairs that collide with many
  random hostnames. The scanner keeps only certs where "tencent" appears
  in the issuer name or the SAN list, and caps each pattern at the 500
  newest certs. Even then, expect manual triage.
- A cert with `tencent-cloud.com` in the SAN is routine. Tencent issues
  and uses certs all the time. Only the `hysandbox*` SAN form ties a cert
  to the fleet proxy.

## What "tied to the fleet" means

The known fleet cert: CN `*.hysandbox.tencent-cloud.com`, DigiCert,
issued 2026-08-18, serial `040b3c091fd4e4d8ccff7b8fe33b7979`. The scanner
never reports this serial. A new cert counts as fleet-linked if it has a
`hysandbox.tencent-cloud.com` (or `hysandbox-ats`) SAN and a Tencent /
DigiCert-for-Tencent lineage. Grade those HIGH. Grade Tencent-filtered
hy3/hy4 hits MEDIUM until a sandbox link is shown.

## crt.sh lag

crt.sh `entry_timestamp` can trail the cert `not_before` date by days or
weeks. "No new certs in the window" means "no new crt.sh entries", not
"no new certs exist". Absence is weak evidence.

## Rate limiting

crt.sh rate-limits aggressively (HTTP 429 seen 2026-10-14 from shared
egress). The scanner sleeps 10 s between patterns and aborts the run on a
429. A 429 abort is a gap in coverage, not a clean result. Re-run later.

## Triage rule

Keep a hit only if the SAN list or the filtered issuer ties it to Tencent
sandbox infrastructure. Bare hy3/hy4 matches without a Tencent link are
noise and the scanner drops them.
