# Analog frontend (LM334 + ADS1115)

Current source and ADC for the DT-670 readout. Architecture per [[0002-lm334-ads1115-frontend]].

## Facts

- **LM334Z** two-terminal current source: I ≈ 67.7 mV / R_set at 25 °C. Target R_set ≈ 6.77 kΩ → 10 µA.
  - R_set chain: 6.2 kΩ 1% metal film + PT10 **1 kΩ trimmer** in series (window 6.2–7.2 kΩ → 9.4–10.9 µA; target mid-travel). 1 kΩ substituted because Reichelt had no 2 kΩ PT10.
  - Temp drift ~0.33 %/°C → ≈ 0.5 K error over ±8 °C lab swing — negligible at ±5 K target.
  - Headroom: needs ≥1 V, has ~4 V (5 V − 1.05 V max diode voltage).
- **ADS1115** breakout: 16-bit, I²C addr 0x48, differential A0−A1, PGA **±2.048 V** → 62.5 µV/count ≈ 0.03 K. VDD→5 V, SDA→A4, SCL→A5. I²C coexists cleanly with Ethernet shield on SPI.
- Sense lines: each 1 kΩ series + 100 nF to GND (RC filter) into A0/A1. Topology explicit: `diode leg ─[1 kΩ]─●─ A0/A1`, cap from ● to GND — cap is SHUNT, never in series (see gotcha).
- Decoupling: 100 nF + 10 µF across 5 V near the LM334. **Placed 2026-07-31** (elco + leg / long leg to 5 V, stripe to GND). A/B noise test same day (`data/noise_*.csv`, 60 s @ 200 Hz raw ADS samples via `firmware/noisecap/`): fast noise unchanged (36.6 → 37.0 µV std after 1 s-detrend, ≈16 mK), 50 Hz pickup 12.5 → 10.2 µV — decoupling is for supply robustness, not bench noise. Raw 60 s std (281/314 µV) is dominated by ~1 mV slow thermal drift of the 1N4004 dummy, not electrical noise; firmware's 64-sample average pushes per-reading noise to ~2 mK equiv.
- Circuit topology:

```
+5V ──► LM334 V+
        LM334 R ──[6.2 kΩ 1%]──[1 kΩ trimmer]──┐
        LM334 V− ──────────────────────────────┤ (one shared node)
                                               ├──► F+ ─► DT-670 ANODE (+)
DT-670 CATHODE (−) ─► F− ─────────────────────────► GND
```

- **LM334Z pinout** (flat face toward you, legs down): **Left = V+ (5 V), Middle = R (ADJ, to resistor chain), Right = V− (current out, to shared node)**. Verified 2026-07-30 against ST datasheet rev 3 figure (TO-92 bottom view, flat edge up: V+ / ADJ / V−) **and** empirically on the bench (reversed insertion gave 550 µA; see gotcha below).
- Verification after trim: 64–68 mV between R and V− legs (= across the R_set chain). NOTE: reverse insertion is NOT µA-harmless with R_set connected — it passes ~550 µA (see gotcha below); still under DT-670's 1 mA abs max, but never rely on it.
- Keep resistor chain physically close to LM334 legs (chip regulates only ~68 mV).
- **Calibrated 2026-07-30 (bench, 1N4004 stand-in diode):** exact-current trim = measure across the **fixed 6.2 kΩ alone** and set trimmer for **62.0 mV → 10.00 µA** (independent of unknown trimmer resistance). Chain voltage (R↔V− legs) stays ~65 mV at any trimmer position — LM334 forces the reference; trimmer changes current, not voltage. Use as regulation sanity check.
- Bench reference values, 1N4004 test diode: **~0.40 V at 10 µA** (healthy); **~0.57 V at ~550 µA** (reversed-LM334 fault signature); **~4.5 V across empty diode seat** = normal open-load compliance, proves wiring, NOT a fault.

## Quirks & gotchas

- `ANTICIPATED` — **Direct wire/bridge between R and V− = R_set 0 → up to 10 mA → destroys DT-670** (1 mA abs max). R and V− join ONLY through the resistor chain. The one dangerous mistake.
- `RESOLVED (2026-07-30)` — **LM334 pinout mirror trap (bit us on first power-up).** ST datasheet TO-92 drawing is a bottom view with the flat edge UP; converting to front view is a rotation about the horizontal axis, so left/right do **NOT** mirror. First KB version wrongly mirrored it (Left=V−/Right=V+), device went in reversed → no regulation, ~550 µA through the load (5 V = 0.6 V internal V−→ADJ junction + 3.7 V across R_set chain + 0.57 V diode). Datasheet's "reverse draws only µA" holds only without the ADJ path connected. Fix: rotate package 180° in place. Correct front view: V+ / R / V− (left/mid/right).
- `RESOLVED (2026-07-30)` — **100 nF sense caps were wired in series with the 1 kΩ into A0/A1 → DC blocked, ADS read ~0 V while diode had 0.40 V.** Symptoms: A0=A1 identical decaying ghost voltage, floating-input bias ≈0.26 V on unused channels, all continuity checks "open", series cap reads MΩ leakage on ohmmeter. Fix: cap shunt from ADS-pin node to GND. Verified after rewire: A0=0.4000 / A1=0.0000 / diff=0.4000. Cross-cutting copy in [[gotchas]].
- `ANTICIPATED` — PT10 wipers can be scratchy: after trimming, tap-test; if current jumps, sweep wiper a few times and re-trim.
- `RESOLVED (2026-07-30)` — Uno internal ADC rejected: 1.1 V internal reference has ±10 % tolerance, could clip ~1.05 V cold-end signal. Hence ADS1115.

## Links

- [[dt670-sensor]], [[wiring-feedthrough]], [[0002-lm334-ads1115-frontend]], [[0003-4wire-kelvin]]
- Source: `raw/dt670-project-handoff.md`
