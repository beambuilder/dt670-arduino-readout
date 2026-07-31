# ADR 0003 — 4-wire (Kelvin) measurement through the feedthrough

- Status: Accepted (2026-07-30)

## Context

Sensor sits in a UHV chamber behind cryo wiring, a 4-pin feedthrough, and shielded cable — all with non-negligible, temperature-dependent resistance.

## Decision

4-wire measurement: force pair carries the 10 µA, sense pair (into the high-impedance ADS1115) carries ~no current. Pairs spliced directly at the sensor leads.

## Consequences

- Wire/feedthrough/cable resistance drops out entirely.
- Requires all 4 feedthrough pins; pin map fixed in [[wiring-feedthrough]].
