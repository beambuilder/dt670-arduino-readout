# ADR 0001 — Accuracy target relaxed from ±1 K to ±5 K

- Status: Accepted (2026-07-30, decision marked final in handoff)

## Context

Original target ±1 K over 73–403 K would require a 0.05–0.1 % precision current source and careful ADC calibration.

## Decision

Relax accuracy target to **±5 K**. Decision is final.

## Consequences

- Everything relaxes ~5×: LM334 suffices as current source; ADS1115 breakout suffices as ADC.
- No factory sensor calibration needed — standard DT-670 tolerance band + published standard curve stays inside ±5 K.
- Enables the whole [[0002-lm334-ads1115-frontend]] architecture.
