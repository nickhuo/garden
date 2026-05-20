---
type: entity
title: "Horace He"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - entity
  - person
status: seed
entity_type: person
role: "Researcher at Thinking Machines Lab; lead author of Defeating Nondeterminism in LLM Inference. Known for PyTorch internals and GPU kernel work."
first_mentioned: 2026-05-14
related:
  - "[[Thinking Machines Lab]]"
  - "[[Batch Invariance]]"
sources:
  - "[[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]]"
---

# Horace He

At [[Thinking Machines Lab]]. Lead author of [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]], which diagnosed batch-invariance failure (not concurrency) as the root cause of LLM nondeterminism at T=0 and shipped the [batch_invariant_ops](https://github.com/thinking-machines-lab/batch_invariant_ops) kernels.

Historically a PyTorch internals contributor; the FlexAttention integration in vLLM is a continuation of that line.
