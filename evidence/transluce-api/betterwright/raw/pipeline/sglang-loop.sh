#!/bin/bash
# Own SGLang supervisor (replaces run.sh's manager; control/NO_SGLANG keeps that one idle).
W=/job/work; L=/job/logs
MODEL=/home/user/models/huggingface/hub/models--RadixArk--Qwen3.8-Flash-Next-NVFP4/snapshots/7b719225242aacd3dbd3f9407468c2ee9a9d2594
if [ ! -f $W/state/warm-wiped ]; then rm -rf /job/cache/triton /job/home/.tilelang /job/home/.cache/sglang /job/cache/sglang; mkdir -p /job/cache/triton; touch $W/state/warm-wiped; fi
export SGLANG_CACHE_DIR=/job/cache/sglang TORCHINDUCTOR_CACHE_DIR=/job/cache/sglang/inductor
while [ ! -f $W/control/EXIT ]; do
  if [ -f $W/control/SGLANG_PAUSE ]; then sleep 5; continue; fi
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
    --host 127.0.0.1 --port 30010 $EXTRA > $L/sglang.log 2>&1
  echo "$(date -Is) sglang exited $?" >> $L/sglang-manager.log
  sleep 5
done
