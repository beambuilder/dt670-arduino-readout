# 2026-07-30 — Main firmware, live plot, RC-filter debugging

## What happened

- Wrote, flashed, verified main firmware `firmware/dt670srv/`: ADS1115 → DT-670 curve (49 official datasheet breakpoints, 50–440 K, PROGMEM) → HTTP/JSON at 192.168.2.2:80. 67 % flash, 38 % SRAM.
- Wrote `python/liveplot.py` (Panel + HoloViews): 2 Hz poll, live browser plots of V and T at localhost:5006. Fixed broken Anaconda base env first (numpy 2.4.6 → pinned 1.26.4).
- First live ADC reading exposed a fault: diff A0−A1 ≈ 0 V while multimeter showed 0.40 V across the dummy diode. Wrote `firmware/adsdiag/` (single-ended channel prints); found both inputs floating with identical decaying ghost voltage.
- Root cause (via continuity ladder + user's own question about cap orientation): **100 nF filter caps wired in series between 1 kΩ and ADS inputs — DC blocked.** Rewired shunt-to-GND; chain immediately read A0=0.4000 / A1=0.0000 / diff=0.4000.
- End-to-end verified: `{"v":0.40000,"t_k":368.51,"t_c":95.36,"flag":"ok"}` on the live plot. (368 K is a curve coincidence of the 1N4004 — pipeline proof, not a temperature.)

## Decisions made

- [[0005-http-json-protocol]] — HTTP/JSON readout protocol (closes the open question from [[0004-ethernet-readout]]).

## Learned & where filed

- Series-cap trap, symptoms, debug recipe → [[analog-frontend]] + [[gotchas]].
- Never measure resistance on a powered circuit (user's first continuity round was invalid) → [[gotchas]].
- adsdiag floating-input signatures (0.26 V bias; identical decaying pair = common node) → [[arduino-firmware]].
- numpy 2.x breaks base env; `conda run pip` broken, use `python.exe -m pip` → [[python-readout]] + [[gotchas]].
- arduino-cli needs full path in Claude shells; serial read without reset via `DtrEnable=$false` → [[arduino-firmware]].

## Unfinished & next

- 10 µF + 100 nF rail decoupling near LM334 not placed yet.
- Real DT-670 not yet installed — next session: decoupling, swap diode, room-temp sanity (~0.56 V / ~298 K), optional ice-bath/LN2 validation. See [[current-task]].
