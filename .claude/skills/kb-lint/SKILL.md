---
name: kb-lint
description: Health audit of the memory/ knowledge base — stale claims, orphan pages, broken wikilinks, untagged gotchas, dead file references, outdated current-task. Use when the user says "lint the KB", "audit memory", "is the KB healthy", or roughly monthly when no lint appears in recent log.md entries.
---

# kb-lint

## When to use

- On request ("lint the KB", "audit memory").
- Roughly monthly — check `memory/log.md` for the last lint entry.

## Checks

- Stale claims contradicting current code.
- Orphan pages missing from `memory/index.md`.
- Broken `[[wikilinks]]` (target page does not exist).
- Gotchas without status tags (`OPEN` / `RESOLVED (YYYY-MM-DD)` / `ANTICIPATED`).
- References to files/paths that no longer exist.
- Outdated `current-task.md` (next step already done or no longer executable).
- Content duplicated from repo CLAUDE.md files.
- Persisted relative dates ("today", "recently").
- Non-append edits to `log.md` (compare against git history).

## Procedure

1. Run all checks across `memory/`.
2. Present a **categorized report** — do **not** silently edit.
3. Fix only what the user approves.
4. Append to `memory/log.md`: `## [YYYY-MM-DD] lint | <N issues found, M fixed>`.

## Outputs

- Categorized issue report.
- Approved fixes applied + log entry.
