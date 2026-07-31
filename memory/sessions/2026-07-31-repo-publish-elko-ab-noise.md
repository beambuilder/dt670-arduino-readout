# 2026-07-31 — Repo published + 10 µF decoupling A/B noise test

## What happened

- Created public GitHub repo **https://github.com/beambuilder/dt670-arduino-readout** (README: educational, Lake Shore mentioned with no-affiliation disclaimer; `.gitignore`), initial commit + push of everything.
- Wrote noise tooling: `firmware/noisecap/` (raw ADS1115 diff samples, 200 Hz, serial CSV) + `python/noisecap.py` (logger) + `python/noisecompare.py` (stats/plot).
- A/B measurement: 60 s baseline without elkos → user placed **10 µF elko (long leg/+ to 5 V, stripe to GND) + 100 nF** across 5 V/GND at LM334 → 60 s with. Data + plot in `data/`.
- Result: fast noise unchanged (36.6 → 37.0 µV std after 1 s detrend, ≈16 mK); 50 Hz pickup 12.5 → 10.2 µV; raw 60 s std (281/314 µV) dominated by ~1 mV slow thermal drift of the 1N4004 dummy, not supply noise. Caps kept for supply robustness.
- Reflashed `firmware/dt670srv` afterwards (flash-replaces-server gotcha held).
- Committed data + KB updates, pushed (`f82bd82`).

## Decisions made

- Keep decoupling caps despite no measurable bench-noise benefit (robustness against Ethernet load transients / chamber wiring). Recorded on [[analog-frontend]] — no ADR needed.

## Learned & where filed

- Decoupling A/B numbers + "raw std is drift, not noise" → [[analog-frontend]] facts.
- noisecap sketch + COM5-vanishes-until-USB-replug quirk → [[arduino-firmware]].
- Noise scripts + pyserial → [[python-readout]].

## Unfinished & next

- Swap 1N4004 → real DT-670 (ESD, ≤1 mA; expect ~0.56 V / ~298 K at room temp). Then ice-bath/LN2 validation, then chamber install. See [[current-task]].
