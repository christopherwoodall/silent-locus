# URLs — dead-drop family evidence pack

The user approved publishing the live inbox UUIDs in this submission.

## Live dead-drop inboxes (webhook.site)

- Inbox A (42 requests at packaging): https://webhook.site/#!/2ccf61c9-01a6-4a6a-9e2a-c903d393261a
- Inbox B (33 requests at packaging): https://webhook.site/#!/ab53d845-0e43-4c18-9f5b-513e7da7a33e
- API form (no auth beyond UUID): https://webhook.site/token/<uuid>/requests

## Sibling urlquery reports

- amap probe v5 (triple exfil): https://urlquery.net/report/5008c990-1383-4adb-bff6-8efde3825306
- loader (jina-laundering probe): https://urlquery.net/report/33fa9bd2-a2fe-4856-8147-1725430170ea
- amap probe v3 (ntfy + beacon, no webhook.site): https://urlquery.net/report/0a541d23-7077-4a23-9a24-4809c65ea5b0

## Carrier / echo infrastructure referenced in beacons

- httpbin base64 COMBO-INIT carrier (href field of beacons; exact URLs in cache/)
- httpbun.com/anything/mochouC (echo endpoint, loader report)
- ntfy.sh topics (exfil channel, v3/v5 reports)

## Targets

- https://www.amap.com/place/B00190BBTX (Mochou Lake Park, Nanjing)
- Amap getPoiInfo targets B0138027SQ, B0G3LMF2G1 (API routes; see beacon payloads)

## Related

- termina.digital (interrogating party's claimed home): https://termina.digital
- Transluce finding #147 (epoch-clock fingerprint, adjacent context)
