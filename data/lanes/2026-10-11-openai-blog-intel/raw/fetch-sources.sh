#!/bin/bash
# Recovery fetch: re-acquire public OpenAI sources into lane raw/
# Original /tmp caches (2026-10-11 ~10:45 CDT) were removed before retention.
# Method mirrors original provenance: curl -sL, Chrome UA.
set -u
RAW="$(dirname "$0")"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
declare -a URLS=(
  "blog-false-front-operations|https://openai.com/index/disrupting-ai-enabled-false-front-operations/"
  "blog-model-distillation-campaign|https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/"
  "blog-eu-text-provenance|https://openai.com/index/eu-text-provenance/"
  "blog-introducing-dots|https://openai.com/index/introducing-dots/?ref=implicator.ai"
  "blog-computer-use-ironclad|https://openai.com/index/advancing-computer-use-with-ironclad/"
  "blog-gpt-6-astra|https://openai.com/index/gpt-6-astra/"
  "blog-path-to-astra|https://openai.com/index/path-to-astra/"
  "blog-misalignment-reporting-framework|https://openai.com/index/model-misalignment-reporting-framework/"
  "blog-chatgpt-ambitious-work|https://openai.com/index/chatgpt-for-your-most-ambitious-work/"
  "blog-gpt-5-4-mini-nano|https://openai.com/index/introducing-gpt-5-4-mini-and-nano/"
  "blog-introducing-agents-api|https://openai.com/index/introducing-the-agents-api/"
  "card-gpt-5-6-preview|https://deploymentsafety.openai.com/gpt-5-6-preview"
  "card-gpt-5-6|https://deploymentsafety.openai.com/gpt-5-6"
  "card-gpt-5-6-august-update|https://deploymentsafety.openai.com/gpt-5-6-august-update"
  "card-gpt-6-astra|https://deploymentsafety.openai.com/gpt-6-astra"
  "card-gpt-6-1-sol|https://deploymentsafety.openai.com/gpt-6-1-sol"
  "card-gpt-6-october|https://deploymentsafety.openai.com/gpt-6-october"
  "card-gpt-live|https://deploymentsafety.openai.com/gpt-live"
  "card-chatgpt-images-2-5|https://deploymentsafety.openai.com/chatgpt-images-2-5"
  "alignment-metagaming|https://alignment.openai.com/metagaming/"
  "alignment-monitorability-evals|https://alignment.openai.com/monitorability-evals/"
  "alignment-auto-review|https://alignment.openai.com/auto-review/"
  "alignment-metagaming-latents|https://alignment.openai.com/metagaming-latents/"
  "alignment-laser|https://alignment.openai.com/laser/"
  "alignment-measuring-reward-seeking|https://alignment.openai.com/measuring-reward-seeking/"
  "alignment-argo|https://alignment.openai.com/argo/"
  "alignment-validating-public-evals|https://alignment.openai.com/validating-public-evals/"
  "alignment-misalignment-reports|https://alignment.openai.com/misalignment-reports/"
  "blog-hf-incident|https://openai.com/index/hugging-face-incident-and-the-road-ahead/"
  "report-hf-incident-technical|https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf"
)
MANIFEST="$RAW/SHA256SUMS.recovery"
: > "$MANIFEST"
for entry in "${URLS[@]}"; do
  slug="${entry%%|*}"; url="${entry#*|}"
  out="$RAW/$slug.html"
  case "$slug" in report-hf-incident-technical) out="$RAW/$slug.pdf";; esac
  if [ -f "$out" ] && [ -s "$out" ]; then echo "skip $slug (present)"; continue; fi
  code=$(curl -sL --max-time 90 -A "$UA" -o "$out" -w "%{http_code}" "$url")
  bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)
  if [ "$code" = "200" ] && [ "$bytes" -gt 1000 ]; then
    sum=$(sha256sum "$out" | cut -d' ' -f1)
    echo "$sum  $slug $(basename $out) $bytes $code $TS $url" >> "$MANIFEST"
    echo "ok $slug $bytes"
  else
    echo "FAIL $slug http=$code bytes=$bytes"
  fi
  sleep 2
done
echo "done"
