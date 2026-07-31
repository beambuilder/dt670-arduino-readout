# DT-670 sensor

Lake Shore DT-670-SD silicon diode, the temperature sensor for the UHV chamber readout.

## Facts

- Range 1.4–500 K; project uses 73–403 K (−200 °C … +130 °C).
- Excitation: **10 µA DC** forward current. Signal ≈ 0.33–1.05 V over our range; slope ≈ −2.1 mV/K above 100 K.
- **Absolute maximum current: 1 mA** — exceeding it can destroy the sensor.
- Any standard tolerance band stays inside ±5 K over 73–403 K using the published standard curve — no factory calibration needed (see [[0001-accuracy-relaxed-to-5k]]).
- Voltage → temperature via official **Lake Shore Curve DT-670** breakpoint table (DT-670 datasheet appendix), linear interpolation. Firmware needs span ≥ 60–420 K.
- Reference points: ~0.56 V at 25 °C; 77.4 K (LN2) ≈ 1.02 V.
- Mounted inside vacuum chamber; wiring: sensor → 4-pin feedthrough → shielded cable → electronics (see [[wiring-feedthrough]]).

## Quirks & gotchas

- `ANTICIPATED` — Never exceed 1 mA. The one dangerous build mistake: direct bridge between LM334 R and V− pins → R_set = 0 → up to 10 mA → sensor destroyed. See [[analog-frontend]].
- `ANTICIPATED` — ESD precautions while soldering the sensor leads.
- `ANTICIPATED` — Reversed polarity gives garbage reading (~1.6 V at room temp) but no damage; swap at terminal block.

## Links

- [[analog-frontend]], [[wiring-feedthrough]], [[arduino-firmware]]
- Source: `raw/dt670-project-handoff.md`
