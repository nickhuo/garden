---
source_url: https://karpathy.bearblog.dev/sequoia-ascent-2026/
fetched: 2026-05-22
---

# Sequoia Ascent 2026 — Andrej Karpathy on AI Agents and Software 3.0

> Captured via WebFetch (summary + detailed outline). The bearblog post accompanies Karpathy's Sequoia Ascent 2026 remarks. Direct quotes below are reproduced as captured.

## 1. December 2025 was an agentic inflection point

- Around December 2025, code-generation quality shifted notably — "the chunks just came out fine" without requiring correction.
- Tools like Claude Code, Codex, and Cursor agents moved from helpful-but-flawed to consistently reliable.
- The programming unit changed from writing individual lines to delegating larger "macro actions" (implement features, refactor subsystems, write and fix tests).
- The profession itself is being refactored: programmers become orchestrators of agents rather than sole code writers.

## 2. Software 3.0: the context window as the new program

- **Software 1.0**: humans write explicit code.
- **Software 2.0**: humans create datasets and neural networks; programs are learned into weights.
- **Software 3.0**: humans program LLMs through prompts, context, tools, examples, memory, and instructions.
- The context window becomes "your lever over the interpreter" — the LLM interprets context and performs computation over digital information.
- Example: OpenClaw installation becomes a copy-pasteable agent skill rather than complex shell scripts targeting multiple platforms.

## 3. MenuGen and the moment software disappears

- MenuGen originally required frontend code, APIs, image generation, deployment, auth, payments, and infrastructure.
- Software 3.0 version: a multimodal model takes a menu photo and "renders dish images directly onto the menu image."
- "Much of the app disappears" — the neural network directly transforms input media to output media.
- Implication: some apps should cease existing as traditional applications; AI isn't just faster building of old systems.
- The old software stack was "scaffolding around a transformation the model can now perform directly."

## 4. The new opportunity is not just faster programming

- LLMs automate information processing that wasn't previously programmable.
- LLM Wiki pattern: agents incrementally compile raw sources into persistent Markdown wikis with summaries, entity pages, concept pages, and cross-links.
- Classical programs couldn't maintain knowledge bases "robustly... across messy human documents."
- Key lesson: ask not only "What existing workflow can AI speed up?" but also "What information transformation was impossible before?"

## 5. Verifiability explains where AI moves fastest

- "Traditional software automates what you can specify; LLMs automate what you can verify."
- Tasks with automatic reward signals improve fastest: math, coding, tests, benchmarks, games, engineering tasks.
- Coding agents feel "dramatically better" because models receive immediate feedback — tests pass/fail, programs run/crash, benchmarks measurable.
- Where tasks lack verification signals, improvement stagnates or remains rough.

## 6. Jagged intelligence has two axes: verifiability and training attention

- Capability depends on both verifiability AND training-lab emphasis during pretraining, post-training, and RL.
- Rough formula: capability spike = verifiability × training attention × data coverage × economic value.
- Chess example: GPT-4's chess improvement partly reflected "much more chess data... included in the training mix," not smooth general improvement.
- Models are "artifacts of pretraining mixtures, RL environments, benchmark pressure, product priorities, and economic incentives."
- Practical founder question: "Are you on the model's rails?" Tasks in verified, heavily-trained regions may excel; outside those circuits, models may fail at basic tasks (the "car wash walking" problem).
- Solutions: better context, tools, fine-tuning, custom evaluations, or proprietary RL environments.

## 7. Vibe coding vs. agentic engineering

- **Vibe coding**: raises the floor — allows nearly anyone to create software by describing needs.
- **Agentic engineering**: raises the ceiling — professional discipline coordinating fallible agents while preserving correctness, security, taste, and maintainability.
- Agentic engineers don't blindly accept generated code; they design specs, supervise plans, inspect diffs, write tests, manage permissions, and preserve quality.
- MenuGen payment bug example: the agent matched Stripe purchases to Google accounts by email, but "the Stripe email and Google login email can differ."
- The frontier skill isn't memorizing APIs — agents handle that — but understanding underlying concepts: storage, memory copies, invariants, identity, security boundaries, system shape.

## 8. Hiring should change

- Traditional coding puzzles are increasingly mismatched to agentic-engineer capabilities.
- Better interview: build a substantial project with agents, deploy it securely, then have adversarial agents attempt breaking it.
- Tests real skills: decomposing work for agents, writing useful specs, preserving quality while moving fast, reviewing generated work, securing systems, using agents as leverage.
- "The old '10x engineer' idea may become much more extreme."

## 9. Founders should look for valuable verifiable environments

- Opportunity: find domains that are valuable, verifiable, and **undertrained by frontier labs**.
- If creators build domain-specific environments with reliable rewards, they can improve performance through fine-tuning or RL even if the base model isn't excellent there.
- Obvious domains (coding, math) are already heavily targeted; many economically important domains have "latent verifiable structure that has not yet been exploited."
- This is a startup wedge.

## 10. Agent-native infrastructure: build for the agent, not just the human

- Most software is still built for humans clicking through screens — "go to this URL, click this button."
- The user increasingly isn't the human directly but the human's agent.
- Products need agent-native surfaces: Markdown docs, CLIs, APIs, MCP servers, structured logs, machine-readable schemas, copy-pasteable instructions, safe permissioning, auditable actions, headless flows.
- Framework in terms of **sensors** and **actuators**: sensors turn world state into digital information; actuators let agents change things.
- MenuGen deployment remains the benchmark: building the app was easy; wiring Vercel, auth, payments, DNS, secrets, and production settings was hard — a mature agent-native world should automate this.

## 11. Ghosts, not animals

- LLMs are not animals — they lack biological drives, embodied survival, curiosity, play, or intrinsic motivation.
- They are "statistical simulations of human artifacts, shaped by pretraining, post-training, RL, product feedback, and economic incentives."
- Systems can be "brilliant in one moment and bizarrely dumb in the next" — not smooth human minds but "jagged, alien tools."
- Right posture: neither dismissal nor blind trust, but "empirical familiarity" — learn where they work, fail, were trained, and need guardrails.

## 12. Education: you can outsource thinking, but not understanding

- Key insight: "You can outsource your thinking, but you can't outsource your understanding."
- Even with agents doing more work, humans need understanding to direct them — knowing what's worth building, what questions matter, what results are suspicious, what tradeoffs are acceptable.
- LLM knowledge bases aren't just answer machines but "tools for transforming information into understanding."
- `microGPT` project example: an educational artifact small enough for humans and agents to inspect; the human expert contributes a distilled artifact and taste; the agent explains interactively to learners.

## The big picture

- AI is becoming "a new operating layer for digital work."
- Scarce things are shifting: less scarce are code generation, API recall, boilerplate, first drafts, repetitive setup; more scarce are understanding, taste, eval design, security, system boundaries, agent orchestration, domain feedback loops, knowing when models are off the rails.
- Founder questions: What becomes possible when the primary user is an agent for a human? What workflows rebuild around sensors, actuators, and verifiable loops? What software should disappear into direct model transformations? What domains are valuable, verifiable, and untrained? What human judgment must stay in the loop?
