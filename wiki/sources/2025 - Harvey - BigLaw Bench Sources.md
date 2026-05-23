---
type: source
title: "Harvey — BigLaw Bench Deep Dive: Sources"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - evaluation
  - legal
status: developing
source_type: blog
author: "Harvey"
date_published: 2025-01-01
url: "https://www.harvey.ai/blog/biglaw-bench-sources"
confidence: medium
related:
  - "[[Harvey]]"
  - "[[Citation Precision and Recall]]"
  - "[[Attributed Text Generation]]"
sources:
  - "https://www.harvey.ai/blog/biglaw-bench-sources"
---

# Harvey — BigLaw Bench: Sources

How Harvey scores source/citation quality in its internal legal benchmark.

## Definition of an effective source

> "Links to a specific piece of text **within** a source document." (span-level, not document-level — though see the scoring caveat below.)

## Scoring methodology

- **Document-level scoring** (a deliberate "lower-bound" standard): +1 point when a substantive claim carries "a valid source... affirmatively connecting those sentences to a specific **document**."
- Deductions for unsourced claims that require verification.
- **Superfluous sources**: neither rewarded nor penalized.
- Internally Harvey holds a *higher* bar than the public BigLaw Bench standard.

## Why not enforce passage-level scoring publicly

Three sourcing challenges they call out:
1. **Specificity** — identify the exact passage justifying an assertion across many docs.
2. **Uniqueness** — sources must be cleanly demarcated from the answer text.
3. **Quality–answer tradeoff** — *demanding granular sources reduces answer detail/fidelity and can introduce hallucinations.* This is why the public metric is document-level: passage-level sourcing trades off against answer quality.

> [!gap] Harvey uses "stylized sources" with "consistent parsing" but does not disclose the span-matching mechanism.
