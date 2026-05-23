---
type: entity
title: "Harvey"
entity_type: organization
created: 2026-05-23
updated: 2026-05-23
tags:
  - ai-agents
  - llm
  - citation
  - rag
  - legal
status: developing
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Citation Precision and Recall]]"
  - "[[OpenEvidence]]"
  - "[[Multi-Agent Systems]]"
sources:
  - "[[2025 - Harvey - BigLaw Bench Sources]]"
  - "[[2025 - Harvey - Using Agents to Scale Knowledge Sources]]"
---

# Harvey

Legal AI for professional services. Citation precision is a core product requirement because attorneys must cite verifiable authority. The legal counterpart to [[OpenEvidence]].

## Citation approach

- **Curated, authoritative corpus only** — vetted government portals + authoritative legal databases; **LexisNexis alliance (June 2025)** adds **Shepard's Citations** to validate cited authorities. No open-web citing.
- **Pipeline**: structured metadata extraction + embedding-based search + **LLM binary document-matching** (does this doc support this claim, yes/no).
- **Agent fleet** for sourcing & QA: Sourcing Agent, Legal Review Agent, **Citation Quality Agent**, URL Classification Agent, Decision Agent — see [[2025 - Harvey - Using Agents to Scale Knowledge Sources]].
- **Verification gate**: hallucinated citation → **automatic rejection**; ambiguous cases routed to human review.
- **Effective source** defined as linking to a *specific piece of text within* a document (span-level intent), though the public **BigLaw Bench** metric scores at document level as a lower bound — see [[2025 - Harvey - BigLaw Bench Sources]].

## Scale

6 → 60+ jurisdictions, 20 → 400+ legal data sources (since Aug 2025). Valued ~$8B.

> [!gap] A Medium analysis claims Harvey "hallucinates in 1 of 6 queries" — low-confidence, contested, not independently verified. Harvey states its verification systems catch most phantom citations, with edge cases on obscure/recent rulings.
