---
name: kb-query
description: Answer substantive questions from the memory/ knowledge base — "what did we decide about X", "did we already solve Y", "why did we choose Z", "have we seen this error before". Use whenever the answer likely lives in past sessions, ADRs, topic pages, or gotchas rather than in the code.
---

# kb-query

## When to use

- User asks what was decided, tried, learned, or solved before.
- You suspect the KB already covers a problem you're about to re-solve.

## Procedure

1. Read `memory/index.md`.
2. Follow `[[wikilinks]]` into candidate pages; go one hop deeper if useful.
3. If that misses, grep `memory/` as the fallback path.
4. Answer with inline citations to KB paths (e.g. `memory/decisions/0003-....md`).
5. If the answer required novel synthesis worth keeping: confirm with the user, then file it on the right page and update `memory/index.md`.
6. For non-trivial queries, append to `memory/log.md`: `## [YYYY-MM-DD] query | <question>`.

## Outputs

- The answer, with KB-path citations.
- Optionally: a newly filed synthesis page (user-confirmed) + index/log updates.
