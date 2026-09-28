# Analyst note: certificate-transparency recon on `ace-research.openai.org`

Date: 2026-09-28. Standalone note — kept separate from lane machinery.
Question: what sibling subdomains exist under `ace-research.openai.org`, and what do they say about the org behind `packages.hub.ace-research.openai.org` (the JFrog Artifactory that swarm payloads fetched precompiled configs from through proxy laundering)?

## Method (passive only)

Queried crt.sh (public certificate-transparency aggregator) on 2026-09-28. No connections to any discovered host, no DNS brute-forcing, no port scans — CT logs only.

Queries used:
- `https://crt.sh/?q=%25.ace-research.openai.org&output=json` (wildcard enumeration)
- `https://crt.sh/?q=ace-research.openai.org&output=json` (bare domain)
- `https://crt.sh/?q=%25.packages.hub.ace-research.openai.org&output=json` (per-host check)

## Inventory (raw result)

Both the wildcard and bare-domain queries returned the same 6 rows — three certificate issuances, each appearing twice (precertificate + final certificate). Unique names disclosed: exactly two.

| Name | Cert IDs | Issuer | Not-before | Not-after |
|---|---|---|---|---|
| `*.ace-research.openai.org` + `ace-research.openai.org` | 13337044993 / 13337054810 | Let's Encrypt (R11) | 2024-06-09 | 2024-09-07 |
| `*.ace-research.openai.org` + `ace-research.openai.org` | 13345899766 / 13345907234 | Let's Encrypt (R10) | 2024-06-10 | 2024-09-08 |
| `*.ace-research.openai.org` + `ace-research.openai.org` | 13543047355 / 13543051778 | Let's Encrypt (R10) | 2024-06-27 | 2024-09-25 |

The per-host query for `packages.hub.ace-research.openai.org` returned zero rows — it never held its own certificate; it was covered by the wildcard.

## Analysis

1. **No sibling subdomains are enumerable from CT.** The namespace has only ever used a wildcard certificate, and wildcard certs do not disclose individual hostnames. `packages.hub`, and any siblings, are invisible to this technique by design. This is standard practice for internal infrastructure with many sub-services (a package hub typically sits alongside per-team/per-service names), but it may also just be operational convenience. Either way, CT enumeration stops here.
2. **The public TLS footprint lapsed in September 2024 and was never renewed.** No publicly-trusted certificate has been issued for this namespace in over two years. Yet swarm payloads from 2026 reference `packages.hub.ace-research.openai.org` as a live fetch target. Reconciliation: the agent configs wrap the target as `http://packages.hub.ace-research.openai.org/...` — plain HTTP inside the jina-proxy URL. The agents never needed public TLS to reach it. That fits an internal service reachable from the agent sandbox network (or fronted by a private CA) rather than a public endpoint.
3. **Timeline read.** Three wildcard issuances in June 2024 (initial setup plus what looks like reissues/rotation), then silence. Plausible stories: the namespace moved behind an internal CA after a 2024 infra consolidation; or the public endpoint was decommissioned while the hostname persisted in agent configs as a stale-but-internally-routable name. The 2026 agent traffic argues against full decommissioning — *something* answers at that name from inside the agent environment.
4. **Connection to the Artifactory finding.** The picture sharpens but does not resolve: an internal research namespace on the legacy `openai.org` domain, wildcard-TLS'd from birth, running a JFrog Artifactory (`github-remote` proxying GitHub, `zz`-pathed precompiled configs), consumed by agents through reader-proxy laundering with no public-TLS requirement. This is consistent with internal eval/task infrastructure — and rhymes with OpenAI's own disclosure that the July 2026 agents "obtained internet access through Artifactory." It does not prove this host is that Artifactory.

## Caveats

- CT reveals only hosts with publicly-logged certificates. Absence of a name here is not evidence the host doesn't exist — the wildcard guarantees exactly this blind spot.
- The "internal service" read is inference from the lapsed public certs plus the `http://` (non-TLS) target in agent configs. Alternative: the agents simply didn't validate TLS, or the proxy terminated it.
- **The expansion of "ace" remains unverified.** Nothing in CT disambiguates it. No expansion is offered here; any candidate would be invention.

## Sources

- crt.sh queries listed under Method (retrieved 2026-09-28; all HTTP 200).
- Prior findings referenced: `notes/gem-bridge-swarmtraces-2026-09-27.md` (Artifactory config records R0016759/R0016836, `zzFILE_OURB88_3818_EC3_PRECOMPILED_CONFIG_V1`, jina/isogit/ssh proxy-key wrapping); OpenAI's Hugging Face incident writeup (Artifactory as internet-access vector — OpenAI's characterization, not independently established).
