# Plan 2026-07-30 — main firmware + Python live plot

Goal: main DT-670 firmware (HTTP/JSON over W5500) + Python holoviz live plot at 2 Hz in browser.

Protocol decision: HTTP/JSON endpoint (was open question; user's request — Python polling at 2 Hz — fits polling model; was suggested default). Record as ADR 0005 at checkpoint.

Steps:
1. Fetch official Lake Shore DT-670 standard curve breakpoint table (60–420 K) — do NOT invent values.
2. `firmware/dt670srv/dt670srv.ino`:
   - ADS1115 diff A0−A1, GAIN_TWO (±2.048 V), 64-sample avg @ 860 SPS (~75 ms/burst).
   - Curve table in PROGMEM, linear interpolation → kelvin (+ °C).
   - W5500 HTTP server at 192.168.2.2:80, GET / → JSON: {"v": volts, "t_k":, "t_c":, "flag": ok|open|reversed|out_of_range}.
   - Serial debug print at 115200 kept.
   - Note: dummy 1N4004 reads ~0.40 V → below/off DT-670 curve low-V end (0.33 V @ 403 K? no—curve V at 420 K ≈ 0.30 V) → expect valid-ish T ~ 395–400 K region or out_of_range; raw V is the check value.
3. Compile + upload COM5 (`arduino-cli`), verify: ping 192.168.2.2, then `curl http://192.168.2.2/`.
4. `python/liveplot.py`: panel + holoviews Buffer stream, periodic callback 500 ms, GET JSON, plot V (and T) vs time; `pn.serve(show=True)` on localhost:5006. Check base env has panel/holoviews/requests; install missing via pip.
5. kb-checkpoint at session end (ADR 0005, firmware page update, session note).
