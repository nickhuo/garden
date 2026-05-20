<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Entity name");
const entityType = await tp.system.suggester(
  ["person", "organization", "product", "repository", "framework", "place"],
  ["person", "organization", "product", "repository", "framework", "place"],
  false,
  "Entity type"
);
const role = await tp.system.prompt("Role / one-line description");
const firstSource = await tp.system.prompt("First mentioned in (source wikilink, optional)", "");
const domain = await tp.system.suggester(
  ["ai-agents", "llm", "productivity", "other"],
  ["ai-agents", "llm", "productivity", "other"],
  false,
  "Primary domain"
);
tR += `---
type: entity
title: "${title}"
created: ${today}
updated: ${today}
tags:
  - ${domain}
  - entity
status: seed
related: []
sources: []
entity_type: ${entityType}
role: "${role}"
first_mentioned: "${firstSource}"
---

# ${title}

## Summary

<one paragraph>

## What it is

- 

## Why it matters

- 

## Notable claims / artifacts

- 

## Connections

- 
`;
%>
