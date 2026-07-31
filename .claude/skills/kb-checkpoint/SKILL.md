---
name: kb-checkpoint
description: Session-end write-back to the memory/ knowledge base — makes sessions compound instead of restarting. Use at session end, before /clear or quitting, when the user says "checkpoint", "wrap up", "save state", "we're done for today", or when a session with meaningful changes is winding down (suggest it proactively then). Persists what was done, learned, decided, and corrected into current-task.md, topic pages, gotchas.md, ADRs, a session note, and log.md.
---

# kb-checkpoint

## When to use

- Session end, before `/clear` or quitting.
- User says "checkpoint", "wrap up", or similar.
- Proactively: a session with meaningful changes (code, discoveries, decisions) is winding down — suggest running it.

## Procedure

1. **Review the session:** what was done, learned, decided, corrected — especially things the user corrected you on, and anything that took long to (re)discover.
2. **Update `memory/current-task.md`:** current state, blockers, and a **concrete next step a cold session can execute** (a command, a file to open, a question to answer — not "continue work").
3. **File knowledge:** topic-specific quirks/findings onto the relevant `memory/topics/` pages (create from `_template.md` if needed), with status tags. Cross-cutting traps go to `memory/gotchas.md`. Record the fix, not just the risk.
4. **Decisions:** real decisions become ADRs in `memory/decisions/NNNN-<slug>.md` (Status: Accepted), linked from relevant pages. ADRs are immutable once Accepted.
5. **Index:** refresh `memory/index.md` if pages were added or renamed.
6. **Session note:** write `memory/sessions/YYYY-MM-DD-<slug>.md` with sections: What happened / Decisions made / Learned & where filed / Unfinished & next. Episodic only — durable knowledge lives on topic pages; the note links to where it was filed.
7. **Log:** append to `memory/log.md`: `## [YYYY-MM-DD] checkpoint | <one-line summary>`, linking the session note. Never edit prior entries.
8. **Dates:** convert all relative dates ("today", "last week") to absolute before persisting.
9. **Git:** stage the KB changes (`git add memory/`) and show a short summary — the human commits.

## Outputs

- List of KB files updated.
- The next-step line from `current-task.md`.
