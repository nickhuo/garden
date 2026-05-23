---
type: concept
title: "Generation-Time vs Post-hoc Citation"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - rag
status: seed
complexity: intermediate
domain: llm
aliases:
  - "G-Cite"
  - "P-Cite"
  - "inline citation vs post-hoc citation"
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Citation Precision and Recall]]"
sources:
  - "[[2025-09-25 - Generation-Time vs Post-hoc Citation]]"
---

# Generation-Time vs Post-hoc Citation

## One-Line Definition

The two ways to attach citations to generated text: **G-Cite** emits citations *during* decoding (inline); **P-Cite** drafts the answer first, then attaches/verifies citations in a *separate pass*. (Source: [[2025-09-25 - Generation-Time vs Post-hoc Citation]])

## The tradeoff

| | G-Cite (generation-time) | P-Cite (post-hoc) |
|---|---|---|
| Coverage | Lower (~37–65%) | **Higher (~74–99%)** |
| Answer correctness (human) | 69% | **78%** |
| Citation hallucination | 41% | **37%** |
| Latency | Lower baseline | Moderate extra pass |
| Best for | precision-critical | **high-stakes / high-coverage** |

## Recommendation

**Retrieval-centric, P-Cite-first for high-stakes** applications; reserve G-Cite where precision matters more than coverage. The biggest lever is neither paradigm but **retrieval quality** — adding retrieval gave ~50-point correctness gains regardless of citation method.

## Why P-Cite usually wins

Drafting first, then citing, lets a dedicated verification pass see the *whole* answer and map each claim to the best source — which is also where post-hoc correction ([[2025-04-22 - CiteFix - Post-Processing Citation Correction|CiteFix]]) and verification ([[Citation Verification Pipeline]]) plug in. G-Cite makes only local decisions mid-decode and can't revise.

## Caveat

P-Cite's separate pass means citations are assigned *independently of the evidence used during generation* — so faithful attribution still isn't guaranteed by P-Cite alone; it needs a verification step on top.
