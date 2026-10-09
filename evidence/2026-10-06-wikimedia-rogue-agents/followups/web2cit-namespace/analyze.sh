#!/bin/bash
# analyze.sh — build the Web2Cit/data catalog from raw API dumps.
# Usage: ./analyze.sh (run from the lane dir)
# Inputs:  raw/rev_batch_*.json (prop=revisions, latest, with content)
#          raw/firstrev_batch_*.json (prop=revisions, rvlimit=1 rvdir=newer)
# Outputs: catalog.tsv, redirects.tsv, flaglist.tsv, editors.tsv,
#          crossdomain.tsv, firstrev.tsv
set -u
RAW=raw

domain_of() {
  # $1 = title -> reversed-DNS domain
  :
}

# 1. Catalog: title | derived_domain | last_editor | last_timestamp | content_bytes
echo -e "title\tderived_domain\tlast_editor\tlast_timestamp\tcontent_bytes" > catalog.tsv
for f in $RAW/rev_batch_*.json; do
  [ -e "$f" ] || continue
  jq -r '.query.pages[] |
    select(.revisions != null) |
    [.title,
     (.title | sub("^Web2Cit/data/";"") | sub("/(templates|tests|patterns|dnr|test)\\.json$";"") | split("/") | reverse | join(".")),
     (.revisions[0].user // ""),
     (.revisions[0].timestamp // ""),
     ((.revisions[0].content // "") | length | tostring)
    ] | @tsv' "$f"
done >> catalog.tsv

# 2. Redirects (domain-alias mechanism)
echo -e "from_title\tto_title" > redirects.tsv
for f in $RAW/rev_batch_*.json; do
  [ -e "$f" ] || continue
  jq -r '.query.redirects // [] | .[] | [.from, .to] | @tsv' "$f"
done | sort -u >> redirects.tsv

# 3. Suspicious keyword scan over the DERIVED DOMAIN column only
SUSP='geocode|geodata|geoservices|arcgis|weather|forecast|meteorol|geoloc|geoip|ipapi|ip-api|ipinfo|whatismyip|shorten|shorturl|bit\.ly|tinyurl|is\.gd|goo\.gl|pastebin|paste|hastebin|termbin|webhook|requestbin|httpbin|httpbun|postman-echo|proxy|tunnel|ngrok|whois|speedtest'
awk -F'\t' -v re="$SUSP" 'NR==1 || tolower($2) ~ re' catalog.tsv > flaglist.tsv

# 4. Editor frequency
tail -n +2 catalog.tsv | cut -f3 | sort | uniq -c | sort -rn > editors.tsv

# 5. Cross-domain URL scan: hostnames in content that differ from the title-derived domain
echo -e "title\tderived_domain\tforeign_host" > crossdomain.tsv
for f in $RAW/rev_batch_*.json; do
  [ -e "$f" ] || continue
  jq -r '.query.pages[] |
    select(.revisions != null) |
    (.title | sub("^Web2Cit/data/";"") | sub("/(templates|tests|patterns|dnr|test)\\.json$";"") | split("/") | reverse | join(".")) as $d |
    .revisions[0].content as $c |
    ($c | scan("https?://[A-Za-z0-9.-]+") | sub("^https?://";"") | ascii_downcase) as $h |
    select($h != "" and ($h != $d) and (($h | endswith("." + $d)) | not)) |
    [.title, $d, $h] | @tsv' "$f" | sort -u
done >> crossdomain.tsv

# 6. First-revision table — SUPERSEDED.
# Multi-page rvlimit/rvdir is rejected by the API (invalidparammix). The agent's
# complete creation footprint was instead established via
# list=logevents&letype=create&leuser=<account> (see FINDINGS §8).
# The firstrev_gen_*.json / firstrev_batch_*.json inputs are therefore not required.
