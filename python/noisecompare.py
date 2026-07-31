"""Compare two noisecap CSVs (without vs with 10 uF rail decoupling).

Usage:
    python python/noisecompare.py data/noise_no_elko.csv data/noise_with_elko.csv \
        [--labels "no elko" "with elko"] [--png data/noise_compare.png]

Stats per file: mean, std, p2p, in counts / uV / mK-equivalent
(DT-670 sensitivity ~2.3 mV/K near 300 K), plus 50/100 Hz spectral amplitude.
"""

import argparse

import numpy as np

LSB_UV = 62.5          # uV per count at GAIN_TWO
SENS_UV_PER_MK = 2.3   # DT-670 ~2.3 mV/K near 300 K -> 2.3 uV/mK


def load(path):
    data = np.genfromtxt(path, delimiter=",", names=True)
    t = data["t_us"] * 1e-6
    raw = data["raw"]
    return t - t[0], raw


def tone_amp_uv(t, raw, freq):
    """Amplitude of a sine at `freq` Hz via least-squares projection."""
    x = (raw - raw.mean()) * LSB_UV
    c = np.cos(2 * np.pi * freq * t)
    s = np.sin(2 * np.pi * freq * t)
    a = 2 * np.mean(x * c)
    b = 2 * np.mean(x * s)
    return float(np.hypot(a, b))


def stats(path):
    t, raw = load(path)
    uv = raw * LSB_UV
    std_uv = float(uv.std())
    return {
        "n": len(raw),
        "dur_s": float(t[-1]),
        "mean_v": float(uv.mean() * 1e-6),
        "std_counts": float(raw.std()),
        "std_uv": std_uv,
        "std_mk": std_uv / SENS_UV_PER_MK,
        "p2p_counts": int(raw.max() - raw.min()),
        "p2p_uv": float((raw.max() - raw.min()) * LSB_UV),
        "amp50_uv": tone_amp_uv(t, raw, 50.0),
        "amp100_uv": tone_amp_uv(t, raw, 100.0),
        "_t": t,
        "_raw": raw,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs=2)
    ap.add_argument("--labels", nargs=2, default=["no elko", "with elko"])
    ap.add_argument("--png", default=None)
    args = ap.parse_args()

    results = [stats(f) for f in args.files]

    rows = [
        ("samples", "{n}", 1),
        ("duration [s]", "{dur_s:.1f}", 1),
        ("mean [V]", "{mean_v:.5f}", 1),
        ("std [counts]", "{std_counts:.2f}", 1),
        ("std [uV]", "{std_uv:.1f}", 1),
        ("std [mK equiv]", "{std_mk:.1f}", 1),
        ("p2p [counts]", "{p2p_counts}", 1),
        ("p2p [uV]", "{p2p_uv:.0f}", 1),
        ("50 Hz amp [uV]", "{amp50_uv:.1f}", 1),
        ("100 Hz amp [uV]", "{amp100_uv:.1f}", 1),
    ]
    w = 18
    print(f"{'metric':<{w}} {args.labels[0]:>{w}} {args.labels[1]:>{w}}")
    for name, fmt, _ in rows:
        a = fmt.format(**results[0])
        b = fmt.format(**results[1])
        print(f"{name:<{w}} {a:>{w}} {b:>{w}}")

    ratio = results[0]["std_uv"] / results[1]["std_uv"] if results[1]["std_uv"] else float("inf")
    print(f"\nstd ratio ({args.labels[0]} / {args.labels[1]}): {ratio:.2f}x")

    if args.png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 7))
        for i, (res, label) in enumerate(zip(results, args.labels)):
            t, raw = res["_t"], res["_raw"]
            uv = (raw - raw.mean()) * LSB_UV
            axes[0][i].plot(t, uv, lw=0.4)
            axes[0][i].set_title(f"{label}: std {res['std_uv']:.1f} uV "
                                 f"({res['std_mk']:.1f} mK equiv)")
            axes[0][i].set_xlabel("t [s]")
            axes[0][i].set_ylabel("deviation [uV]")

            dt = np.median(np.diff(t))
            freqs = np.fft.rfftfreq(len(uv), dt)
            spec = np.abs(np.fft.rfft(uv)) / len(uv) * 2
            axes[1][i].semilogy(freqs[1:], spec[1:], lw=0.6)
            axes[1][i].set_xlabel("f [Hz]")
            axes[1][i].set_ylabel("amplitude [uV]")
            axes[1][i].set_xlim(0, freqs[-1])
        ylim = max(ax.get_ylim()[1] for ax in axes[0])
        for ax in axes[0]:
            ax.set_ylim(-ylim, ylim)
        fig.tight_layout()
        fig.savefig(args.png, dpi=120)
        print(f"plot -> {args.png}")


if __name__ == "__main__":
    main()
