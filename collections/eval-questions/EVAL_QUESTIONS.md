# EVAL Questions — Unified Corpus (W3 enrichment)

**Records:** 10201 across 11 evals (DeepSearchQA banked separately, untouched). Enriched 2026-10-05 by `_tools/enrich.py` (stdlib only).

## Corpus totals

| eval | questions | license |
|---|---|---|
| openai-simpleqa | 4326 | MIT (simple-evals repo) |
| google-facts-grounding | 860 | cc-by-4.0 |
| google-frames | 824 | apache-2.0 |
| assistantbench | 181 | apache-2.0 |
| mind2web | 1009 | cc-by-4.0 |
| webvoyager | 643 | apache-2.0 |
| webarena | 812 | apache-2.0 |
| tau-bench | 165 | MIT |
| sealqa | 619 | apache-2.0 |
| webwalkerqa | 680 | apache-2.0 |
| openai-mle-bench | 82 | MIT |

### Topic distribution (top 15, corpus-wide)

- other: 2520
- entertainment: 2012
- science: 1161
- politics: 883
- sports: 661
- geography: 614
- travel: 313
- shopping: 310
- tech: 277
- history: 268
- health: 132
- retail: 115
- food: 82
- education: 70
- finance: 55

### Expected-source domains (top 20, corpus-wide)

(Marker entries with empty `domain_or_url` and `selfhosted:*` env tags excluded from domain counts; marker totals below.)

- en.wikipedia.org: 7978
- selfhosted:gitlab: 204
- selfhosted:shopping: 192
- selfhosted:shopping_admin: 184
- google.com: 178
- imdb.com: 145
- mathshistory.st-andrews.ac.uk: 134
- selfhosted:reddit: 129
- selfhosted:map: 128
- wikiwand.com: 85
- es.wikipedia.org: 77
- espn.com: 76
- kaggle.com: 74
- amazon.com: 69
- britannica.com: 65
- kids.kiddle.co: 62
- apple.com: 62
- bbc.com: 57
- booking.com: 56
- github.com: 53

### Empty-source markers (why the list is empty)

- `context-provided-no-web-needed`: 553
- `synthetic-policy-no-live-web`: 165
- `no-metadata-no-prior`: 50

---

## openai-simpleqa

- **Questions:** 4326
- **License:** MIT (simple-evals repo)
- **Source:** https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- entertainment: 1319
- science: 858
- politics: 709
- other: 475
- geography: 424
- sports: 368
- history: 173

**Most common expected-source domains (top 15):**

- en.wikipedia.org: 4890
- mathshistory.st-andrews.ac.uk: 134
- imdb.com: 124
- wikiwand.com: 85
- es.wikipedia.org: 77
- britannica.com: 65
- kids.kiddle.co: 62
- familysearch.org: 49
- researchgate.net: 45
- rsc.org: 44
- web.archive.org: 42
- dbpedia.org: 39
- degruyter.com: 35
- alchetron.com: 33
- archives.nypl.org: 33

**Examples:**

- Q (simpleqa-02652, topic=geography): Which lake in Kashmir, India, is known as "the jewel in the ring"?
  sources: https://en.wikipedia.org/wiki/Nigeen_Lake, https://srinagar.nic.in/tourist-place/nigeen-lake/#:~:text=The%20Nigeen%20lake%20is%20surrounded,the%20jewel%20in%20the%20ring%E2%80%9D., https://www.tripadvisor.in/ShowUserReviews-g297623-d338344-r365499934-Nigeen_Lake-Srinagar_Srinagar_District_Kashmir_Jammu_and_Kashmir.html
  fp: "lake in kashmir india is known as the"
  fp: "jewel in the ring"
- Q (simpleqa-01235, topic=geography): What was the population of Spring Rock Township, Clinton County, Iowa, at the time of the 2000 Census?
  sources: https://en.wikipedia.org/wiki/Spring_Rock_Township,_Clinton_County,_Iowa, https://www.iowadatacenter.org/datatables/Township/mcdpopulation2000.pdf, https://www.iowadatacenter.org/datatables/Township/mcdpopbycounty19902000.pdf
  fp: "population of spring rock township clinton county iowa"
  fp: "time of the 2000 census"
- Q (simpleqa-03234, topic=politics): Give the full name of the Indian politician from Jammu and Kashmir who is popularly known as Sher-e-Gool Gulabgarh.
  sources: https://en.wikipedia.org/wiki/Ajaz_Ahmed_Khan, https://en.wikipedia.org/wiki/Ajaz_Ahmed_Khan#:~:text=Aijaz%20Ahmad%20Khan%20popularly%20known,Assembly%20from%20Gool%20Arnas%20constituency., https://www.lokmattimes.com/topics/ajaz-ahmed/
  fp: "give the full name of the indian politician"
  fp: "jammu and kashmir who is popularly known as"
  fp: "sher e gool gulabgarh"


## google-facts-grounding

- **Questions:** 860
- **License:** cc-by-4.0
- **Source:** https://huggingface.co/datasets/google/FACTS-grounding-public/resolve/main/examples.csv
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- other: 622
- health: 99
- gov-policy: 26
- tech: 25
- finance: 22
- entertainment: 14
- shopping: 14
- geography: 10
- science: 8
- politics: 7

**Most common expected-source domains (top 15):**

- en.wikipedia.org: 287
- supremecourt.gov: 5
- apple.com: 4
- google.com: 4
- microsoft.com: 3
- nasa.gov: 1
- amazon.com: 1
- fda.gov: 1
- spotify.com: 1

**Markers:** `context-provided-no-web-needed`: 553

**Examples:**

- Q (facts-0666, topic=other): Can you explain CAUTION?
  sources: [context-provided-no-web-needed]
  fp: "can you explain caution"
- Q (facts-0049, topic=other): Compare how technology has affected children's attention space to how reading affects it. What are the technological advances that negatively shifted the way children's attention span works? Also what are some that posit
  sources: [context-provided-no-web-needed]
  fp: "compare how technology has affected children s attention"
  fp: "reading affects it what are the technological advances"
  fp: "negatively shifted the way children s attention span"
- Q (facts-0074, topic=other): Only using the provided text, in which types of solid tumors does BRAF mutations occur?
  sources: [context-provided-no-web-needed]
  fp: "using the provided text in which types of"
  fp: "solid tumors does braf mutations occur"


## google-frames

- **Questions:** 824
- **License:** apache-2.0
- **Source:** https://huggingface.co/datasets/google/frames-benchmark/resolve/main/test.tsv
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- other: 285
- entertainment: 166
- geography: 103
- politics: 93
- sports: 82
- history: 38
- science: 18
- health: 18
- finance: 10
- gov-policy: 3

**Most common expected-source domains (top 15):**

- en.wikipedia.org: 2132
- en.m.wikipedia.org: 26
- nba.com: 9
- nfl.com: 9
- fifa.com: 6
- mlb.com: 6
- netflix.com: 3
- un.org: 2
- cdc.gov: 1
- en.wikipedia.org/wiki/grazia_deledda: 1
- en.wikipedia.org/wiki/list_of_female_nobel_laureates: 1
- nasa.gov: 1
- nhl.com: 1
- w.wiki: 1
- apple.com: 1

**Examples:**

- Q (frames-0548, topic=entertainment): How many years after Anton Grylewicz's date of birth was the second SpongeBob Squarepants movie released? Round down to the nearest year (e.g. January 1999 to December 2000 = 1 year, despite being closer to 2).
  sources: https://en.wikipedia.org/wiki/Anton_Grylewicz, https://en.wikipedia.org/wiki/SpongeBob_SquarePants#Franchise
  fp: "years after anton grylewicz s date of birth"
  fp: "second spongebob squarepants movie released round down to"
  fp: "nearest year e g january 1999 to december"
- Q (frames-0096, topic=other): In which of the three Intertidal zones would you most likely find the Septifer bilocularis?
  sources: https://en.wikipedia.org/wiki/Septifer_bilocularis, https://en.wikipedia.org/wiki/Mytilidae, https://en.wikipedia.org/wiki/Intertidal_zone
  fp: "three intertidal zones would you most likely find"
  fp: "intertidal zones would you most likely find the"
- Q (frames-0374, topic=other): How old was Russian vodka tycoon Yuri Shefler when Serene, the yacht he commissioned, was delivered to him?
  sources: https://en.wikipedia.org/wiki/Serene_(yacht), https://en.wikipedia.org/wiki/Yuri_Shefler
  fp: "old was russian vodka tycoon yuri shefler when"
  fp: "serene the yacht he commissioned was delivered to"


## assistantbench

- **Questions:** 181
- **License:** apache-2.0
- **Source:** https://huggingface.co/datasets/AssistantBench/AssistantBench/resolve/main/assistant_bench_v1.0_test.jsonl
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- other: 116
- entertainment: 20
- sports: 12
- geography: 6
- travel: 5
- science: 5
- food: 5
- shopping: 3
- tech: 2
- politics: 2

**Most common expected-source domains (top 15):**

- en.wikipedia.org: 100
- google.com: 10
- nba.com: 5
- imdb.com: 3
- amazon.com: 2
- nfl.com: 1
- github.com: 1
- ebay.com: 1
- apple.com: 1
- findmeglutenfree.com: 1
- cdc.gov: 1
- monday.com: 1
- booking.com: 1
- microsoft.com: 1
- supremecourt.gov: 1

**Markers:** `no-metadata-no-prior`: 50

**Examples:**

- Q (5a51e05719b356ab3597aa50e3d057eb67ef3530fd2092fac0eaabd4b343bea4, topic=other): What is the CVSS score for the latest (until May 2024) critical vulnerability in the OpenSSL library?
  sources: en.wikipedia.org
  fp: "cvss score for the latest until may 2024"
  fp: "critical vulnerability in the openssl library"
- Q (211ace94acd5df42b52ab308ab1d79c3dc81e41cb093cef185ed20f25e9f377a, topic=science): Which game company, with a popular GOG Galaxy integration on GitHub (over 100 stars), has development offices in NYC?
  sources: github.com
  fp: "game company with a popular gog galaxy integration"
  fp: "stars has development offices in nyc"
- Q (f16dd8c68dcc27ea386f49f8cbb6e46d1c9ede8a8c20b3416ddae1483eb38b09, topic=other): Which restaurants in the Farmingdale, New York neighborhood take online dinner reservations for a party of 10 through Open Table?
  sources: en.wikipedia.org
  fp: "restaurants in the farmingdale new york neighborhood take"
  fp: "online dinner reservations for a party of"


## mind2web

- **Questions:** 1009
- **License:** cc-by-4.0
- **Source:** https://huggingface.co/datasets/osunlp/Mind2Web/resolve/main/data/train/train_{0..10}.json
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- travel: 284
- entertainment: 213
- shopping: 178
- other: 166
- food: 65
- sports: 55
- tech: 30
- geography: 17
- history: 1

**Most common expected-source domains (top 15):**

- united.com: 24
- budget.com: 24
- ticketcenter.com: 22
- newegg.com: 21
- spothero.com: 21
- uniqlo.com: 20
- resy.com: 20
- yelp.com: 20
- kayak.com: 19
- gamestop.com: 19
- imdb.com: 18
- espn.com: 18
- rei.com: 17
- new.mta.info: 17
- aa.com: 17

**Examples:**

- Q (117c1176-b5bd-4b9a-9be2-80a7f390e207, topic=entertainment): Find the US box office revenue for the highest tomatometer rated movie that the actress playing Sam Carpenter in the most recent Scream movie has been in.
  sources: rottentomatoes.com
  fp: "find the us box office revenue for the"
  fp: "highest tomatometer rated movie that the actress playing"
  fp: "sam carpenter in the most recent scream movie"
- Q (70b3ef5b-d900-44cf-9b62-9ecece97954c, topic=shopping): Find climbing gear and sort the results by price high to low.
  sources: rei.com
  fp: "find climbing gear and sort the results by"
  fp: "price high to low"
- Q (8aedabbf-a7b4-4da7-8eaf-9e159a3ec99b, topic=entertainment): review the dinner menu of La Bergamote restaurant in Hell's Kitchen.
  sources: nyc.gov
  fp: "review the dinner menu of la bergamote restaurant"
  fp: "dinner menu of la bergamote restaurant in hell"


## webvoyager

- **Questions:** 643
- **License:** apache-2.0
- **Source:** https://raw.githubusercontent.com/MinorJerry/WebVoyager/main/data/WebVoyager_data.jsonl
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- Wolfram Alpha: 46
- Allrecipes: 45
- Booking: 44
- ESPN: 44
- Apple: 43
- ArXiv: 43
- Cambridge Dictionary: 43
- Google Search: 43
- Huggingface: 43
- BBC News: 42

**Most common expected-source domains (top 15):**

- google.com: 126
- wolframalpha.com: 46
- allrecipes.com: 45
- booking.com: 44
- espn.com: 44
- apple.com: 43
- arxiv.org: 43
- dictionary.cambridge.org: 43
- huggingface.co: 43
- bbc.com: 42
- coursera.org: 42
- amazon.com: 41
- github.com: 41

**Examples:**

- Q (Google Flights--16, topic=Google Flights): Find the cheapest one-way flight from New York to Tokyo departing on January 15, 2024, and provide the airline and total flight duration.
  sources: https://www.google.com/travel/flights/
  fp: "find the cheapest one way flight from new"
  fp: "2024 and provide the airline and total flight"
  fp: "york to tokyo departing on january"
- Q (Google Flights--0, topic=Google Flights): Book a journey with return option on same day from Edinburg to Manchester on December 28th and show me the lowest price option available.
  sources: https://www.google.com/travel/flights/
  fp: "day from edinburg to manchester on december"
  fp: "show me the lowest price option available"
  fp: "book a journey with return option on same"
- Q (Amazon--26, topic=Amazon): Find a portable Bluetooth speaker on Amazon with a water-resistant design, under $50. It should have a minimum battery life of 10 hours.
  sources: https://www.amazon.com/
  fp: "find a portable bluetooth speaker on amazon with"
  fp: "water resistant design under"
  fp: "minimum battery life of"


## webarena

- **Questions:** 812
- **License:** apache-2.0
- **Source:** https://raw.githubusercontent.com/web-arena-x/webarena/main/config_files/test.raw.json
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- other: 603
- shopping: 107
- entertainment: 27
- travel: 16
- geography: 15
- tech: 15
- finance: 13
- food: 6
- health: 4
- gov-policy: 3

**Most common expected-source domains (top 15):**

- selfhosted:gitlab: 204
- selfhosted:shopping: 192
- selfhosted:shopping_admin: 184
- selfhosted:reddit: 129
- selfhosted:map: 128
- selfhosted:wikipedia: 23

**Examples:**

- Q (webarena-0246, topic=other): Show me the name of the customer who is the most unhappy with Chloe tank
  sources: selfhosted:shopping_admin
  fp: "unhappy with chloe tank"
  fp: "name of the customer"
- Q (webarena-0092, topic=geography): Which US states border Vermont?
  sources: selfhosted:map
  fp: "which us states border vermont"
- Q (webarena-0564, topic=other): create a repository named live_a_life that includes a README file with the links to the most active 3 DIY ideas on DIY subreddit?
  sources: selfhosted:gitlab, selfhosted:reddit
  fp: "create a repository named live a life that"
  fp: "includes a readme file with the links to"
  fp: "diy ideas on diy subreddit"


## tau-bench

- **Questions:** 165
- **License:** MIT
- **Source:** https://github.com/sierra-research/tau-bench
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- retail: 115
- airline: 50

**Most common expected-source domains (top 15):**


**Markers:** `synthetic-policy-no-live-web`: 165

**Examples:**

- Q (tau-retail-058, topic=retail): You are ivan_hernandez_6923 living in San Diego, 92133. You want to modify two items in an order you just received: a coffee machine and a laptop. For the coffee machine, you want to keep the capacity and type but change
  sources: [synthetic-policy-no-live-web]
  fp: "want to modify two items in an order"
  fp: "received a coffee machine and a laptop for"
  fp: "coffee machine you want to keep the capacity"
- Q (tau-airline-015, topic=airline): Your user id is james_patel_9828 and want to remove passenger Sophia from your upcoming flights from LAS to DEN on May 19 and DEN to LAS on May 20, with reservation ID GV1N64. You don't remember your reservation ID for t
  sources: [synthetic-policy-no-live-web]
  fp: "want to remove passenger sophia from your upcoming"
  fp: "rounds of interaction but then suddenly find it"
  fp: "want the cancellation to be done quickly since"
- Q (tau-retail-094, topic=retail): You name is Lei Wilson and your zip code is 32255. You are confident, organized, creative, impatient. You received a laptop and you want to exchange it to i7 processor, 8GB, 1TB SSD. If the agent asks for which laptop, i
  sources: [synthetic-policy-no-live-web]
  fp: "name is lei wilson and your zip code"
  fp: "confident organized creative impatient you received a laptop"
  fp: "ssd if the agent asks for which laptop"


## sealqa

- **Questions:** 619
- **License:** apache-2.0
- **Source:** https://huggingface.co/datasets/vtllms/sealqa
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- science: 169
- entertainment: 141
- sports: 128
- other: 78
- politics: 57
- history: 46

**Most common expected-source domains (top 15):**

- en.wikipedia.org: 537
- un.org: 17
- fifa.com: 13
- nba.com: 11
- data.un.org: 9
- transfermarkt.us: 9
- namu.wiki: 7
- google.com: 6
- factly.in: 6
- sahitya-akademi.gov.in: 6
- boxofficemojo.com: 5
- spotify.com: 5
- gimaths.com: 5
- fao.org: 5
- forbes.com: 4

**Examples:**

- Q (seal-hard-0015, topic=history): How many UNESCO World Heritage Cultural Sites are there in the country with the largest number of sites on the list, reflecting the country’s dedication to preserving its invaluable landmarks and wonders?
  sources: https://en.wikipedia.org/wiki/World_Heritage_Sites_by_country#:~:text=and%20North%20America-,Italy,note%2032%5D%5Bnote%2033%5D%5Bnote%207%5D,-6%5Bnote
  fp: "unesco world heritage cultural sites are there in"
  fp: "country with the largest number of sites on"
  fp: "list reflecting the country s dedication to preserving"
- Q (seal-hard-0117, topic=science): Based on data from the U.S. Environmental Protection Agency, which year between 2010 and 2020 saw the highest CO₂ emissions from crop cultivation in the United States?
  sources: https://cfpub.epa.gov/ghgdata/inventoryexplorer/#agriculture/entiresector/allgas/category/all:~:text=Map%20View-,Choose%3A,-1.%20Sector%3A
  fp: "u s environmental protection agency which year between"
  fp: "2010 and 2020 saw the highest co emissions"
  fp: "crop cultivation in the united states"
- Q (longseal-0231, topic=sports): Which constructor holds the second-highest number of World Drivers' Championship titles?
  sources: https://en.wikipedia.org/wiki/List_of_Formula_One_World_Drivers%27_Champions#By_chassis_constructor
  fp: "constructor holds the second highest number of world"
  fp: "holds the second highest number of world drivers"


## webwalkerqa

- **Questions:** 680
- **License:** apache-2.0
- **Source:** https://huggingface.co/datasets/callanwu/WebWalkerQA/resolve/main/data/main-00000-of-00001.jsonl
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- other: 175
- tech: 133
- entertainment: 110
- science: 102
- education: 70
- geography: 38
- politics: 15
- finance: 9
- sports: 8
- shopping: 7

**Most common expected-source domains (top 15):**

- cs.zju.edu.cn: 51
- riotgames.com: 45
- cs.swust.edu.cn: 45
- mrs.org: 42
- rovio.com: 40
- ion.org: 40
- illuvium.io: 39
- uni-president.com.cn: 35
- sigchi.org: 34
- poms.org: 34
- icse-conferences.org: 31
- cstc.hrbeu.edu.cn: 30
- ehaweb.org: 28
- cs.scu.edu.cn: 28
- vldb.org: 26

**Examples:**

- Q (webwalkerqa-0063, topic=entertainment): Which two Angry Birds games released by Rovio incorporate innovative and environmental themes, one being a mobile AR game from 2019 and the other related to an Earth Day event in 2024?
  sources: https://www.rovio.com/, https://www.rovio.com/articles/rovio-and-resolution-games-reveal-first-angry-birds-mobile-ar-game-angry-birds-ar-isle-of-pigs/, https://www.rovio.com/articles/birds-helping-birds-angry-birds-dream-blast-earth-day-campaign/
  fp: "two angry birds games released by rovio incorporate"
  fp: "innovative and environmental themes one being a mobile"
  fp: "related to an earth day event in 2024"
- Q (webwalkerqa-0590, topic=science): 在2024年，西南科技大学计算机科学与技术学院分别与哪两个重要实体进行了合作，以提升智能技术和军事技能？
  sources: https://cs.swust.edu.cn/, https://cs.swust.edu.cn/newsdetail/news-8951, https://cs.swust.edu.cn/newsdetail/news-9141
  fp: "与技术学院分别与"
  fp: "哪两个重要实体进"
  fp: "行了合作以提升智"
- Q (webwalkerqa-0599, topic=tech): 2023年3月23日与2023年5月14日，华南师范大学计算机学院各自开展的是什么考试？
  sources: http://cs.scnu.edu.cn/, http://cs.scnu.edu.cn/a/20230316/5402.html, http://cs.scnu.edu.cn/a/20230427/5454.html
  fp: "日华南师范大学计"
  fp: "算机学院各自开展"
  fp: "的是什么考试"


## openai-mle-bench

- **Questions:** 82
- **License:** MIT
- **Source:** https://github.com/openai/mle-bench
- **Retrieved:** 2026-10-05

**Topic distribution (top 10):**

- tech: 70
- health: 5
- entertainment: 2
- finance: 1
- travel: 1
- science: 1
- geography: 1
- sports: 1

**Most common expected-source domains (top 15):**

- kaggle.com: 73
- storage.googleapis.com: 45
- en.wikipedia.org: 32
- sites.google.com: 9
- github.com: 8
- googleapis.com: 5
- arxiv.org: 5
- cvpr2020.thecvf.com: 4
- demos.md.ai: 4
- unsplash.com: 4
- developers.google.com: 3
- nybg.org: 3
- raw.githubusercontent.com: 3
- youtube.com: 3
- prod-files-secure.s3.us-west-2.amazonaws.com: 3

**Examples:**

- Q (plant-pathology-2021-fgvc8, topic=tech): # Overview ## Description ### Problem Statement Apples are one of the most important temperate fruit crops in the world. Foliar (leaf) diseases pose a major threat to the overall productivity and quality of apple orchard
  sources: https://bsapubs.onlinelibrary.wiley.com/doi/10.1002/aps3.11390, https://www.kaggle.com/wiki/MeanFScore, https://sites.google.com/view/fgvc8, http://cvpr2021.thecvf.com/
  fp: "overview description problem statement apples are one of"
  fp: "important temperate fruit crops in the world foliar"
  fp: "leaf diseases pose a major threat to the"
- Q (bms-molecular-translation, topic=tech): ## Description In a technology-forward world, sometimes the best and easiest tools are still pen and paper. Organic chemists frequently draw out molecular work with the Skeletal formula, a structural notation used for ce
  sources: http://en.wikipedia.org/wiki/Levenshtein_distance, https://www.kaggle.com/c/bms-molecular-translation/discussion/242403
  fp: "description in a technology forward world sometimes the"
  fp: "best and easiest tools are still pen and"
  fp: "paper organic chemists frequently draw out molecular work"
- Q (imet-2020-fgvc7, topic=tech): # Overview ## Description The [Metropolitan Museum of Art](https://www.metmuseum.org/) in New York, also known as The Met, has a diverse collection of over 1.5M objects of which over 200K have been digitized with imagery
  sources: https://www.metmuseum.org/, https://sites.google.com/view/fgvc7/home, http://cvpr2020.thecvf.com/, https://en.wikipedia.org/wiki/F1_score, https://www.kaggle.com/docs/competitions#kernels-only-FAQ
  fp: "overview description the metropolitan museum of art in"
  fp: "new york also known as the met has"
  fp: "digitized with imagery can you help find the"

---

## Method notes

### Topic assignment
- **Metadata first:** openai-simpleqa (`metadata.topic`), sealqa (`topic`), mind2web (`subdomain`→`domain`), tau-bench (`airline`/`retail` kept as-is), webvoyager (`web_name`, the site itself), webwalkerqa (`info.domain` as fallback). Metadata values normalized to a canonical label set (sports, politics, science, history, geography, tech, finance, health, entertainment, gov-policy, food, travel, shopping, education, other).
- **Keyword-rule fallback** for google-facts-grounding, google-frames (its `reasoning_types` is a reasoning category, not a topic), assistantbench, webarena (its `sites` are environments), webwalkerqa, openai-mle-bench (classified on the competition slug; `tech` fallback — all 82 are ML competitions), and mind2web records whose metadata is `Other`/`General`. Rules are ordered regex lists (politics → gov-policy → health → finance → science → history → geography → sports → entertainment → tech → food → travel → shopping); first match wins, else `other`. Which rule fired is not recorded per question. CJK questions (433 webwalkerqa + 2 simpleqa) use a separate ordered Chinese substring rule list covering the same labels plus `education`.

### expected_sources
- `why="metadata"`: simpleqa (`metadata.urls`), sealqa (parquet `urls` column, decoded with `_tools/pqdec.py`), frames (`wiki_links`), mind2web (`website`, TLD-normalized: `aa`→`aa.com`, `sports.yahoo`→`sports.yahoo.com`, `nyc`→`nyc.gov`, known-TLD values kept), webvoyager (`web` site URL), webwalkerqa (`root_url` + `info.source_website`). Distinct article URLs kept (up to 3) even on one domain.
- `why="named-in-question"`: domains/URLs regex-extracted from the question text.
- `why="prior"`: conservative priors on QA evals only — en.wikipedia.org for wh-/how-many-style questions with no other source; official-site domains for a small brand map (apple, tesla, nasa, cdc, white house, …) when the brand is named; kaggle.com for mle-bench (agent traces hit competition pages per repo notes).
- `why="selfhosted"`: webarena tasks run against six self-hosted environments (shopping, shopping_admin, gitlab, map, reddit, wikipedia) — limited live-web trace value, flagged explicitly.
- Empty-list markers (single entry, `domain_or_url=""`): tau-bench `synthetic-policy-no-live-web` (165); facts-grounding `context-provided-no-web-needed` (553 — the grounding doc ships with the question); assistantbench `no-metadata-no-prior` (50 — gold_url/difficulty null in this release).

### fingerprint_phrases
- Corpus-wide n-gram document frequency over word 4..8-grams across all 10,201 questions (1,089,394 unique n-grams). Per question, candidates scored by (df asc, length desc); up to 3 non-overlapping picked, relaxed to 2 with overlap if needed; guaranteed ≥1.
- Filters: no stopword-leading n-grams; ≤50% weak tokens; ≥1 content token (≥2 for 6+-grams); digit-bearing tokens dropped except 4-digit years; URL/email spans stripped before tokenizing (chopped URL tokens make bad verbatim phrases); CJK text tokenized per-character and treated as content (433 webwalkerqa + 2 simpleqa questions), rejoined without spaces for verbatim search.
- Rationale: agents execute eval questions rather than pasting them, so probes target distinctive instruction fragments and named-entity + verb combos (e.g. "how many episodes of X aired") suitable for verbatim search on urlquery.net / urlscan / Google. High-df boilerplate (tau-bench instruction templates, mle-bench Kaggle boilerplate, webarena task templates) is automatically penalized by df.

### Outputs
- `all-questions.jsonl`: unified corpus, one JSON object per line, schema `{"eval","eval_org","question_id","question","topic","expected_sources":[{"domain_or_url","why"}],"fingerprint_phrases":[...],"license","retrieved"}`.
- `<eval-slug>/questions-enriched.jsonl`: per-eval enriched copies (provenance).
- Raw sources and `questions.jsonl` were read, never modified. Scripts: `_tools/enrich.py`, `_tools/build_index.py`.
