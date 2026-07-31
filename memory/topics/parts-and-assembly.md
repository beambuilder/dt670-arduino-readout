# Parts & assembly

Parts inventory and the agreed assembly + calibration procedure.

## Parts (all received)

- Reichelt: Arduino Uno R3 · Ethernet Shield 2 / W5500 clone · ADS1115 breakout · LM334Z ×2 · 6.2 kΩ 1% metal film ×2 · PT10 1 kΩ trimmer · 1 kΩ 1% ×2 · 100 nF ×4 · 10 µF · perfboard · 4-pin screw terminal · LiYCY 4×0.25 shielded cable · 9 V/1.33 A supply.
- Elsewhere: DT-670-SD (Lake Shore), 4-pin vacuum feedthrough (vacuum supplier).

## Assembly & calibration procedure (agreed 2026-07-30)

1. Build board sensorless (LM334 + chain, RC filters, ADS1115, terminals; stack shield).
2. **Trim current** with multimeter (µA mode, or 1.000 V across known 100 kΩ) in place of sensor → **10.0 µA ± 0.1 µA** at room temp.
3. Solder sensor pairs at the leads, route per [[wiring-feedthrough]] pin map, close chamber, connect cable.
4. Room-temp smoke test: differential ≈ **0.56 V at 25 °C** (~1.6 V or garbage → polarity reversed; swap at terminal block).
5. Verify: ice-water bath → 0 °C within ±1–2 °C. Optional LN2 dip → 77.4 K ≈ 1.02 V.
6. Flash firmware ([[arduino-firmware]]).

## Quirks & gotchas

- (see [[analog-frontend]] and [[wiring-feedthrough]] for build traps)

## Links

- [[analog-frontend]], [[wiring-feedthrough]], [[arduino-firmware]]
- Source: `raw/dt670-project-handoff.md`
