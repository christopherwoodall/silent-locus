---
base_model: medismera/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic
language:
- en
- zh
- ar
library_name: transformers
license: apache-2.0
mradermacher:
  readme_rev: 1
quantized_by: mradermacher
tags:
- qwen
- qwen3.8
- abliterated
- uncensored
- agentic
- tool-calling
- function-calling
- hermes-agent
- mythos-class
- task-tree
- sglang
- vllm
- fp8
- awq
- mamba
- linear-attention
- coding
- reasoning
- cot
---
## About

<!-- ### quantize_version: 2 -->
<!-- ### output_tensor_quantised: 1 -->
<!-- ### convert_type: hf -->
<!-- ### vocab_type:  -->
<!-- ### tags:  -->
<!-- ### quants:  x-f16 Q4_K_S Q2_K Q8_0 Q6_K Q3_K_M Q3_K_S Q3_K_L Q4_K_M Q5_K_S Q5_K_M IQ4_XS -->
<!-- ### quants_skip:  -->
<!-- ### skip_mmproj:  -->
static quants of https://huggingface.co/medismera/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic

<!-- provided-files -->

***For a convenient overview and download list, visit our [model page for this model](https://hf.tst.eu/model#Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF).***

weighted/imatrix quants are available at https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-i1-GGUF
## Usage

If you are unsure how to use GGUF files, refer to one of [TheBloke's
READMEs](https://huggingface.co/TheBloke/KafkaLM-70B-German-V0.1-GGUF) for
more details, including on how to concatenate multi-part files.

## Provided Quants

(sorted by size, not necessarily quality. IQ-quants are often preferable over similar sized non-IQ quants)

| Link | Type | Size/GB | Notes |
|:-----|:-----|--------:|:------|
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.mmproj-Q8_0.gguf) | mmproj-Q8_0 | 0.7 | multi-modal supplement |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.mmproj-f16.gguf) | mmproj-f16 | 1.0 | multi-modal supplement |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q2_K.gguf) | Q2_K | 11.0 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q3_K_S.gguf) | Q3_K_S | 12.4 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q3_K_M.gguf) | Q3_K_M | 13.6 | lower quality |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q3_K_L.gguf) | Q3_K_L | 14.7 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.IQ4_XS.gguf) | IQ4_XS | 15.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q4_K_S.gguf) | Q4_K_S | 15.9 | fast, recommended |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q4_K_M.gguf) | Q4_K_M | 16.9 | fast, recommended |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q5_K_S.gguf) | Q5_K_S | 19.1 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q5_K_M.gguf) | Q5_K_M | 19.6 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q6_K.gguf) | Q6_K | 22.5 | very good quality |
| [GGUF](https://huggingface.co/mradermacher/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic-GGUF/resolve/main/Qwen3.8-27B-OBLITERATED-Mythos-Class-Agentic.Q8_0.gguf) | Q8_0 | 29.1 | fast, best quality |

Here is a handy graph by ikawrakow comparing some lower-quality quant
types (lower is better):

![image.png](https://www.nethype.de/huggingface_embed/quantpplgraph.png)

And here are Artefact2's thoughts on the matter:
https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9

## FAQ / Model Request

See https://huggingface.co/mradermacher/model_requests for some answers to
questions you might have and/or if you want some other model quantized.

## Thanks

I thank my company, [nethype GmbH](https://www.nethype.de/), for letting
me use its servers and providing upgrades to my workstation to enable
this work in my free time. Additional thanks to [@nicoboss](https://huggingface.co/nicoboss) for giving me access to his private supercomputer, enabling me to provide many more imatrix quants, at much higher quality, than I would otherwise be able to.

<!-- end -->
