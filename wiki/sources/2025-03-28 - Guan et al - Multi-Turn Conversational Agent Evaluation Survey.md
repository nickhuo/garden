---
type: source
title: "Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey"
source_type: paper
author: "Shengyue Guan, Jindong Wang, Jiang Bian, Bin Zhu, Jian-guang Lou, Haoyi Xiong"
date_published: 2025-03-28
url: "https://arxiv.org/abs/2503.22458"
created: 2026-05-23
updated: 2026-05-23
status: developing
confidence: high
key_claims:
  - "Multi-turn agent evaluation has three core targets: task success, response quality, and end-to-end user experience."
  - "PRISMA-style review of ~250 sources (from 1,123 unique records); 272 papers offered targeted evaluation insights — establishing the breadth of multi-turn evaluation methods (automatic metrics + human protocols)."
  - "Multi-turn robustness is invisible to single-shot evaluation; reasoning depends on prior steps."
tags:
  - ai-agents
  - evaluation
  - llm
  - survey
related:
  - "[[Online Evaluation Bottlenecks]]"
  - "[[User Simulator Evaluation]]"
  - "[[Research - Online Evaluation in Production]]"
sources: []
---

# Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey

Guan et al., arXiv 2503.22458 (v1 2025-03-28). A PRISMA-inspired survey (~250 sources synthesized) of how multi-turn conversational agents are evaluated, on two axes: *which aspects* and *how*.

## Three evaluation targets

1. **Task success** — did the conversation accomplish the goal.
2. **Response quality** — turn-level correctness/helpfulness.
3. **End-to-end user experience** — the whole-session signal closest to what online evaluation measures.

## What it contributes here

The "end-to-end user experience" target is the multi-turn analogue of the online question "did this land for *this* user?" — and the source of a key bottleneck: **credit assignment across turns** (a delayed session outcome must be attributed to specific earlier actions). Feeds [[Online Evaluation Bottlenecks]]. Multi-turn variation also motivates [[User Simulator Evaluation]] on the offline side.
