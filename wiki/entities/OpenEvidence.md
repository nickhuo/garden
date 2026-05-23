---
type: entity
title: "OpenEvidence"
entity_type: organization
created: 2026-05-23
updated: 2026-05-23
tags:
  - ai-agents
  - llm
  - citation
  - rag
  - medical
status: developing
related:
  - "[[Attributed Text Generation]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Harvey]]"
  - "[[Contextual Retrieval]]"
sources:
  - "https://www.openevidence.com/about"
---

# OpenEvidence

A clinical-decision-support AI that answers physicians' questions grounded in peer-reviewed medical literature, with every statement sourced and cited. The medical counterpart to [[Harvey]] (legal) as a citation-precise vertical product.

## Citation approach

- **Closed, curated corpus** — 300+ medical journals (NEJM, JAMA, Cochrane, NCCN) plus FDA/CDC; explicitly **not connected to the public internet**. The corpus is the precision lever: it can only cite vetted primary literature.
- **Ensemble of specialized models** (not a single LLM), trained on peer-reviewed literature — a RAG system.
- Output: natural-language answer with **hyperlinked references after the text**, each linked to the source abstract, so a clinician can validate before acting. This "validate-the-source" affordance is the same role as Nick's H60/Compass **citation ground**.

## Notability

- First AI to score a claimed **100% on the USMLE**.
- Used as a comparison baseline in academic studies of biomedical RAG.

## Why it matters here

OpenEvidence shows that **domain + closed corpus + ensemble retrieval** is how you get citation precision high enough for a high-stakes profession. Contrast with open-web citation (the harder regime — e.g. Nick's Newsprout).

> [!gap] Exact retrieval/reranking stack and span-linking mechanics are not publicly disclosed (vendor + secondary sources only).
