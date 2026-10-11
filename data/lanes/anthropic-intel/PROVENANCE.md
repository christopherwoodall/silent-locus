# Provenance

Source: Anthropic research report, 2026-10-09.
URL: https://www.anthropic.com/research/investigating-unintended-model-actions
Retrieved 2026-10-09 via browser fetch (see legacy-PROVENANCE.md).

Factum records (batch 53886de8135e4968896f5b3f075164c7):

- source_fc3aa052bf7c4512b0c8798ac7c5afa6 — the report URL.
- observation_08d649fd89844c69a1734a19e163b897 — intel.report.
- observation_56fd5cf66a1d4d61b62604df2b49fd5b — intel.behavior
  software-flaw-exploitation.
- observation_2e3120d372704d1fb61703c22e24be69 — intel.behavior
  unauthorized-form-submission.
- observation_6222c00dcf624fd0941d76ca050e0194 — intel.behavior
  restriction-circumvention.
- observation_2a063d865aec4ae481b73989851eebe1 — intel.behavior
  url-shortener-abuse.
- observation_e27d24f9bbb8408bb07306068827ce36 — intel.ttp sql-injection-via-url.
- observation_f08b78a060f242399a839f4f2abf02bb — intel.ttp
  token-extraction-from-client-config.
- observation_b2ba7274275846b18d9a2831d0770d9f — intel.ttp url-shortener-abuse.
- observation_4957811d3a994beeb4bceced108358fc — intel.ttp form-auto-submission.

Category definitions: docs/taxonomy/behavior-categories.md and
docs/taxonomy/ttp-taxonomy.md.

## IP-range mining (2026-10-10, provider egress fleet)

Provider: Anthropic. Official page: "IP addresses" (Claude Platform Docs).

- URL: https://platform.claude.com/docs/en/api/ip-addresses
  (identical content at https://docs.anthropic.com/en/api/ip-addresses)
- Retrieved: 2026-10-11T01:05:18Z via curl (HTTP 200, 316578 bytes).
- Raw cached: raw/anthropic-ip-addresses-20261010.html
- sha256: 674ae88addab3ab7826e80adbae3438d0c85cb6145c01e7496b67d49e9794ab0
- trust.anthropic.com (Vanta-hosted trust center, fetched 2026-10-11): no
  IP/egress section found. docs.anthropic.com searched for "IP allowlist" /
  "egress" — the canonical page is the one above.

Ranges extracted verbatim from page bytes:
- Inbound IPv4: 160.79.104.0/23 (active)
- Inbound IPv6: 2607:6bc0::/48 (active)
- Outbound IPv4: 160.79.104.0/21 (active; used for MCP tool calls)
- Phased out (no longer in use, status retired): 34.162.46.92/32,
  34.162.102.82/32, 34.162.136.91/32, 34.162.142.92/32, 34.162.183.95/32

Overlap check vs rmn.re Aug-Sep 2026 burst-creator corpus IPs
(185.228.3.86, 185.228.3.47, 185.228.3.66, 105.71.5.91, 45.130.202.7,
159.26.105.49): NONE inside any extracted range (clean negative, computed
with ipaddress module, 2026-10-11T01:37Z).

Records: 1 source + 8 infra.ioc (bundle-ip-ranges.json), all tagged
{"lane": "anthropic-intel"}, grade OBSERVED, basis upstream. No edges.
