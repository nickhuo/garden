---
type: concept
title: Tree of Thoughts
created: 2026-05-19
updated: 2026-05-19
tags:
- ai-agents
- reasoning
- decision-making
- search
status: seed
related:
- "[[CoALA]]"
- "[[ReAct]]"
- "[[Shunyu Yao]]"
sources:
- "[[2023-09-05 - Sumers et al - Cognitive Architectures for Language Agents]]"
---

# Tree of Thoughts

A **deliberate planning** method (Yao et al., 2023) that generalizes chain-of-thought from a single linear trace to a **tree** of reasoning steps, explored with search. At each node the model proposes candidate next "thoughts," evaluates them, and the search (BFS/DFS/best-first) decides which branches to expand.

## In CoALA terms

[[Tree of Thoughts]] is the canonical example of a **full planning sub-cycle**:
- **Proposal** — generate candidate thoughts.
- **Evaluation** — LLM scores each candidate's promise.
- **Selection** — tree search picks which to expand (vs [[ReAct]]'s no-evaluation commit).

But it has **no long-term memory** — it's pure deliberation within working memory. It trades the breadth of grounding for depth of reasoning.

## Contrast with ReAct

[[ReAct]] acts in the world with a fixed cycle and no evaluation; ToT thinks hard internally with explicit propose/evaluate/select but doesn't ground. CoALA's framing makes the complementarity obvious: a capable agent wants ToT's deliberation *and* ReAct's grounding *and* the long-term memory neither has.
