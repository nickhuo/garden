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

- **Ingest:** drop source in `.raw/`, say "ingest [filename]" or "ingest [URL]". Every source passes the **seed gate** (`_rubrics/source-quality.md`) first, then a **one-hop citation chase** — see Vault-specific deltas → Source-Quality Gate & Citation Lineage.
- **Query:** ask any question — read `hot.md` → `index.md` → 3-5 relevant pages, then synthesize
- **Lint:** say "lint the wiki" for a health check report
- **Save:** say "save this" mid-chat to file the conversation as a source
- **Autoresearch:** say "research [topic]". Confirms scope, then runs paused rounds (pause after each round per `WIKI.md`). Every candidate source passes the **seed gate** before filing, and core sources get the **one-hop citation chase** (see Vault-specific deltas). **Always runs on a dedicated `research/<topic-slug>` branch — never commit autoresearch output directly to `main`.** On completion, auto-finalize without asking: commit the new/updated pages on the branch, push the branch, and open a PR to `main` with `gh pr create`, then report the PR link for Nick to review. **Do not merge — Nick reviews and merges.** PR title `Autoresearch: <Topic>`; body summarizes rounds, pages created, key findings, and open questions (mirror the skill's completion report). This auto-push of the `research/*` branch is the one sanctioned exception to the global "confirm before pushing" rule; `main` is still never pushed by autoresearch. Per Nick's global rule, **do not add a Claude co-author/attribution line** to the PR.

See `WIKI.md` for full operation definitions and anti-patterns.

## gbrain (semantic + knowledge-graph layer)

This repo is also indexed by **gbrain** (`github.com/garrytan/gbrain`) — a semantic-search +
typed-link/timeline knowledge graph that sits **on top of** the wiki. It is **non-destructive and
additive**: gbrain imports the markdown into a **separate PGLite database at `~/.gbrain/`** (outside
this repo, never committed) and never rewrites wiki files. The PARA + llm-wiki schema is unchanged —
gbrain does **not** require its own `people/companies/concepts/` layout.

- **Access:** query via the **`gbrain` MCP server** (stdio, registered at user scope → available in
  every Claude session). Tools cover hybrid/keyword search, page reads, `backlinks`, `graph`, and
  `timeline`. CLI equivalents: `gbrain query "…"`, `gbrain search "…"`, `gbrain graph <slug>`.
- **Read-path discipline:** the curated path (`hot.md` → `index.md` → 3–5 pages) stays **primary**
  for deliberate, high-signal context. Reach for the gbrain MCP for **fuzzy / semantic / cross-page
  retrieval** and **graph traversal** the curated path can't cheaply answer. They complement, not
  replace, each other (and Obsidian's own link graph).
- **Scope:** indexes **`wiki/` + `.raw/`** only (not `digest/`, `portfolio/`, `Fundraising/`).
- **Reindex cadence:** after every **ingest** (or any non-trivial wiki edit), reindex with the
  **Reindex command** below — **`gbrain import`, not `gbrain sync`**. Search mode is **`balanced`**
  (12K budget, ≤25 chunks, no LLM expansion).
- **Embeddings:** provider is **ZeroEntropy** (`zeroentropyai:zembed-1`, 2560-d). Key lives in
  `~/.zshrc` as `ZEROENTROPY_API_KEY`. ⚠️ The embedding model **sizes the PGLite schema at `init`
  time** — switching providers/dimensions later requires `gbrain init --pglite --embedding-model …`
  (which **wipes + re-imports**), not `config set`.
- **Don't:** run `gbrain skillpack scaffold` into this repo (it would collide with the existing
  llm-wiki / claude-obsidian / gstack skills), and don't restructure the wiki to gbrain's schema.

**Reindex command (the "reindex-after" step).** gbrain's `sync` is **git-based and only accepts a
git-repo-root path** — pointing it at `03_Resources` pulls in `digest/`, `portfolio/`,
`Fundraising/` (out of scope; and `digest/`'s bare `slug:` frontmatter trips `SLUG_MISMATCH` and
blocks the whole sync), while pointing it at `wiki/` fails (`wiki/` is not a git root). So **do not
use `gbrain sync` in this vault.** Reindex with path-scoped, git-free, incremental `import`:

```bash
gbrain import /Users/nickhuo/Core/brain/03_Resources/wiki  --no-embed && \
gbrain import /Users/nickhuo/Core/brain/03_Resources/.raw  --no-embed && \
gbrain embed --stale
```

`import` skips unchanged files (content-hash) and `embed --stale` only embeds new/changed chunks, so
this is cheap to re-run after every ingest. Needs `ZEROENTROPY_API_KEY` (already in `~/.zshrc`). All
pages live in the single `default` source (named/sub-dir sources don't work — `sync` needs a git
root, `import` only targets `default`).

⚠️ **MCP freshness gap.** PGLite is single-process: the long-running `gbrain serve` (MCP) caches its
DB view at session start, so a CLI `import` reindex is **not visible to the MCP `query` tool until
the Claude session restarts** (the CLI's own `gbrain query` sees it immediately). After an ingest,
either (a) trust the reindex + restart the session before relying on MCP retrieval, or (b) verify
via CLI `gbrain query`. The write always lands correctly on disk; only the live MCP view lags.

**MCP registration (load-bearing flag).** Register at user scope with **`GBRAIN_NO_UPDATE_CHECK=1`**:

```bash
claude mcp add gbrain --scope user \
  -e ZEROENTROPY_API_KEY=ze_… \
  -e GBRAIN_NO_UPDATE_CHECK=1 \
  -- /Users/nickhuo/.bun/bin/gbrain serve
```

⚠️ Without `GBRAIN_NO_UPDATE_CHECK=1`, `gbrain serve` hangs ~30s on a startup update-check and
Claude Code marks the server **"✗ Failed to connect"** (the 85 tools never load). Do **not**
substitute `GBRAIN_OFFLINE=1` — it also blocks the ZeroEntropy embedding calls that query-time
search depends on. After registering, **restart the Claude session** so the tools load.

### Orchestration with claude-obsidian operations

Two contracts bind gbrain into the plugin skills (`wiki-ingest`, `wiki-query`, `wiki-lint`,
`save`, `autoresearch`). Like the Source-Quality Gate, **this overrides the plugin skills** where
they differ.

**The two contracts:**
1. **Query-first** — before any read/judgement step, run `gbrain query` to locate relevant pages,
   then read them. Don't rely on guessing pages from `index.md`.
2. **Reindex-after** — after any write to `wiki/` (ingest, save, autoresearch round, page edit), run
   the **Reindex command** above (`gbrain import …` + `embed --stale`, **not** `gbrain sync`). The
   index must never drift from the wiki.

**Per operation:**
- **wiki-query** — `hot.md` (recency) → **`gbrain query`** (retrieval over all chunks) → read the
  top-N real pages → synthesize with citations. gbrain replaces the "guess 3–5 pages" step.
- **wiki-ingest** — *before writing*: `gbrain query` the source's main claims for a **collision
  check** (already covered? update vs. create? contradicts an existing thesis?). *After writing*:
  the **Reindex command**. This runs **after** the seed gate + citation chase, not instead.
- **autoresearch** — *before searching*: `gbrain query` "what do we already know" to focus scope.
  *After each round's pages* (on the `research/*` branch): the **Reindex command**.
- **save** — after filing the conversation: the **Reindex command**.
- **wiki-lint** — run gbrain's `doctor`, `orphans --json`, `lint` as an extra **data-layer** pass
  alongside the plugin's wikilink-semantic checks.

**Overlap / ownership (so the two systems don't double-work or fight):**
- **Retrieval vs. synthesis** — gbrain owns *retrieval* (which pages are relevant); the wiki flow
  owns *synthesis* (reading + writing the cited answer).
- **lint** — wikilink-semantic health (orphans, dead links, missing backlinks) stays with the
  plugin + Obsidian (they understand `[[wikilinks]]`); gbrain's `lint`/`doctor` only adds data-layer
  checks (stale embeddings, frontmatter parse, placeholder text).
- **link graph** — the `[[wikilink]]` graph belongs to Obsidian; gbrain's mention-graph is
  supplementary. **Never** let gbrain edit wiki files to add backlinks (`check-backlinks fix` writes
  files — forbidden: Nick doesn't hand-edit, gbrain doesn't touch content).

Install / re-init mechanics live in the gstack **`setup-gbrain`** skill. (The gstack `sync-gbrain`
skill is for code repos and does **not** apply here — use the **Reindex command** instead.)

## Vault-specific deltas

### Source-Quality Gate & Citation Lineage

**Binding for both Ingest and Autoresearch.** This overrides the plugin skills and `program.md`'s confidence/source-preference rules wherever they differ. The rubric itself lives in `_rubrics/source-quality.md` (Nick-editable); this section defines how it is applied.

**The gate (runs before any source page is written):**

1. Score the candidate against `_rubrics/source-quality.md`.
2. **Pass** → file the source page. Record `seed_score` (e.g. `12/14`) and set `confidence` per the rubric's score→confidence mapping. Then run the citation chase below.
3. **Fail** → **do not file.** Report a compact card: total score, per-dimension breakdown, the specific reasons it fell short, and concrete suggestions (e.g. "this is secondary — its primary source appears to be X; want me to chase/ingest that instead?"). Then ask whether to override. File only on explicit override, and when overridden, set `confidence: low` and add a `> [!gap]` quality-caveat callout to the page body.

In **autoresearch**, the gate runs on every candidate the search surfaces — only gate-passing sources are filed; rejected candidates are reported with reasons.

**One-hop citation chase (after a source qualifies):**

1. Extract the external sources the qualified source cites (links, references, "via", named papers/posts).
2. De-dupe against `wiki/index.md` and `.raw/.manifest.json` — don't re-fetch what's already in the wiki.
3. Fetch each candidate (WebFetch; `defuddle` if available) and run the **same gate** on it.
4. Each upstream source that **passes** → save to `.raw/` and build a full `wiki/sources/` page with the normal ingest treatment (entities, concepts, index, hot, log — and DragonScale address if enabled).
5. Upstream sources that **fail** → do **not** build a page; list them in the parent's lineage section as "cited but below bar (reason)".
6. **Stop at one hop.** Never chase the citations of the chased sources — no recursion.
7. Cross-link: the parent page gets a `cited_sources:` frontmatter list of `"[[Upstream Source]]"` wikilinks plus a `## Lineage / 引用脉络` body section summarizing each upstream source and what it contributes; each child page notes it was reached via the parent.

**Interaction with existing limits/mechanisms:**

- Autoresearch's `max pages` budget (default 15, `program.md`) still binds; citation-chase pages count toward it. When the budget is hit, prefer the parent plus the highest-scoring upstream sources; list the rest under Open Questions.
- The DragonScale single-writer address-allocation rule still holds — the chase runs inline, never via parallel sub-agents.

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
