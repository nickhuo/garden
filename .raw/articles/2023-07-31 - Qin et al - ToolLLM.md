---
source_url: https://arxiv.org/abs/2307.16789
fetched: 2026-05-22
---

# ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs

**Authors:** Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, Maosong Sun (Tsinghua University NLP / OpenBMB; Yale; ModelBest; Tencent / WeChat AI).

**Venue:** arXiv:2307.16789 [cs.AI], submitted 2023-07-31, revised 2023-10-03. ICLR 2024 spotlight.

**Repo:** https://github.com/OpenBMB/ToolBench (MIT-ish, Apache for tooling)

## Abstract / problem

Open-source LLMs (e.g. LLaMA) lag far behind proprietary models like ChatGPT in tool use — invoking external APIs to fulfill instructions. ToolLLM is a general tool-use framework spanning data construction, model training, and evaluation.

## ToolBench dataset (three construction stages, all automated with ChatGPT)

1. **API collection** — 16,464 real-world RESTful APIs across 49 categories scraped from RapidAPI Hub.
2. **Instruction generation** — ChatGPT prompted to generate diverse instructions covering single-tool and multi-tool scenarios. Three instruction sets:
   - **I1** — single-tool instructions
   - **I2** — intra-category multi-tool instructions
   - **I3** — intra-collection multi-tool instructions
3. **Solution path annotation** — for each instruction, ChatGPT searches for a valid solution path (a sequence of API calls). Each path is an ordered series of (thought, API call, response) triples.

## DFSDT — Depth-First Search-based Decision Tree

Standard ReAct/CoT does linear reasoning and gets stuck in error states. DFSDT lets the model evaluate multiple reasoning traces and expand the search space — backtracking from failed API calls and trying alternate branches. Boosts annotation success and inference quality (~+13% pass rate vs CoT in multi-API settings).

## ToolLLaMA

LLaMA fine-tuned on ToolBench. Equipped with a neural API retriever that recommends relevant APIs from the 16k+ pool for each instruction (no need to feed all APIs into context). Demonstrates performance comparable to ChatGPT on complex instructions and generalizes to unseen APIs. Strong zero-shot generalization to the out-of-distribution **APIBench** (the Gorilla benchmark).

## ToolEval — automatic evaluator

LLM-based (ChatGPT) automatic evaluation with two metrics:
- **Pass Rate** — proportion of instructions completed within a budget.
- **Win Rate** — pairwise comparison of two solution paths judged by ChatGPT against reference.

ToolLLaMA matches ChatGPT on pass rate (~50% in DFS multi-API settings) and is competitive on win rate.

## Notes / known issues

- RapidAPI dependency makes the live environment unstable — APIs go down, change, rate-limit. This motivated **StableToolBench** (arXiv:2403.07714) which adds a caching API server + simulated API responses for reproducibility.
- ToolEval (ChatGPT judge) inherits LLM-judge biases.
