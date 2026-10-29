# PROVENANCE — VULONE AI-agent campaign lead (india-cert-in lane)

All captures are passive GET (curl or read-only APIs). No POST, no login, no session, no interaction.

## Primary sources

| File | Source URL | Retrieved (UTC) | Method | sha256 |
|---|---|---|---|---|
| vulone-primary-report.html | https://vulone.com/blog/a-china-linked-operator-used-ai-agents-to-attack-governments-across-asia | 2026-10-23T11:54:35Z | curl -sSL GET, UA Chrome/120 Linux | c277b12d1d7021308f410d69bebeabc605b8d0a299aaebce36b60cc9a2a27d72 |
| vulone-report.html | https://safeguard.sh/resources/blog/ai-agent-intrusion-campaign-asia-48-targets | 2026-10-23T11:52:45Z | curl -sSL GET, UA Chrome/120 Linux | 4eea10daa98acc6df66303a79a09fc2493ea44c315bfa922939ed8a87eb5f1a5 |
| securityonline-coverage.html | https://securityonline.info/ai-driven-hacking-campaign-asia/ | 2026-10-23T11:54:35Z | curl -sSL GET, UA Chrome/120 Linux | fad5274c7a6e1f1dbc3dcb13f4be9189de68a67671781defc74c02df9dd7f3e5 |

Derived text files (vulone-primary-report.txt, vulone-report.txt, securityonline-coverage.txt) are HTML-to-text extractions of the above, made with python3 (tag strip), same session.

## Passive infrastructure observations

| File | Method | Retrieved (UTC) | Note |
|---|---|---|---|
| shodan-202.61.139.15.txt + -slim.txt | `custom.legacy-shodan` shodan.py host (passive API) | 2026-10-23T11:53Z | --full dump contains two concatenated JSON objects and one truncated `tcp.raw` string (connector output artifact; field values quoted in the memo are from intact sections) |
| shodan-202.61.139.137.txt + -slim.txt | `custom.legacy-shodan` shodan.py host (passive API) | 2026-10-23T11:53–11:55Z | --full dump shows only port 22 (SSH); slim record carries the historical service list |
| otx-202.61.139.15.json | curl GET keyless OTX indicator API | 2026-10-23T11:54:17Z | HTTP 200 |
| otx-202.61.139.137.json | curl GET keyless OTX indicator API | 2026-10-23T11:54:2xZ | HTTP 200 |

## Direct probe (single, passive)

- `curl GET http://202.61.139.15:9000/` on 2026-10-23T11:53:12Z: HTTP 000 (connection failed / timeout after 10.4 s). One attempt only; not retried.
- No probe of cdac.in. No WSO2 console access. No login attempts anywhere.
