# DT-670 → Arduino Temperature Readout

Hobby/educational project: reading a **Lake Shore DT-670-SD silicon diode** temperature sensor (73–403 K target range, ±5 K accuracy goal) with an Arduino Uno for a UHV chamber, served over Ethernet as HTTP/JSON and live-plotted on a PC.

> **Disclaimer:** This is a purely personal, educational project. I am **not affiliated with Lake Shore Cryotronics** in any way; their sensor and public datasheet curve are simply what this project reads out.

## How it works

- **Excitation:** LM334 constant-current source trimmed to 10 µA (6.2 kΩ + 1 kΩ trimmer).
- **Measurement:** ADS1115 16-bit ADC, differential A0−A1, ±2.048 V PGA, 4-wire (Kelvin) sense with RC-filtered sense lines.
- **Conversion:** official Lake Shore DT-670 curve (49 breakpoints, 50–440 K) in PROGMEM, linear interpolation.
- **Readout:** Uno R3 + Ethernet Shield 2 (W5500) serves `{"v":…,"t_k":…,"t_c":…,"flag":…}` at `http://192.168.2.2/`; `python/liveplot.py` (Panel/HoloViews) plots it live.

## Layout

| Path | Contents |
|---|---|
| `firmware/dt670srv/` | Main sketch: ADS1115 read → DT-670 curve → HTTP/JSON server |
| `firmware/pingtest/`, `firmware/adstest/`, `firmware/adsdiag/`, `firmware/noisecap/` | Bring-up / debug / noise-measurement sketches |
| `python/` | Live plot + noise capture/analysis scripts |
| `memory/` | Project knowledge base (decisions, gotchas, session notes) maintained with Claude Code |
| `raw/` | Immutable source documents and plans |

## Status

Full chain verified end-to-end on the bench with a dummy diode (1N4004). Next: rail decoupling A/B noise test, then installing the real DT-670.
