# Wiring & feedthrough

4-wire (Kelvin) wiring from DT-670 through the UHV feedthrough to the electronics. See [[0003-4wire-kelvin]].

## Facts

- 4-wire: force pair carries the 10 µA, sense pair ~no current → cryo-wire/feedthrough/cable resistance drops out.
- Force+sense pairs spliced **directly at the sensor leads** (Kelvin point); meet again only at the electronics.
- Feedthrough pin map:

| Pin | Name | Role | Inside chamber | Outside |
|---|---|---|---|---|
| 1 | F+ | 10 µA out | anode lead (+) | LM334 V− |
| 2 | S+ | sense high | anode lead (+) | 1 kΩ → ADS1115 A0 |
| 3 | S− | sense low | cathode lead (−) | 1 kΩ → ADS1115 A1 |
| 4 | F− | return | cathode lead (−) | GND |

- ANODE (+) → LM334 V− via F+; CATHODE (−) → GND via F−. Cathode never touches the LM334.
- Cable: LiYCY 4×0.25 shielded. In-chamber cryo wiring already purchased.

## Quirks & gotchas

- `ANTICIPATED` — Ground cable shield at the **electronics end ONLY** (no ground loop).
- `ANTICIPATED` — Reversed polarity → garbage (~1.6 V at room temp), no damage; swap at terminal block.

## Links

- [[dt670-sensor]], [[analog-frontend]]
- Source: `raw/dt670-project-handoff.md`
