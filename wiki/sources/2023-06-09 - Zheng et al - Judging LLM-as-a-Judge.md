---
type: source
title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
source_type: paper
author: "Zheng, Chiang, Sheng, et al. (UC Berkeley, Stanford, CMU)"
date_published: 2023-06-09
url: https://arxiv.org/abs/2306.05685
created: 2026-05-20
updated: 2026-05-20
status: mature
confidence: high
tags: [ai-agents, llm, evaluation, llm-as-judge, benchmark]
key_claims:
  - "Strong LLM judges (GPT-4) match human preferences at >80% agreement — the same agreement level humans reach with each other."
  - "LLM judges exhibit systematic biases: position bias, verbosity bias, self-enhancement bias, and limited reasoning on hard problems."
  - "MT-Bench (fixed multi-turn questions, judge-scored) and Chatbot Arena (live crowdsourced pairwise battles, Elo) are complementary: a static benchmark and a live online-evaluation platform."
related:
  - "[[LLM-as-Judge]]"
  - "[[Online Evaluation]]"
sources: []
---

# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

Zheng et al., NeurIPS 2023 (arXiv 2306.05685, v4 Dec 2023). The foundational empirical study of using a strong LLM as a scalable proxy for human preference judgment.

## Core result

GPT-4 used as a judge reaches **>80% agreement** with both controlled expert votes and crowdsourced human preferences — equal to the agreement level **between two humans**. This is the empirical license for replacing slow, expensive human grading with automated LLM grading at scale.

## The two instruments (note the offline/online split)

- **MT-Bench** — a *fixed* set of 80 multi-turn questions across 8 categories; an LLM judge scores responses (single-answer grading 1–10, or pairwise). This is an **offline** benchmark: same questions for everyone, reproducible, but static.
- **Chatbot Arena** — a *live* platform where real users submit their own prompts, get two anonymous model responses, and vote for the winner; aggregated into **Elo** ratings. This is **online evaluation**: real users, real intent, fresh distribution, but noisy and uncontrolled. (See [[Online Evaluation]].)

Released: MT-Bench questions, 3K expert votes, 30K Arena conversations with human preferences.

## Documented judge biases (load-bearing for reliability)

- **Position bias** — judge favors the response shown first (or last). Pairwise accuracy can swing >10% just by swapping order. Mitigation: evaluate both orderings, count only consistent verdicts.
- **Verbosity bias** — longer answers preferred regardless of quality.
- **Self-enhancement bias** — a model rates its own outputs higher (motivates cross-family judging, e.g. Nick's Compass dual-judge).
- **Limited reasoning** — judges err on math/reasoning grading where they themselves are weak.

## Why it matters for online eval

Chatbot Arena is the canonical demonstration that **live pairwise preference from real users** is a usable, high-signal online evaluation channel — the bridge from static benchmark numbers to "did this land for *this* user." The same paper documents exactly why the automated judge that scales it cannot be trusted blind.
