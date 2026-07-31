# Plan 2026-07-31 — publish repo + 10 µF elko A/B noise comparison

## Goals

1. Create public GitHub repo, commit + push everything (README: educational project, Lake Shore mentioned, no affiliation).
2. A/B comparison of frontend noise **without vs with** the 10 µF electrolytic (+100 nF) rail decoupling near the LM334.

## Elko placement (from [[analog-frontend]])

10 µF electrolytic + 100 nF ceramic in parallel, across **5 V ↔ GND**, physically close to the LM334 V+ leg. Elko **+ leg to 5 V**, − leg (stripe) to GND. NOT in the signal path, NOT across the diode.

## Method

- New sketch `firmware/noisecap/`: ADS1115 diff A0−A1, GAIN_TWO, 860 SPS continuous; sampled every 5 ms (200 Hz) → `t_us,raw` over serial 115200. 200 Hz Nyquist covers 50/100 Hz mains ripple.
- `python/noisecap.py`: logs COM5 serial to CSV for N seconds (default 60 s ≈ 12000 samples).
- `python/noisecompare.py`: per-file stats (mean, std, p2p, RMS in counts/µV/mK-equiv @ ~2.3 mV/K DT-670 sensitivity near 300 K) + 50/100 Hz spectral lines + comparison table + plot PNG.

## Steps

1. [x] Plan file (this).
2. [ ] README.md, .gitignore, noisecap sketch, python scripts.
3. [ ] Commit, `gh repo create` public, push.
4. [ ] Flash noisecap → capture `data/noise_no_elko.csv` (baseline, elkos absent — current bench state).
5. [ ] USER: place 10 µF (+100 nF) across 5 V/GND near LM334, + leg to 5 V. Power off first.
6. [ ] Re-capture → `data/noise_with_elko.csv`.
7. [ ] Run noisecompare, report table + plot.
8. [ ] Reflash `firmware/dt670srv` (gotcha: any flash replaces it → live plot dead until reflash).
9. [ ] kb-checkpoint, commit results.

## Notes

- Dummy diode is still 1N4004 at ~0.400 V — comparison is of *noise*, absolute value meaningless.
- Uno = COM5; arduino-cli full path `C:\Program Files\Arduino CLI\arduino-cli.exe`.
- Python: `C:\Users\Niclas\anaconda3\python.exe` (pyserial 3.5 present).
