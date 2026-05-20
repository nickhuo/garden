---
type: concept
title: "Interaction Model Architecture"
created: 2026-05-14
updated: 2026-05-14
tags:
  - llm
  - ai-agents
  - concept
  - real-time
  - multimodal
status: developing
complexity: advanced
domain: llm
aliases:
  - "interaction model"
  - "real-time AI architecture"
related:
  - "[[Trainer-Sampler Determinism]]"
  - "[[Multi-Agent Systems]]"
sources:
  - "[[2026-05-11 - Thinking Machines - Interaction Models]]"
---

# Interaction Model Architecture

A two-component design for real-time multimodal AI:

- **Interaction model** — latency-bound, handles streaming I/O on 200ms micro-turns, maintains user presence
- **Background model** — intelligence-bound, handles async reasoning, tool use, complex planning. Results stream back into the live conversation

The architecture argues that **interactivity must be in the model, not the interface**. Retrofitting real-time UX onto turn-based models hits a ceiling — the existing model has no concept of elapsed time, simultaneous speech, or proactive output.

## Three technical pillars

1. **Time-aligned micro-turns** — 200ms continuous chunks for input AND output. Both are streams. No discrete user turns.
2. **Encoder-free early fusion** — Audio → dMel via lightweight embedding; images → 40×40 hMLP patches. End-to-end trained with the transformer (no large standalone encoders).
3. **Persistent streaming sessions** — Server appends 200ms chunks into GPU memory rather than re-prefilling. Eliminates per-chunk memory allocation and metadata overhead. Contributed upstream to SGLang.

## Capabilities unlocked

- Implicit dialog management (no separate turn-taking module)
- Verbal/visual interjections at the model's initiative
- Simultaneous speech (live translation)
- Direct time-awareness
- Concurrent tool ops while engaging the user

## Connection to [[Trainer-Sampler Determinism]]

The interaction model uses **bitwise trainer-sampler alignment** as a stability tool — <5% performance overhead, large stability win. Same technique as [[2025-09-10 - He - Defeating Nondeterminism in LLM Inference]], applied to training instead of reproducible inference.

## Relation to multi-agent thinking

The split is reminiscent of [[Multi-Agent Systems]] orchestrator-worker, but the foreground worker is **latency-bound** and the background "orchestrator" is **intelligence-bound** — a specialization the agents wiki hasn't articulated yet.

## Empirical (TML-Interaction-Small)

276B params, 12B active.

- FD-bench V1.5: 77.8 (audio)
- Turn-taking latency: 0.40s
- TimeSpeak: 64.7% (vs 4.3% for GPT Realtime-2.0 minimal)
- CueSpeak: 81.7% (vs 2.9%)
- Charades mIoU: 32.4 (vs 0%)

Competitors hit near-chance on proactive-output tasks, suggesting the gap is architectural, not training-data.

## Open

- Long-session context management
- Network reliability dependence
- Coordination protocols between foreground and background models
