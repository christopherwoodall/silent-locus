---
license: apache-2.0
task_categories:
- question-answering
language:
- en
tags:
- factuality
- search
- retrieval
- deep research
- comprehensiveness
- agent
- posttraining
- benchmark
- Google DeepMind
pretty_name: DeepSearchQA
size_categories:
- n<1K
configs:
- config_name: deepsearchqa
  default: true
  data_files:
  - split: eval
    path: DSQA-full.csv
---
# DeepSearchQA
#### A 900-prompt factuality benchmark from Google DeepMind, designed to evaluate agents on difficult multi-step information-seeking tasks across 17 different fields.

▶ [Google DeepMind Release Blog Post](https://blog.google/technology/developers/deep-research-agent-gemini-api/)\
▶ [DeepSearchQA Leaderboard on Kaggle](https://www.kaggle.com/benchmarks/google/dsqa)\
▶ [Technical Report](https://storage.googleapis.com/deepmind-media/DeepSearchQA/DeepSearchQA_benchmark_paper.pdf)\
▶ [Evaluation Starter Code](https://www.kaggle.com/code/andrewmingwang/deepsearchqa-starter-code)


## Benchmark

DeepSearchQA is a 900-prompt benchmark for evaluating agents on difficult multi-step information-seeking tasks across 17 different fields. Unlike traditional benchmarks that target single-answer retrieval or broad-spectrum factuality, DeepSearchQA features a dataset of challenging, hand-crafted tasks designed to evaluate an agent’s ability to execute complex search plans to generate exhaustive answer lists.

Each task is structured as a "causal chain", where discovering information for one step is dependent on the successful completion of the previous one, stressing long-horizon planning and context retention. All tasks are grounded in the open web with objectively verifiable answer sets. 

DeepSearchQA is meant to be used to evaluate LLMs or LLM agents with access to the web.

## Dataset Description

This dataset is a collection of 900 examples. Each example is composed of:

* A problem (`problem`) which is the prompt testing parametric knowledge.
* A problem category (`problem_category`) specifying which of 17 different domains the problem belongs to.
* A gold answer (`answer`) which is used in conjunction with the evaluation prompt to judge the correctness of an LLM's response.
* An answer type classification (`answer_type`) specifying whether a single answer or set of answers is expected as a response. This information should NOT be given to the LLM during inference time. 65% of answers are of type `Set Answer`.

See the [Technical Report](https://storage.googleapis.com/deepmind-media/DeepSearchQA/DeepSearchQA_benchmark_paper.pdf) for methodology details.

## Limitations
While DeepSearchQA offers a robust framework for evaluating comprehensive retrieval, it relies on
specific design choices that entail certain limitations. By employing an exclusively outcome-based
evaluation, we effectively treat any agent that is evaluated as a black box. In the absence of trajectory data, it is difficult
to distinguish between an agent that reasoned correctly and one that arrived at the correct list through
inefficient or accidental means (e.g., lucky guessing). Additionally, the static web assumption, while
necessary for reproducibility, limits the evaluation of “breaking news” retrieval where ground truth is
volatile. A task’s ground truth may become outdated if source websites are removed or their content
is significantly altered. This is a prevalent challenge for all benchmarks operating on the live web,
necessitating periodic manual reviews and updates to the dataset.

Questions, comments, or issues? Share your thoughts with us in the [discussion forum](https://www.kaggle.com/benchmarks/google/dsqa/discussion).

## Evaluation Prompt
The autorater which should be used for DeepSearchQA is `gemini-2.5-flash` with the grading prompt found in the [starter notebook](https://www.kaggle.com/code/andrewmingwang/deepsearchqa-starter-code) on Kaggle. Using a different autorater model or grading prompt will likely result in statistically significant deviation in results.

## Citation

Coming soon.