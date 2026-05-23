---
type: concept
title: "Attributed Text Generation"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - rag
  - retrieval
status: seed
complexity: intermediate
domain: llm
aliases:
  - "citation generation"
  - "attribution"
  - "grounded generation"
  - "cited generation"
related:
  - "[[Citation Precision and Recall]]"
  - "[[Generation-Time vs Post-hoc Citation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Contextual Retrieval]]"
  - "[[Reranking]]"
  - "[[BM25 and Hybrid Retrieval]]"
sources:
  - "[[2023-05-23 - Gao et al - ALCE]]"
---

# Attributed Text Generation

## One-Line Definition

Generating text in which **every substantive claim is linked to a supporting source** (ideally a specific span), so a reader can validate the claim against its evidence. (Source: [[2023-05-23 - Gao et al - ALCE]])

## Why it's the core of trustworthy AI products

In high-stakes domains (medical → [[OpenEvidence]], legal → [[Harvey]]) the answer is only usable if the user can **check it**. Citation converts an unverifiable assertion into a verifiable one. It is the product-level form of grounding: the user's fallback when they don't trust the model.

## The two failure modes (distinct!)

1. **Content hallucination** — the claim isn't supported by *any* retrieved source. Expensive to fix (needs better retrieval/generation).
2. **Citation error / mis-attribution** — the claim *is* supported by the retrieved set, but the model cited the wrong source. **[[2025-04-22 - CiteFix - Post-Processing Citation Correction|CiteFix]] finds ~80% of "unverifiable" facts are this** — cheap to fix post-hoc.

Separating these is the key design insight: most citation failure is the cheap kind.

## What good attribution requires

- **Span specificity** — link to the exact passage, not the whole document (Harvey's "effective source" definition).
- **Uniqueness** — citations cleanly demarcated from answer text.
- **Coverage vs precision balance** — cite enough that claims are supported, without decorative citations that don't pull weight ([[Citation Precision and Recall]]).

## Pipeline ingredients

Retrieval (the dominant lever) → [[Reranking]] → cited generation ([[Generation-Time vs Post-hoc Citation]]) → verification ([[Citation Verification Pipeline]]). Built on [[Contextual Retrieval]] and [[BM25 and Hybrid Retrieval]].
