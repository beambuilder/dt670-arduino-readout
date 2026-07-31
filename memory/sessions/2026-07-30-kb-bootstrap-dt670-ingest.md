# Session 2026-07-30 — KB bootstrap + DT-670 handoff ingest

## What happened

- Memory-layer structure (skills + CLAUDE.md) copied in from another project; `memory/` and `raw/` did not exist yet — bootstrapped full KB skeleton.
- Moved `dt670-project-handoff.md` → `raw/dt670-project-handoff.md` and ingested it.
- Initialized git repo and staged KB.

## Decisions made

- Filed 4 pre-existing decisions from the handoff as ADRs 0001–0004 (accuracy ±5 K; LM334+ADS1115; 4-wire; Ethernet W5500). No new decisions made this session.

## Learned & where filed

- Sensor specs / curve / reference voltages → [[dt670-sensor]]
- Circuit, LM334 pinout (datasheet is bottom view!), trimmer substitution → [[analog-frontend]]
- Feedthrough pin map, shield grounding → [[wiring-feedthrough]]
- Firmware requirements + open protocol question → [[arduino-firmware]]
- Parts + assembly/calibration procedure → [[parts-and-assembly]]
- Catastrophic R–V− bridge trap → [[gotchas]]

## Unfinished & next

- Firmware not started. Next: ask user for Ethernet protocol (HTTP/JSON default), then write sketch per [[arduino-firmware]]. See [[current-task]].
