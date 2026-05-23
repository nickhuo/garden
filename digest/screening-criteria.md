---
name: HF Papers Screening Criteria
maintained_by: Nick + Digital Twin
last_updated: 2026-04-21
version: 1
---

# Screening Criteria — HF Daily Papers

> Living rubric for filtering HuggingFace Daily Papers into Nick's daily digest. Update this file as Nick's focus evolves — the daily pipeline reads this file and applies these rules with judgment.
>
> **How to evolve this file:** Tell the Digital Twin `update screening criteria: {change}` and it will edit the rules, bump the version, and append the change log.

## Nick's current focus (as of 2026-04-21)

- **Role target:** Full-time **AI Engineer**, US, graduating May 2026, **SF/Silicon Valley** primary
- **Headline project:** Goal-oriented AI agent at Donut Labs — 46 crypto workflows, **+22% task success**, **−86% real-time inference cost**
- **Technical depth:** Agents (LangGraph, MCP), RAG, fine-tuning (LoRA/SFT/RL), inference optimization, eval design
- **OSS interest:** n8n, mem0, Dify, litellm
- **Content channels:** X `@heynickhuo`, blog `nickhuo.com` (long-form synthesis)

---

## Keep a paper if ANY of these apply

### Core (tag 🟢 — directly actionable)

- **Agent architecture** — frameworks, memory/continuity, self-evolution, skill discovery, tool use, multi-agent, MCP
- **Agent reliability & evaluation** — benchmarks for agents, reward hacking, stability, environmental curiosity, verification, monitoring
- **Post-training** — SFT, RLVR / RLHF / RLAIF, distillation (on-policy, offline), LoRA, model merging, calibration
- **Inference optimization** — KV cache tricks, quantization, early exit, speculative decoding, compiler/runtime (NPU/GPU), throughput
- **Retrieval / RAG** — dense retrievers, embedding models, retrieval eval, RAG architecture, reranking, long-context memory
- **LLM evals / benchmarks** — that reshape how we evaluate agents or LLMs (not leaderboard-chasing on saturated benches)

### Adjacent (tag 🟡 — keep if method is transferable or angle is strong)

- **Voice / multimodal agents** — when the paper advances agent capability, not just perception
- **World models** — especially when paired with agents or VLA
- **Code agents / code LLMs** — debugging, web coding, repair, games
- **Safety / guardrails** — symbolic guardrails, policy enforcement, jailbreak defense
- **Reasoning** — CoT variants, self-play, reasoning transfer, faithfulness

### Watch (tag ⚪ — field-of-view only, keep sparingly)

- **Frontier capability results** with broad narrative value (e.g. a new model class hits a milestone) — even if not immediately usable
- **Position papers** that crystallize a debate Nick may want to weigh in on publicly

---

## Drop if ANY of these apply

- No LLM / no agent angle **AND** no transferable method
- Pure application in: genomics, medical imaging, neuroscience, pure time series, remote sensing, pure CV — **unless** the *method* transfers to LLM/agent land
- Narrow NLP sub-task with no broader generalization (e.g. low-resource MwE, specific idiom detection)
- Dataset papers where the dataset is not about LLM/agent behavior
- Tooling papers for non-ML software domains
- Papers whose contribution is a minor incremental bench gain in a saturated area

---

## Output rules

- **Embed PDF link** for every kept paper: `[{arxiv_id}](https://arxiv.org/pdf/{arxiv_id})`
- Each paper gets three tight lines: **Problem** / **Method** / **Key result** — see `README.md` for format
- Cluster by topic (Agents / Evals / Post-training / Inference / RAG / Multimodal / Other)
- Never invent metrics. If abstract has none → write "No quantitative result reported"
- Client-ready bar: Nick reads this first thing in the morning with coffee

---

## Actionable section (always at the end)

After the paper list, produce:

1. **本日 research 风向 (TL;DR)** — 2–3 sentences
2. **X selector** — up to 3 tweet angles (punchy hook + which paper it's anchored to)
3. **Blog candidates** — 1–2 synthesis angles
4. **OSS opportunities** — up to 3 (repo + star count + why Nick should engage)
5. **Resume / interview talking points** — 1–3, each tied back to Nick's Donut Labs narrative (46 workflows / +22% / −86%)

---

## Update log

| Date | Version | Change | Reason |
|---|---|---|---|
| 2026-04-21 | v1 | Initial criteria | Based on Donut Labs project + AI Eng 2026 job search |
