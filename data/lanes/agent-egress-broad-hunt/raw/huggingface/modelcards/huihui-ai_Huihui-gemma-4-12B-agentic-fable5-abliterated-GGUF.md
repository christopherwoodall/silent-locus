---
license: apache-2.0
library_name: gguf
pipeline_tag: text-generation
base_model:
- yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF
tags:
- gemma4
- coding
- agentic
- terminal
- tool-use
- reasoning
- thinking
- gguf
- llama.cpp
- local-llm
- abliterated
- uncensored
- GGUF

extra_gated_prompt: >-
    **Usage Warnings**


    “**Risk of Sensitive or Controversial Outputs**“: This model’s safety filtering has been significantly reduced, potentially generating sensitive, controversial, or inappropriate content. Users should exercise caution and rigorously review generated outputs.

    “**Not Suitable for All Audiences**:“ Due to limited content filtering, the model’s outputs may be inappropriate for public settings, underage users, or applications requiring high security.

    “**Legal and Ethical Responsibilities**“: Users must ensure their usage complies with local laws and ethical standards. Generated content may carry legal or ethical risks, and users are solely responsible for any consequences.

    “**Research and Experimental Use**“: It is recommended to use this model for research, testing, or controlled environments, avoiding direct use in production or public-facing commercial applications.

    “**Monitoring and Review Recommendations**“: Users are strongly advised to monitor model outputs in real-time and conduct manual reviews when necessary to prevent the dissemination of inappropriate content.

    “**No Default Safety Guarantees**“: Unlike standard models, this model has not undergone rigorous safety optimization. huihui.ai bears no responsibility for any consequences arising from its use.


---

# huihui-ai/Huihui-gemma-4-12B-agentic-fable5-abliterated-GGUF


This is an uncensored version of [yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF) created with abliteration. 

This ablation was performed entirely using llama.cpp's GGUF model, without relying on Transformers, 

For the specific ablation method, please refer to [cvector-generator](https://github.com/ggml-org/llama.cpp/blob/master/tools/cvector-generator/README.md).



## GGUF


Use the [llama.cpp](https://github.com/ggml-org/llama.cpp) split program to merge model (llama-gguf-split needs to be compiled.),

```
huggingface-cli download huihui-ai/Huihui-gemma-4-12B-agentic-fable5-abliterated-GGUF --local-dir ./huihui-ai/Huihui-gemma-4-12B-agentic-fable5-abliterated-GGUF --token xxx


llama-cli -m huihui-ai/Huihui-gemma-4-12B-agentic-fable5-abliterated-GGUF/Huihui-gemma4-v2-abliterated-Q8_0.gguf -c 8192

```

### Usage Warnings


 - **Risk of Sensitive or Controversial Outputs**: This model’s safety filtering has been significantly reduced, potentially generating sensitive, controversial, or inappropriate content. Users should exercise caution and rigorously review generated outputs.

 - **Not Suitable for All Audiences**: Due to limited content filtering, the model’s outputs may be inappropriate for public settings, underage users, or applications requiring high security.

 - **Legal and Ethical Responsibilities**: Users must ensure their usage complies with local laws and ethical standards. Generated content may carry legal or ethical risks, and users are solely responsible for any consequences.

 - **Research and Experimental Use**: It is recommended to use this model for research, testing, or controlled environments, avoiding direct use in production or public-facing commercial applications.

 - **Monitoring and Review Recommendations**: Users are strongly advised to monitor model outputs in real-time and conduct manual reviews when necessary to prevent the dissemination of inappropriate content.

 - **No Default Safety Guarantees**: Unlike standard models, this model has not undergone rigorous safety optimization. huihui.ai bears no responsibility for any consequences arising from its use.


### Donation

If you like it, please click 'like' and follow us for more updates.  
You can follow [x.com/support_huihui](https://x.com/support_huihui) to get the latest model information from huihui.ai.

##### Your donation helps us continue our further development and improvement, a cup of coffee can do it.
- bitcoin（BTC):
```
  bc1qqnkhuchxw0zqjh2ku3lu4hq45hc6gy84uk70ge
```
- Support our work on Ko-fi (https://ko-fi.com/huihuiai)!
