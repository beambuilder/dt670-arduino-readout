# ADR 0002 — LM334 current source + ADS1115 ADC frontend

- Status: Accepted (2026-07-30)

## Context

At ±5 K ([[0001-accuracy-relaxed-to-5k]]) a precision current source is unnecessary. Uno's internal ADC rejected: 1.1 V internal reference (±10 % tolerance) could clip the ~1.05 V cold-end signal.

## Decision

- **LM334Z** adjustable current source, R_set ≈ 6.77 kΩ (6.2 kΩ 1% + 1 kΩ trimmer) → 10 µA.
- **ADS1115** 16-bit I²C ADC, differential A0−A1, PGA ±2.048 V → 62.5 µV/count ≈ 0.03 K resolution.

## Consequences

- LM334 drift ≈ 0.5 K over ±8 °C lab swing — negligible.
- I²C (A4/A5) coexists with Ethernet shield on SPI.
- Trimmer mis-set / R–V− bridge is the one sensor-destroying risk (see [[analog-frontend]]).
