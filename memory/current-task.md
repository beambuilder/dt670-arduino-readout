# Current task

**Full measurement chain works end-to-end (bench, dummy diode).** Next: hardware polish, then real DT-670 installation + verification.

## State (as of 2026-07-31)

- **Excitation current verified at diode seat 2026-07-31: 10.5 µA** (DMM µA across F+ → GND, empty seat — valid, LM334 true current source). Within 9.4–10.9 µA window, no re-trim. Cleared for real DT-670 install. See [[analog-frontend]].

- **Main firmware `firmware/dt670srv/` written, flashed, verified.** ADS1115 diff A0−A1 (±2.048 V, 64-sample avg @ 860 SPS), Lake Shore DT-670 curve (49 breakpoints, 50–440 K, from official datasheet) in PROGMEM, HTTP/JSON on `http://192.168.2.2/` ([[0005-http-json-protocol]]). Response: `{"v":0.40000,"t_k":368.51,"t_c":95.36,"flag":"ok","age_ms":7}`. Flags: ok/open/reversed/out_of_range. Serial mirror 115200.
- **Python live plot works:** `python/liveplot.py` (Panel+HoloViews, 2 Hz poll, browser at localhost:5006). See [[python-readout]]. Run: `conda activate base`, `python python\liveplot.py`.
- **Sense-wiring fault found + fixed:** 100 nF filter caps had been wired in series (DC blocked → ADS read 0 V) — now shunt to GND. Debug recipe + symptoms in [[gotchas]] / [[analog-frontend]]. `firmware/adsdiag/` (4× single-ended + diff print) kept for future frontend debugging.
- Dummy 1N4004 reads 0.400 V → reported "368.5 K" is curve coincidence, not temperature — pipeline proof only.
- Toolchain quirk: `arduino-cli` not on PATH in Claude shells — use `& "C:\Program Files\Arduino CLI\arduino-cli.exe"`. Uno = COM5.

## Blockers / open questions

- None blocking. ~~10 µF + 100 nF decoupling~~ **placed + A/B noise-tested 2026-07-31** — no noise change on bench (see [[analog-frontend]], `data/noise_compare.png`); kept in for supply robustness. Repo now public: https://github.com/beambuilder/dt670-arduino-readout.

## Next step (cold-session executable)

1. Swap 1N4004 → real DT-670 (ESD precautions, ≤1 mA abs max; polarity per [[wiring-feedthrough]]). Current already verified 10.5 µA at seat. Room-temp sanity: expect ~0.56 V / ~298 K on the live plot.
2. Optional validation per [[parts-and-assembly]]: ice-water bath → 273.15 K ±1–2 K; LN2 dip → 77.4 K ≈ 1.02 V.
3. Then: mount in chamber, route through feedthrough.
