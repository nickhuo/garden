<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Short title for the question (filename)");
const question = await tp.system.prompt("The full question");
const quality = await tp.system.suggester(
  ["draft", "solid", "definitive"],
  ["draft", "solid", "definitive"],
  false,
  "Answer quality"
);
const domain = await tp.system.suggester(
  ["ai-agents", "llm", "productivity", "other"],
  ["ai-agents", "llm", "productivity", "other"],
  false,
  "Primary domain"
);
tR += `---
type: question
title: "${title}"
created: ${today}
updated: ${today}
tags:
  - ${domain}
  - question
status: developing
related: []
sources: []
question: "${question}"
answer_quality: ${quality}
---

# ${title}

## Question

${question}

## Answer

<synthesis, cite wikilinks>

## Evidence

- 

## Caveats / unknowns

- 

## Related

- 
`;
%>
