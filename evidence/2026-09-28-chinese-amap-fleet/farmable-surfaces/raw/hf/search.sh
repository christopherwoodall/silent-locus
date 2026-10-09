#!/bin/bash
# HF hub API sweeps — operator markers, amap fleet dataset, agent infra
OUT=.
for q in uqscan uqcors uqtag sub_poi_navi lhr.life is.gd httpbun openai_research urlquery; do
  curl -s --max-time 60 "https://huggingface.co/api/datasets?search=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=100" -o "$OUT/ds__$q.json"
  curl -s --max-time 60 "https://huggingface.co/api/models?search=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=100" -o "$OUT/mo__$q.json"
  curl -s --max-time 60 "https://huggingface.co/api/spaces?search=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=100" -o "$OUT/sp__$q.json"
done
for q in amap 高德 "poi entrance" entrance navigation 入口 navi "poi navigation" "entrance navi"; do
  curl -s --max-time 60 "https://huggingface.co/api/datasets?search=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=100" -o "$OUT/dsA__$q.json"
done
for q in "webhook receiver" requestbin "cors proxy" "tunnel dashboard" "url to markdown" fetch-proxy webhook.site; do
  curl -s --max-time 60 "https://huggingface.co/api/spaces?search=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=100" -o "$OUT/spI__$q.json"
done
echo done; ls -la
