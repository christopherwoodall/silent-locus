# Transluce finding #178 — provenance

Tracker finding #178, submitted 2026-10-14T06:25:03+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/178`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/178`
- Retrieved: 2026-10-14T11:57:40Z (UTC)
- Method: `tl.py finding 178` via the `custom.transluce` connector
  (Secure Vault bearer <redacted>), run by the `lab-intel-transluce-scan` hook;
  verified verbatim against the 2026-10-14 08:40 CDT scan census pull.
- sha256: `8966108c3938ce84144cf2d81ff3002082a672bad2d737371e0b506f0267f159`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-178_20261014T115740Z.json`
  (with `.sha256` and `.PROVENANCE.txt`), copied here to `raw/` for lane
  self-containment.

## Content

Summary: "May 11, 2026 archive records show BGSU library retrieval and backend-port/routing probes through proxies. Public catalogue content was returned; successful bypass, private-data access and AI authorship are unproven."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `fetch-proxy-abuse` — 169 of 170 Arquivo captures ran through r.jina.ai (1 through markdown.new); actor unknown, AI authorship unproven.
2. `backend-port-probing` — five captures hit lib.bgsu.edu ports 8089/8081 and 129.1.14.56:8089/version; indexed proxy status 422; service exposure unconfirmed.
3. `url-routing-probes` — 72 URLs vary routes around container identifier 8059 (case, scheme, slashes, query values, nesting); bypass intent uncertain.

Finding evidence links:

- `https://arquivo.pt/wayback/20260511183247id_/https://r.jina.ai/http://lib.bgsu.edu:8089/repositories/3/resources`
- `https://arquivo.pt/wayback/20260511183303id_/https://r.jina.ai/http://129.1.14.56:8089/version`
- `https://arquivo.pt/wayback/20260511183409id_/https://r.jina.ai/https://lib.bgsu.edu/robots.txt`
- `https://arquivo.pt/wayback/20260511183620id_/https://r.jina.ai/https://lib.bgsu.edu/findingaids/repositories/3/resources/768`
- `https://arquivo.pt/wayback/20260511192924id_/https://r.jina.ai/https://lib.bgsu.edu/findingaids/repositories/3/top_containers;/8059`
- `https://docs.archivesspace.org/api/`
- `https://github.com/archivesspace/archivesspace/blob/master/common/config/config-defaults.rb`
- `https://rdap.arin.net/registry/ip/129.1.14.56`
