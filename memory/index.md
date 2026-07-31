# KB index

Project: **DT-670 silicon diode → Arduino temperature readout** for UHV chamber (73–403 K, ±5 K).

- [[current-task]] — what to do next (start here after index)
- [[gotchas]] — cross-cutting / catastrophic traps
- [[log]] — append-only session log

## Topics

- [[dt670-sensor]] — Lake Shore DT-670-SD: ratings, curve, reference voltages
- [[analog-frontend]] — LM334 current source + ADS1115 ADC, circuit, pinout, trim
- [[wiring-feedthrough]] — 4-wire pin map, shield grounding, polarity
- [[arduino-firmware]] — main sketch dt670srv (done, verified), test sketches, toolchain
- [[python-readout]] — PC-side live plot (Panel/HoloViews), conda env quirks
- [[parts-and-assembly]] — parts inventory, assembly & calibration procedure

## Decisions (ADRs)

- [[0001-accuracy-relaxed-to-5k]] — ±1 K → ±5 K (final)
- [[0002-lm334-ads1115-frontend]] — LM334 + ADS1115 architecture
- [[0003-4wire-kelvin]] — 4-wire measurement
- [[0004-ethernet-readout]] — Uno R3 + W5500 Ethernet
- [[0005-http-json-protocol]] — HTTP/JSON readout protocol

## Sources (`raw/`, immutable)

- `raw/dt670-project-handoff.md` — full design-conversation handoff (2026-07-30)
