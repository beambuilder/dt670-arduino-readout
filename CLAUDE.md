# CLAUDE.md

Lean router. Knowledge lives in `memory/`, not here.

## Session protocol

**Start (every session):**
1. Read `memory/index.md` and `memory/current-task.md`.
2. Read only the topic pages relevant to today's task — not the whole KB.

**During:**
- Before non-trivial work, write the plan to `raw/plans/<YYYY-MM-DD>-<task>.md` so compaction or `/clear` cannot destroy it.
- When a quirk/trap is discovered, record it immediately on the relevant page — do not wait for session end.

**End (before `/clear` or quitting):** run the **kb-checkpoint** skill.

## Rules

- `memory/` is the source of truth for cross-session knowledge. Sub-repos with their own CLAUDE.md keep repo-specific conventions there — never duplicate them into the KB (duplicates go stale).
- `memory/log.md` is append-only. ADRs are immutable once Accepted — supersede with a new ADR, never edit in place. Every gotcha carries a status tag (`OPEN` / `RESOLVED (YYYY-MM-DD)` / `ANTICIPATED`).
- Link pages with `[[wikilinks]]` (page name, no path/extension).
- Convert relative dates ("today", "last week") to absolute before persisting.
- Retrieval: `memory/index.md` + links first; if that misses, grep `memory/` as the second path.
- Subagents report findings back to the main session; **only the main session writes to `memory/`**.
- The human curates `raw/` (immutable sources — never edit); Claude maintains `memory/`.

## Operations

- **kb-checkpoint** — session-end write-back: update current-task, file findings/gotchas, ADRs, session note, log entry, stage with git.
- **kb-query** — answer "what did we decide / did we already solve X" from the KB with citations.
- **kb-ingest** — file a new source dropped into `raw/` into the KB.
- **kb-lint** — KB health audit (stale claims, orphans, broken links, missing status tags).

Start here: read `memory/index.md`, then `memory/current-task.md`.
