# PROVENANCE — Transluce finding #173 evidence (dead-drop follow-up)

Retrieval window: 2026-10-08 12:47–12:49 UTC (07:47–07:49 CDT). All
retrievals were read-only GET. No value is redacted. Hashes are in
SHA256SUMS.txt.

## urlquery public API (via ~/workspace/skills/urlquery/bin/uq.py)

Authenticated with the stored `custom.urlquery` credential through the
skill's surrogate helper. `uq.py report <id>` calls
`GET https://api.urlquery.net/public/v1/report/<id>`.
`uq.py overview <id>` calls
`GET https://api.urlquery.net/public/v1/report/<id>/overview`.

| File | Source URL | Method | sha256 |
|---|---|---|---|
| report_cae7c9a4.json | https://api.urlquery.net/public/v1/report/cae7c9a4-3de1-4c21-834c-aa8c0a855a1f | uq.py report | 711c72585da624f8124894358064cfa42f5ff604a92a8f6b9d246c85ff3c75f9 |
| report_b9812d90.json | https://api.urlquery.net/public/v1/report/b9812d90-64bb-4516-9f68-8496a6c92a6f | uq.py report | 68d82ef3412590d6741382d6567a45a092b2baf57fbc930b041fd5acf5074f90 |
| report_575882e1.json | https://api.urlquery.net/public/v1/report/575882e1-1d48-4ec6-bb50-90142a2e1c04 | uq.py report | 866d36d922f8932317a6643d8766be97ce1a8179a4be7f5ac2157e26f355722e |
| report_f5c035e5.json | https://api.urlquery.net/public/v1/report/f5c035e5-1fd3-4eff-9625-05b709093bfc | uq.py report | 234f26ec756d06dfe16976eccdbb29dd4b3fdf01d8bfdf13f042c539f5fc53fa |
| report_685636b5.json | https://api.urlquery.net/public/v1/report/685636b5-e539-4f7e-849f-5b810fa2d30b | uq.py report | fd90ec39fa17bef35bd136ee0bd4210a05569ffea6b32d231135be4f2ebaf7ab |
| overview_cae7c9a4.json | https://api.urlquery.net/public/v1/report/cae7c9a4-3de1-4c21-834c-aa8c0a855a1f/overview | uq.py overview | de6801690c8e0940acb6522652b4baa10417831b9f295d1e0cfebffaa3fad615 |
| overview_b9812d90.json | https://api.urlquery.net/public/v1/report/b9812d90-64bb-4516-9f68-8496a6c92a6f/overview | uq.py overview | bdf8a22200e41e94ca22e0a67da599903afd48bb7240bc5290ec2fdfbd325cdd |

The five report files are finding #173's urlquery evidence links (the
first two named in the collection task, the other three named in the
finding itself). Each report JSON embeds the submitted page (base64),
the scan result, and the scanner-side IP/ASN. Note: the `ip` field is
urlquery's scanner exit, not the submitter.

## Web pages (curl, GET only, desktop Chrome user agent)

| File | Source URL | Method | sha256 |
|---|---|---|---|
| chinese-agent-fleet.html | https://swarmcha.se/posts/chinese-agent-fleet | curl -sL | fc0b96d47c4e04f288c98b4a3f673f8ad02e94c580eefeaf7d78d0dce617f143 |
| termina-we-mean-no-harm.html | https://termina.digital/we-mean-no-harm | curl -sL | 1ec44fafa48bdbceed89ea7e20b26218a1926639f1d0f912f5f444e002aee071 |
| mailbox-termina-digital.html | https://mailbox.termina.digital/ | curl -sL | 6f60ceb7de8dd7a3b96bf29258aef0db707a548e3218c661394a04f72d3d46cb |

The swarmcha.se page carries the preliminary report "We found a Chinese
agent fleet" (4 Oct 2026, updated 5–6 Oct). The two termina.digital pages
are finding #173 evidence links.

## Transluce findings-tracker API (via ~/workspace/skills/transluce/bin/tl.py)

| File | Source URL | Method | sha256 |
|---|---|---|---|
| finding173.json | GET /api/findings/173 on d3ncjnql1bmhe8.cloudfront.net (via `tl.py finding 173`) | tl.py | 58837015d47c50faed5cf709f99dc4c65c59bb455a0ce8b23e8eb55a36c715e5 |

This is the finding record itself (submitter Christopher Ta, created
2026-10-08T06:35:28Z): summary, description with timeline, evidence
links, and attachment metadata.

## NOT retrieved

Finding #173 carries an attachment
`fleet-infra-contact-evidence.zip` (150,696 bytes,
sha256 870c748c4095c42086eec3bcad28fcf9d8fdff2b963005b8961ee773f8a02da3,
uploaded 2026-10-08T06:35:28Z). The transluce skill exposes no
attachment-download path, and no download URL was guessed. The metadata
above is quoted verbatim from finding173.json.
