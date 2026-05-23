---
source_url: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
pdf_url: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
fetched: 2026-05-22
---

# A Practical Guide to Building Agents (OpenAI)

> 34-page OpenAI guide for product and engineering teams building their first agents. Text extracted from the official PDF via pypdf and cleaned of layout artifacts. Code samples paraphrased; the guide uses OpenAI's Agents SDK throughout.

## What is an agent?

- "Agents are systems that independently accomplish tasks on your behalf." They perform whole **workflows** (a sequence of steps to meet a user goal) with a high degree of independence.
- Apps that integrate LLMs but don't use them to control workflow execution — simple chatbots, single-turn LLMs, sentiment classifiers — are **not** agents.
- Core characteristics:
  1. **Leverages an LLM to manage workflow execution and make decisions.** It recognizes when a workflow is complete and can proactively correct its actions; on failure it can halt and transfer control back to the user.
  2. **Has access to various tools** to interact with external systems (to gather context and take actions), dynamically selecting the appropriate tools depending on the workflow's current state, always operating within clearly defined guardrails.

## When should you build an agent?

Agents suit workflows where traditional deterministic / rule-based approaches fall short. Example: payment fraud — a rules engine is a checklist; an LLM agent is "a seasoned investigator" evaluating context and subtle patterns. Prioritize workflows that have resisted automation:

1. **Complex decision-making** — nuanced judgment, exceptions, context-sensitive decisions (e.g. refund approval in customer service).
2. **Difficult-to-maintain rules** — systems made unwieldy by extensive, intricate rulesets (e.g. vendor security reviews).
3. **Heavy reliance on unstructured data** — interpreting natural language, extracting meaning from documents, conversational interaction (e.g. processing a home insurance claim).

Validate the use case meets these criteria; otherwise a deterministic solution may suffice.

## Agent design foundations

An agent has three core components:
1. **Model** — the LLM powering reasoning and decision-making.
2. **Tools** — external functions or APIs the agent can use to take action.
3. **Instructions** — explicit guidelines and guardrails defining how the agent behaves.

### Selecting your models

- Not every task needs the smartest model; a simple retrieval or intent-classification task may use a smaller, faster model, while harder tasks (approve a refund) benefit from a more capable model.
- Recommended approach: prototype with the **most capable model for every task** to establish a baseline, then **swap in smaller models** to see if they still hit acceptable results.
- Principles: (1) set up evals to establish a performance baseline; (2) focus on meeting your accuracy target with the best models available; (3) optimize for cost and latency by replacing larger models with smaller ones where possible.

### Defining tools

- Tools extend capabilities via APIs of underlying systems. For legacy systems without APIs, agents can use **computer-use models** to interact through web/application UIs as a human would.
- Each tool should have a **standardized definition**, enabling flexible many-to-many relationships between tools and agents. Well-documented, tested, reusable tools improve discoverability and version management.
- Three types of tools:
  - **Data** — retrieve context/information needed to execute the workflow (query transaction databases or CRMs, read PDFs, search the web).
  - **Action** — interact with systems to take actions (send emails/texts, update a CRM record, hand off a ticket to a human).
  - **Orchestration** — agents themselves can serve as tools for other agents (see the Manager pattern). Examples: refund agent, research agent, writing agent.
- As required tools increase, consider splitting tasks across multiple agents.

### Configuring instructions

Best practices:
- **Use existing documents** — derive routines from existing SOPs, support scripts, or policy docs (in customer service, routines map roughly to knowledge-base articles).
- **Prompt agents to break down tasks** — provide smaller, clearer steps from dense resources.
- **Define clear actions** — every step should correspond to a specific action or output.
- **Capture edge cases** — anticipate incomplete information or unexpected questions with conditional steps/branches.
- You can use advanced models (o1, o3-mini) to auto-generate instructions from existing documents (sample prompt: convert a help-center doc into a numbered, unambiguous instruction list for an LLM agent).

## Orchestration

Customers typically succeed with an **incremental approach** rather than immediately building a fully autonomous, complex architecture. Two categories:
1. **Single-agent systems** — one model with appropriate tools and instructions executes workflows in a loop.
2. **Multi-agent systems** — workflow execution distributed across multiple coordinated agents.

### Single-agent systems

- A single agent handles many tasks by incrementally adding tools, keeping complexity manageable.
- Every orchestration approach needs the concept of a **"run"** — typically a loop that runs until an exit condition. Common exit conditions: tool calls, a certain structured output, errors, or reaching a maximum number of turns.
- In the Agents SDK, `Runner.run()` loops over the LLM until either (1) a **final-output tool** is invoked (defined by a specific output type), or (2) the model returns a response without any tool calls (e.g. a direct user message). "This concept of a while loop is central to the functioning of an agent."
- **Prompt templates** manage complexity without going multi-agent: a single flexible base prompt that accepts policy variables, instead of many individual prompts.

### When to consider multiple agents

- General recommendation: **maximize a single agent's capabilities first.** More agents give intuitive separation but add complexity/overhead.
- Split when agents fail to follow complicated instructions or consistently select wrong tools. Guidelines:
  - **Complex logic** — prompts with many conditional branches (if-then-else) that get hard to scale → divide each logical segment across separate agents.
  - **Tool overload** — the issue is tool **similarity/overlap**, not just count. "Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools." Split if improving tool clarity (names, params, descriptions) doesn't help.

### Multi-agent systems — two patterns

- **Manager (agents as tools)** — a central "manager" agent coordinates specialized agents via **tool calls**, each handling a specific task/domain; the manager synthesizes results into a cohesive interaction. Ideal when you want one agent to control execution and have access to the user. (Modeled as a graph; edges = tool calls.)
- **Decentralized (agents handing off to agents)** — multiple agents operate as **peers**, handing off tasks based on specialization. A **handoff** is a one-way transfer (in the Agents SDK, a handoff is a type of tool/function); calling it immediately starts execution on the new agent and transfers conversation state. Optimal when you don't need a single agent maintaining central control/synthesis (e.g. conversation triage). (Edges = handoffs.) Example: a `triage_agent` with `handoffs=[technical_support, sales, order_management]`.

### Declarative vs non-declarative graphs

- **Declarative** frameworks require defining every branch, loop, and conditional upfront as a graph of nodes (agents) and edges (deterministic/dynamic handoffs). Good for visual clarity but becomes cumbersome as workflows grow dynamic/complex, often requiring a domain-specific language.
- The Agents SDK adopts a **code-first** approach: express workflow logic with familiar programming constructs without pre-defining the entire graph, enabling more dynamic, adaptable orchestration.

## Guardrails

- Guardrails manage data-privacy risks (e.g. preventing system-prompt leaks) and reputational risks (e.g. brand-aligned behavior). They should be **layered** with robust authn/authz, strict access controls, and standard software-security measures.
- Think of guardrails as a **layered defense mechanism** — combine LLM-based guardrails, rules-based guardrails (regex), and the OpenAI moderation API.

### Types of guardrails

- **Relevance classifier** — flags off-topic queries (e.g. "How tall is the Empire State Building?").
- **Safety classifier** — detects unsafe inputs (jailbreaks, prompt injections) attempting to exploit vulnerabilities.
- **PII filter** — vets model output for personally identifiable information.
- **Moderation** — flags harmful/inappropriate inputs (hate speech, harassment, violence).
- **Tool safeguards** — assign each tool a risk rating (low/medium/high) based on read-only vs write, reversibility, required permissions, financial impact; use ratings to trigger automated actions (pause for checks before high-risk functions, escalate to a human).
- **Rules-based protections** — blocklists, input length limits, regex filters (e.g. prevent SQL injection).
- **Output validation** — ensure responses align with brand values via prompt engineering and content checks.

### Building guardrails

Heuristic: (1) focus first on data privacy and content safety; (2) add new guardrails based on real-world edge cases and failures encountered; (3) optimize for both security and user experience.

The Agents SDK treats guardrails as **first-class** concepts, relying on **optimistic execution** by default: the primary agent generates outputs while guardrails run concurrently, raising exceptions (tripwires) if constraints are breached.

### Plan for human intervention

Human intervention is a critical safeguard, especially early in deployment (identify failures, uncover edge cases, build a robust eval cycle). It lets the agent gracefully transfer control when it can't complete a task (customer service: escalate to a human; coding agent: hand control back to the user). Two primary triggers:
- **Exceeding failure thresholds** — limits on retries or actions; escalate if exceeded (e.g. fails to understand intent after multiple attempts).
- **High-risk actions** — sensitive, irreversible, or high-stakes actions trigger human oversight until confidence grows (cancel orders, authorize large refunds, make payments).

## Conclusion

Start with strong foundations (capable models + well-defined tools + clear structured instructions). Use orchestration patterns that match your complexity level — start with a single agent, evolve to multi-agent only when needed. Guardrails are critical at every stage, from input filtering and tool use to human-in-the-loop. "The path to successful deployment isn't all-or-nothing. Start small, validate with real users, and grow capabilities over time."
