---
type: source
title: "VeriCite: Reliable Citations in RAG via Rigorous Verification"
created: 2026-05-23
updated: 2026-05-23
tags:
  - llm
  - citation
  - rag
  - evaluation
status: developing
source_type: paper
author: "(arXiv 2510.11394)"
date_published: 2025-10-13
url: "https://arxiv.org/abs/2510.11394"
confidence: high
related:
  - "[[Citation Verification Pipeline]]"
  - "[[Citation Precision and Recall]]"
  - "[[Attributed Text Generation]]"
sources:
  - "https://arxiv.org/pdf/2510.11394"
---

# VeriCite

A two-stage verification framework for RAG citations (arXiv 2510.11394, 2025). Exemplifies the **pre + post** verification structure in [[Citation Verification Pipeline]].

## Two-stage architecture

- **Pre-generation verification** — verify/guide *before* drafting, steering generation toward attributable outputs (don't let the model write claims it can't support).
- **Post-generation verification** — after drafting, validate citations and flag unsupported claims; feed back into **answer refinement**.

## What it checks

- **Claim-level** — is each factual statement substantiated by retrieved docs?
- **Span-level** — do specific text segments align with the source material?
- **Citation matching** — does the cited passage actually reflect the document content?

## Loop

Initial answer generation → verification → answer refinement (iterate). Document retrieval feeds both generation and verification.

Demonstrates that rigorous, structured verification (not just a single post-hoc check) materially improves citation reliability.

> [!gap] Reported with BLEU/ROUGE plus citation metrics; full numeric tables are in the appendix and were not extracted here.
