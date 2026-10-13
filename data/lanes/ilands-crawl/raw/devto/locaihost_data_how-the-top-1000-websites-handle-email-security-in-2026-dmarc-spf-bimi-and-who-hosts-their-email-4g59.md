---
title: How the top 1,000 websites handle email security in 2026: DMARC, SPF, BIMI and who hosts their email
url: https://dev.to/locaihost_data/how-the-top-1000-websites-handle-email-security-in-2026-dmarc-spf-bimi-and-who-hosts-their-email-4g59
published_at: 2026-10-10T14:47:39Z
edited_at: 2026-10-11T02:53:05Z
author: locaihost_data
tags: security, email, dns, data
reactions: public=1 positive=1 comments=0
---

---
title: "How the top 1,000 websites handle email security in 2026: DMARC, SPF, BIMI and who hosts their email"
published: true
description: "We checked the DNS of the 1,000 most popular websites. 85% publish DMARC, 47% reject spoofed mail, 21% show a BIMI logo, and Google hosts over a third."
tags: security, email, dns, data
canonical_url: https://locaihost.org/blog/email-security-top-1000/
---

Anyone can put any domain in the From line of an email. Three DNS records decide whether the receiving server believes it. SPF lists the servers allowed to send for a domain. DMARC tells receivers what to do when a message fails those checks: nothing (`p=none`), send it to spam (`p=quarantine`) or refuse it (`p=reject`). BIMI then lets a domain that enforces DMARC show its logo in the inbox.

Since February 2024, Google and Yahoo have required DMARC from anyone sending them bulk mail, so most large senders have published something. We wanted to know what they published. On 10 October 2026 we looked up the email DNS of the 1,000 most popular websites on the Tranco list (list `8PX5V`) and recorded their policies and their mail hosts.

Five findings:

- **85% publish DMARC, but only 69% enforce it.** 84.5% of the 1,000 domains have a DMARC record. 69.4% set it to quarantine or reject for all mail, and 47.4% reject outright. The other 13.6% publish `p=none`, which only monitors.
- **Rank matters a little.** 62% of the top 100 reject spoofed mail, against 46% of domains ranked 101–1,000.
- **SPF is almost universal and usually strict.** 89.6% publish SPF. Of those, 53.8% end it with `-all` (hard fail) and 40.4% with `~all` (soft fail).
- **BIMI has taken off; MTA-STS hasn't.** 21.3% publish a BIMI record, against only 4.5% for MTA-STS, which forces encrypted delivery.
- **Google hosts more of this mail than anyone.** Of the 875 domains that accept mail, 37.3% use Google Workspace and 17.4% Microsoft 365. Proofpoint filters 9.0% before the mail reaches the mailbox.

## DMARC and SPF by rank

| Measure | Top 100 | 101–1,000 | All |
|---|---:|---:|---:|
| DMARC record | 87.0% | 84.2% | 84.5% |
| DMARC enforced | 76.0% | 68.7% | 69.4% |
| DMARC `p=reject` | 62.0% | 45.8% | 47.4% |
| SPF record | 93.0% | 89.2% | 89.6% |
| BIMI record | 27.0% | 20.7% | 21.3% |
| MTA-STS policy | 11.0% | 3.8% | 4.5% |

*"Enforced" means quarantine or reject, applied to 100% of mail. Rank is the position among the 1,000 domains we kept, in Tranco order.*

Across all 1,000 domains, the DMARC policy split was 474 at reject, 235 at quarantine and 136 at `none`. 155 had no record. Few hedged: only 15 of the 845 records (1.8%) applied their policy to less than 100% of mail. 24 (2.8%) rejected spoofs of the main domain but used a weaker policy for its subdomains.

A `p=none` record is usually a first step. A domain watches the reports, finds its legitimate senders, then tightens the policy. Most of the 136 `p=none` domains are doing that: 85% of them ask for aggregate reports. Some very large names are still there, though, including `samsung.com` and `yandex.ru`, and Microsoft's consumer mail domains `outlook.com`, `live.com` and `msn.com`. For consumer mailbox domains, `p=none` is often deliberate. Mailing lists and forwarding break authentication, and a strict policy would bounce real mail. A company domain doesn't have that excuse.

The SPF split matters less than it looks. Under DMARC, a receiver judges a message by the DMARC result, so `-all` versus `~all` mostly matters to receivers that don't check DMARC. 37 domains (4.1% of those with SPF) have no `all` of their own and hand over to another record with `redirect=`, and 15 use the neutral `?all`. None of the 1,000 used `+all`, which would let any server send as the domain.

## Who hosts the mail

Of the 1,000 domains, 875 have an MX record, so they accept mail. The rest are mostly link shorteners, download hosts and developer infrastructure.

| Mailbox host | Domains | Share |
|---|---:|---:|
| Google Workspace | 326 | 37.3% |
| Microsoft 365 | 152 | 17.4% |
| Own mail servers | 147 | 16.8% |
| Unrecognised MX host | 105 | 12.0% |
| Gateway, mailbox hidden | 81 | 9.3% |
| Amazon WorkMail / SES | 13 | 1.5% |
| Tencent Exmail | 8 | 0.9% |
| Alibaba Mail, Yandex 360 | 6 each | 0.7% each |
| Zoho Mail | 5 | 0.6% |
| Other named providers (12) | 26 | 3.0% |

*Base: the 875 domains that accept mail. "Own mail servers" means MX hosts under the domain's own name. Google's and Microsoft's own domains count under their own services.*

The rows that are not Google or Microsoft deserve a closer look. "Own mail servers" means the MX host is under the domain's own name, as with `apple.com` and `paypal.com`. Most of the "unrecognised" group is the same thing one step removed. `imdb.com` receives mail on `amazon.com` servers, `webex.com` on `cisco.com` servers and `vk.com` on `mail.ru` servers. Together, the two groups make up 28.8% of the domains that accept mail.

In front of the mailbox, 124 domains (14.2% of those accepting mail) use a security gateway that filters inbound mail first:

| Inbound gateway | Domains | Share of the 875 |
|---|---:|---:|
| Proofpoint | 79 | 9.0% |
| Mimecast | 24 | 2.7% |
| Cisco Secure Email | 11 | 1.3% |
| Five others | 10 | 1.1% |
| None detected | 751 | 85.8% |

*The five others: Broadcom and Trend Micro (3 each), Barracuda (2), Sophos and Hornetsecurity (1 each).*

Behind those gateways, SPF identifies the mailbox in 43 of the 124 cases: 24 use Microsoft 365 and 19 Google Workspace. The rest list only the gateway or their own servers in SPF, so the mailbox host stays hidden.

## Who enforces DMARC

Enforcement differs by mail host. Domains on Google Workspace enforce DMARC more often than those on Microsoft 365. Domains behind a gateway enforce it most often. This is a correlation, not a cause: buying Proofpoint and setting `p=reject` both point to a company with a dedicated email-security team.

| Mail host | Domains | DMARC enforced |
|---|---:|---:|
| Gateway, mailbox hidden | 81 | 86.4% |
| Google Workspace | 326 | 82.2% |
| Microsoft 365 | 152 | 72.4% |
| Unrecognised MX host | 105 | 67.6% |
| Own mail servers | 147 | 66.7% |
| No MX (accepts no mail) | 125 | 37.6% |

The last row is the weakest point. A domain that never sends mail can still be forged, and attackers like such domains because nobody watches them. The standard lock-down is two records: `v=spf1 -all` (no server may send) and DMARC `p=reject`. Only 31 of the 125 non-mail domains (24.8%) have both. 76 (60.8%) have either no DMARC record or `p=none`.

By top-level domain, `.com` led: 75.0% of its 596 domains enforce DMARC and 51.0% reject. Country-code domains followed at 63.5% (159 domains), then government, education and international bodies at 60.0% (35), and `.org` and `.net` at 57.0% (128).

## Who reads the reports

DMARC lets a domain ask receivers for daily aggregate reports (the `rua` tag). 91.5% of DMARC records ask for them. 63.6% send them to an outside service, usually a vendor that turns the XML into dashboards. Counting each domain once per vendor:

| Report receiver | Domains |
|---|---:|
| Valimail (`vali.email`) | 74 |
| Proofpoint | 71 |
| dmarcian | 55 |
| Agari (Fortra) | 29 |
| Mimecast DMARC Analyzer | 28 |
| Cloudflare | 26 |
| Red Sift OnDMARC | 22 |
| Postmark | 22 |

13 domains send their reports to `dhs.gov`, the collection point used by US federal civilian agencies. 11 of them are agencies such as `nasa.gov` and `whitehouse.gov`, and the other two are the companies Box and Dynatrace. Another 22 report to `google.com`, all of them Google properties such as `youtube.com` and `android.com`.

## DNS and CDN

The same lookups show who runs the infrastructure. AWS Route 53 answers DNS for 24.6% of the 1,000 domains. Cloudflare answers for 16.3%, and 15.7% run their own name servers. Akamai answers for 9.4% and NS1 for 4.4%. 31.2% publish a CAA record that limits which certificate authorities may issue for them. Of the 902 domains with a homepage, Cloudflare serves 25.7%, Akamai and Amazon CloudFront 14.1% each, and Fastly 9.0%. We detected no CDN for the other 33.8%.

## Methodology and caveats

- **Domains.** Tranco list [`8PX5V`](https://tranco-list.eu/list/8PX5V/1000000), generated 9 October 2026 from 30 days (10 September to 9 October) of Chrome UX Report, Farsight, Majestic, Cloudflare Radar and Cisco Umbrella data, as registrable domains. We removed 73 infrastructure host names listed by hand (CDN, API and telemetry domains such as `gstatic.com` and `akamaiedge.net`). We then dropped any domain that neither served a homepage nor had an MX record: 197 more, mostly CDN and device-telemetry hosts. A homepage behind a bot wall (HTTP 401, 403 or 429) counts as served. The first 1,000 remaining domains, down to Tranco rank 1,272, are the sample. The script lists every exclusion.
- **Snapshot.** All lookups ran on 10 October 2026, 14:03–14:40 UTC, from Apify's cloud. DNS records change, so this is one day's picture.
- **What "detected" means.** A record counts if it exists in public DNS and parses: SPF is a `v=spf1` TXT record at the domain, DMARC a `v=DMARC1` record at `_dmarc`, BIMI a `v=BIMI1` record at `default._bimi`, MTA-STS a `v=STSv1` record at `_mta-sts`. We didn't check BIMI logos or certificates, and we didn't fetch MTA-STS policy files. Mail hosts and gateways are matched from MX host names, and from SPF includes when a gateway hides the mailbox. A host we have no rule for is reported as unrecognised, not guessed. Domains with a null MX (RFC 7505) count as having no MX.
- **Cross-check.** About an hour after the run, we re-resolved MX, SPF, DMARC and BIMI for all 1,298 domains through public resolvers. The results disagreed on 7 MX answers (all of them null MX, which the two tools count differently), 2 SPF records, 2 DMARC policies and no BIMI records. One domain, `indeed.com`, answered our cloud resolver with `0.0.0.0` and no MX. It was therefore dropped from the sample, though it does accept mail.
- **Reproducible.** Four Node.js scripts [fetch the list](https://locaihost.org/blog/email-security-top-1000/analysis/email-security-2026-fetch.mjs), [run the lookups](https://locaihost.org/blog/email-security-top-1000/analysis/email-security-2026-run.mjs), [compute every figure](https://locaihost.org/blog/email-security-top-1000/analysis/email-security-2026.mjs) ([results.json](https://locaihost.org/blog/email-security-top-1000/analysis/results.json)) and [run the cross-check](https://locaihost.org/blog/email-security-top-1000/analysis/email-security-2026-check.mjs). We use only company domains, and we collect no personal data. Report addresses are reduced to the receiving domain.

*Source: Tranco list 8PX5V (tranco-list.eu); DNS, HTTP and TLS lookups by locaihost data, 10 October 2026.*

---

The data came from our [Domain Intel Actor](https://apify.com/locaihost/domain-intel) on Apify, which returns these fields (email host, gateway, SPF, DMARC, BIMI, MTA-STS, DNS, CDN, TLS) for any list of domains. To check your own suppliers, customers or portfolio the same way, it costs $3 per 1,000 domains.
