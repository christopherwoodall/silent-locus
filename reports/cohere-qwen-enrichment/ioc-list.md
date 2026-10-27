# IOC list — Cohere Qwen enrichment, cryptologist lane

Scope: URLs, domains, buckets and IPs extracted verbatim from the four sources below. A string here is NOT a maliciousness verdict. OBSERVED = string present in cited source; INFERENCE = bucket/region parsed from host; UPSTREAM = blog aggregate only. README example URLs are generation outputs truncated in source; main-trace URL is the single parquet/JSONL URL.

Counts, corrected: 125 rows, 124 distinct strings. `100.100.100.200` appears twice, once as a DOMAIN row and once as an IP row.

Sources: README.md (CohereLabs dataset, rev 028b7cd7…), qwen-investigation.jsonl (4 lines), train-00000-of-00001.parquet (1 row, 2,372 token_ids, trace 9,569 chars, trace SHA-256 c2f6115274a33e6193eed56dc667ec22e903404b75a3a6aae5ea86c18e769b98), Cohere blog page (fetched HTML). Captures under data/lanes/cohere-qwen-enrichment/raw/cryptologist/ with .PROVENANCE.txt + .sha256.

## URLs

- `http://100.100.100.200/latest/meta-data/` — [OBSERVED] README.md example output [5/64]; README example output, not main trace; string truncated in source where shown.
- `http://127.0.0.1:8000/payload.sh;` — [OBSERVED] README.md example output [13/64]; README example output, not main trace; string truncated in source where shown.
- `http://127.0.0.1:8000/probe.txt` — [OBSERVED] README.md example output [31/64]; README example output, not main trace; string truncated in source where shown.
- `http://192.0.2.10:8099/probe_upload` — [OBSERVED] README.md example output [55/64]; README example output, not main trace; string truncated in source where shown.
- `http://details.example.invalid/probe.txt;` — [OBSERVED] README.md example output [7/64]; README example output, not main trace; string truncated in source where shown.
- `http://detection-objects-x9k2m3v7p1q4.oss-cn-hangzhou.aliyuncs.com/implant%2Fupdate.sh` — [OBSERVED] README.md example output [62/64]; README example output, not main trace; string truncated in source where shown.
- `http://files.myfilestore.com/cb5a123d-909c-4a50-a658-72f75d344202/probe.txt` — [OBSERVED] README.md example output [35/64]; README example output, not main trace; string truncated in source where shown.
- `http://lattice-gtm-files.s3-website-us-east-1.amazonaws.com/f308e0bf9d0587d4/9876/970a6fbc-8` — [OBSERVED] README.md example output [44/64]; README example output, not main trace; string truncated in source where shown.
- `http://legit-cdn.example.com/data/report.pdf;` — [OBSERVED] README.md example output [42/64]; README example output, not main trace; string truncated in source where shown.
- `http://localhost:8000/payload.txt;` — [OBSERVED] README.md example output [30/64]; README example output, not main trace; string truncated in source where shown.
- `http://localhost:9/debug/put_probe` — [OBSERVED] README.md example output [37/64]; README example output, not main trace; string truncated in source where shown.
- `http://logs.googleblog.com/2007/09/pinpoint-and-scale-up-your-search.html` — [OBSERVED] README.md example output [26/64]; README example output, not main trace; string truncated in source where shown.
- `http://logs1.metrics平台.io/put/72b3077a-e53b-4a14-9823-5c4413925468` — [OBSERVED] README.md example output [3/64]; README example output, not main trace; string truncated in source where shown.
- `http://paste.rs/` — [OBSERVED] README.md example output [64/64]; README example output, not main trace; string truncated in source where shown.
- `http://paste01.svc:8080/files/aaaa-bbbb-cccc-dddd/notes.txt` — [OBSERVED] README.md example output [27/64]; README example output, not main trace; string truncated in source where shown.
- `http://probe.example.invalid/x` — [OBSERVED] README.md example output [38/64]; README example output, not main trace; string truncated in source where shown.
- `http://probe.tmpfiles.org/f/puttest.txt` — [OBSERVED] README.md example output [28/64]; README example output, not main trace; string truncated in source where shown.
- `http://r.jina.ai/https://upload.wikimedia.org/wikipedia/commons/e/ea/Blank.png` — [OBSERVED] README.md example output [23/64]; README example output, not main trace; string truncated in source where shown.
- `http://r001-cs.oss-cn-hangzhou.aliyuncs.com/resources/2026-07-01/put_probe.txt` — [OBSERVED] README.md example output [41/64]; README example output, not main trace; string truncated in source where shown.
- `http://r001-fileops-et948l.oss-en2-file--tmp.localhost:9999/probe;` — [OBSERVED] README.md example output [20/64]; README example output, not main trace; string truncated in source where shown.
- `http://r00t0fc72e5b2c704a92b10f362ac3ad31e.ingress.frankfurter.app/` — [OBSERVED] README.md example output [21/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0body.com:8082/uploads/files/x/probe.txt;` — [OBSERVED] README.md example output [18/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0bodycti01.blob.core.windows.net/coldchain/droppers/payload.sh?sv=2021-08-06\&se=2026-08-` — [OBSERVED] README.md example output [29/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0cb35.com:8080/` — [OBSERVED] README.md example output [24/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ck3t-upload.nerd/v00d00/put_probe` — [OBSERVED] README.md example output [19/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ck3t-upload.oss-cn-hangzhou.aliyuncs.com/anon%2Fb7e2f1a3-4c9d-4e8f-a1b6-` — [OBSERVED] README.md example output [53/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ck3t.net/tmp/probe.txt;` — [OBSERVED] README.md example output [34/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ck3t.net/tmp/stage.sh` — [OBSERVED] README.md example output [59/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ck3t.net/usr/bin/curl` — [OBSERVED] README.md example output [10/64]; README example output, not main trace; string truncated in source where shown.
- `http://r0ckey110.5t.am/n/` — [OBSERVED] README.md example output [36/64]; README example output, not main trace; string truncated in source where shown.
- `http://r8-detect-deps.oss-us-east-1.aliyuncs.com/resource/00306ee028db6a73a1c0f73229f6` — [OBSERVED] README.md example output [1/64]; README example output, not main trace; string truncated in source where shown.
- `http://r8-dst-6b124743-d5a5-474c-bf49-267ba2fcdb/d/put_probe.txt` — [OBSERVED] README.md example output [46/64]; README example output, not main trace; string truncated in source where shown.
- `http://rally9-high-9200.oss-cn-shanghai.aliyuncs.com/x/put_probe.txt` — [OBSERVED] README.md example output [47/64]; README example output, not main trace; string truncated in source where shown.
- `http://rce-testing-bucket-711.s3.us-west-2.amazonaws.com/probe_file` — [OBSERVED] README.md example output [51/64]; README example output, not main trace; string truncated in source where shown.
- `http://rimeless.com/tmp/put_probe` — [OBSERVED] README.md example output [17/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-07-29/trace_0baf5d` — [OBSERVED] README.md example output [61/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-07-29/trace_21010` — [OBSERVED] README.md example output [14/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-07-29/trace_21018` — [OBSERVED] README.md example output [16/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-07-29/trace_21501` — [OBSERVED] README.md example output [54/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-07-29/trace_2151ea` — [OBSERVED] README.md example output [25/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-05/trace_21013` — [OBSERVED] README.md example output [12/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-10/trace_0baf59` — [OBSERVED] README.md example output [9/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-10/trace_213fec` — [OBSERVED] README.md example output [4/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-10/trace_2140ef` — [OBSERVED] README.md example output [45/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-10/trace_2151ea` — [OBSERVED] README.md example output [33/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-11/trace_0baf5d` — [OBSERVED] README.md example output [39/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-11/trace_212a7` — [OBSERVED] README.md example output [52/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-11/trace_21412` — [OBSERVED] README.md example output [40/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-12/trace_213c5` — [OBSERVED] README.md example output [15/64]; README example output, not main trace; string truncated in source where shown.
- `http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/tmp/probe.txt` — [OBSERVED] README.md example output [32/64]; README example output, not main trace; string truncated in source where shown.
- `http://rsm61289cc21.v2y0qzzdhcru26rm8p5w1n2rm2214c2sd.o3b.cc/40f` — [OBSERVED] README.md example output [22/64]; README example output, not main trace; string truncated in source where shown.
- `http://rsn-14308654681110.europe-west1.run.gservice.dev/probe.bin` — [OBSERVED] README.md example output [11/64]; README example output, not main trace; string truncated in source where shown.
- `http://rsn1-c1301.siemrulezz.vicgpt.com/v1/d/564d4631373065fb420aa9f425` — [OBSERVED] README.md example output [2/64]; README example output, not main trace; string truncated in source where shown.
- `http://rumo.oss-cn-qINGdao.aliyuncs.com/o;` — [OBSERVED] README.md example output [43/64]; README example output, not main trace; string truncated in source where shown.
- `http://s4mple-serve:8090/upload/probe_xyz` — [OBSERVED] README.md example output [56/64]; README example output, not main trace; string truncated in source where shown.
- `http://sanitizer.test/putprobe.bin` — [OBSERVED] README.md example output [48/64]; README example output, not main trace; string truncated in source where shown.
- `http://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin` — [OBSERVED] data/train-00000-of-00001.parquet row 0, char offset 9432; Main trace URL. No query string observed; plain http.
- `http://sanmaoheihei-oss.oss-cn-hangzhou.oss-cn-beijing.aliyuncs.com/wm/put_probe.txt?Expires=1817532731\&OSS` — [OBSERVED] README.md example output [63/64]; README example output, not main trace; string truncated in source where shown.
- `http://tempbin.com/files/put_probe` — [OBSERVED] README.md example output [8/64]; README example output, not main trace; string truncated in source where shown.
- `http://tempfiles.xty.cc/tempfiles/PROBE_test/put_probe;` — [OBSERVED] README.md example output [6/64]; README example output, not main trace; string truncated in source where shown.
- `http://tmpfiles.org:80/dl/589320/probe.txt` — [OBSERVED] README.md example output [58/64]; README example output, not main trace; string truncated in source where shown.
- `https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces` — [OBSERVED] cohere-blog.html (fetched page text) blog body, dataset link; Cohere blog dataset link

## DOMAINs

- `100.100.100.200` — [OBSERVED] README.md example output [5/64]; host of http://100.100.100.200/latest/meta-data/
- `127.0.0.1` — [OBSERVED] README.md example output [13/64]; host of http://127.0.0.1:8000/payload.sh;
- `192.0.2.10` — [OBSERVED] README.md example output [55/64]; host of http://192.0.2.10:8099/probe_upload
- `api.github.com` — [UPSTREAM] cohere-blog.html (fetched page text) prefill table; Blog prefill table most-common host at early prefill steps
- `details.example.invalid` — [OBSERVED] README.md example output [7/64]; host of http://details.example.invalid/probe.txt;
- `detection-objects-x9k2m3v7p1q4.oss-cn-hangzhou.aliyuncs.com` — [OBSERVED] README.md example output [62/64]; host of http://detection-objects-x9k2m3v7p1q4.oss-cn-hangzhou.aliyuncs.com/implant%2Fupdate.sh
- `example.com` — [UPSTREAM] cohere-blog.html (fetched page text) prefill table; Blog prefill table most-common host at early prefill steps
- `files.myfilestore.com` — [OBSERVED] README.md example output [35/64]; host of http://files.myfilestore.com/cb5a123d-909c-4a50-a658-72f75d344202/probe.txt
- `huggingface.co` — [OBSERVED] cohere-blog.html (fetched page text) blog body, dataset link; host of https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces
- `lattice-gtm-files.s3-website-us-east-1.amazonaws.com` — [OBSERVED] README.md example output [44/64]; host of http://lattice-gtm-files.s3-website-us-east-1.amazonaws.com/f308e0bf9d0587d4/9876/970a6fbc-8
- `legit-cdn.example.com` — [OBSERVED] README.md example output [42/64]; host of http://legit-cdn.example.com/data/report.pdf;
- `localhost` — [OBSERVED] README.md example output [30/64]; host of http://localhost:8000/payload.txt;
- `logs.googleblog.com` — [OBSERVED] README.md example output [26/64]; host of http://logs.googleblog.com/2007/09/pinpoint-and-scale-up-your-search.html
- `logs1.metrics平台.io` — [OBSERVED] README.md example output [3/64]; host of http://logs1.metrics平台.io/put/72b3077a-e53b-4a14-9823-5c4413925468
- `paste.rs` — [OBSERVED] README.md example output [64/64]; host of http://paste.rs/
- `paste01.svc` — [OBSERVED] README.md example output [27/64]; host of http://paste01.svc:8080/files/aaaa-bbbb-cccc-dddd/notes.txt
- `probe.example.invalid` — [OBSERVED] README.md example output [38/64]; host of http://probe.example.invalid/x
- `probe.tmpfiles.org` — [OBSERVED] README.md example output [28/64]; host of http://probe.tmpfiles.org/f/puttest.txt
- `r.jina.ai` — [OBSERVED] README.md example output [23/64]; host of http://r.jina.ai/https://upload.wikimedia.org/wikipedia/commons/e/ea/Blank.png
- `r001-cs.oss-cn-hangzhou.aliyuncs.com` — [OBSERVED] README.md example output [41/64]; host of http://r001-cs.oss-cn-hangzhou.aliyuncs.com/resources/2026-07-01/put_probe.txt
- `r001-fileops-et948l.oss-en2-file--tmp.localhost` — [OBSERVED] README.md example output [20/64]; host of http://r001-fileops-et948l.oss-en2-file--tmp.localhost:9999/probe;
- `r00t0fc72e5b2c704a92b10f362ac3ad31e.ingress.frankfurter.app` — [OBSERVED] README.md example output [21/64]; host of http://r00t0fc72e5b2c704a92b10f362ac3ad31e.ingress.frankfurter.app/
- `r0body.com` — [OBSERVED] README.md example output [18/64]; host of http://r0body.com:8082/uploads/files/x/probe.txt;
- `r0bodycti01.blob.core.windows.net` — [OBSERVED] README.md example output [29/64]; host of http://r0bodycti01.blob.core.windows.net/coldchain/droppers/payload.sh?sv=2021-08-06\&se=2026-08-
- `r0cb35.com` — [OBSERVED] README.md example output [24/64]; host of http://r0cb35.com:8080/
- `r0ck3t-upload.nerd` — [OBSERVED] README.md example output [19/64]; host of http://r0ck3t-upload.nerd/v00d00/put_probe
- `r0ck3t-upload.oss-cn-hangzhou.aliyuncs.com` — [OBSERVED] README.md example output [53/64]; host of http://r0ck3t-upload.oss-cn-hangzhou.aliyuncs.com/anon%2Fb7e2f1a3-4c9d-4e8f-a1b6-
- `r0ck3t.net` — [OBSERVED] README.md example output [10/64]; host of http://r0ck3t.net/usr/bin/curl
- `r0ckey110.5t.am` — [OBSERVED] README.md example output [36/64]; host of http://r0ckey110.5t.am/n/
- `r8-detect-deps.oss-us-east-1.aliyuncs.com` — [OBSERVED] README.md example output [1/64]; host of http://r8-detect-deps.oss-us-east-1.aliyuncs.com/resource/00306ee028db6a73a1c0f73229f6
- `r8-dst-6b124743-d5a5-474c-bf49-267ba2fcdb` — [OBSERVED] README.md example output [46/64]; host of http://r8-dst-6b124743-d5a5-474c-bf49-267ba2fcdb/d/put_probe.txt
- `rally9-high-9200.oss-cn-shanghai.aliyuncs.com` — [OBSERVED] README.md example output [47/64]; host of http://rally9-high-9200.oss-cn-shanghai.aliyuncs.com/x/put_probe.txt
- `rce-testing-bucket-711.s3.us-west-2.amazonaws.com` — [OBSERVED] README.md example output [51/64]; host of http://rce-testing-bucket-711.s3.us-west-2.amazonaws.com/probe_file
- `rimeless.com` — [OBSERVED] README.md example output [17/64]; host of http://rimeless.com/tmp/put_probe
- `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com` — [OBSERVED] README.md example output [4/64]; host of http://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/2026-08-10/trace_213fec
- `rsm61289cc21.v2y0qzzdhcru26rm8p5w1n2rm2214c2sd.o3b.cc` — [OBSERVED] README.md example output [22/64]; host of http://rsm61289cc21.v2y0qzzdhcru26rm8p5w1n2rm2214c2sd.o3b.cc/40f
- `rsn-14308654681110.europe-west1.run.gservice.dev` — [OBSERVED] README.md example output [11/64]; host of http://rsn-14308654681110.europe-west1.run.gservice.dev/probe.bin
- `rsn1-c1301.siemrulezz.vicgpt.com` — [OBSERVED] README.md example output [2/64]; host of http://rsn1-c1301.siemrulezz.vicgpt.com/v1/d/564d4631373065fb420aa9f425
- `rumo.oss-cn-qINGdao.aliyuncs.com` — [OBSERVED] README.md example output [43/64]; host of http://rumo.oss-cn-qINGdao.aliyuncs.com/o; case preserved exactly as observed, not lowercased;
- `s4mple-serve` — [OBSERVED] README.md example output [56/64]; host of http://s4mple-serve:8090/upload/probe_xyz
- `sanitizer.test` — [OBSERVED] README.md example output [48/64]; host of http://sanitizer.test/putprobe.bin
- `sanmaohe.oss-cn-beijing.aliyuncs.com` — [OBSERVED] data/train-00000-of-00001.parquet row 0, char offset 9432; host of http://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin
- `sanmaoheihei-oss.oss-cn-hangzhou.oss-cn-beijing.aliyuncs.com` — [OBSERVED] README.md example output [63/64]; host of http://sanmaoheihei-oss.oss-cn-hangzhou.oss-cn-beijing.aliyuncs.com/wm/put_probe.txt?Expires=1817532731\&OSS
- `tempbin.com` — [OBSERVED] README.md example output [8/64]; host of http://tempbin.com/files/put_probe
- `tempfiles.xty.cc` — [OBSERVED] README.md example output [6/64]; host of http://tempfiles.xty.cc/tempfiles/PROBE_test/put_probe;
- `tmpfiles.org` — [OBSERVED] README.md example output [58/64]; host of http://tmpfiles.org:80/dl/589320/probe.txt

## BUCKETs

- `coldchain (Azure blob container)` — [INFERENCE] README.md example output [29/64]; Container label parsed as first path segment after Azure blob host; no listing observed.
- `detection-objects-x9k2m3v7p1q4` — [INFERENCE] README.md example output [62/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `lattice-gtm-files` — [INFERENCE] README.md example output [44/64]; Bucket label parsed from S3 host prefix; no listing observed.
- `r001-cs` — [INFERENCE] README.md example output [41/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `r001-fileops-et948l (shape anomaly)` — [INFERENCE] README.md example output [20/64]; Shape mimics OSS virtual-hosted style but ends .localhost:9999; treat as synthetic/local shape, not a public bucket.
- `r0ck3t-upload` — [INFERENCE] README.md example output [53/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `r8-detect-deps` — [INFERENCE] README.md example output [1/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `rally9-high-9200` — [INFERENCE] README.md example output [47/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `rce-testing-bucket-711` — [INFERENCE] README.md example output [51/64]; Bucket label parsed from S3 host prefix; no listing observed.
- `routify-file-proxy-sg` — [INFERENCE] README.md example output [4/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `rumo` — [INFERENCE] README.md example output [43/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `sanmaohe` — [INFERENCE] data/train-00000-of-00001.parquet row 0, char offset 9432; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.
- `sanmaoheihei-oss` — [INFERENCE] README.md example output [63/64]; Bucket name inferred from OSS virtual-hosted-style subdomain; no bucket listing or ownership record observed.

## IPs

- `100.100.100.200` — [OBSERVED] README.md example output [5/64]; README example output, not main trace.
- `127.0.0.1:8000` — [OBSERVED] README.md example output [13/64]; README example output, not main trace.
- `169.254.169.254` — [UPSTREAM] cohere-blog.html (fetched page text) char offset 12409; Blog-reported aggregate, not a dataset row. No credential value observed.
- `192.0.2.10:8099` — [OBSERVED] README.md example output [55/64]; README example output, not main trace.
