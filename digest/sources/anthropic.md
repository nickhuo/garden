---
type: source
name: Anthropic
slug: anthropic
category: ai-lab
tier: 1
author: Anthropic
topics: [llm, alignment, research, claude, agents, interpretability]
language: en
status: active
added: 2026-05-03
notes: News + Research are separate sections; both worth ingesting. Research drops > product announcements for technical depth.

channels:
  - id: anthropic-blog
    medium: blog
    url: "https://www.anthropic.com/news"
    feed: "https://www.anthropic.com/rss.xml"
    feed_verified: false
    needs_scraper: false
    last_checked:
    last_post:

  - id: anthropic-engineering
    medium: blog
    url: "https://www.anthropic.com/engineering"
    feed:
    feed_verified: false
    needs_scraper: true
    last_checked:
    last_post:
    notes: Imported from zarazhangrui/follow-builders — scrape-only, no native RSS

  - id: anthropic-claude-blog
    medium: blog
    url: "https://claude.com/blog"
    feed:
    feed_verified: false
    needs_scraper: true
    last_checked:
    last_post:
    notes: Imported from zarazhangrui/follow-builders

  - id: anthropic-x
    medium: x
    url: "https://x.com/claudeai"
    handle: claudeai
    feed_verified: true
    needs_scraper: true
    last_checked:
    last_post:
    notes: Brand product account — marketing-prone, score with caution
---
**Why monitor**: First-party frontier lab. Highest career-relevance for AI Engineer track. Interpretability work is unique to Anthropic.
