---
type: entity
title: "Noah Shinn"
created: 2026-06-18
updated: 2026-06-18
tags: [ai-agents, entity, person]
status: seed
entity_type: person
entity_tier: thinker
role: "Researcher; lead author of Reflexion (verbal reinforcement learning for language agents)."
core_claim: "A language agent can learn from failure through natural-language self-reflection stored in memory — no weight updates required."
first_mentioned: 2026-06-18
related: ["[[Verbal Reinforcement Learning]]", "[[2023-03-20 - Shinn et al - Reflexion]]", "[[Shunyu Yao]]", "[[Karthik Narasimhan]]"]
sources: ["[[2023-03-20 - Shinn et al - Reflexion]]"]
---

# Noah Shinn

Lead author of **[[2023-03-20 - Shinn et al - Reflexion|Reflexion]]** (NeurIPS 2023), which introduced
[[Verbal Reinforcement Learning]] — reinforcing language agents through linguistic feedback and an
episodic reflection memory rather than gradient updates. Reflexion's 91% pass@1 on HumanEval (beating
GPT-4's 80%) made it one of the most-cited demonstrations that **in-context self-correction** can
substitute for fine-tuning when the task is verifiable.

## In the wiki

- **2023 — [[2023-03-20 - Shinn et al - Reflexion]]** — verbal RL; Actor / Evaluator / Self-Reflection
  loop over an episodic memory buffer.

Co-authored with [[Shunyu Yao]] and [[Karthik Narasimhan]], extending their [[ReAct]] line.
