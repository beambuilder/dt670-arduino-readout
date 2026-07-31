# 2026-07-30 — Bench bring-up: Ethernet ping + LM334 pinout trap + 10 µA calibration

## What happened

- First power-up of the assembled frontend, with a **1N4004 as stand-in** for the DT-670 (deliberate — cheap, indestructible at these currents).
- Installed `arduino-cli` toolchain; wrote + flashed `firmware/pingtest/pingtest.ino`; **ping to 192.168.2.2 works** through the PC's USB-Ethernet dongle (static 192.168.2.1/24).
- First measurements showed no regulation: 3.7 V across the R_set chain (~550 µA), diode at 0.57 V, only 0.6 V across LM334 V+→R. Diagnosed as **LM334 inserted reversed** because the KB pinout table was mirrored.
- Verified against ST datasheet (rev 3, TO-92 bottom-view figure, flat edge up: V+ / ADJ / V−): bottom→front conversion does **not** mirror left/right. Correct front view = **V+ / R / V−** (left/mid/right).
- User rotated the LM334 180° in place → regulation immediately correct: 65.6 mV across chain, diode 0.40 V.
- **Calibrated to exactly 10.00 µA**: 62.0 mV across the fixed 6.2 kΩ alone. Confirmed chain voltage is trimmer-independent (LM334 forces reference).
- Wrote `firmware/adstest/adstest.ino` (ADS1115 A0−A1 differential, 64-sample average, serial print); compiles; not flashed — USB was unplugged.

## Decisions made

- None architectural (no new ADR). Ethernet protocol question still open.

## Learned & where filed

- Correct LM334Z pinout + mirror-trap post-mortem → [[analog-frontend]] (facts + `RESOLVED` gotcha).
- Reversed LM334 with R_set connected passes ~550 µA, not "several µA" → [[analog-frontend]].
- Exact-current trim method (62.0 mV across fixed 6.2 kΩ) + 1N4004 bench reference voltages (0.40 V healthy / 0.57 V reversed-fault / 4.5 V open seat) → [[analog-frontend]].
- Toolchain, COM port, IPs, dongle setup, W5500 hardware-ping fact → [[arduino-firmware]].

## Unfinished & next

- Flash `firmware/adstest`, compare ADS1115 reading vs multimeter (needs USB replugged; Uno = COM5).
- Ask user: Ethernet protocol (HTTP/JSON default) → then write main firmware. See [[current-task]].
