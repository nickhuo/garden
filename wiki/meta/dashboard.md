---
type: meta
title: "Dashboard"
created: 2026-05-11
updated: 2026-05-13
tags:
  - meta
  - dashboard
status: evergreen
related:
  - "[[index]]"
sources: []
---

# Wiki Dashboard

Requires the [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) plugin. If queries show as raw code blocks, Dataview isn't enabled.

## Recent activity

```dataview
TABLE type, status, updated
FROM "03_Resources/wiki"
WHERE type != "meta"
SORT updated DESC
LIMIT 15
```

## Seed pages (need development)

```dataview
LIST status
FROM "03_Resources/wiki"
WHERE status = "seed"
SORT updated ASC
```

## Entities missing source citations

```dataview
LIST
FROM "03_Resources/wiki/entities"
WHERE !sources OR length(sources) = 0
```

## Concepts missing source citations (migration backlog)

```dataview
TABLE _legacy_source_count AS "legacy count", length(sources) AS "current"
FROM "03_Resources/wiki/concepts"
WHERE _legacy_source_count > 0
SORT _legacy_source_count DESC
```

## Stale mature pages

```dataview
TABLE updated
FROM "03_Resources/wiki"
WHERE status = "mature" AND updated < date(today) - dur(60 days)
SORT updated ASC
```

## Sources by author

```dataview
TABLE author, date_published, source_type
FROM "03_Resources/wiki/sources"
SORT date_published DESC
```

## Theses by confidence

```dataview
TABLE confidence, evidence_strength, status
FROM "03_Resources/wiki/theses"
SORT confidence DESC
```

## Orphan candidates (no outbound links in body — heuristic, may have false positives)

```dataview
LIST
FROM "03_Resources/wiki"
WHERE length(file.outlinks) = 0 AND type != "meta"
```
