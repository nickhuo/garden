<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Thesis title (declarative, opinionated)");
const confidence = await tp.system.suggester(
  ["low", "medium", "high"],
  ["low", "medium", "high"],
  false,
  "Confidence"
);
const evidence = await tp.system.suggester(
  ["thin", "moderate", "strong"],
  ["thin", "moderate", "strong"],
  false,
  "Evidence strength"
);
const domain = await tp.system.suggester(
  ["ai-agents", "llm", "productivity", "other"],
  ["ai-agents", "llm", "productivity", "other"],
  false,
  "Primary domain"
);
tR += `---
type: thesis
title: "${title}"
created: ${today}
updated: ${today}
tags:
  - ${domain}
  - thesis
status: developing
related: []
sources: []
confidence: ${confidence}
evidence_strength: ${evidence}
---

# ${title}

## Claim

<one or two declarative sentences. No hedging.>

## Why I believe this

- 

## Strongest counter-argument

<state it as steelman, not strawman>

## Evidence

- For: [[]]
- Against: [[]]

## What would change my mind

- 

## Related claims

- 
`;
%>
