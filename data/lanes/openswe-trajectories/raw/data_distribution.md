# Data Distribution

## v1.0

Open-SWE-Traces v1.0 consists of **151,219** total trajectories across two LLMs and two agent scaffolds.

### Table 1: Agent, Model, and PR Category-wise Distribution

| Agent | Model (Type) | Category | PR by Category | Total PR | Resolved | Unresolved | Unknown | Traj. by Category | Total Traj. |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **OpenHands** | **Minimax-M2.5** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 10,719 <br> 2,083 <br> 5,180 <br> 1,040 | **19,022** <br><br><br> | 8,725 <br> 1,415 <br> 3,619 <br> 604 | 9,892 <br> 2,236 <br> 6,253 <br> 1,129 | 5,751 <br> 1,093 <br> 2,374 <br> 512 | **24,368** <br> **4,744** <br> **12,246** <br> **2,245** | **43,603** <br><br><br> |
| **OpenHands** | **Qwen3.5-122B** <br>*(Non-Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 10,505 <br> 2,017 <br> 4,905 <br> 1,024 | **18,451** <br><br><br> | 6,188 <br> 1,041 <br> 2,194 <br> 410 | 11,450 <br> 2,320 <br> 6,005 <br> 1,349 | 5,970 <br> 988 <br> 2,070 <br> 478 | **23,608** <br> **4,349** <br> **10,269** <br> **2,237** | **40,463** <br><br><br> |
| **SWE-agent** | **Minimax-M2.5** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 11,477 <br> 2,037 <br> 4,991 <br> 1,017 | **19,522** <br><br><br> | 10,603 <br> 1,504 <br> 3,943 <br> 699 | 10,633 <br> 2,091 <br> 5,416 <br> 1,066 | 7,005 <br> 1,040 <br> 2,291 <br> 528 | **28,241** <br> **4,635** <br> **11,650** <br> **2,293** | **46,819** <br><br><br> |
| **SWE-agent** | **Qwen3.5-122B** <br>*(Non-Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 7,926 <br> 814 <br> 1,238 <br> 533 | **10,511** <br><br><br> | 6,147 <br> 404 <br> 533 <br> 264 | 5,872 <br> 599 <br> 845 <br> 434 | 4,245 <br> 358 <br> 400 <br> 233 | **16,264** <br> **1,361** <br> **1,778** <br> **931** | **20,334** <br><br><br> |

### Table 2: Language-wise Distribution

| Language | OpenHands (Minimax) | OpenHands (Qwen3.5) | SWE-agent (Minimax) | SWE-agent (Qwen3.5) | Total Traj. |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Python** | 10,522 / 4,428 | 8,206 / 3,939 | 10,899 / 4,488 | 4,716 / 2,284 | **34,343** |
| **Go** | 10,124 / 4,487 | 9,980 / 4,479 | 8,862 / 3,988 | 4,022 / 2,187 | **32,988** |
| **TypeScript** | 7,703 / 3,339 | 7,184 / 3,189 | 8,819 / 3,519 | 3,339 / 1,777 | **27,045** |
| **JavaScript** | 6,033 / 2,639 | 5,477 / 2,497 | 7,301 / 2,904 | 2,950 / 1,551 | **21,761** |
| **Rust** | 3,978 / 1,866 | 4,986 / 2,225 | 5,346 / 2,270 | 2,989 / 1,497 | **17,299** |
| **Java** | 2,736 / 1,203 | 2,536 / 1,164 | 3,061 / 1,278 | 1,180 / 629 | **9,513** |
| **PHP** | 2,305 / 971 | 1,890 / 864 | 2,292 / 971 | 991 / 509 | **7,478** |
| **C** | 151 / 68 | 143 / 64 | 162 / 72 | 85 / 48 | **541** |
| **C++** | 51 / 21 | 61 / 30 | 77 / 32 | 62 / 29 | **251** |
| **Total** | **43,603 / 19,022** | **40,463 / 18,451** | **46,819 / 19,522** | **20,334 / 10,511** | **151,219** |

---

## v1.1

Open-SWE-Traces v1.1 consists of **263,226** total trajectories across two LLMs and three agent scaffolds.

# Table 1: Agent, Model, and PR Category-wise Distribution

| Agent | Model (Type) | Category | PR by Category | Total PR | Resolved | Unresolved | Unknown | Traj. by Category | Total Traj. |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **OpenHands** | **DeepSeek-V4-Flash-0731** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 16,061 <br> 4,241 <br> 10,068 <br> 2,290 | **32,660** <br><br><br> | 11,725 <br> 3,116 <br> 6,540 <br> 1,729 | 12,318 <br> 3,584 <br> 9,298 <br> 1,985 | 0 <br> 0 <br> 0 <br> 0 | **24,043** <br> **6,700** <br> **15,838** <br> **3,714** | **50,295** <br><br><br> |
| **OpenHands** | **Qwen3.6-27B** <br>*(Non-Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 13,891 <br> 3,671 <br> 8,882 <br> 2,101 | **28,545** <br><br><br> | 8,808 <br> 2,147 <br> 4,570 <br> 1,257 | 10,968 <br> 3,069 <br> 7,751 <br> 1,809 | 0 <br> 0 <br> 0 <br> 0 | **19,776** <br> **5,216** <br> **12,321** <br> **3,066** | **40,379** <br><br><br> |
| **SWE-agent** | **Qwen3.6-27B** <br>*(Non-Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 17,050 <br> 4,223 <br> 10,752 <br> 2,368 | **34,393** <br><br><br> | 17,418 <br> 3,819 <br> 8,764 <br> 2,150 | 17,549 <br> 4,726 <br> 12,646 <br> 2,814 | 3,346 <br> 917 <br> 2,569 <br> 543 | **38,313** <br> **9,462** <br> **23,979** <br> **5,507** | **77,261** <br><br><br> |
| **mini-SWE-agent** | **Qwen3.6-27B** <br>*(Non-Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 19,443 <br> 5,028 <br> 12,286 <br> 2,783 | **39,540** <br><br><br> | 17,655 <br> 3,826 <br> 8,737 <br> 2,013 | 24,794 <br> 7,036 <br> 17,876 <br> 3,916 | 4,361 <br> 1,166 <br> 3,199 <br> 712 | **46,810** <br> **12,028** <br> **29,812** <br> **6,641** | **95,291** <br><br><br> |

### Table 2: Language-wise Distribution

| Language | OpenHands (DeepSeek-0731) | OpenHands (Qwen3.6) | SWE-agent (Qwen3.6) | mini-SWE-agent (Qwen3.6) | Total Traj. |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Python** | 32,170 / 19,700 | 26,482 / 18,397 | 50,004 / 21,112 | 53,755 / 23,374 | **162,411** |
| **Go** | 6,013 / 4,205 | 4,603 / 3,336 | 7,124 / 3,629 | 13,229 / 5,059 | **30,969** |
| **TypeScript** | 4,054 / 2,881 | 2,999 / 2,185 | 6,348 / 3,047 | 9,264 / 3,598 | **22,665** |
| **JavaScript** | 3,045 / 2,209 | 2,470 / 1,771 | 5,006 / 2,466 | 6,735 / 2,807 | **17,256** |
| **Rust** | 2,542 / 1,842 | 1,822 / 1,377 | 4,289 / 2,042 | 6,055 / 2,301 | **14,708** |
| **Java** | 1,287 / 953 | 1,073 / 794 | 2,377 / 1,121 | 3,405 / 1,295 | **8,142** |
| **PHP** | 1,071 / 786 | 838 / 624 | 1,884 / 866 | 2,570 / 994 | **6,363** |
| **C** | 83 / 60 | 60 / 41 | 164 / 76 | 193 / 79 | **500** |
| **C++** | 30 / 24 | 32 / 20 | 65 / 34 | 85 / 33 | **212** |
| **Total** | **50,295 / 32,660** | **40,379 / 28,545** | **77,261 / 34,393** | **95,291 / 39,540** | **263,226** |

---

## v1.2

Open-SWE-Traces v1.2 distribution consists of **263,371** total trajectories across two LLMs and three agent scaffolds.

### Table 1: Agent, Model, and PR Category-wise Distribution

| Agent | Model (Type) | Category | PR by Category | Total PR | Resolved | Unresolved | Unknown | Traj. by Category | Total Traj. |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **OpenHands** | **Qwen3.8-27B** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 12,834 <br> 3,331 <br> 7,758 <br> 1,676 | **25,599** <br><br><br> | 6,412 <br> 1,576 <br> 3,186 <br> 759 | 6,422 <br> 1,755 <br> 4,572 <br> 917 | 0 <br> 0 <br> 0 <br> 0 | **12,834** <br> **3,331** <br> **7,758** <br> **1,676** | **25,599** <br><br><br> |
| **OpenHands** | **Qwen3.8-Flash-Next** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 12,948 <br> 3,392 <br> 7,918 <br> 1,769 | **26,027** <br><br><br> | 6,681 <br> 1,698 <br> 3,546 <br> 885 | 6,267 <br> 1,694 <br> 4,372 <br> 884 | 0 <br> 0 <br> 0 <br> 0 | **12,948** <br> **3,392** <br> **7,918** <br> **1,769** | **26,027** <br><br><br> |
| **SWE-agent** | **Qwen3.8-27B** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 17,037 <br> 4,180 <br> 9,776 <br> 2,220 | **33,213** <br><br><br> | 8,370 <br> 1,887 <br> 4,252 <br> 1,131 | 8,667 <br> 2,293 <br> 5,524 <br> 1,089 | 0 <br> 0 <br> 0 <br> 0 | **17,037** <br> **4,180** <br> **9,776** <br> **2,220** | **33,213** <br><br><br> |
| **SWE-agent** | **Qwen3.8-Flash-Next** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 17,874 <br> 4,334 <br> 10,216 <br> 2,264 | **34,688** <br><br><br> | 9,089 <br> 2,067 <br> 4,700 <br> 1,219 | 8,785 <br> 2,267 <br> 5,516 <br> 1,045 | 0 <br> 0 <br> 0 <br> 0 | **17,874** <br> **4,334** <br> **10,216** <br> **2,264** | **34,688** <br><br><br> |
| **mini-SWE-agent** | **Qwen3.8-27B** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 20,836 <br> 5,166 <br> 12,544 <br> 2,859 | **41,405** <br><br><br> | 26,770 <br> 6,068 <br> 13,537 <br> 3,550 | 22,363 <br> 6,024 <br> 15,254 <br> 3,029 | 5,044 <br> 1,292 <br> 3,574 <br> 762 | **54,177** <br> **13,384** <br> **32,365** <br> **7,341** | **107,267** <br><br><br> |
| **mini-SWE-agent** | **Qwen3.8-Flash-Next** <br>*(Thinking)* | bug-fix <br> enhancement <br> feature-request <br> other | 18,799 <br> 4,565 <br> 10,831 <br> 2,382 | **36,577** <br><br><br> | 9,451 <br> 2,157 <br> 4,913 <br> 1,286 | 9,348 <br> 2,408 <br> 5,918 <br> 1,096 | 0 <br> 0 <br> 0 <br> 0 | **18,799** <br> **4,565** <br> **10,831** <br> **2,382** | **36,577** <br><br><br> |


### Table 2: Language-wise Distribution

| Language | OpenHands (Qwen3.8-27B) | OpenHands (Qwen3.8-Flash) | SWE-agent (Qwen3.8-27B) | SWE-agent (Qwen3.8-Flash) | mini-SWE-agent (Qwen3.8-27B) | mini-SWE-agent (Qwen3.8-Flash) | Total Traj. |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Python** | 15,682 / 15,682 | 15,972 / 15,972 | 19,794 / 19,794 | 19,891 / 19,891 | 65,597 / 24,287 | 20,756 / 20,756 | **157,692** |
| **Go** | 2,918 / 2,918 | 2,793 / 2,793 | 4,026 / 4,026 | 4,439 / 4,439 | 13,206 / 5,338 | 4,867 / 4,867 | **32,249** |
| **TypeScript** | 2,487 / 2,487 | 2,524 / 2,524 | 3,070 / 3,070 | 3,341 / 3,341 | 9,160 / 3,743 | 3,530 / 3,530 | **24,112** |
| **JavaScript** | 1,991 / 1,991 | 1,957 / 1,957 | 2,540 / 2,540 | 2,797 / 2,797 | 7,371 / 3,047 | 2,865 / 2,865 | **19,521** |
| **Rust** | 1,080 / 1,080 | 1,378 / 1,378 | 1,872 / 1,872 | 2,110 / 2,110 | 5,804 / 2,415 | 2,196 / 2,196 | **14,440** |
| **Java** | 663 / 663 | 700 / 700 | 1,052 / 1,052 | 1,103 / 1,103 | 3,149 / 1,348 | 1,259 / 1,259 | **7,926** |
| **PHP** | 728 / 728 | 649 / 649 | 769 / 769 | 907 / 907 | 2,674 / 1,106 | 999 / 999 | **6,726** |
| **C** | 37 / 37 | 40 / 40 | 63 / 63 | 68 / 68 | 220 / 86 | 77 / 77 | **505** |
| **C++** | 13 / 13 | 14 / 14 | 27 / 27 | 32 / 32 | 86 / 35 | 28 / 28 | **200** |
| **Total** | **25,599 / 25,599** | **26,027 / 26,027** | **33,213 / 33,213** | **34,688 / 34,688** | **107,267 / 41,405** | **36,577 / 36,577** | **263,371** |


**Note**:

- In each Table 1, `Resolved`, `Unresolved`, and `Unknown` indicate issue resolution status.
- In each Table 2, counts are formatted as Trajectories / PRs.
  - PR counts are non-unique across agent/model columns and cannot be summed horizontally.
- PR counts are unique `instance_id` counts within each version/agent/model group and are deduplicated across configured source files.
