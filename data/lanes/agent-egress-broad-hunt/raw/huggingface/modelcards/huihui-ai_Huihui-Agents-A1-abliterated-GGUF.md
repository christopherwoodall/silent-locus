---
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
base_model:
- InternScience/Agents-A1
tags:
- moe
- vlm
- vision
- agentic
- abliterated
- uncensored
- huihui
---

# huihui-ai/Huihui-Agents-A1-abliterated-GGUF


This is an uncensored version of [InternScience/Agents-A1](https://huggingface.co/InternScience/Agents-A1) created with abliteration (see [remove-refusals-with-transformers](https://github.com/Sumandora/remove-refusals-with-transformers) to know more about it).
This is a crude, proof-of-concept implementation to remove refusals from an LLM model without using TransformerLens.

## llama.cpp
Use the latest [llama.cpp](https://github.com/ggml-org/llama.cpp),
```
llama-cli -m huihui-ai/Huihui-Agents-A1-abliterated-GGUF/Agents-A1-abliterated-bf16.gguf -c 262144
```

### Usage Warnings


 - **Risk of Sensitive or Controversial Outputs**: This model’s safety filtering has been significantly reduced, potentially generating sensitive, controversial, or inappropriate content. Users should exercise caution and rigorously review generated outputs.

 - **Not Suitable for All Audiences**: Due to limited content filtering, the model’s outputs may be inappropriate for public settings, underage users, or applications requiring high security.

 - **Legal and Ethical Responsibilities**: Users must ensure their usage complies with local laws and ethical standards. Generated content may carry legal or ethical risks, and users are solely responsible for any consequences.

 - **Research and Experimental Use**: It is recommended to use this model for research, testing, or controlled environments, avoiding direct use in production or public-facing commercial applications.

 - **Monitoring and Review Recommendations**: Users are strongly advised to monitor model outputs in real-time and conduct manual reviews when necessary to prevent the dissemination of inappropriate content.

 - **No Default Safety Guarantees**: Unlike standard models, this model has not undergone rigorous safety optimization. huihui.ai bears no responsibility for any consequences arising from its use.


### Donation
##### Your donation helps us continue our further development and improvement, a cup of coffee can do it.
- bitcoin:
```
  bc1qqnkhuchxw0zqjh2ku3lu4hq45hc6gy84uk70ge
```
- Support our work on [Ko-fi](https://ko-fi.com/huihuiai)!

