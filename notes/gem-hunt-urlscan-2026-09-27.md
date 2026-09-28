# urlscan.io hunt — rubygems-goimport-campaign — 2026-09-27

**Verdict: the GemStuffer campaign is essentially invisible on urlscan.io, same as urlquery.** No scan captured the council calendar targets, the r.jina.ai-laundered URLs, the go-import payload tags, or the June wave's SEC payload. Read-only hunt via the public urlscan search API (no account), paced ~1 query/6–10s.

## Query battery results

| query | total | campaign-relevant |
|---|---|---|
| `domain:moderngov.lambeth.gov.uk` | 0 | — |
| `domain:democracy.wandsworth.gov.uk` | 0 | — |
| `domain:moderngov.southwark.gov.uk` | 1 | No — single scan 2020-12-14, unrelated PDF (`documents/s84625/Appendix 1 Draft Rooftop Homes Guide.pdf`), https://urlscan.io/result/b15f7684-ebad-466e-b1a6-0deeece95c11/ |
| `domain:www.southwark.gov.uk` | 73 | No — all generic homepage/service pages. One notable cluster: 4 homepage scans within 12 min on **2026-05-08** (3 days pre-burst), likely unrelated researcher recon of the council estate |
| `ip:20.49.140.101` | 25 | No — all generic Southwark estate pages 2021–2026 (services.southwark.gov.uk OAuth flows, forms.southwark.gov.uk, www.southwark.gov.uk, identity.onevault.digital). None touch `mgCalendarMonthView.aspx` or `mgWebService.asmx`. Confirms the IP is Southwark's web estate (consistent with the urlquery finding that it's their Azure front-end) |
| `domain:www.digitizationguidelines.gov` | 10 | No — generic homepage/file scans 2023–2026 |
| `domain:www.marinajacks.com` | 0 | — |
| `page.domain:r.jina.ai` | 64 | No — all generic reader usage (RSS feeds, arxiv, HN, weibo, substack). Zero council-wrapped URLs |
| `domain:r.jina.ai` (any reference) | 357 | No — top results are phishing kits that merely load r.jina.ai resources |
| `domain:s.jina.ai` | 11 | No — mostly the s.jina.ai homepage; one 2026-05-28 scan of an edgeone.app test site referencing it (incidental) |
| `page.url:"sec.gov/files/county.json"` | 0 | — (June wave payload: zero scans) |
| `filename:county.json` | 328 | No — generic county-government sites |

## Not supported / blocked

- `page.url:*go-import*` wildcard search → HTTP 403 from urlscan (pattern blocked). Web search for indexed urlscan pages mentioning go-import + rubygems → zero results.
- urlscan has no public page-content search; tag content inside scanned pages can't be queried directly.

## Takeaway

Two independent URL-scan lenses (urlquery's 18-query battery, this urlscan battery) both show the same thing: **nobody scanned the campaign's targets or payload URLs through public URL scanners.** The operator's infrastructure left no trace in either corpus. The 25 `ip:` hits usefully corroborate that 20.49.140.101 is genuinely Southwark's estate — the SSRF ladder's raw IP was real target infrastructure, not a decoy.

Raw query output: `/tmp/urlscan/domain_battery.json` (ephemeral).
