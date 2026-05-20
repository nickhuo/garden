# 03_Resources — LLM Wiki

Mode: D (Personal / Second Brain), with research-mode (E) practices for source-heavy domains.
Purpose: persistent, compounding knowledge base for Nick — AI Agents, LLMs, and future topics.
Owner: Nick
Created: 2026-05-10 (migrated from prior AI-Agents sub-wiki schema)

This file overrides the root `Core/CLAUDE.md` for everything inside `03_Resources/`.

## Vault root vs project root (READ THIS)

**Vault root = `brain/`** (one level above `03_Resources/`). **Project root = `03_Resources/`** (where this CLAUDE.md lives).

- Filesystem operations from Claude Code skills are **project-relative**: `wiki/sources/X.md` resolves to `03_Resources/wiki/sources/X.md`.
- Obsidian-level features (Dataview `FROM`, CSS `data-path^=`, wikilinks with paths, REST API calls) are **vault-relative**: must use `03_Resources/wiki/...` and `03_Resources/.raw/...` prefixes.
- The `.obsidian/` config Obsidian actually reads is at `brain/.obsidian/`, not `03_Resources/.obsidian/`. The latter is dead weight (kept as a template).
- To activate the CSS snippet, copy it: `cp 03_Resources/.obsidian/snippets/vault-colors.css ../.obsidian/snippets/vault-colors.css` (from inside `brain/`).

## Structure

```
03_Resources/
├── WIKI.md            (schema reference — read first if plugin not installed)
├── CLAUDE.md          (this file — vault-specific deltas)
├── README.md          (PARA explanation, legacy context)
├── .raw/              (immutable source documents)
│   └── articles/
└── wiki/              (LLM-generated knowledge base)
    ├── index.md, log.md, hot.md, overview.md
    ├── sources/, entities/, concepts/, domains/
    ├── theses/        (extension: Nick's evolving views)
    ├── comparisons/, questions/, meta/
```

## Plugin

This vault is designed for the `claude-obsidian` plugin (github.com/AgriciDaniel/claude-obsidian). If installed, its skills handle ingest/query/lint/save/autoresearch automatically. If not installed, follow `WIKI.md` directly.

**Install (run in Claude Code CLI on Nick's machine):**

```
claude plugin marketplace add AgriciDaniel/claude-obsidian
```

The 11 skills it ships: `wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-fold`, `save`, `autoresearch`, `canvas`, `defuddle`, `obsidian-markdown`, `obsidian-bases`.

Slash commands: `/wiki`, `/save`, `/autoresearch`.

**Note on overlap:** Nick already has `kepano/obsidian-skills` installed (`obsidian-bases`, `obsidian-markdown`, `defuddle`, `obsidian-cli`, `json-canvas`). The claude-obsidian skills overlap on 3-4 of these. Different skill IDs (`obsidian:defuddle` vs `defuddle`), so no actual collision is expected, but the wiki-specific skills (`wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-fold`, `save`, `autoresearch`) are the high-value additions.

## Conventions

All notes use flat YAML frontmatter: `type`, `title`, `created`, `updated`, `tags`, `status` (seed|developing|mature|evergreen), `related`, `sources`. See `WIKI.md` Section "Frontmatter Schema" for type-specific fields.

Wikilinks use `[[Note Name]]` — filenames are vault-unique so paths aren't needed.

`.raw/` contains source documents — never modify them.

`wiki/index.md` is the master catalog — update on every ingest.

`wiki/log.md` is append-only — **new entries go at the TOP**, never edit past entries.

## Operations

- **Ingest:** drop source in `.raw/`, say "ingest [filename]" or "ingest [URL]"
- **Query:** ask any question — read `hot.md` → `index.md` → 3-5 relevant pages, then synthesize
- **Lint:** say "lint the wiki" for a health check report
- **Save:** say "save this" mid-chat to file the conversation as a source
- **Autoresearch:** say "research [topic]" — confirms scope, then runs paused rounds

See `WIKI.md` for full operation definitions and anti-patterns.

## Vault-specific deltas

### Topic boundaries

The wiki spans multiple topics, distinguished by tag and `wiki/domains/<Name>.md`. Currently:

- **ai-agents** — agentic systems, tool use, orchestration, MCPs, context engineering. 27 concepts, 3 entities, 7 sources, 2 theses migrated 2026-05-10 from prior AI-Agents folder.
- **llm** — model internals, training, inference, evaluation, alignment (Karpathy-centric seed). Not yet populated.

When ingesting, tag pages with the primary domain. A page can belong to multiple domains (e.g., `tags: [ai-agents, llm]` for training-time tool use). If a claim spans domains substantively, file it in the primary domain and create a `comparisons/` page if synthesis warrants.

### Thesis pages

Schema extension: `wiki/theses/` holds Nick's evolving opinions/views. Distinct from `comparisons/` (which compares external positions) and `questions/` (which files answered queries). Frontmatter: `type: thesis`, plus `confidence` (low|medium|high) and `evidence_strength` (thin|moderate|strong).

### Migration backlog (2026-05-10)

The migration from the prior AI-Agents schema set `sources: []` placeholders on migrated concept/entity/thesis pages. The original count (`sources: 6`, etc.) is preserved as `_legacy_source_count` for audit. **Next lint pass should backfill `sources` lists** by parsing each page's body for `[[wikilink]]` references to source pages and `.raw/articles/`.

### Anti-patterns specific to this vault

In addition to those in `WIKI.md`:

- Don't create a new `domains/<Topic>.md` until at least 5 pages cite that topic in `tags:`. Until then, the topic lives as a tag only.
- Don't promote a thesis (`wiki/theses/`) until it cites ≥2 sources. Drafts go in chat scratch, not the wiki.

## Reference

- Plugin: https://github.com/AgriciDaniel/claude-obsidian
- WIKI.md (this vault): schema reference
- Karpathy's gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Migration backup: `outputs/03_Resources-backup-20260511-045630.tar.gz` (if you need to revert)
