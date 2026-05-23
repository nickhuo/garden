---
type: concept
title: "Binary Evaluation vs Scoring"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - llm
  - methodology
related:
  - "[[LLM-as-Judge Evaluation]]"
  - "[[Specialized Eval Classifiers]]"
  - "[[Eval Validity]]"
  - "[[Agent Eval Pyramid]]"
sources:
  - "[[2026-01-15 - Husain Shankar - LLM Evals FAQ]]"
  - "[[2025-04-20 - Tripathi et al - Pairwise or Pointwise]]"
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
---

# Binary Evaluation vs Scoring

The principle that evaluation labels should be **binary (pass/fail)**, or otherwise low-cardinality, rather than fine-grained numeric (1-5 Likert) scores. A recurring question is *where this idea comes from* — it has three roots, none of them originally Anthropic.

## Where it comes from

1. **Software-testing / assertion framing.** Treat evals like unit tests: each check is a pass/fail assertion against a specific behavior. Low-cardinality by construction; the deterministic Tier-1 of the [[Agent Eval Pyramid]].
2. **Practitioner codification — the primary popularizer.** Hamel Husain & Shreya Shankar ([[2026-01-15 - Husain Shankar - LLM Evals FAQ]]) made the case explicit and widely adopted (taught at OpenAI/Anthropic, which is why people often misattribute it to Anthropic): *"Start with binary labels… Numeric labels are advanced and usually not necessary."* Decompose a holistic quality judgment into **many specific binary sub-checks** (e.g. "4 of 5 expected facts included") rather than one score.
3. **Judge-reliability research — the empirical backbone.** Both humans and LLM judges are unreliable at fine gradations. [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]] (MT-Bench) shows relative/pairwise easier than absolute fine-grained scoring; [[2025-04-20 - Tripathi et al - Pairwise or Pointwise]] (COLM 2025) shows absolute scoring more robust to manipulation than pairwise (35% vs 9% flip). The convergent lesson: **avoid high-cardinality Likert**; a clear binary with explicit criteria is the robust sweet spot.

## Why binary wins in practice

- **Consistency** — adjacent Likert points (3 vs 4) are subjective; a binary line is not.
- **Statistical power** — detecting a difference on a binary metric needs smaller samples than on a 1-5 scale (matters under the [[Online Evaluation Bottlenecks]] power constraint).
- **Forces a decision** — annotators can't hide in the middle; a domain expert must define what "acceptable" means.
- **Composability** — many binary sub-checks reconstruct granularity without sacrificing clarity, and each maps cleanly to a trained classifier ([[Specialized Eval Classifiers]]).

## Relation to Anthropic (the common misattribution)

Anthropic's [[LLM-as-Judge Evaluation]] guidance actually uses **graded 0.0-1.0 rubrics** (multi-axis, not collapsed to one number). Its only strictly-binary layer is deterministic Tier-1 unit tests. So "binary not scoring" is *aligned with* Anthropic's "don't collapse to one number / use deterministic checks" but **originates** from the practitioner + assertion + judge-reliability lineage above, not from Anthropic.

## Open questions

- When *is* a numeric score worth the cost? (Husain/Shankar: "advanced, usually not necessary" — but ranking/triage may need ordinality.)
- Does decomposing into many binary checks just relocate the subjectivity into "which checks"? (Construct validity — see [[Eval Validity]].)
