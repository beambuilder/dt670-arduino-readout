# ADR 0004 — Readout via Arduino Uno R3 + Ethernet Shield 2 (W5500)

- Status: Accepted (2026-07-30)

## Context

No USB ports free on the acquisition machine; readout must reach it over the network.

## Decision

Arduino Uno R3 + Ethernet Shield 2 (W5500 clone), stock `Ethernet` library. Powered from 9 V/1.33 A barrel supply (confirmed sufficient; load ≈ 250 mA).

## Consequences

- ATmega328P limits: 2 KB SRAM, 32 KB flash → DT-670 curve table goes in PROGMEM.
- Output protocol still **undecided** (HTTP/JSON suggested default vs UDP broadcast vs Modbus TCP) — open question for firmware task, see [[arduino-firmware]].
