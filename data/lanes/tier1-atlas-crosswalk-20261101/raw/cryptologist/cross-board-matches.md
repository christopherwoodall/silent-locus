# Cross-board matches: verified vs merely similar

Rule: a match is VERIFIED only when the same bytes appear in 2 or
more files. A fingerprint (first 16 hex chars of SHA-256) stands in
for the string. No value is reproduced here.

## Verified byte-for-byte matches (18)

All 18 are framework or template vocabulary. None is a live
identifier. Classification is SECONDARY. Presence is OBSERVED.

| Fingerprint | Shape | Length | Files | What it is |
|---|---|---:|---:|---|
| 9e82559240ddbb88 | 7 letters - 5 letters - 6 letters | 20 | 10 | CSS media-feature word in error page |
| 433839e38cca9232 | 23 letters | 23 | 10 | React property name in page data |
| 2b302fdb8b7d1c14 | 5-6-3-3-5 letters, hyphenated | 26 | 5 | Mobile web-app meta-tag name |
| 35f35c41d134eef0 | 4-5-10 letters, hyphenated | 21 | 4 | UI component class token |
| ca2d89ce1d5b517e | 24 letters | 24 | 4 | React page property name |
| a3935294c08c04e8 | 6-3-3-7 letters, hyphenated | 22 | 4 | Mobile web-app meta-tag name |
| 4f16d2616cf95dfb | 5-6-3-3-6-3-5 letters, hyphenated | 37 | 4 | Mobile web-app style meta-tag name |
| cc209238d8478555 | 4-6-10 letters, hyphenated | 22 | 3 | UI hover-class token |
| 4288f65cad5c2f7a | Mixed letters, digits, underscores | 39 | 3 | Font CSS-module class name |
| 5cccc6c226752057 | Mixed letters, digits, underscores | 44 | 3 | Font CSS-module class name |
| 19a23a346c4e3567 | 21 letters | 21 | 2 | Script timing-call name in page data |
| a12f81da3073f332 | 6-4-12 letters, hyphenated | 24 | 2 | Site-verification meta-tag name |
| 6127613613a40f7b | 5-6-3-3-7 letters, hyphenated | 28 | 2 | Mobile web-app meta-tag name |
| b01624641f32e5e8 | 20 letters | 20 | 2 | Page-data slot key in flight data |
| 48a1d34f1a08d8cb | 10-9 letters, hyphenated | 20 | 2 | UI group-hover class token |
| 4486265a1a5e5c89 | 4-8-7 letters, hyphenated | 21 | 2 | CSS grid-template property word |
| f83310a777608688 | Mixed, underscores | 24 | 2 | Error-digest constant tied to 404 |
| 2acb818de7eaae48 | 1-9-9 letters, hyphenated | 21 | 2 | Rate-limit header name in docs |

Full file lists per fingerprint: `analysis.json`, field
`cross_token_matches`.

Note on the site-verification row: the tag NAME matches. The tag
VALUES differ across the 2 files. Name shared, value not shared.
That is template, not identity.

Note on the font-class rows: the same font build classes appear
in 3 files, and the same static chunk filename shape appears in
2 of them. Both boards serve their own copy. That is a shared
starter or build, not shared live infrastructure.

## Verified shared lines (4)

All 4 are generic page boilerplate, not board content:

| Fingerprint | Length | Files | What it is |
|---|---|---:|---:|
| 4e0a72d80cf02ea8 | 30 | 5 | JSON content-type header line |
| 0dadde39b3b61474 | 22 | 3 | Charset meta line |
| 506a4604bd27acd7 | 37 | 2 | JSON content-type header line, quoted form |
| d94dd50dc4cdd54e | 43 | 2 | Meta property line |

These lines come from HTML error pages. They prove shared page
scaffolding, not board coordination.

## Merely similar (same shape, different values)

- Bearer-header shape: 16 files. Same shape, no shared value.
- Key-assignment shape: 11 files. Same shape, no shared value.
- UUID shape: 3 files. Same shape, no shared value.
- Signed-URL shape class: 1 file only. No second board is similar.
- Hosting class (workers, app, page, render, fly, railway):
  many boards. Same class, no shared host.
- Public hosts (code hosting, fonts, social, tag manager):
  many boards. Same dependency, not shared infra.
- Board-to-board links: 3 cases where one board's host appears
  in another board's capture. A link is a reference, not shared
  infrastructure.

## Verdict

Shared template: yes, extensive, all framework-level.
Shared infrastructure: none found.
Coincidence: equal-size pair, common public hosts, common words.
No cross-board live identifier survives verification.
