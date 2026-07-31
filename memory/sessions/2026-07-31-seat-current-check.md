# 2026-07-31 — Seat-current check before DT-670 install

## What happened

- Short session: verified excitation current at the diode seat before installing the real DT-670.
- Method discussed: DMM in µA mode directly across the empty seat (F+ → GND) is valid because the LM334 is a true current source (DMM burden voltage irrelevant given ~4 V headroom). Alternative precision method remains 62.0 mV across the fixed 6.2 kΩ.
- **Measured: 10.5 µA across F+ → GND.** Within the 9.4–10.9 µA trim window; deemed good, no re-trim.

## Decisions made

- None (no ADRs). 10.5 µA accepted as-is — +5 % vs nominal shifts diode voltage ~1–2 mV, negligible at ±5 K.

## Learned & where filed

- Seat-current measurement method + 10.5 µA reference value → [[analog-frontend]] (Facts).

## Unfinished & next

- Install real DT-670 (ESD precautions, polarity per [[wiring-feedthrough]]); expect ~0.56 V / ~298 K room temp on live plot. Then ice-bath / LN2 validation per [[parts-and-assembly]].
