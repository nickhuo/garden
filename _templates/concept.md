<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Concept name");
const domain = await tp.system.suggester(
  ["ai-agents", "llm", "productivity", "other"],
  ["ai-agents", "llm", "productivity", "other"],
  false,
  "Primary domain"
);
const tags = await tp.system.prompt("Additional tags (comma-separated, no spaces)", "");
const allTags = [domain].concat(tags.split(",").map(t => t.trim()).filter(t => t));
const tagList = allTags.map(t => `\n  - ${t}`).join("");
tR += `---
type: concept
title: "${title}"
created: ${today}
updated: ${today}
tags:${tagList}
status: seed
related: []
sources: []
---

# ${title}

## Summary

<one paragraph definition in your own words>

## Key points

- 

## Evidence

- 

## Connections

- Related to: [[]]
- Contrasts with: [[]]
- Examples: [[]]

## Open questions

- 
`;
%>
