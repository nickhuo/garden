---
source_url: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
title: "Designing AI-resistant technical evaluations"
author: "Anthropic Engineering"
date_fetched: 2026-05-13
date_published: 2025
---

# Designing AI-resistant technical evaluations

Source: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations

## Summary

Anthropic engineering discusses how they redesigned their technical hiring process to remain meaningful in an era where AI coding assistants can solve many traditional coding interview problems. The post lays out the problem (AI can trivially pass standard LeetCode-style screens), their design principles, and the specific evaluation formats they adopted.

## Key content

### The problem with traditional evaluations

Standard technical screening — LeetCode-style problems, algorithmic puzzles, take-home projects — can be largely solved by current AI coding assistants (Claude, GPT-4, Copilot). This creates several issues:
- Signal collapse: scores no longer discriminate between candidates who understand vs. those who can prompt
- Arms race dynamics: raising difficulty just shifts where AI assistance tips the scale, not whether it does
- Adverse selection: evaluations that ban AI use may filter out high-quality candidates who use AI fluently in their actual work

### Design principles for AI-resistant evaluations

Anthropic settled on evaluations that test abilities AI cannot substitute:

1. **Live debugging of unfamiliar code** — Candidates receive a broken, novel codebase and must diagnose faults in real time. Understanding without context cannot be faked by AI because the candidate must explain their reasoning live and respond to follow-up probes.

2. **System design discussions** — Open-ended architecture conversations where the interviewer actively challenges assumptions. AI can draft a design, but cannot navigate a live socratic dialogue where the interviewer pushes on tradeoffs specific to Anthropic's constraints.

3. **Genuine comprehension probes** — Questions that require candidates to demonstrate they understand *why* something works, not just that they can produce working code. E.g., "why would you choose this data structure here?" followed by adversarial counter-proposals.

4. **Paired problem-solving with transparency about AI use** — Some evaluations explicitly allow AI tools and assess *how* a candidate uses them: do they verify AI output, catch errors, integrate suggestions critically?

5. **Work-sample tasks tied to actual job scope** — Problems drawn directly from real engineering challenges Anthropic faced, where domain context matters and generic solutions fail.

### Evaluation dimensions that remain AI-resistant

- **Debugging under uncertainty** — Systematic hypothesis formation and elimination
- **Communication of mental models** — Explaining reasoning to a live interviewer who probes
- **Judgment about tradeoffs** — Not which solution is correct, but which is right *for this context*
- **Critical use of AI tools** — Does the candidate trust blindly or verify and correct?

### Implications for the field

The post argues that the hiring industry is at an inflection point. Evaluations that test rote algorithmic knowledge are obsolete. The new signal is: can the candidate reason clearly about systems, communicate that reasoning, and use AI tools as a force-multiplier rather than a crutch?

Anthropic frames AI tool fluency as a first-class engineering competency — not a cheat, but a skill that should be explicitly evaluated.

### Specific formats adopted

- **Debugging interview**: live session with a real buggy repo (not a toy problem); candidate has 45 min; interviewer watches process not just outcome
- **Design deep-dive**: 45 min architecture discussion with intentional constraint injection mid-session
- **AI-assisted take-home** (for some roles): explicitly allow all AI tools; graded on quality of output AND candidate's explanation of their AI interaction strategy

### Connection to Anthropic's broader views

The post connects to Anthropic's public writing on evals (see the alignment/safety evals work): good evals measure the thing you actually care about, not a proxy that can be gamed. The same principle applies to hiring evals.

Anthropic's engineering team is itself heavy users of Claude for coding — so the meta-point is: they want to hire people who can work the way their own engineers work, which includes fluent AI use.
