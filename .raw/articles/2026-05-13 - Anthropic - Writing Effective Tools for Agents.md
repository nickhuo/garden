---
source_url: https://www.anthropic.com/engineering/writing-tools-for-agents
title: "Writing effective tools for agents — with agents"
author: Anthropic Engineering
date_fetched: 2026-05-13
---

# Writing effective tools for agents — with agents

*Source: https://www.anthropic.com/engineering/writing-tools-for-agents*

---

Tool quality is one of the most important levers for improving agent performance, but writing good tool definitions is hard. This post shares what we've learned about making tools work well for agents, and introduces a workflow where agents help write and improve their own tools.

## Why tool quality matters so much

When Claude uses a tool, everything it knows about that tool comes from the tool definition: the name, description, and parameter schema. If those are ambiguous, incomplete, or misleading, the agent will use the tool incorrectly even if the underlying API is perfect.

We've found that tool definitions are often the highest-leverage place to improve agent performance — often more impactful than prompt tuning. In our SWE-bench work, for example, we spent more time optimizing our tools than the overall prompt.

This is the core insight behind the Agent-Computer Interface (ACI) framing: just as software is unusable without a good user interface, tools are unusable without a good agent interface.

## What makes a tool definition good

### Names should be unambiguous and action-oriented

Tool names are the first signal Claude uses to decide whether a tool is relevant. Good names:
- Are verb-first: `search_files`, `create_ticket`, `get_user_by_email`
- Convey the action and object clearly
- Avoid abbreviations that aren't universally understood
- Are distinguishable from each other — similar tools should have clearly different names

### Descriptions should answer "when should I use this?"

The description is the most important field. Claude reads it to decide whether to call the tool at all. Good descriptions:
- Start with one sentence explaining what the tool does
- Explain when to use it (and when NOT to use it)
- Clarify the relationship to similar tools
- Mention important constraints (rate limits, side effects, required permissions)

Bad description: `"Search for things."`
Good description: `"Full-text search across all documents in the workspace. Use this when you need to find documents by content. Do NOT use this to look up a specific document by ID — use get_document instead. Returns up to 20 results sorted by relevance."`

### Schemas should prevent misuse

JSON Schema is expressive but often underused. Beyond marking fields as required vs optional:
- Use `enum` to constrain string fields to valid values
- Add `description` on every field, not just the tool level
- Use `minimum`/`maximum`/`maxLength` to communicate valid ranges
- Structure nested objects to make relationships clear

### Examples teach what schemas can't express

Some things are hard to express in JSON Schema: date formats, ID conventions, which optional fields go together. This is where `input_examples` matter. Providing 1-5 realistic examples of complete tool calls teaches Claude the conventions through demonstration.

### Error messages should guide recovery

When tools fail, the error message is the agent's main signal for what to do next. Good errors:
- Say what went wrong specifically
- Suggest what to try instead
- Include relevant context (what value was passed, what was expected)

Bad error: `"Invalid input"`
Good error: `"Invalid date format: '2024-11-6'. Expected YYYY-MM-DD (e.g., '2024-11-06')."`

## Using agents to improve tool definitions

Writing good tool definitions is a skill, but it's also learnable work that doesn't require human intuition. We've found that Claude can effectively critique and improve tool definitions when given the right context.

### The tool-critique workflow

The basic pattern:

1. Show Claude your current tool definitions
2. Ask it to identify ambiguities, missing documentation, or misuse risks
3. Have it propose improvements
4. (Optionally) have it generate test cases to validate the improved definitions

This works because the task is well-specified: Claude knows what makes a good tool definition (from its training on tool-calling patterns and API documentation), and the evaluation criterion is clear (an agent should be able to use this tool correctly without additional context).

### Generating test cases with agents

Beyond critiquing definitions, Claude can generate test cases that reveal edge cases in tool design:

1. Give Claude the tool definition
2. Ask it to generate a diverse set of inputs, including edge cases
3. Run those inputs through your validation layer
4. Gaps where inputs fail reveal places where the schema or docs are underspecified

This creates a tight feedback loop: agents surface ambiguities that humans miss because we have too much implicit context about how a tool "should" be used.

### The meta-tooling pattern

For mature tool surfaces, you can go further: build a **tool-quality agent** that:
1. Takes a tool definition as input
2. Generates test invocations
3. Evaluates whether a fresh Claude instance uses the tool correctly given only the definition
4. Proposes targeted improvements

This is a form of self-improvement: the agent participates in improving its own tools. We've found this loop converges quickly — most tool definitions need 1-2 rounds of agent critique to reach acceptable quality.

## Common failure modes

### The "obvious to humans" failure

Humans write tool docs assuming the reader shares their context. Claude doesn't. If a tool expects a user ID in the format `USR-XXXXX` and the description says "the user's ID," Claude will guess the format — sometimes correctly, sometimes not. Make implicit conventions explicit.

### The "too many similar tools" failure

When multiple tools do similar things, Claude spends tokens deciding between them instead of using them. The fix is often to consolidate tools or to make the selection criterion crystal clear in each tool's description.

### The "success is silent" failure

Tools often return nothing (or a generic `{"status": "success"}`) when they succeed, and an error message when they fail. Agents need to know that the action completed. Return enough confirmation that the agent can verify success without a follow-up call.

### The "hallucinated parameters" failure

When Claude is uncertain about a required parameter's value, it may hallucinate a plausible-sounding value rather than asking. Preventions:
- Make optional fields actually optional in the schema (agents fill in required fields even when they shouldn't)
- Add examples that show what correct values look like
- Design tools to validate inputs and return actionable errors when values are implausible

## Practical starting points

If you're building tools for agents today:

1. **Start with descriptions.** A well-written description is worth more than a perfect schema. Write as if explaining to a capable junior engineer who has no context.

2. **Add field-level descriptions.** Every parameter should have a `description` in the schema, not just the tool itself.

3. **Add 2-3 examples.** Cover the most common use case, one edge case, and the minimal valid invocation. Use realistic data.

4. **Run your tools through Claude.** Give Claude only the tool definition (no additional context) and see if it can use the tool correctly. This quickly reveals what's missing.

5. **Treat errors as part of the interface.** Design your error messages before your success cases. Agents fail forward.

## Conclusion

Good tools are the foundation of reliable agents. The investment in tool quality pays compound returns: every improvement in a tool definition improves every future agent session that uses it. Using agents to critique and improve tool definitions closes the loop — you get expert tool users telling you where your tools fall short.

The ACI framing helps: every tool is an interface for an agent, and interfaces deserve the same rigorous design discipline we apply to human-facing APIs.
