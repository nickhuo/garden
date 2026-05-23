---
type: concept
title: "Citation Verification Pipeline"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - rag
  - evaluation
status: developing
complexity: advanced
domain: llm
aliases:
  - "citation pre-verification"
  - "citation post-verification"
  - "attribution pipeline"
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Precision and Recall]]"
  - "[[Generation-Time vs Post-hoc Citation]]"
  - "[[Reranking]]"
  - "[[Contextual Retrieval]]"
  - "[[Trace-Based Evaluation]]"
sources:
  - "[[2025-10-13 - VeriCite - Rigorous Citation Verification]]"
  - "[[2025-04-22 - CiteFix - Post-Processing Citation Correction]]"
  - "[[2025 - Harvey - Using Agents to Scale Knowledge Sources]]"
---

# Citation Verification Pipeline

## One-Line Definition

The end-to-end design that makes citations trustworthy, split into **pre-verification** (before/at generation: control what *can* be cited) and **post-verification** (after generation: check and correct what *was* cited).

## Pre-verification (the bigger lever)

What you do *before* the model writes, so it can only produce attributable claims:

1. **Curated corpus** — restrict retrieval to vetted, authoritative sources ([[OpenEvidence]] 300+ journals, no open web; [[Harvey]] gov portals + LexisNexis). *You can't mis-cite what isn't in the corpus.* This is why vertical products are so precise.
2. **Strong retrieval** — hybrid [[BM25 and Hybrid Retrieval]] + [[Reranking]] + [[Contextual Retrieval]]. Retrieval quality dominates citation quality (~50-pt gains).
3. **Generation steering** — guide the model toward claims it can support (VeriCite's pre-generation phase); claim-grounded decoding.

## Post-verification (the safety net)

What you do *after* drafting:

1. **Entailment check** — NLI-score each claim against its cited passage ([[Citation Precision and Recall]]); flag unsupported claims.
2. **Citation correction** — re-map mis-attributed claims to the right retrieved source ([[2025-04-22 - CiteFix - Post-Processing Citation Correction|CiteFix]]: keyword / BERTScore / LLM matching, **+15.5% accuracy**). Cheap, because **~80% of failures are mis-citation, not hallucination**.
3. **Hard gate** — hallucinated citation → **automatic rejection** ([[Harvey]]); ambiguous → human review.
4. **Iterative refinement** — feed verification results back into a redraft (VeriCite loop).

## The canonical shape

```
curated corpus → hybrid retrieve → rerank        ← pre-verification
   → draft answer (P-Cite) → NLI entailment check
   → correct mis-citations → reject/repair on fail ← post-verification
   → user-facing source links (the "citation ground")
```

## For Nick

H60/Compass **citation ground** = the user-facing tail of this pipeline (validate-the-source fallback). The leverage is upstream: a curated-corpus + reranking pre-verification stage, and an NLI + CiteFix-style post-verification stage with an auto-reject gate. For **Newsprout** (open web, no curated corpus), the pre-verification lever is weaker, so post-verification carries more weight. Surface the per-claim checks in [[Trace-Based Evaluation]].
