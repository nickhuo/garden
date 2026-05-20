<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Comparison title (e.g., 'X vs Y' or 'A approaches to B')");
const subjects = await tp.system.prompt("Subjects being compared (wikilinks, comma-separated)");
const dimensions = await tp.system.prompt("Dimensions of comparison (comma-separated)");
const subjectList = subjects.split(",").map(s => `\n  - "${s.trim()}"`).join("");
const dimList = dimensions.split(",").map(d => `\n  - ${d.trim()}`).join("");
const domain = await tp.system.suggester(
  ["ai-agents", "llm", "productivity", "other"],
  ["ai-agents", "llm", "productivity", "other"],
  false,
  "Primary domain"
);
tR += `---
type: comparison
title: "${title}"
created: ${today}
updated: ${today}
tags:
  - ${domain}
  - comparison
status: developing
related: []
sources: []
subjects:${subjectList}
dimensions:${dimList}
verdict: "<one-line verdict>"
---

# ${title}

## Verdict

<one line: who wins, under what conditions>

## Subjects

- 

## Comparison table

| Dimension | Subject A | Subject B |
| --- | --- | --- |
|  |  |  |

## When each wins

- Subject A wins when: 
- Subject B wins when: 

## Open questions

- 
`;
%>
