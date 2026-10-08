#!/bin/bash
# Temporary-job entrypoint: setup -> SGLang manager -> command runner. Everything lives under /job.
set -u
W=/job/work; L=/job/logs
mkdir -p $W/control/inbox $W/control/ran $W/state $W/opt $W/app /job/tmp/bwhome $L
export PATH=$W/opt/bun:$PATH
export BETTERWRIGHT_CHROMIUM_ARGS=--no-sandbox BETTERWRIGHT_HEADLESS=1 BETTERWRIGHT_NO_DAEMON=1
MODEL=/home/user/models/huggingface/hub/models--RadixArk--Qwen3.8-Flash-Next-NVFP4/snapshots/7b719225242aacd3dbd3f9407468c2ee9a9d2594
WARM=/home/user/ai/maintenance/20260919-upgrades/runtime-cache/qwen38-flash-next-sglang

setup() {
  if [ ! -x $W/opt/bun/bun ]; then
    curl -fsSL -o /job/tmp/bun.zip https://github.com/oven-sh/bun/releases/latest/download/bun-linux-x64.zip || return 1
    (cd /job/tmp && unzip -oq bun.zip && mkdir -p $W/opt/bun && mv bun-linux-x64/bun $W/opt/bun/bun && rm -rf bun.zip bun-linux-x64)
  fi
  bun --version
  if [ ! -d $W/app/node_modules/betterwright ]; then
    (cd $W/app && [ -f package.json ] || echo '{"name":"bw-traces","private":true}' > package.json; bun add betterwright@2.8.7) || return 1
  fi
  export BETTERWRIGHT_HOME=/job/home/.betterwright
  (cd $W/app && bun x betterwright setup < /dev/null) || echo "setup returned $?"
  (cd $W/app && bun x betterwright doctor < /dev/null) || true
  # warm JIT caches copied from the production runtime (read-only source)
  if [ -d $WARM ] && [ ! -f $W/state/warm-copied ]; then
    mkdir -p "$TRITON_CACHE_DIR" /job/home/.tilelang /job/home/.cache/sglang /job/cache/sglang
    cp -a $WARM/triton/. "$TRITON_CACHE_DIR"/ 2>/dev/null; cp -a $WARM/.tilelang/. /job/home/.tilelang/ 2>/dev/null
    cp -a $WARM/sglang/. /job/home/.cache/sglang/ 2>/dev/null; cp -a $WARM/sglang/. /job/cache/sglang/ 2>/dev/null
    touch $W/state/warm-copied
  fi
}

sglang_manager() {
  while [ ! -f $W/control/EXIT ]; do
    if [ -f $W/control/NO_SGLANG ]; then sleep 5; continue; fi
    EXTRA=$(cat $W/control/sglang_args.txt)
    echo "$(date -Is) starting sglang: $EXTRA" >> $L/sglang-manager.log
    QWEN_MTP_SHORTLIST=131072 QWEN_MTP_HOTMAP=/opt/qwen-mtp-hotmap.json PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    python3 -m sglang.launch_server --model-path $MODEL --served-model-name qwen3.8-flash-next --tp 1 --trust-remote-code \
      --quantization modelopt_fp4 --fp4-gemm-backend flashinfer_cutlass --context-length 262144 --kv-cache-dtype fp8_e4m3 \
      --mem-fraction-static 0.98 --page-size 64 --chunked-prefill-size 4096 --ple-offload-embedding \
      --linear-attn-prefill-backend triton --linear-attn-decode-backend flashinfer --mamba-ssm-dtype bfloat16 \
      --mamba-radix-cache-strategy extra_buffer --mamba-track-interval 64 \
      --model-loader-extra-config '{"enable_multithread_load":true,"num_threads":16}' \
      --reasoning-parser auto --tool-call-parser auto --sampling-defaults model --stream-interval 4 \
      --host 127.0.0.1 --port 30010 $EXTRA >> $L/sglang.log 2>&1
    echo "$(date -Is) sglang exited $?" >> $L/sglang-manager.log
    sleep 5
  done
}

setup > $L/setup.log 2>&1
echo "setup done $(date -Is)" >> $L/setup.log
sglang_manager &
while [ ! -f $W/control/EXIT ]; do
  for f in $W/control/inbox/*.sh; do
    [ -e "$f" ] || continue
    n=$(basename "$f" .sh); mv "$f" $W/control/ran/$n.sh
    echo "$(date -Is) run $n" >> $L/commands.log
    ( bash $W/control/ran/$n.sh > $L/cmd-$n.log 2>&1; echo "exit=$?" >> $L/cmd-$n.log ) &
  done
  sleep 2
done
echo "$(date -Is) EXIT requested" >> $L/commands.log
pkill -TERM -f sglang.launch_server; pkill -TERM -f dispatcher.mjs; sleep 20; pkill -KILL -f sglang; pkill -KILL -f chrom
exit 0
