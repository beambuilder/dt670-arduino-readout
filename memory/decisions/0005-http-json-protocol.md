# ADR 0005 — Ethernet readout protocol: HTTP/JSON

- **Status:** Accepted (2026-07-30)
- **Context:** [[0004-ethernet-readout]] fixed Uno R3 + W5500 as transport but left the application protocol open (candidates: HTTP/JSON, UDP broadcast, Modbus TCP). User's readout requirement arrived 2026-07-30: Python script polling at 2 Hz feeding a live browser plot (HoloViz).
- **Decision:** Plain HTTP/1.1 GET on port 80 returning a single JSON object: `{"v":<volts>,"t_k":<K|null>,"t_c":<°C|null>,"flag":"ok|open|reversed|out_of_range","age_ms":<ms since sample>}`. t_k/t_c are null unless flag is "ok".
- **Rationale:** Client is a poller — request/response fits naturally; trivially consumed by `requests`/curl/browser; human-debuggable; W5500 + stock Ethernet lib handle it in ~100 lines; no protocol library needed on either end. UDP broadcast adds client complexity for no benefit at 2 Hz; Modbus TCP adds tooling burden with no PLC in sight.
- **Consequences:** One reading per TCP connection (~ms overhead, irrelevant at 2 Hz). If a PLC/SCADA consumer ever appears, supersede with a new ADR (Modbus TCP) rather than extending this one.
- **Implemented in:** `firmware/dt670srv/dt670srv.ino`, consumed by `python/liveplot.py` ([[python-readout]]).
