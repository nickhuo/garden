---
type: entity
title: "Andrej Karpathy"
created: 2026-05-20
updated: 2026-06-01
tags:
  - ai-agents
  - llm
  - entity
  - person
status: developing
entity_type: person
entity_tier: thinker
role: "AI researcher and educator; coined 'Software 2.0' (2017) and 'Software 3.0' / LLM-as-OS framing (2025). Former Director of AI at Tesla, founding member of OpenAI."
core_claim: "Logic keeps migrating out of hand-written code and into the model — but understanding can never be outsourced."
first_mentioned: 2026-05-20
related:
  - "[[Software 2.0]]"
  - "[[Software 3.0]]"
  - "[[Agentic Engineering]]"
  - "[[Verifiability]]"
  - "[[Jagged Intelligence]]"
  - "[[Model-Centric Architecture]]"
  - "[[The Bitter Lesson]]"
  - "[[Richard Sutton]]"
sources:
  - "[[2017-11-11 - Karpathy - Software 2.0]]"
  - "[[2026-05-22 - Karpathy - Sequoia Ascent 2026]]"
---

# Andrej Karpathy

AI researcher and educator (ex-Director of AI at Tesla, founding member of OpenAI). The clearest articulator of how the *software stack itself* changes under machine learning.

## Worldview / 核心主张

1. **The stack is changing in stages.** Software 1.0 = explicit code; **[[Software 2.0]]** = learned weights ("the program is the weights, written in a human-unfriendly language"); **[[Software 3.0]]** = programming the model in natural language, with the context window as "your lever over the interpreter." Logic steadily migrates out of hand-written code and into the model.
2. **Partial autonomy, not full.** Against the "year of agents" hype he favors a human-controllable **autonomy slider** — keep a human in the loop. This is the *user-keeps-final-control* leg of [[Model-Centric Architecture]].
3. **Understanding is not outsourceable.** "You can outsource your thinking, but you can't outsource your understanding." Knowledge bases are tools for *transforming information into understanding*, not answer machines — the thesis directly motivating this vault's LLM-wiki pattern.

## Methodology / 方法论

- **Distill to the smallest inspectable artifact.** nanoGPT / `microGPT`: a stripped, readable core + human taste + an agent that can explain it interactively. He teaches by building the minimal version that still works.
- **Empirical familiarity as posture.** LLMs are "**ghosts, not animals**" — statistical simulations of human artifacts, brilliant then "bizarrely dumb." Correct stance is neither dismissal nor blind trust but earned, hands-on calibration of where they break.
- **Name the era, then operationalize it.** His essays coin a frame (2.0, 3.0, agentic engineering) and immediately ground it in a worked example (MenuGen collapsing a web stack into one multimodal transform; the Stripe/Google email-mismatch bug as the cautionary identity-error case).

## Body of work (in the wiki)

- **2017 — [[2017-11-11 - Karpathy - Software 2.0]]** — weights as a new software stack; why weights beat code (homogeneous compute, constant runtime, agility, cross-module optimization) and the costs (opacity, bias, adversarial fragility).
- **2026 — [[2026-05-22 - Karpathy - Sequoia Ascent 2026]]** — the agentic-engineering capstone: the Dec-2025 coding-agent reliability jump, [[Software 3.0]], [[Verifiability]] ("automate what you can *verify*"), [[Jagged Intelligence]], [[Vibe Coding]] vs [[Agentic Engineering]], and [[Agent-Native Infrastructure]] (build sensors/actuators, not screens).

## Throughlines

- **Migration of logic from code → weights → prompts** is the single arc connecting every piece.
- **Verifiability as the engine of progress** (2026) is the *why-now* under the Software 2.0 thesis — and the same engine [[The Bitter Lesson]] points at.
- **Pedagogy as a first-class activity** — the educator's instinct (minimal artifact, explain-don't-just-answer) runs through all his work.

## Tensions

- **vs [[Richard Sutton]]** — complementary, not opposed: Sutton supplies the scaling-beats-hand-engineering backbone ([[The Bitter Lesson]]); Karpathy adds the *human-in-the-loop* and *understanding* constraints a pure-experience view underweights.
- **vs full-autonomy agent maximalism** (cf. [[Geoffrey Huntley]]'s no-human-in-the-loop [[Ralph Loop]]) — Karpathy explicitly keeps the autonomy slider human-controllable.

## Corpus to ingest

- "Software Is Changing (Again)" 2025 talk (the LLM-as-OS framing referenced but not yet a source page).
- nanoGPT / `microGPT` write-ups as primary artifacts for the pedagogy thread.
