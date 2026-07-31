"""Capture raw ADS1115 samples from the noisecap sketch into a CSV.

Usage:
    python python/noisecap.py --out data/noise_no_elko.csv [--port COM5] [--seconds 60]

Opening the port resets the Uno (DTR); the script waits for the "t_us,raw"
header before recording, so the capture always starts clean.
"""

import argparse
import os
import time

import serial


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM5")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    with serial.Serial(args.port, 115200, timeout=5) as port:
        # wait for header (printed after the DTR reset + ADS init)
        deadline = time.time() + 15
        while True:
            line = port.readline().decode("ascii", errors="replace").strip()
            if line == "t_us,raw":
                break
            if line.startswith("ERR"):
                raise SystemExit(f"firmware error: {line}")
            if time.time() > deadline:
                raise SystemExit("no header from sketch - is noisecap flashed?")

        rows = []
        t_end = time.time() + args.seconds
        while time.time() < t_end:
            line = port.readline().decode("ascii", errors="replace").strip()
            parts = line.split(",")
            if len(parts) != 2:
                continue
            try:
                rows.append((int(parts[0]), int(parts[1])))
            except ValueError:
                continue

    with open(args.out, "w") as f:
        f.write("t_us,raw\n")
        for t_us, raw in rows:
            f.write(f"{t_us},{raw}\n")

    n = len(rows)
    if n == 0:
        raise SystemExit("no samples captured")
    vals = [r for _, r in rows]
    mean = sum(vals) / n
    std = (sum((v - mean) ** 2 for v in vals) / n) ** 0.5
    print(f"{args.out}: {n} samples, mean {mean:.1f} counts "
          f"({mean * 62.5e-6:.5f} V), std {std:.2f} counts "
          f"({std * 62.5:.1f} uV), p2p {max(vals) - min(vals)} counts")


if __name__ == "__main__":
    main()
