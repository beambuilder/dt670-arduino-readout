# Arduino firmware

Firmware for Uno R3 + Ethernet Shield 2 (W5500). **Main sketch `firmware/dt670srv/` written, flashed, verified end-to-end 2026-07-30** (dummy 1N4004: 0.400 V → JSON over Ethernet).

## Main sketch: `firmware/dt670srv/`

- ADS1115 diff A0−A1, GAIN_TWO (±2.048 V, 62.5 µV/LSB), **860 SPS**, 64-sample burst ≈ 75 ms; continuous measure loop, HTTP served between bursts.
- Lake Shore Curve DT-670 in PROGMEM: **49 breakpoints, 50–440 K**, taken from the official datasheet appendix table (extracted from the PDF, not guessed); linear interpolation on falling voltage.
- HTTP/JSON on `192.168.2.2:80` ([[0005-http-json-protocol]]): `{"v":…,"t_k":…,"t_c":…,"flag":"ok|open|reversed|out_of_range","age_ms":…}`; t_k/t_c null unless ok. Thresholds: reversed < −0.05 V, open > 1.5 V.
- Serial debug mirror 115200. Footprint: 67 % flash, 38 % SRAM.
- Consumed by `python/liveplot.py` — see [[python-readout]].

## Test/debug sketches

- `firmware/pingtest/` — W5500 bring-up, static IP **192.168.2.2**, `Ethernet.init(10)` (CS pin 10 on Shield 2). Flashed + ping verified end-to-end.
- `firmware/adstest/` — ADS1115 differential A0−A1 over serial. Superseded by adsdiag for debugging.
- `firmware/adsdiag/` — **keep for frontend debugging:** prints A0..A3 single-ended vs GND + diff01 once/s. Floating input reads ≈0.26 V bias; identical decaying values on two channels = common/floating node. Found the series-cap fault (see [[analog-frontend]]).

## Toolchain & network (working setup, 2026-07-30)

- `arduino-cli` 1.5.1 (winget), core `arduino:avr`, libs `Ethernet` 2.0.2, `Adafruit ADS1X15` 2.6.2. Uno = **COM5** when USB plugged; upload: `arduino-cli upload -p COM5 --fqbn arduino:avr:uno firmware/<sketch>`.
- **`arduino-cli` not on PATH in Claude's PowerShell sessions** — call `& "C:\Program Files\Arduino CLI\arduino-cli.exe"` with full path.
- Reading serial without resetting the Uno (PowerShell): `New-Object System.IO.Ports.SerialPort COM5,115200` with `DtrEnable = $false`.
- PC side: USB-Ethernet dongle interface "Ethernet 2" (ASIX), static **192.168.2.1/24** — setting it needs admin PowerShell (`New-NetIPAddress -InterfaceAlias 'Ethernet 2' -IPAddress 192.168.2.1 -PrefixLength 24`).
- W5500's hardware TCP/IP stack answers ICMP ping by itself once `Ethernet.begin(mac, ip)` runs — no ping code needed.

## Requirements (agreed 2026-07-30)

- Read ADS1115 differential A0−A1, PGA ±2.048 V, average ~64 samples.
- Voltage → temperature via official **Lake Shore Curve DT-670** table (datasheet appendix), linear interpolation, span ≥ 60–420 K.
- Serve temperature over Ethernet via W5500 (stock `Ethernet` library).
- Output protocol: **HTTP/JSON — decided 2026-07-30**, see [[0005-http-json-protocol]].
- Nice-to-haves (all implemented in dt670srv): raw voltage alongside K/°C; sanity flags for open sensor (V ≈ rail) and reversed polarity (V ≈ 1.6 V at room temp).

## Constraints

- ATmega328P: 2 KB SRAM, 32 KB flash → curve table in **PROGMEM**.
- Ethernet required (no free USB ports) — see [[0004-ethernet-readout]].
- Power: 9 V/1.33 A barrel (5.5/2.1 mm center-positive, regulated); total load ≈ 250 mA — fine.

## Quirks & gotchas

- `RESOLVED (2026-07-30)` — `arduino-cli` invisible to Claude's PowerShell (PATH); use full path `C:\Program Files\Arduino CLI\arduino-cli.exe`.
- `ANTICIPATED` — Flashing any sketch replaces dt670srv → live plot shows "no response" until reflashed. Reflash: `upload -p COM5 --fqbn arduino:avr:uno firmware/dt670srv`.

## Links

- [[dt670-sensor]], [[analog-frontend]], [[python-readout]], [[0004-ethernet-readout]], [[0005-http-json-protocol]]
- Source: `raw/dt670-project-handoff.md`
