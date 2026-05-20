<%*
const today = tp.date.now("YYYY-MM-DD");
const title = await tp.system.prompt("Source title (without date prefix)");
const author = await tp.system.prompt("Author or org");
const sourceType = await tp.system.suggester(
  ["blog", "paper", "repo", "talk", "thread", "podcast", "chat"],
  ["blog", "paper", "repo", "talk", "thread", "podcast", "chat"],
  false,
  "Source type"
);
const url = await tp.system.prompt("Source URL");
const datePub = await tp.system.prompt("Date published (YYYY-MM-DD)", today);
const tags = await tp.system.prompt("Tags (comma-separated)", "ai-agents");
const tagList = tags.split(",").map(t => `\n  - ${t.trim()}`).join("");
tR += `---
type: source
title: "${title}"
created: ${today}
updated: ${today}
tags:${tagList}
status: developing
related: []
sources:
  - "[[.raw/articles/${datePub} - ${author} - ${title}.md]]"
source_type: ${sourceType}
author: "${author}"
date_published: ${datePub}
url: ${url}
confidence: medium
key_claims: []
---

# ${title}

## Summary

<one paragraph>

## Key claims

- <claim 1>
- <claim 2>

## Notes

<your synthesis, your words>

## Connections

- Related to: [[]]
- Cited by: [[]]

## Open questions

- 
`;
%>
