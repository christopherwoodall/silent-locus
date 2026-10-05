# infra.md — candidate infrastructure log (c2-pattern-analyst)
# Format: timestamp | source | indicator | pivots | grade
# READ-ONLY: Shodan + public scan data. No live connections made.

2026-10-05T07:15Z | egress-check | api.shodan.io unreachable (curl timeout, also google.com) | n/a | INFRA-DOWN
2026-10-05T07:50Z | shodan http.title:"webhook.site" | 118.69.18.194:80 "Webhook.site Clone" + :8888 "AI Web Chat & Model Management" + :9090 VN login + :22 (AS18403 residential) | 4-svc same IP | GENUINELY NEW
2026-10-05T07:50Z | shodan http.title:"webhook.site" | gityzxmznuljhwtwvmo.spminstrument.com @104.26.0.130:443 (Cloudflare, scanned 2026-10-05) | 1 pivot | LEAD (ungraded)
2026-10-05T07:55Z | shodan http.html:"httpbun" | letss.win: 95.169.18.20:8443 Httpbun + :2083 Ncat proxy (AS25820); 207.57.145.214:8443 Httpbun + :22 (AS1054) | hostname+port+title x2 ASN | GENUINELY NEW cluster
2026-10-05T07:55Z | shodan http.html:"httpbun" | 62.234.187.97:8080 Httpbun + :3000 "New API" LLM gateway + :80 nginx (AS45090 Tencent Beijing) | 2-svc co-host | GENUINELY NEW
2026-10-05T07:55Z | shodan http.html:"httpbun" | 167.71.138.56 DigitalOcean homelab (NPM, Uptime Kuma, httpbin:8080) | n/a | NOT-AGENT (hobbyist)
