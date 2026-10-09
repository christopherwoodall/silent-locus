# PROVENANCE — revision-enumerator raw cache
Lane: wikipedia-edit-hunt, worker revision-enumerator. Branch: wikipedia-edit-hunt-2026-10-06.
Collection: 2026-10-06, paced curl (>=6s), User-Agent "revision-enumerator/2026-10-06 (research; silent-locus hunt)".
Seed: data/2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv (54 diff URLs, WMF 2026-10-04).
Passive public OSINT only; nothing edited on any wiki.

## Endpoints and query params

### Revision metadata + full content (batch per wiki, 9 requests, all HTTP 200)
`GET https://<HOST>/w/api.php`
- action=query, prop=revisions
- revids=<oldids pipe-joined>
- rvprop=ids|timestamp|user|comment|tags|flags|content
- rvslots=main, format=json, formatversion=2

### Per-revision diffs (49 valid responses, all HTTP 200)
`GET https://<HOST>/w/api.php`
- action=compare, torev=<oldid>
- fromrev=<parentid>  (or fromtext= empty base when parentid=0 — one case: test 741406)
- format=json, formatversion=2
- CORRECTION 2026-10-06: first attempt for test.wikipedia.org/741406 mixed fromtext= with fromslots=main -> invalidparammix API error was briefly cached as a "diff" and falsely logged OK; retried with fromtext alone (valid diff returned, file replaced, correction logged in collection.log).

## Retrieval timestamps (batch phase) and row counts

- bg.wikipedia.org: 2026-10-06T18:40:18Z, 1 revids requested
- commons.wikimedia.org: 2026-10-06T18:40:25Z, 6 revids requested
- en.wikipedia.org: 2026-10-06T18:40:32Z, 11 revids requested
- incubator.wikimedia.org: 2026-10-06T18:40:40Z, 8 revids requested
- meta.wikimedia.org: 2026-10-06T18:40:47Z, 6 revids requested
- simple.wikipedia.org: 2026-10-06T18:40:54Z, 1 revids requested
- test.wikipedia.org: 2026-10-06T18:41:01Z, 13 revids requested
- test2.wikipedia.org: 2026-10-06T18:41:08Z, 4 revids requested
- www.mediawiki.org: 2026-10-06T18:41:16Z, 4 revids requested

Total requested: 54. Resolved: 49. Missing (badrevids/missing:true, HTTP 200): 5 — meta 30732691, 30732696, 30732698, 30732699, 30732700 (all Web2Cit config pages).

Diff request log lines: 49; HTTP 200 diff lines: 49 (incl. 1 failed + 1 retried for 741406). Result: 49 diff files under raw/diffs/.

## File inventory

`raw/api-dumps/<wiki>_<oldid>.json` (54): per-oldid raw API record, extracted verbatim from its host's batch response (page + revision objects as returned; missing oldids carry their `badrevids` object). Retrieval timestamp = the batch's timestamp above.

`raw/<host>_revisions.json` (9): complete raw batch responses as received.

`raw/diffs/<host>_<oldid>.txt` (49): header (endpoint, params, retrieval timestamp) + full raw action=compare JSON response. HTML diff body preserved unmodified.

`raw/revisions.tsv` (54 rows incl. header): wiki, page, oldid, user, timestamp_utc, comment, tags, minor, parent_oldid, content_sha256, content_bytes. comment/page/user/title fields backslash-escaped. Missing oldids have empty fields.

### sha256 (files in raw/)

```
4e2a15285f517c57cb30dce1334383bb9fdb07213d90564f0deab349c44451c9       695  bg.wikipedia.org_revisions.json
f013ab1aa34354a7b72c0238ee7a727fec1776e2c5199e52e6b5684c3b7c110c      2622  commons.wikimedia.org_revisions.json
e2bf434948e015841611a7738de061fec9f13d74648cf88001eeae33fc2ff958      7401  en.wikipedia.org_revisions.json
8dddd594df0a34906283c8d4c0cd096ff1fe2bf44008fe58ce438146b41526cc     53356  incubator.wikimedia.org_revisions.json
7f8fac1abb4626c70cc4db0e9ab5f31ec1eb44bd247cbf38a48a1a0272a9b8fa       756  meta.wikimedia.org_revisions.json
4991c1e77a4d0702301a5153229b2a34c51b398f9554f33b0698a49911b6bbb5       681  simple.wikipedia.org_revisions.json
b7d60a82ae8482d9da40c1158d89fe0e7bac19865d38ac52c5cb973b451ec5e7      5656  test.wikipedia.org_revisions.json
5e627bab668460ab3aa1cedc462c1be167d685563e3fa5bc16bfbfc81a30a864      4965  test2.wikipedia.org_revisions.json
18b86507629890ae311680c8a74b2ffc4930c98fb1da46807c1ce3364926b2a2      1700  www.mediawiki.org_revisions.json
f46eb696d71d75dba540c4149130636e72ae3515bca35b9ec31621f0e4e9888f      1724  api-dumps/bg.wikipedia.org_12923296.json
d2dd710c41146d43f8e7d6d3bf35bd5d14d1653a2afb3903fa88e0dcea3f0ab9      4055  api-dumps/commons.wikimedia.org_1213399057.json
22d0c7b6566f2e03f08df89301ba9cffc779f4fed5da844623ebe9c896ab8231      4051  api-dumps/commons.wikimedia.org_1213503714.json
b495af4b350e22653eb33b327112e075f0cc87673c70a442572764e4ded85a19      4137  api-dumps/commons.wikimedia.org_1213503789.json
4b3c1a892b46f973930ef94b955e771f4f599f78bfdae88c07f6c31a86d457a8      4160  api-dumps/commons.wikimedia.org_1213513506.json
688fd425fad7a2abe8d36b8204f5efa10305a31584d2e457188a6f07bd62cf16      4084  api-dumps/commons.wikimedia.org_1233683454.json
c59aca2c8714aa29c4a66086fe0211ceabbb12727f6dea63ef7916194ea5b040      4086  api-dumps/commons.wikimedia.org_1238390511.json
8b104a3fd7423ba89b4a79d1fad0e94c2661366ef531185e392cb54933f673f0      2619  api-dumps/en.wikipedia.org_1353490694.json
16e84006127c6ab2af87aa04f396672c06d7a4266a9dae6dc5abeddcca211d86      2629  api-dumps/en.wikipedia.org_1353490935.json
7bc6d706d69512d928207be12143a5610095abdfd79f44058e6e348f39eef822      6869  api-dumps/en.wikipedia.org_1353491551.json
deee13d5462fabd9adbece723cb949a0bf06caa7f31ce1c21cda3755a1df280d      7150  api-dumps/en.wikipedia.org_1353492663.json
3792bcf8db04f257017f6534496874a8791d59e24668b89ee35500efe09cc626      2820  api-dumps/en.wikipedia.org_1353498400.json
2322a0764834759a5438e262139ef634a326445c026f841a0d7b586b27aeb02b      2023  api-dumps/en.wikipedia.org_1353501383.json
772d9c41500d2698aa0c0873dd8e1a4c9b971711d6668bf10ca8a5336a27483f      2641  api-dumps/en.wikipedia.org_1353507315.json
e61721ab035403c30442eef357b836ada71373be5e9dc1815f30941c28096295      7028  api-dumps/en.wikipedia.org_1353518652.json
257d424ea3746c4e9598e90c0001575e04d96bb19abeb834068721b99d99049f      7003  api-dumps/en.wikipedia.org_1353543060.json
33d40b01d3b7b1d0f7f470aa4b45c742f60ba558cf9943ed40c3d0182270e9ab      7102  api-dumps/en.wikipedia.org_1356314507.json
048918ad295d0a8d7a00da4c0c0dcccced400581ad713e8a7cae258217003506      6980  api-dumps/en.wikipedia.org_1356419247.json
425b036af204e82b7c0238b8573869a5d8c100218e05c8c4080f76fee6a5340a     61057  api-dumps/incubator.wikimedia.org_7226103.json
1a9f12a3197822904e5b44ca078b7b666c4f3b4d34c5ff29a7eb9cd3ecd64940     61118  api-dumps/incubator.wikimedia.org_7226104.json
0850c463385a49ab1309feb92ac965ed5fd3a2d13d4f6801f19cb1be10621ad1     61179  api-dumps/incubator.wikimedia.org_7226105.json
79c7aa5c6149377a22c1d4c2e813e6ab0b95c5cb66cbf1b457617dd3c35e40b8     61156  api-dumps/incubator.wikimedia.org_7226107.json
c4923332df9eb212da6c7bccd64f8de4458e390f801da74891116e83fba4350c     61255  api-dumps/incubator.wikimedia.org_7226108.json
45839bcd48aa3f41872b5581f0db3d33589d05c14fe243ef2b7325de3859c2a8     61226  api-dumps/incubator.wikimedia.org_7226109.json
81c3a8af2f700295e59d323fe97a6e31465c1bb777e5fbfbf5acc5ce8c75f31d     61238  api-dumps/incubator.wikimedia.org_7226110.json
97c41052afbd365ea0a63256870fdc2c69feb6d57958ec3a72d9ddf996dc0e90     61340  api-dumps/incubator.wikimedia.org_7226111.json
d2c618c99e7fcf8c9cb37317086aa292de4cc942a90a3cd5357652102bc46660      1393  api-dumps/meta.wikimedia.org_30732655.json
c5016e00d89826c06f442ad9c3b4e9c0465ba080fd91513bb0ba0267f56ecfbe       304  api-dumps/meta.wikimedia.org_30732691.json
2ad36e2e2afe0c83a701dd88330080e860cd60187497868f07ade3b665876b3b       304  api-dumps/meta.wikimedia.org_30732696.json
029c0f75c0293b73a8b0055302804e8be81f7ea26350d5116288888157e9f66b       304  api-dumps/meta.wikimedia.org_30732698.json
b9f537be5e912d8a0107647cc8e94a8ca23342863df0515fdac174e153d51d5b       304  api-dumps/meta.wikimedia.org_30732699.json
aa8491e62698f92fbe6af9c06620edbcbeed376df02e0aee46dfb9862aa7d105       304  api-dumps/meta.wikimedia.org_30732700.json
3e87ef0aea1af74c7da23b832ba0aed3aca08ae5d92ac04364e540d6650304f2      1722  api-dumps/simple.wikipedia.org_10891416.json
eb750073edc2255bfc9dd579536fb9dd60eba52f2554ed3fc7cc73d23c21b16f      6045  api-dumps/test.wikipedia.org_741398.json
f03b3caf2b3fa43f8979dcc6f9e5fb86ec14c48fae109e7155a0b22cf179015d      6104  api-dumps/test.wikipedia.org_741399.json
96ce3605480c4adcb3d6d0880c011e7d52f81afebac5522b054002bcae02b1f0      6130  api-dumps/test.wikipedia.org_741400.json
79f512e0fb201aa233ede51fc6fd5a475c84150cabfc46370d2cfdd81b649294      6193  api-dumps/test.wikipedia.org_741405.json
d790e3c732a48973ffd8169d6c6e67910ac7ba32d6003631c038c715125f64b2      1032  api-dumps/test.wikipedia.org_741406.json
830e6fcdd00390841edb92482f1f68766c019fcdac5c4b983ccb40b01f5c6779      6191  api-dumps/test.wikipedia.org_741409.json
46b3fe87464abe7dad20ad01712f8d4c887c351410f62c33448e68726e9f496c      6146  api-dumps/test.wikipedia.org_744268.json
a13a5e290e1bc170603ead8855cf260698dea7e735991970f395e0cd47c11202      6053  api-dumps/test.wikipedia.org_744270.json
0b669bf01af5549ec0c089ca7a6914abbcaaee47e84f445188ceb307b80f4797      6140  api-dumps/test.wikipedia.org_744271.json
05e6d4b5c399038be52878e2dc37ccdc6917501399afe083ca57cd60f569debd      6053  api-dumps/test.wikipedia.org_744272.json
bab0502fca15f339fdb649eaf1c2d968316e3184954ad5087eeab6fe473af608      2411  api-dumps/test.wikipedia.org_744412.json
5be9e0f7d8ef86be1b49b92fe4903ba6bc06988f888b4a77e1895933aabc9c23      2057  api-dumps/test.wikipedia.org_744414.json
991bf6b758067ebd4508155f0a35574cbafb057f900473978000a4408599af8d      6134  api-dumps/test.wikipedia.org_747327.json
09a62e59822048a94a400e0ad5a7daddafab19c97c79dd0a3345adb68656b2fa      6202  api-dumps/test2.wikipedia.org_612931.json
6790460f940e96a28bdc895a5a921c325d4eb66e61ca9d071f2d22cc7d0d58bf      6261  api-dumps/test2.wikipedia.org_612932.json
eaa9e0d8731763aaecce8a753a2e1ee64f2c127b99e3fb7bb527eacb711516ae      6287  api-dumps/test2.wikipedia.org_612933.json
a40011ead56f0fc287a24540775b7f1305a214b91e7058f3c31994240e1d0135      1934  api-dumps/test2.wikipedia.org_613856.json
66e21aed8c67bea6e3f880b4f008eb3dec494926d2ac92e763fa261aaf9b2405      2842  api-dumps/www.mediawiki.org_8370989.json
60cc635b30877b93065140a08be42c0c55ac738a29b370f6fc9d88c49e76aca6      2901  api-dumps/www.mediawiki.org_8370994.json
eb7368ecd07efc192eafd5c091f2952987585cb63b4450f9a2fd9c04594b967f      2927  api-dumps/www.mediawiki.org_8370995.json
be12fac0585ad16d4d77644ca49756224bdf61943309f270778f04f1dbde409f      2953  api-dumps/www.mediawiki.org_8370996.json
716f83530cd9137f1c488cce2aded14b51b298940988460bed09a7a1315c7685      1707  diffs/bg.wikipedia.org_12923296.txt
3e6167fb5ff20741f46526c0830e86e47ae7f954fa769b0432a71568e9460960      1250  diffs/commons.wikimedia.org_1213399057.txt
2725ea24661cab24cf7ed42068f9df09ef51853d910778ccb3ec212f58a52b70      1465  diffs/commons.wikimedia.org_1213503714.txt
a03e95445b351338c150165464ba9c47d9f162b708f6681f64851b85150c282b      1612  diffs/commons.wikimedia.org_1213503789.txt
8d608dead7b36b14ad8e4590e19df989ad92be407fd8747478bfa84ac0ec3681      6812  diffs/commons.wikimedia.org_1213513506.txt
58f65afdb876592799171f51950a3c2bb68e04cff553855c8630eddc1cab4c03      1459  diffs/commons.wikimedia.org_1233683454.txt
d9e016302073a12bfe6e8818cf3e6a96642d361f62161b2606079dd3759d66d8      1253  diffs/commons.wikimedia.org_1238390511.txt
177890feac24cba5b94cad085f8b359e4e95ae3651ee7a5d69c77233c120f708       895  diffs/en.wikipedia.org_1353490694.txt
0c5298ed71dd4b75d0b6d0379e43803b5e2271605471337de60efdd6f4391f6b       902  diffs/en.wikipedia.org_1353490935.txt
abc63a7eeceb0ad972630a7da3f740f5897676e3192f7f4bd75570022c25a5c0      1705  diffs/en.wikipedia.org_1353491551.txt
7aee639b91b0bd4f1fb4715957547dd51016a1cdaa17ca519a76c0e8909d2f12      2294  diffs/en.wikipedia.org_1353492663.txt
5f0673abcbd5089c4ecd2984b3bb41324265468f5b341934032e30149edbcb2c      1121  diffs/en.wikipedia.org_1353498400.txt
8ebabb95f9cd61ad40df1e3ccbb8cbf88257158b1fc49e86800adb40820b4f60      1527  diffs/en.wikipedia.org_1353501383.txt
5cf3302050ae462f22224fd331f80f7629d47205fc747fe6967b97d7e783cd7c      1114  diffs/en.wikipedia.org_1353507315.txt
d06c79ed797e62ed61d41baf2d2ca737bdd28bf4c819a622d75d49cdc4e97553      1549  diffs/en.wikipedia.org_1353518652.txt
830e033c0caec601eb530eb778769021169803ea72bd709752230c0eda0aebea      1526  diffs/en.wikipedia.org_1353543060.txt
e97c40874eacf7c81ef67e761e182fb25f9bfbd01487635271a96bebc0ed404d      1719  diffs/en.wikipedia.org_1356314507.txt
a6d8ad0c75ef06f8e3af5123a9dbcb4ee443c2a960be5b1c58c3de52bcbd410c      1599  diffs/en.wikipedia.org_1356419247.txt
536d6981431d2ed012eb0ff8292aefa3aa7a02e70f8092d134bb905c926acd17      1247  diffs/incubator.wikimedia.org_7226103.txt
a66ea5113e4df5e840e954fe56555c6d7be3a26cf3ed738e169fbc6ec1f1090d      1588  diffs/incubator.wikimedia.org_7226104.txt
f0aa71ec54c8dfb8eddbe7b4d9e78b8c344d978a098583dcb29754ddf1b439b7      1929  diffs/incubator.wikimedia.org_7226105.txt
8b8f54d202bda9597b087f650363381f0180c441f97205404471fe18e2265136      1337  diffs/incubator.wikimedia.org_7226107.txt
ef8b470c0179f3befb0473a7902138ac141a7c8344b2caa1d1b0c847df08bc98      1291  diffs/incubator.wikimedia.org_7226108.txt
dafaf94a28c4cda1f9604b1587155f5d9ee8ed7072588464f98230322171e798      1242  diffs/incubator.wikimedia.org_7226109.txt
6493d158b81d2fac267d5f4f3fbdbe9ce25848cb00fc92bf788380210e85eda5      1485  diffs/incubator.wikimedia.org_7226110.txt
f70edec6ccadd055703cc71b925dac8454bbc1185ab669675045890bd1cd7a12      1187  diffs/incubator.wikimedia.org_7226111.txt
a12668e158a9b77de40fa52109b9a3dbf4d081c4529aa7bd829d9a0de2c052fc      1060  diffs/meta.wikimedia.org_30732655.txt
16d62f6c8d74ffe99a6039aeb68ed4c6f8d5ed486aaa0d9a87cbb9b851ff09d9      1800  diffs/simple.wikipedia.org_10891416.txt
12135e6aeac93d0dedbebacdafaf17b1a7ac8d16463571d721ef376ad52cf5b0      1241  diffs/test.wikipedia.org_741398.txt
900fe96c9b6c02716b883bf6e05be57f7298c137970d4431e64d12b6c0b5d43a      1210  diffs/test.wikipedia.org_741399.txt
e9ed6f742133caabe71b03f3fb2b846fef702ad1da24dd96261200b348619aad      1197  diffs/test.wikipedia.org_741400.txt
f6eef041db6fb5c12ee12d557f14a1ac667d4091a9d90274d1f2da2d17add81c      2041  diffs/test.wikipedia.org_741405.txt
21b433d5b7f59b2405a6ab8dea5fe9da820f7f5eae6d6656f456599ae4a42d52      1038  diffs/test.wikipedia.org_741406.txt
d88d885353004c47cf4b1516bbe7305e0e4a6bd290f5f9333452746803ff0626      1247  diffs/test.wikipedia.org_741409.txt
1c12d3200c9d7b321d5bfd6d5437ecd1276e1a85f54395cd926d608aa27a71b7      1937  diffs/test.wikipedia.org_744268.txt
d236b23e67dfe6db6f7951cb6348cc47086f221482a88e0ded73b1d07fe0e196      1953  diffs/test.wikipedia.org_744270.txt
e3010055433c13c1fc2f134248623f93219691f9c37369316d122de852393281      1917  diffs/test.wikipedia.org_744271.txt
29f9a03383b355d1fd378fd71ac79666b5004443cdab0dbac38cf22bb7364914      1933  diffs/test.wikipedia.org_744272.txt
948e88fc689f7af0cb387208ecfff26ee7f10c6b9fea137bd790fadfee66f9bd      1322  diffs/test.wikipedia.org_744412.txt
d521d56dffc4a8bf20471696d4cebe1752a3049a41b5c1d1a3dec5a92f03beb1       921  diffs/test.wikipedia.org_744414.txt
48c7ebfabe5aa84d804a393ca978d59b89e82107fd6027346976f898bb812bff      1518  diffs/test.wikipedia.org_747327.txt
ec6884b1f7184907353d75d15b507ed6415187c3128de8f3007bae85d805e041      1130  diffs/test2.wikipedia.org_612931.txt
f87918605fc8e02b822ccf0649d9f3938e93f5833ed62eaadb8556542d9b0c56      1157  diffs/test2.wikipedia.org_612932.txt
32a80a4009494518ae9e15e993ab54786c8fe37bc8a7605af04e3abf3b18c6a5      1196  diffs/test2.wikipedia.org_612933.txt
8ee005f3faf9af822e3ad1ed20d156cc73dca2ceebcc55626437e065877f26e0      1797  diffs/test2.wikipedia.org_613856.txt
18f753e7b7e2697b900617abdf3091452b67ad0bacb23bb5ce0415fe26f30874       997  diffs/www.mediawiki.org_8370989.txt
410eccd201b4ee0140641646d310ea233080403d615179f65d05b35f779a2c60      1269  diffs/www.mediawiki.org_8370994.txt
51298c176caf9abc0688d8b2dff6863340de9d398506fc6e3b4c0c2271b71f1c      1192  diffs/www.mediawiki.org_8370995.txt
956b8d64b7499210df7acef09940b9989c3228dfa1090bdcf7ac39cfa46dbb58      1451  diffs/www.mediawiki.org_8370996.txt
ca62bf6f4bf0f1513483c4888d4a824cf40fe8b91cfae1a7454bd9cdcf1d4040      9567  revisions.tsv
```

Transport note: first batch attempt failed (all HTTP 000) because oldids.txt carried CRLF \r from the seed CSV; stripped and re-ran clean. Verbatim log: wikipedia-lane/collection.log.

---

# PROVENANCE — account-profiler raw cache
Worker: account-profiler (wikipedia-lane). Branch: wikipedia-edit-hunt-2026-10-06.
Collection: 2026-10-06, paced curl (>=6s per host), 4 parallel per-host workers for the newusers pull.
Passive public OSINT only; nothing edited on any wiki.

## Per-account data (28 temp accounts)

### globaluserinfo (meta.wikimedia.org, 28 requests)
`GET https://meta.wikimedia.org/w/api.php` — action=query, meta=globaluserinfo, guiuser=<account>, guiprop=groups|merged|unattached|editcount, format=json.
Files: `raw/globaluserinfo/2026-<id>.json` (28). Retrieved 2026-10-06T18:3xZ (paced).

### Registration (list=users&usprop=registration, 7 requests)
`GET https://<host>/w/api.php` — action=query, list=users, ususers=<account>, usprop=registration|editcount|groups, format=json.
Files: `raw/registration-*.json` (7). All accounts carry groups `*`+`temp`.

### Per-account newusers probes (3 requests)
`GET https://<host>/w/api.php` — action=query, list=logevents, letype=newusers, letitle=User:<account>, leprop=ids|timestamp|user|comment|details|title|type, lelimit=10, format=json.
Files: `raw/newusers-probe-*.json` (3). All three show a single `autocreate` event.

### Contribution histories (usercontribs)
`GET https://<host>/w/api.php` — action=query, list=usercontribs, ucuser=<account>, uclimit=500, ucprop=ids|title|timestamp|comment|sizediff|flags|tags, ucdir=older, format=json.
Files: `raw/contribs-2026-28355-02-{enwiki,testwiki,test2wiki,mediawikiwiki}.json` (19 edits), `raw/contribs-2026-36867-71-incubatorwiki.json` (1), `raw/contribs-2026-36867-71-metawiki.json` (0 live; 5 deleted), `raw/contribs-2026-36837-35-metawiki.json` (1), `raw/contribs-2026-31558-62-testwiki.json` (3), `raw/contribs-burst1-testwiki-2026-*.json` (5, BURST-1 lead).

### Lock status
- `raw/locklog-globalauth/2026-<id>.json` (28): `GET https://meta.wikimedia.org/w/api.php` — action=query, list=logevents, letype=globalauth, letitle=User:<account>, leprop=ids|timestamp|user|comment|details|title|type, lelimit=10. All 28: zero events.
- `raw/blocklog-2026-36867-71-metawiki.json` (1): letype=block, letitle=User:~2026-36867-71 — the single local sanction (indef "Unauthorized bot", 2026-06-25T22:29:53Z, NguoiDungKhongDinhDanh).

### accounts.tsv
`raw/accounts.tsv` — 28 rows: account, registration_utc, global_editcount, wikis_edited, first_edit_utc, last_edit_utc, incident_edits, locked_global, notes. Derived from the above API responses + raw/revisions.tsv. NOTE: temporary accounts auto-create on first edit; registration_utc ≈ first-edit timestamp, not a signup event.

## Six-month newusers pull (2026-04-01–2026-09-30, 9 wikis)
`GET https://<host>/w/api.php` — action=query, list=logevents, letype=newusers, leaction=newusers/autocreate, lestart=<next-month>T00:00:00Z, leend=<month>T00:00:00Z, leprop=ids|timestamp|title|type, lelimit=500, format=json; paged via lecontinue to exhaustion.
SCOPE NOTE: leaction=newusers/autocreate only. All ~2026-* temp accounts are autocreated (verified 3/3 on sampled accounts; positive control 5/5 incident accounts found in pulled data); regular `create` signups can never be `~2026-*`. Not sampling: every autocreate event in the window is kept.
Files: `raw/newusers-2026-04-01_2026-09-30.<shortwiki>.jsonl` (one event object per line).
Short names: enwiki=en.wikipedia.org, testwiki=test.wikipedia.org, test2wiki=test2.wikipedia.org, mediawikiwiki=www.mediawiki.org, commonswiki=commons.wikimedia.org, incubatorwiki=incubator.wikimedia.org, simplewiki=simple.wikipedia.org, bgwiki=bg.wikipedia.org, metawiki=meta.wikimedia.org.

### Row counts and sha256 (FINAL — fill at pull completion)
```
(pending)
```
