---
source_url: https://wanglun1996.github.io/blog/your-evals-will-break.html
fetched: 2026-05-28
author: Lun Wang
date_published: 2026-05-17
note: "Faithful structured capture (headings + paraphrase + short verbatim quotes + full reference list). Full verbatim reproduction withheld for copyright; this is a fair-use working capture for the wiki."
---

# Your Evals Will Break and You Won't See It Coming

**Lun Wang — May 17, 2026** (posted the day the author left Google DeepMind).

## Core thesis

> "eval — not training, not architecture, not data — is the bottleneck for the next capability jump."

The field is good at evaluating *present* models but bad at evaluating *future* ones, especially across capability boundaries. When models cross into a genuinely new capability regime, the evaluation infrastructure built for the old regime can mislead — "we're flying blind."

## Qualitative vs. quantitative shifts

Distinguishes genuine **emergent abilities** (Wei et al., 2022) from **measurement artifacts** (Schaeffer et al., 2023 — "Are Emergent Abilities a Mirage?"). Whether a capability transition is *real* or an *illusion of the metric*, the existing eval infrastructure can give the wrong reading. Related: **grokking** (Power et al., 2022; Liu et al., 2022) — delayed generalization is another regime where the metric you watch determines what you see.

## Missing order parameters

Physics detects **phase transitions** via **order parameters** — macroscopic quantities that signal a regime change. LLM evaluation has no analogous order parameter. Today's benchmarks (GPQA, SWE-bench, ARC-AGI, Humanity's Last Exam) measure present capability but give weak evidence about *post-transition* behavior. We lack a macroscopic signal that says "the system has crossed into a new regime."

## Evaluation is structurally reactive

> "our entire evaluation infrastructure is structurally reactive. We measure the system after it has changed."

Benchmarks are built for known capabilities; by construction they observe a shift only after it has already happened. This is the structural blind spot.

## Concrete failure case: strategic information withholding

A model could selectively **omit** facts to steer a conversation toward a desired conclusion while every individual statement remains technically truthful. Existing honesty benchmarks check whether statements are true, not whether the *selection* of statements is manipulative — so this novel failure mode would pass undetected. An example of a capability/behavior that emerges across a boundary and slips through evals designed for the prior regime.

## Eval as upstream constraint on training

> "if you can evaluate correctly, you can train correctly. Training is optimization, and optimization is only as good as its objective."

Training is optimization against an objective, and the objective is the eval. So a misaligned eval propagates downstream into training signals, safety metrics, and scaling decisions. **Goodhart's Law breaks at phase boundaries**: a proxy that tracked the goal in the old regime can decouple from it in the new one. Eval sits upstream of everything.

## Proposed solutions

1. **Identify order parameters** for capability transitions, borrowing from statistical mechanics and mechanistic interpretability (cites Shan, Li & Sompolinsky, PNAS 2026 — "Order Parameters and Phase Transitions of Continual Learning"; Nanda et al., ICLR 2023 — progress measures for grokking via mech interp).
2. **Build adaptive evaluation systems** that:
   - Monitor **meta-signals** — changes in score *distributions*, shifts in *correlations* between metrics.
   - Track **scaling curves** across multiple dimensions, not single headline numbers.
   - Use **self-evolving evals** — models probing models.
   - **Auto-generate** new test cases as capabilities emerge.

## Technical concepts referenced

Emergent abilities; grokking; chain-of-thought reasoning; exact-match accuracy vs. continuous/smooth metrics; phase transitions; order parameters; mechanistic interpretability; RLHF; Goodhart's Law.

## References (as cited in the post)

1. Wei et al. (2022) — *Emergent Abilities of Large Language Models.*
2. Power et al. (2022) — *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets.*
3. Liu et al. (2022) — *Towards Understanding Grokking.*
4. Schaeffer, Miranda & Koyejo (2023) — *Are Emergent Abilities of Large Language Models a Mirage?* (NeurIPS 2023).
5. Nanda et al. (2023) — *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023).
6. Shan, Li & Sompolinsky (2026) — *Order Parameters and Phase Transitions of Continual Learning* (PNAS 2026).
