# DT-670 → Arduino Temperature Readout — Project Handoff

Conversation export for continuing in Claude Code. Everything decided so far is captured below;
the immediate next task is at the bottom.

---

## 1. Project goal

- Measure temperature from **−200 °C to +130 °C** (73 K … 403 K).
- Accuracy target: originally ±1 K, **relaxed to ±5 K** to simplify the electronics (decision final).
- Sensor: **Lake Shore DT-670-SD silicon diode** (range 1.4–500 K, excitation 10 µA DC,
  signal ≈ 0.33–1.05 V over our range, slope ≈ −2.1 mV/K above 100 K).
- Sensor is mounted **inside a vacuum chamber**; wiring goes sensor → 4-pin electrical
  feedthrough flange → shielded cable → electronics. In-chamber cryo wiring already purchased.
- Readout: **Arduino Uno R3 + Ethernet Shield 2 (W5500)** — Ethernet required because no USB
  ports are free. Powered from a 9 V / 1.33 A (12 W) barrel plug supply — confirmed fine
  (total load ≈ 250 mA; needs 5.5/2.1 mm center-positive, regulated).

## 2. Why this architecture (design discussion summary)

At ±1 K the build would have needed a 0.05–0.1 % precision current source and careful ADC
calibration. At **±5 K** everything relaxes ~5×:

- **Current source:** LM334 two-terminal adjustable current source. I ≈ 67.7 mV / R_set at 25 °C.
  Its ~0.33 %/°C room-temperature drift ≈ 0.5 K error over a ±8 °C lab swing — negligible here.
  Needs ≥1 V headroom; has ~4 V (5 V − 1.05 V max diode voltage).
- **ADC:** ADS1115 breakout (16-bit, I²C, addr 0x48), differential A0−A1 on the **±2.048 V** PGA
  range → 62.5 µV/count ≈ 0.03 K resolution. Chosen over the Uno's internal ADC because the
  internal 1.1 V reference (±10 % tolerance) could clip the ~1.05 V cold-end signal.
  I²C (A4/A5) coexists cleanly with the Ethernet shield on SPI.
- **4-wire (Kelvin) measurement:** force pair carries the 10 µA, sense pair carries ~no current,
  so cryo-wire/feedthrough/cable resistance drops out entirely.
- **Sensor tolerance:** any standard DT-670 tolerance band stays well inside ±5 K over 73–403 K
  using the published standard curve — no factory calibration needed.

## 3. Circuit (as built)

```
+5V ──► LM334 V+
        LM334 R ──[6.2 kΩ 1%]──[1 kΩ trimmer]──┐
        LM334 V− ──────────────────────────────┤ (one shared node)
                                               │
                                               ├──► F+ (feedthrough pin 1) ─► DT-670 ANODE (+)
DT-670 CATHODE (−) ─► F− (pin 4) ────────────────► GND

Sense: anode  ─► S+ (pin 2) ─[1 kΩ]─┬─► ADS1115 A0
                                    └─[100 nF]─► GND
       cathode─► S− (pin 3) ─[1 kΩ]─┬─► ADS1115 A1
                                    └─[100 nF]─► GND

ADS1115: VDD→5V, GND→GND, SDA→A4, SCL→A5
Cable shield grounded at the electronics end ONLY (no ground loop).
Decoupling: 100 nF + 10 µF across 5 V near the LM334.
```

### Trimmer change
Reichelt's PT10 was not available in 2 kΩ → **1 kΩ trimmer chosen** (in series with 6.2 kΩ 1%).
Adjustment window 6.2–7.2 kΩ → 9.4–10.9 µA; target R_set ≈ 6.77 kΩ sits mid-travel.
PT10 wipers can be scratchy: after trimming, tap-test; if the current jumps, sweep the wiper
a few times and re-trim.

### LM334Z pinout (verified against ST datasheet — datasheet drawing is a BOTTOM view!)
Holding the TO-92 with the **flat face toward you, legs down**:

| Position | Pin | Connects to |
|---|---|---|
| Left | **V−** (current output) | Shared node: resistor chain end + F+ wire to anode |
| Middle | **R (ADJ)** | Other end of 6.2 kΩ + trimmer chain |
| Right | **V+** | Arduino 5 V |

Verification: after trimming, voltage between R and V− legs should read ≈ 64–68 mV.
Reverse insertion is harmless (reverse ≤20 V draws only µA) — you'd just see ~no current.
Keep the resistor chain physically close to the LM334 legs (chip regulates only ~68 mV).

### Critical clarifications already discussed (get these right)
1. **ANODE (+) connects to LM334 V−** via F+. The cathode goes to GND via F−.
   Cathode never touches the LM334. Reversed polarity = garbage reading, no damage.
2. **R and V− are joined ONLY through the resistor chain.** A direct wire/solder bridge
   between R and V− means R_set = 0 → LM334 slams to up to 10 mA → exceeds the DT-670's
   1 mA absolute maximum and can destroy the sensor. This is the one dangerous mistake.
3. Never exceed 1 mA through the sensor; ESD precautions while soldering it.

## 4. Feedthrough pin map

| Pin | Name | Role | Inside chamber | Outside |
|---|---|---|---|---|
| 1 | F+ | 10 µA out | soldered to anode lead (+) | LM334 V− |
| 2 | S+ | sense high | soldered to anode lead (+) | 1 kΩ → ADS1115 A0 |
| 3 | S− | sense low | soldered to cathode lead (−) | 1 kΩ → ADS1115 A1 |
| 4 | F− | return | soldered to cathode lead (−) | GND |

Force+sense pairs are spliced **directly at the sensor leads** (Kelvin point) and meet again
only at the electronics.

## 5. Parts (ordered from Reichelt, received)

Arduino Uno R3 · Ethernet Shield 2 / W5500 clone · ADS1115 breakout · LM334Z ×2 ·
6.2 kΩ 1% metal film ×2 · **PT10 1 kΩ trimmer** · 1 kΩ 1% ×2 · 100 nF ×4 · 10 µF ·
perfboard · 4-pin screw terminal · LiYCY 4×0.25 shielded cable · 9 V/1.33 A supply.
From elsewhere: DT-670-SD (Lake Shore), 4-pin vacuum feedthrough (vacuum supplier).

## 6. Assembly & calibration procedure (agreed)

1. Build board sensorless (LM334 + chain, RC filters, ADS1115, terminals; stack shield).
2. **Trim current** with multimeter (µA mode, or 1.000 V across a known 100 kΩ) in place of
   the sensor → set **10.0 µA ± 0.1 µA** at room temperature.
3. Solder sensor pairs at the leads, route per pin map, close chamber, connect cable.
4. Room-temp smoke test: differential reading ≈ **0.56 V at 25 °C**. (~1.6 V or garbage →
   polarity reversed; swap at the terminal block.)
5. Verify: ice-water bath → 0 °C within ±1–2 °C. Optional LN2 dip → 77.4 K ≈ 1.02 V.
6. Flash firmware (next step).

## 7. Current status

- All parts received. Board assembly in progress; LM334 orientation and node topology
  clarified and understood. Hardware questions resolved.

## 8. NEXT TASK — write the Arduino firmware

Requirements agreed in conversation:

- Read ADS1115 differential **A0 − A1**, PGA ±2.048 V, average ~64 samples.
- Convert voltage → temperature using the official **Lake Shore Curve DT-670** table
  (from the DT-670 datasheet appendix) with linear interpolation between breakpoints.
  Needed span: at least 60 K … 420 K to cover 73–403 K with margin.
- Serve the temperature over Ethernet via the W5500 shield (stock `Ethernet` library).
  Output protocol not yet chosen — ask user: simple HTTP/JSON endpoint, UDP broadcast,
  or Modbus TCP. HTTP/JSON is the suggested default.
- Nice-to-haves discussed: report raw voltage alongside kelvin/°C; sanity flags for
  open sensor (V ≈ rail) and reversed polarity (V ≈ 1.6 V at room temp).
- Board: Arduino Uno R3 (ATmega328P, 2 KB SRAM, 32 KB flash) — keep the curve table in
  PROGMEM.
