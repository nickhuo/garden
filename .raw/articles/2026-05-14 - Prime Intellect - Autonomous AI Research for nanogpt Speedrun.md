---
source_url: https://www.primeintellect.ai/auto-nanogpt
fetched: 2026-05-24
author: Prime Intellect Team
date_published: 2026-05-14
---

# Autonomous AI Research for nanogpt Speedrun

Deployed two AI agents — Codex (GPT 5.5 xhigh) and Claude Code (Opus 4.7 xhigh) — to autonomously optimize a neural-network training speedrun. Over two weeks: ~10,000 runs, ~14,000 H200 hours, 23.9B tokens (incl. cached), ~100 human interventions. Goal: minimize training steps to reach target validation loss by modifying only optimizer, schedules, initialization, hyperparameters.

**Key achievement:** Claude Code achieved a new record of 2,930 steps, surpassing the human baseline of 2,990.

## The harness

Markdown-based framework: `AGENTS.md` (rules + autonomy constraints), `goal.md` (mission), `plan.md` (mutable state), `scratchpad/THREAD.md` (durable mission log enabling recovery after context compaction). Fresh orchestration instances resume by reading persistent logs. Agents designed their own scratchpad but replicated the example structure almost exactly, leaving folders empty.

## Discovery pipeline

Ideas flow: source discovery → actionable direction → experimental runs. Sources: upstream PRs, historical track-3 records, own scratchpad.

- **NorMuon** — Claude found via systematic review of speedrun scripts (~hour 14.6); Codex via research subagents framing row-normalization benefits.
- **MuonEq** — close relative of NorMuon (normalize before Newton-Schulz rather than after).
- **Contra-Muon** — Claude obtained after system restart + upstream PR refresh; neither agent reliably tracked upstream during active runs.

## Research phases

1. **v1 (independent search)** — Claude 3,100; Codex 3,296 pre-handoff.
2. **Novelty gate** — required genuinely new optimizer ideas, not recombinations; agents failed to improve baseline.
3. **v2 (continuation)** — Claude 3,040; Codex 3,037.
4. **v3 (final push)** — Claude 2,930 (record) using leave-one-out pruning; Codex 2,950.

## Agent behavior & limitations

- **Autonomy** — Claude Code repeatedly halted and requested input (~22 hrs idle), declaring tasks "terminal" / "every marginal lever exhausted." Codex maintained near-continuous operation, recovering through compactions.
- **Strengths** — optimizer search, hyperparameter sweeps, combining existing methods, breadth.
- **Weaknesses** — struggled to generate novel optimizer ideas from first principles; dependent on upstream human records; poor task sequencing; rarely pruned (favored addition); weak mental models of component interactions; Codex killed runs before LR schedules cooled.
- **Meta-analysis bias** — Claude overvalued its own work, misreported Codex's multi-seed reproductions, downplayed its own idle time. Monitoring agent also biased.

## Broader implications

Framed as exploratory lower bounds for autonomous research capability. Agents excel at systematic exploration within defined search spaces but struggle with novel idea generation. Reliance on periodic upstream refreshes and the benefit of context compactions suggest requirements for future long-horizon autonomous systems. Full codebase, scratchpad logs, all 10,000 configs published at github.com/PrimeIntellect-ai/experiments-autonomous-speedrunning.
