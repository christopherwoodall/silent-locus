---
annotations_creators:
- manual
language:
- zh
license:
- apache-2.0
pretty_name: Titan CV Agent Benchmark
task_categories:
- visual-question-answering
task_ids:
- visual-question-answering
---


# Titan CV Agent Benchmark

[[中文版]](README_CN.md)

**The Titan CV Benchmark is primarily designed to evaluate the performance of AGENTS in the field of computer vision (CV).** We have collected more than 200 test examples to comprehensively test the performance of the agent, particularly their capability to solve problems step by step.

> [!IMPORTANT]
>
> **Demo Video: https://youtu.be/dcUb4lUnGj4**
>
> **Github: https://github.com/DataCanvasAILab/Titan-CV-Agent-Benchmark**
>
> **Media files are also available for download via the link below: [Google Drive](https://drive.google.com/file/d/14lcUsIBm1YshG-wajzWQdicBpitRhRGW/view?usp=drive_link)**



## Basic principles

In order to distinguish the traditional benchmark of VLM, all collected samples will follow the following principles:

① **Diverse modalities**, including various types of images and videos, and **rich application domains** such as industry, medicine, agriculture, environment, society, culture, sports, and scientific research.

② Each problem will try to maintain its complexity, and **it cannot be solved in a single step** (e.g., using a VLM alone). Instead, it requires multi-step serial thinking.

③ Each problem will focus on the intelligence of the intelligent agent. **The problems should appear simple to humans but be complex for machines.** Except in the medical field, it can be easily understood by any inexperienced adult, but it needs to fully mobilize its thinking and cognitive abilities. **For machines, traditional advantages such as memorization, calculation, or speed are not helpful in solving these problems**, and they need spatial cognition or advanced understanding abilities similar to humans.

④ Each question is complex, but **the answer is simple and verifiable**, avoiding the ambiguity and complexity of open-ended question evaluation. If it is a question similar to the position difference, certain options will be given to avoid ambiguity, but at the same time, in order to prevent the intelligent agent from guessing the correct answer, the alternative answers are usually set to more than 6 to reduce the risk of guessing.



## Titan CV Agent Series

[Titan CV Agent Sandbox](https://github.com/DataCanvasAILab/Titan-CV-Agent-Sandbox)

[Titan CV Agent Executor](https://github.com/DataCanvasAILab/Titan-CV-Agent-Executor)

[Titan CV Agent Benchmark](https://github.com/DataCanvasAILab/Titan-CV-Agent-Benchmark)



## Quantity Classification

This test set collects most of the CV problems on the market and divides them into **4 categories and 22 subcategories**:

### Industrial Manufacturing and People's Livelihood Technology (35%)

1. **Industrial Manufacturing** (10%) (Industrial Automation Detection / Packaging and Logistics Sorting System / Building Safety Monitoring / Energy and Power Inspection)

2. **Public Safety** (8%) (Security Monitoring and Abnormal Behavior Detection / Face and License Plate Recognition / Crowd Density Estimation and Traffic Analysis / Fireworks and Fire Automatic Detection and Warning)

3. **Medical Health** (8%) (Medical Image Analysis / Visual Assistance and Blind Navigation Technology / Personalized Rehabilitation)

4. **Agricultural Production** (6%) (Pest and Disease Detection / Drone Image Processing / Plant Identification and Gardening Guidance / Crop Quality Inspection)

5. **Environmental Monitoring** (3%) (Remote Sensing Image Analysis / Garbage Classification / Animal Identification and Ecological Protection / Soil and Water Quality Analysis / Disaster Emergency Response and Rescue)

### Smart City and Smart Life (30%)

6. **Fintech** (8%) (risk control / ticket identification and authenticity detection / blockchain / investment advice)
7. **Transportation and logistics** (8%) (autonomous driving technology / intelligent traffic management / license plate recognition and parking management / logistics management / package management)
8. **Smart terminals** (6%) (augmented reality and virtual reality / smart home / smart wearables / smart toys and game interaction / indoor navigation and mapping / human-computer interaction gesture and posture recognition)
9. **E-commerce** (5%) (cross-border e-commerce / smart retail and automatic checkout / online shopping / human 3D modeling / virtual fitting)
10. **Social life** (3%) (emotion recognition and user experience / content tagging / topic detection / intelligent advertising recommendation)

### Cultural tourism and sports entertainment (20%)

11. **Cultural education** (4%) (online classroom / educational marketing / smart education / art restoration / handwriting font recognition)
12. **Travel guide** (4%) (smart park / scenic spot parking / life interconnection / Cultural and creative products)
13. **Media and entertainment** (3%) (content creation / content review / video summary / intelligent editing / forgery detection / emoticon generation)
14. **Sports technology** (3%) (human behavior analysis / sports analysis / sports tracking / somatosensory games)
15. **Photo editing and beauty** (2%) (shooting optimization, beauty / smart album / makeup simulation / hair design)
16. **Pet breeding** (2%) (pet monitoring / pet health care / smart feeding / pet interaction)
17. **Art collection** (2%) (authenticity identification of cultural relics and jewelry / art value assessment)

### Scientific research and professional fields (15%)

18. **Scientific research** (4%) (marine life identification / animal migration research / psychological research)
19. **Office workplace** (4%) (meeting records and automatic summaries / remote collaboration / intelligent attendance)
20. **Government and judicial affairs** (3%) (government collaboration / smart human resources / evidence analysis / intelligent trial / Contract review)
21. **Military and defense** (2%) (situational awareness / camouflage detection / enemy equipment identification)
22. **Aerospace** (2%) (satellite image analysis / aircraft takeoff and landing monitoring / runway foreign object detection / pilot assistance system)

**Note:** Data items in these categories will be collected gradually. The currently available public datasets only cover categories 1 through 8, and the remaining items will be gradually open sourced.



## Quantity distribution

|                                                        |                               | Relative Proportion (%) | Subtotal Proportion (%) | Absolute Quantity | Subtotal Quantity |
| ------------------------------------------------------ | ----------------------------- | ----------------------- | ----------------------- | ----------------- | ----------------- |
| **Industrial manufacturing and livelihood technology** | Industrial manufacturing      | 10                      | 35                      | 50                | 175               |
|                                                        | Public security               | 8                       |                         | 40                |                   |
|                                                        | Healthcare                    | 8                       |                         | 40                |                   |
|                                                        | Agricultural production       | 6                       |                         | 30                |                   |
|                                                        | Environmental monitoring      | 3                       |                         | 15                |                   |
| **Smart city and smart life**                          | Fintech                       | 8                       | 30                      | 40                | 150               |
|                                                        | Transportation and logistics  | 8                       |                         | 40                |                   |
|                                                        | Smart terminals               | 6                       |                         | 30                |                   |
|                                                        | E-commerce                    | 5                       |                         | 25                |                   |
|                                                        | Social life                   | 3                       |                         | 15                |                   |
| **Cultural tourism and sports entertainment**          | Culture and education         | 4                       | 20                      | 20                | 100               |
|                                                        | Travel guide                  | 4                       |                         | 20                |                   |
|                                                        | Media and entertainment       | 3                       |                         | 15                |                   |
|                                                        | Sports technology             | 3                       |                         | 15                |                   |
|                                                        | Photo editing and beauty      | 2                       |                         | 10                |                   |
|                                                        | Pet breeding                  | 2                       |                         | 10                |                   |
|                                                        | Art collection                | 2                       |                         | 10                |                   |
| **Scientific research and professional fields**        | Scientific research           | 4                       | 15                      | 20                | 75                |
|                                                        | Office                        | 4                       |                         | 20                |                   |
|                                                        | Government and justice        | 3                       |                         | 15                |                   |
|                                                        | Military and national defense | 2                       |                         | 10                |                   |
|                                                        | Aerospace                     | 2                       |                         | 10                |                   |
| Total                                                  | N/A                           | 100                     |                         | 500               |                   |

**Note:** Data items in these categories will be collected gradually. Currently, the public dataset only involves 1 to 8 of them. The remaining items will be gradually open sourced.



## Data format example

### Data format

Each data item contains 6 fields:

```
"id": Data item number, named according to "categories_subcategories_items".
"media_path": The path to the media file associated with the data item.
"media_type": Media type that the data item depends on.
"query": The question posed regarding the media content.
"answer": Answer to the question.
"note": Notes, such as a record of how the answer was obtained.
```

### Data example

```json
[
    {
        "id": "1_1_1",
        "media_path": "media/01/1_1_1.mp4",
        "media_type": "video",
        "query": "有一个监控摄像头设置在生产线出料口，加工完的金属零件会沿着绿色倾斜平面滑落到下方接料盒，请统计一共有多少金属零件被生产出来？请回答一个整数，例如：10。请直接输出答案，不要输出任何符号、解释或说明。",
        "answer": "11",
        "note": "2+3+4+2=11"
    },
    {
        "id": "1_1_2",
        "media_path": "media/01/1_1_2.mp4",
        "media_type": "video",
        "query": "为了监督工人的产品专配过程，防止漏装、错装，工人的左手边、右手边和中间各有三堆零件，请阐述其零件拿取顺序，零件可以重复拿取。请按照：(中文单字,中文单字,中文单字)的格式直接回答，例如：(中,左,左)。请直接输出答案，不要输出任何符号、解释或说明。",
        "answer": "(右,左,中)",
        "note": "共计4个零件"
    },
    {
        "id": "1_1_3",
        "media_path": "media/01/1_1_3.mp4",
        "media_type": "video",
        "query": "请制作一个焊接检测系统，检测绿色电路板中零件数量和每个零件需要自动焊接多少次？请按照：(零件数量（整数）,每个零件需要自动焊接次数（整数）)的格式直接回答，例如：(10,1)。请直接输出答案，不要输出任何符号、解释或说明。",
        "answer": "(60,2)",
        "note": ""
    }
]
```



## Data Media Examples

### Industrial Manufacturing

![01_collage](imgs/01_collage.jpg)

### Public safety

![02_collage](imgs/02_collage.jpg)

### Healthcare

![03_collage](imgs/03_collage.jpg)

### Agricultural production

![04_collage](imgs/04_collage.jpg)

### Environmental monitoring

![05_collage](imgs/05_collage.jpg)

### Financial technology

![06_collage](imgs/06_collage.jpg)

### Transportation and logistics

![07_collage](imgs/07_collage.jpg)

### Smart terminals

![08_collage](imgs/08_collage.jpg)



## Acknowledgments

**This project is supported by:**

***[Datacanvas - Empowering AI Native Businesses Worldwide](https://www.datacanvas.com/en/AboutUs)***

> TEL: +86 400-805-7188
>
> Email: sophia@zetyun.com
>
> Beijing Office: 6F&8F, Building C, HEYING Center, 10 Xiaoyingxi Road, Haidian District, Beijing, China
>
> Shanghai Office: 10F, Building 1, SHIBEI TBC Center, Lane 1401, Jiangchang Road, Jing'an District, Shanghai, China



## License

**Titan CV Agent Benchmark uses the following license agreement:**

**Apache License Version 2.0**