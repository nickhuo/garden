---
type: synthesis
title: "Research: AI Product Citation — Open Evidence & Harvey"
created: 2026-05-23
updated: 2026-05-23
tags:
  - research
  - citation
  - rag
  - evaluation
  - llm
status: developing
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Precision and Recall]]"
  - "[[Generation-Time vs Post-hoc Citation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[OpenEvidence]]"
  - "[[Harvey]]"
  - "[[Reranking]]"
  - "[[Contextual Retrieval]]"
  - "[[LLM-as-Judge]]"
  - "[[Trace-Based Evaluation]]"
sources:
  - "[[2023-05-23 - Gao et al - ALCE]]"
  - "[[2025-09-25 - Generation-Time vs Post-hoc Citation]]"
  - "[[2025-04-22 - CiteFix - Post-Processing Citation Correction]]"
  - "[[2025-10-13 - VeriCite - Rigorous Citation Verification]]"
  - "[[2025 - Harvey - BigLaw Bench Sources]]"
  - "[[2025 - Harvey - Using Agents to Scale Knowledge Sources]]"
---

# Research: AI Product Citation — Open Evidence & Harvey

## Overview

How do best-in-class vertical AI products cite, why is their citation so precise, how is citation quality measured, and what does a citation pipeline's pre/post-verification look like? The short answer: **precision comes mostly from the corpus, not the model.** [[OpenEvidence]] (medical) and [[Harvey]] (legal) both restrict generation to a curated, authoritative corpus, retrieve hard, draft, then verify and correct citations before showing the user a clickable source. The reusable backbone is [[Attributed Text Generation]] → [[Citation Verification Pipeline]] → [[Citation Precision and Recall]].

## Q1 — How they cite

- **[[OpenEvidence]]**: RAG over a **closed corpus** of 300+ peer-reviewed journals (NEJM, JAMA, Cochrane, NCCN) + FDA/CDC, *no public internet*; an **ensemble of specialized models**; answer with hyperlinked references after each statement, linked to the source abstract.
- **[[Harvey]]**: cites only **vetted government portals / authoritative legal DBs** + LexisNexis **Shepard's Citations**; pipeline = structured metadata extraction + embedding search + **LLM binary document-matching**; an **agent fleet** (Sourcing, Legal Review, Citation Quality, URL Classification, Decision agents) builds and QA's the corpus. "Effective source = a link to a *specific piece of text within* a document."

## Q2 — Why so precise

1. **Curated corpus is the dominant lever** — you can't mis-cite what isn't vetted-and-indexed. (Source: [[2025 - Harvey - Using Agents to Scale Knowledge Sources]])
2. **Retrieval quality dominates** — ~50-pt correctness gains from retrieval alone, regardless of citation method. (Source: [[2025-09-25 - Generation-Time vs Post-hoc Citation]])
3. **Span-level linking** — text-within-document, not document-level.
4. **Hard verification gate** — hallucinated citation → automatic rejection; ambiguous → human review.
5. **Most "errors" are cheap** — ~80% of unverifiable facts are mis-citations, not hallucinations, so a post-hoc correction pass recovers them. (Source: [[2025-04-22 - CiteFix - Post-Processing Citation Correction]])

## Q3 — How to evaluate a citation

- **[[Citation Precision and Recall]]** (ALCE): **recall** = NLI says cited passages *entail* the claim; **precision** = no irrelevant citations. NLI-based, not string overlap; human agreement κ ≈ 0.70. (Source: [[2023-05-23 - Gao et al - ALCE]])
- Extended scorecard: + **correctness** (harmonic mean), **coverage**, latency, + human answer-correctness & citation-hallucination. (Source: [[2025-09-25 - Generation-Time vs Post-hoc Citation]])
- **Product-side** ([[2025 - Harvey - BigLaw Bench Sources|Harvey BigLaw Bench]]): document-level +1-per-sourced-claim (deliberate lower bound — passage-level scoring trades off against answer quality).
- Complementary reference-free hallucination detectors (Lynx, HHEM, TLM, RAGTruth).

## Q4 — Pre- vs post-verification pipeline

```
curated corpus → hybrid retrieve → rerank          ← PRE
   → draft (P-Cite) → NLI entailment check per claim
   → correct mis-citations (CiteFix) → auto-reject on fail  ← POST
   → user-facing clickable source (the "citation ground")
```
- **Pre**: corpus curation + strong retrieval ([[Reranking]], [[Contextual Retrieval]]) + generation steering (VeriCite pre-gen). (Source: [[2025-10-13 - VeriCite - Rigorous Citation Verification]])
- **Post**: per-claim NLI entailment + CiteFix correction (+15.5%) + auto-reject gate + iterative refinement. Use **[[Generation-Time vs Post-hoc Citation|P-Cite-first]]** for high-stakes.

## Key Entities

- [[OpenEvidence]]: medical RAG, closed curated corpus, ensemble models.
- [[Harvey]]: legal AI, agent-curated corpus, auto-reject on hallucinated citation.

## Key Concepts

- [[Attributed Text Generation]]: every claim linked to a source span.
- [[Citation Precision and Recall]]: NLI-entailment metric pair.
- [[Generation-Time vs Post-hoc Citation]]: G-Cite vs P-Cite tradeoff.
- [[Citation Verification Pipeline]]: pre (corpus+retrieval) + post (NLI+correction+gate).

## Connection to Nick's Work

- **H60 / Compass citation ground** = the user-facing tail of the pipeline (validate-the-source fallback). The leverage Nick can add upstream: a curated-corpus + reranking **pre-verification** stage, and an NLI-entailment + CiteFix-style **post-verification** stage with an auto-reject gate. Measure it with [[Citation Precision and Recall]], surfaced in [[Trace-Based Evaluation]].
- **Newsprout** cites from the **open web** — the curated-corpus lever (OpenEvidence/Harvey's biggest advantage) is unavailable, so **post-verification carries more weight**: NLI entailment per claim + CiteFix-style correction become the primary defense, not an add-on.
- **Highest-leverage takeaway**: separate *citation error* from *content hallucination*. ~80% of failures are the cheap kind (mis-attribution), fixable post-hoc — and a smaller model + correction can beat a bigger model alone (~12× cheaper in CiteFix).

## Contradictions

- **Span-level vs document-level**: Harvey *defines* a good source at span level but *scores* at document level (admits passage-level sourcing degrades answer quality). So "span-level citation" is the aspiration; document-level is what's reliably shippable today.
- **Harvey hallucination rate**: a Medium piece claims "1 in 6 queries"; Harvey claims its gates catch most phantom citations. Unreconciled — treat the rate as low-confidence.

## Open Questions

- Neither product discloses **how spans are matched/rendered** (the actual span-linking mechanism).
- No public **head-to-head** citation-quality benchmark across vertical products.
- How far does citation precision/recall **degrade on open-web sources** (the Newsprout regime) vs a curated corpus? — the most decision-relevant gap for Nick.

## Sources

- [[2023-05-23 - Gao et al - ALCE]] — citation precision/recall (high).
- [[2025-09-25 - Generation-Time vs Post-hoc Citation]] — G-Cite vs P-Cite (high).
- [[2025-04-22 - CiteFix - Post-Processing Citation Correction]] — post-hoc correction (high).
- [[2025-10-13 - VeriCite - Rigorous Citation Verification]] — pre+post verification (high).
- [[2025 - Harvey - BigLaw Bench Sources]] — source scoring (medium).
- [[2025 - Harvey - Using Agents to Scale Knowledge Sources]] — citation architecture (medium).
