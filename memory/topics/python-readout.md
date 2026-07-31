# Python readout (live plot)

PC-side consumer of the Arduino's HTTP/JSON endpoint ([[0005-http-json-protocol]]).

## Facts

- `python/liveplot.py` — Panel 1.2.3 + HoloViews 1.17.1 (bokeh), polls `http://192.168.2.2/` at 2 Hz (500 ms periodic callback), streams into `holoviews.streams.Buffer` (30 min history), two linked plots (V_diode, T[K]) + status line. Serves browser UI at `http://localhost:5006`.
- Run (Anaconda prompt): `conda activate base`, then `python python\liveplot.py` — opens browser automatically (`pn.serve(..., show=True)`).
- `t_k: null` from firmware becomes NaN → gap in the T curve; V plots always.
- Env: Anaconda base, Python 3.11.5, **numpy pinned 1.26.4** (see gotcha below), pandas 2.0.3, requests 2.31.0.

## Quirks & gotchas

- `RESOLVED (2026-07-30)` — base env had numpy 2.4.6 → pandas/panel import crash (`numpy.dtype size changed`). Pinned `numpy<2` via `& C:\Users\Niclas\anaconda3\python.exe -m pip install "numpy<2"`. Don't let numpy back to 2.x without rebuilding pandas/numba. Also in [[gotchas]].
- `RESOLVED (2026-07-30)` — `conda run -n base pip install …` fails ("Das System kann die angegebene Datei nicht finden"); call base `python.exe -m pip` directly.

## Links

- [[arduino-firmware]], [[0005-http-json-protocol]], [[gotchas]]
