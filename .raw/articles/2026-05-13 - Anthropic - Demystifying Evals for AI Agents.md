---
source_url: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
title: "Demystifying evals for AI agents"
author: Anthropic
date_fetched: 2026-05-13
type: raw
---

# Demystifying evals for AI agents

> Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
> Fetched: 2026-05-13
> Author: Anthropic Engineering Blog

## Full Content

Evaluating AI agents is fundamentally harder than evaluating single-turn LLM responses. This article from Anthropic's engineering team walks through a practical framework for building evaluation systems for agents, covering three evaluation tiers, key challenges, and how Anthropic's own teams implement them.

### The core challenge: non-determinism and multi-step trajectories

Agents operate across multiple steps, using tools, making decisions, and producing intermediate outputs. Unlike a single-turn LLM response, an agent's trajectory—the sequence of tool calls, reasoning steps, and outputs—may vary across runs even for identical inputs. This creates three distinct evaluation challenges:

1. **Multiple valid paths.** Different trajectories can reach the same correct outcome. Penalizing an agent for not taking the "expected" path is wrong.
2. **Long-horizon credit assignment.** If an agent fails at step 15, was the error at step 3, step 10, or step 15?
3. **Compounding errors.** Small mistakes early in a trajectory can cascade.

### The three-tier eval framework

Anthropic proposes a hierarchy—an eval pyramid—from cheap/fast to expensive/faithful:

#### Tier 1: Unit tests (deterministic checks)

The cheapest and most reliable evals. These are code-based assertions on specific, predictable behaviors:

- **Format checks** — does the agent return valid JSON? Does it call the right tool name?
- **Schema validation** — do outputs match the expected shape?
- **Boundary conditions** — does the agent refuse when it should? Does it handle malformed inputs?
- **Regression guards** — once a bug is fixed, a unit test locks it out forever.

Unit tests should cover every crisp, binary correctness criterion. If something can be checked deterministically, it should be. Don't use LLM judges for things a regex can evaluate.

#### Tier 2: LLM-as-judge (semantic evaluation)

When the correctness criterion is semantic rather than structural, use an LLM to grade. Key design principles:

- **Single-call judges are preferred** — not chains of reasoning, just a graded score on a rubric.
- **Multi-axis rubrics** — don't collapse to a single 1–10 score; break into dimensions (accuracy, completeness, appropriateness, efficiency).
- **Calibrate on human labels** — your judge is only as good as its correlation with human judgment on a calibration set.
- **Separate correctness from style** — these are different axes. An agent can give the right answer in a wrong tone.
- **Judge the final state, not the trajectory** — for most use cases, what matters is whether the agent achieved the right outcome, not how.

A common mistake: using LLM judges for things that should be unit tests. Another common mistake: using a single judge score when the task requires separating multiple independent correctness dimensions.

#### Tier 3: End-to-end evaluation with simulated users

The most expensive and faithful tier. For tasks that inherently require multi-turn interaction (customer service, research assistants, coding assistants):

- **User simulation** — an LLM plays the user, responding to agent messages and driving the conversation toward a task objective. The simulator has access to a user profile and goals; it does NOT have access to the agent's tool calls or internal reasoning.
- **Ground truth from environment state** — for constrained domains (e.g., database-backed customer service), reward comes from final environment state rather than from an LLM judge. This is the [[tau-bench]] approach.
- **Stochasticity budget** — more turns = more accumulated randomness. This is why [[Pass^k Reliability Metric]] matters: pass^1 looks good, but pass^8 shows collapse.

### Trace-based evaluation

Even when the final outcome is the primary eval target, traces (the full sequence of agent actions, tool calls, and reasoning steps) are valuable for debugging:

- **Failure attribution** — given a failed episode, at which step did the agent's trajectory diverge from the correct one? Traces allow post-hoc debugging without re-running expensive end-to-end evals.
- **Intermediate state checks** — some traces have checkpoints where correctness can be assessed mid-trajectory (e.g., "did the agent retrieve the right document before synthesizing?").
- **Coverage metrics** — across a test set, which tool was called most often? Which tool was never called? Coverage metrics from traces surface gaps in capability or test diversity.

Anthropic's internal teams log all tool calls, inputs, outputs, and timing in a structured format. Traces are stored and queryable, enabling both automated eval pipelines and human review.

### Separating correctness from style

A point Anthropic emphasizes: **correctness and style are separate eval dimensions** and conflating them causes systematic bias:

- An agent can produce factually correct output with poor formatting.
- An agent can produce beautifully formatted output with wrong facts.
- An LLM judge that scores holistically conflates these and rewards style even when correctness fails.

Rubrics should include explicit axes: factual accuracy, task completion, appropriate tool selection, format compliance, verbosity (when relevant), tone (when relevant). Factual accuracy should be scored independently and weighted most heavily.

### The importance of calibration sets

LLM judges drift. Over time:

- Model updates change judge behavior.
- Prompt drift changes judge behavior.
- Distribution shifts in inputs change what the judge sees.

Anthropic maintains **calibration sets** — small (50–200 example) human-labeled datasets that periodically validate that the judge still correlates with human judgment. A judge whose correlation with humans drops below a threshold triggers a re-calibration pass.

### Human-in-the-loop as a structural component

Human review is not a fallback for when evals fail. It's a structural component:

- **Calibration** — humans label calibration sets periodically.
- **Spot-checking** — a sample of live agent outputs is reviewed by humans weekly or biweekly.
- **Adversarial probing** — humans probe for failure modes the automated suite doesn't yet cover; new probes become unit tests or rubric dimensions.

### Practical advice summary

1. Start with unit tests. They're underused for agents because people assume agents are inherently non-deterministic — but many behaviors are crisply deterministic.
2. Build the judge before the agent. A good eval framework lets you measure progress; without it you're flying blind.
3. Don't over-rotate to end-to-end. Full simulated-user evals are expensive (tokens + time). Use them for key capability claims, not for every PR.
4. Log traces from day 1. Retroactive trace logging is painful; build it into the eval infrastructure from the start.
5. Calibrate your judge regularly. A judge you haven't calibrated in 3 months may no longer reflect human judgment.
6. Keep correctness and style separate. Aggregate scores that mix these produce misleading signals.

### The meta-principle

**Evals are a product, not a script.** They require ongoing maintenance, calibration, and extension. An eval suite that captures 60% of failure modes is not "60% done" — the uncaptured 40% is often the long tail of adversarial inputs and edge cases that determines production reliability.
