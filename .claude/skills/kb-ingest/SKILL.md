---
name: kb-ingest
description: Ingest a new source the user dropped into raw/ (manual, spec, paper, data description) into the memory/ knowledge base. Use when the user says "ingest this", "I added a file to raw/", "read this manual and file it", or points at a new document in raw/.
---

# kb-ingest

## When to use

- User added a source to `raw/` and asks to ingest/file/process it.

## Procedure

1. **Read the source in full.** For very large files, use a subagent to extract and report back — the main session does all filing (only the main session writes to `memory/`).
2. **List 3–7 key takeaways** to the user.
3. **File content where it is operationally useful:**
   - Component/subject specifics → `memory/topics/` pages (create from `_template.md` if needed).
   - Domain knowledge → `memory/concepts/`.
   - Risks the source reveals → `memory/gotchas.md` or the topic page, tagged `ANTICIPATED`.
4. **Never edit `raw/`** — it is immutable and human-curated.
5. Update `memory/index.md` with any new pages.
6. Append to `memory/log.md`: `## [YYYY-MM-DD] ingest | <source name>`.

## Outputs

- Key-takeaways list.
- List of KB pages created/updated, with links back to the `raw/` source.
