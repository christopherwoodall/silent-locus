#!/bin/bash
# urlscan result API, anonymous read-only GET. No login, no key.
# Idempotent: skips existing nonzero files.
set -u
OUT="$(dirname "$0")"
cd "$OUT" || exit 1
UA="Muse-hunt-lane/1.0 (read-only research)"
fetch() {
  local name="$1"; local id="$2"
  local file="result_${name}.json"
  if [ -s "$file" ]; then echo "SKIP $file exists"; return 0; fi
  local url="https://urlscan.io/api/v1/result/${id}/"
  echo "GET $name $id"
  curl -sS -m 120 -A "$UA" "$url" -o "$file.tmp" || { echo "FAIL $name"; rm -f "$file.tmp"; return 1; }
  mv "$file.tmp" "$file"
  {
    echo "source URL: $url"
    echo "retrieval time (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "method: curl GET, anonymous, no login, no API key"
    echo "scan id: $id"
  } > "$file.PROVENANCE.txt"
  sha256sum "$file" > "$file.sha256"
  sleep 4
}
fetch sanmaohe_apex_1027_1039 "01a17cf1-bd4b-724c-9ce2-27febcda0fd7"
fetch sanmaohe_upload_testbin "01a17c2a-fcc7-745b-9e50-fa8f675b5415"
fetch sanmaohe_apex_1027_0001 "01a17aa9-8860-75f2-8a0f-77e450fbbcaf"
fetch sanmaohe_upload_dir "01a1793c-dc76-70ca-a6a8-4ac8d1e7ac7a"
fetch meta_navchk "01a16546-3e2c-76ca-a97e-af92aeaf1b6a"
fetch meta_recon2 "01a1653e-5e7f-736e-b595-4ed475a143ff"
fetch meta_recon "01a16538-d9bf-747a-b025-330e114fe2a1"
fetch meta_go_creds "01a164f6-74ba-71d9-9029-a278f24385f2"
fetch meta_probe "01a164f2-bdc9-75bc-b9ca-6de1ce1876a0"
fetch meta100_direct_1013 "01a13784-4410-72fb-a954-3572cbbd6e2d"
fetch meta100_direct_0927 "01a0e3c7-39c2-720d-a286-9d64de3518a9"
fetch meta100_apex_1019 "01a1550f-0ca4-75b8-9294-f85f34894f9f"
fetch meta_httpbin_redirect "01a15c68-90bf-75af-9e95-52d182d165e3"
fetch meta_sprout "01a10e3d-0e52-74ea-9bf3-fc9ded00fe63"
fetch meta_webhook_1021 "01a15c30-7ca9-7418-b5dc-af4e24dbc449"
fetch meta_webhook_1016 "01a14397-26da-7165-8c6d-50e2918fa076"
fetch meta_httpbin_b64_img "01a14e71-a1c5-74ad-9a9e-78b04c78672c"
fetch meta_httpbin_b64_meta "01a14e6d-f076-71ee-aa22-d710c174a34f"
fetch meta_clckru "01a1680a-412f-71ad-84ea-3d1dd38638a0"
echo DONE
