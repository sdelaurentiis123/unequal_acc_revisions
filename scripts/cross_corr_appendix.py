#!/usr/bin/env python3
"""
Appendix cross-correlation figures for the unequal-accretion paper (#14).

Implements Z. Haiman's Jun-7 2026 guidance:
  - Report the lag at the MAXIMUM of the (normalized) cross-correlation C(Dt),
    i.e. the principal positive peak within +/- half a precession period,
    NOT a trough-to-peak event lag.
  - Peak-C heatmap: lambda vs r_2 ONLY, positive values; r_1 dropped.
  - A couple of 1D C(Dt) examples (clean + messy) preceding the heatmap.

C(Dt) = < (lambda(t)-<lambda>) (r2(t+Dt)-<r2>) >_t / (sigma_lambda sigma_r2)
(standard normalized Pearson cross-correlation; ranges in [-1,1]).

Outputs (paper root, so main.tex can \\includegraphics them):
  appendix_crosscorr_examples.pdf
  appendix_crosscorr_peakC.pdf
  cross_corr/appendix_peakC_lambda_r2.csv
"""
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

DATA = "/Users/stanislavdelaurentiis/roman_work/metrics_data"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CC = os.path.join(ROOT, "cross_corr")
os.makedirs(CC, exist_ok=True)

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
T_CUT = 3000.0   # tau_b transient cut (matches paper)
DT = 10.0        # snapshot cadence (tau_b)


def load(eb, qb):
    with open(f"{DATA}/data_eb_{eb}_qb_{qb}", "rb") as f:
        d = pickle.load(f)
    n = min(len(d[k]) for k in ["time", "mdot1", "mdot2", "rmin1", "rmin2"])
    t = np.asarray(d["time"])[:n]
    m1 = np.asarray(d["mdot1"])[:n]
    m2 = np.asarray(d["mdot2"])[:n]
    r2 = np.asarray(d["rmin2"])[:n]
    k = t >= T_CUT
    lam = m2[k] / np.where(m1[k] != 0, m1[k], np.nan)
    fin = np.isfinite(lam)
    lam[~fin] = np.nanmedian(lam[fin]) if fin.any() else 0.0
    return t[k], lam, r2[k]


def z(x):
    s = x.std()
    return (x - x.mean()) / s if s > 0 else x - x.mean()


def lagcorr(x, y, maxlag):
    """Normalized cross-correlation C(k)=corr(x(t), y(t+k)) for k in [-ml, ml]."""
    n = len(x)
    lags = np.arange(-maxlag, maxlag + 1)
    out = np.full(len(lags), np.nan)
    for i, k in enumerate(lags):
        if k < 0:
            a, b = x[-k:], y[: n + k]
        elif k > 0:
            a, b = x[: n - k], y[k:]
        else:
            a, b = x, y
        if len(a) > 2 and a.std() > 0 and b.std() > 0:
            out[i] = np.corrcoef(a, b)[0, 1]
    return lags, out


def dominant_period(sig):
    n = len(sig)
    s = sig - sig.mean()
    spec = np.abs(np.fft.rfft(s * np.hanning(n)))
    fr = np.fft.rfftfreq(n, d=DT)
    m = fr > 2 / (n * DT)
    if not m.any():
        return np.nan
    return 1.0 / fr[m][np.argmax(spec[m])]


def peak_for_cell(eb, qb):
    """Return (T, peakC, lag_taub, C, lags, lam_z, r2_z, t)."""
    t, lam, r2 = load(eb, qb)
    lz, rz = z(lam), z(r2)
    T = dominant_period(r2)
    Tw = T if (np.isfinite(T) and 50 < T < 1500) else 300.0
    win = int(min(max(Tw / 2.0, 80.0), 250.0) // DT)  # half-period, clamped
    ml = max(win, 25)
    lags, C = lagcorr(lz, rz, ml)
    # principal positive peak: max of C within +/- win snapshots of zero lag
    sel = np.abs(lags) <= win
    idx = np.where(sel)[0]
    ipk = idx[np.nanargmax(C[idx])]
    return Tw, float(C[ipk]), float(lags[ipk] * DT), C, lags, lz, rz, t


# ---------------- suite sweep ----------------
rows = []
cache = {}
for qb in QB:
    for eb in ECC:
        try:
            Tw, peak, lag, C, lags, lz, rz, t = peak_for_cell(eb, qb)
        except FileNotFoundError:
            continue
        rows.append(dict(eb=eb, qb=qb, T=Tw, peakC=peak, lag_taub=lag,
                         phase_deg=lag / Tw * 360.0))
        cache[(eb, qb)] = (C, lags, lz, rz, t, Tw, peak, lag)
df = pd.DataFrame(rows)
df.to_csv(os.path.join(CC, "appendix_peakC_lambda_r2.csv"), index=False)

clean = df[df.peakC >= 0.7]
print(f"N={len(df)}  clean(peakC>=0.7)={len(clean)}")
print(f"clean median peakC={clean.peakC.median():.2f}  median lag={clean.lag_taub.median():.0f} tau_b"
      f"  ({clean.phase_deg.median():.0f} deg)")

# ---------------- 1D examples ----------------
EXAMPLES = [(0.6, 1.0, "clean"), (0.5, 0.9, "clean"), (0.4, 0.7, "messy")]
fig, axes = plt.subplots(2, 3, figsize=(13.5, 6.2),
                         gridspec_kw=dict(height_ratios=[1.0, 1.0], hspace=0.42, wspace=0.28))
for j, (eb, qb, tag) in enumerate(EXAMPLES):
    C, lags, lz, rz, t, Tw, peak, lag = cache[(eb, qb)]
    # top: z-scored overlay over a representative 2000 tau_b window
    ax = axes[0, j]
    w = (t >= 3000) & (t <= 5000)
    ax.plot(t[w], lz[w], color="black", lw=1.1, label=r"$\lambda(t)$")
    ax.plot(t[w], rz[w], color="tab:red", lw=1.1, label=r"$r_2(t)$")
    ax.set_title(rf"$(e_b,q_b)=({eb},{qb})$  [{tag}]", fontsize=11)
    ax.set_xlabel(r"$t\ [\tau_b]$", fontsize=10)
    if j == 0:
        ax.set_ylabel("z-score", fontsize=10)
        ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax.tick_params(labelsize=8)
    # bottom: C(Dt) with positive-peak marked
    ax = axes[1, j]
    ax.axhline(0, color="gray", lw=0.6)
    ax.axvline(0, color="gray", lw=0.6)
    ax.plot(lags * DT, C, color="tab:blue", lw=1.6)
    ax.plot([lag], [peak], "o", color="crimson", ms=6, zorder=5)
    ax.annotate(rf"$C_{{\rm peak}}={peak:+.2f}$" + "\n" + rf"$\Delta t={lag:+.0f}\,\tau_b$",
                xy=(lag, peak), xytext=(0.04, 0.06), textcoords="axes fraction",
                fontsize=8.5, color="crimson",
                arrowprops=dict(arrowstyle="->", color="crimson", lw=0.8))
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel(r"lag $\Delta t\ [\tau_b]$", fontsize=10)
    if j == 0:
        ax.set_ylabel(r"$C_{\lambda r_2}(\Delta t)$", fontsize=10)
    ax.tick_params(labelsize=8)
fig.savefig(os.path.join(ROOT, "appendix_crosscorr_examples.pdf"), bbox_inches="tight")
plt.close(fig)

# ---------------- positive-peak heatmap (lambda vs r2) ----------------
def e_edges(v):
    e = np.zeros(len(v) + 1)
    e[0] = v[0] - (v[1] - v[0]) / 2
    e[-1] = v[-1] + (v[-1] - v[-2]) / 2
    for i in range(1, len(v)):
        e[i] = (v[i - 1] + v[i]) / 2
    return e


def q_edges(v):
    e = np.zeros(len(v) + 1)
    e[0] = v[0] - 0.05
    e[-1] = v[-1] + 0.05
    for i in range(1, len(v)):
        e[i] = (v[i - 1] + v[i]) / 2
    return e


ee, qe = e_edges(ECC), q_edges(QB)
grid = np.full((len(QB), len(ECC)), np.nan)
for _, r in df.iterrows():
    grid[QB.index(r.qb), ECC.index(r.eb)] = max(r.peakC, 0.0)  # positive only

fig, ax = plt.subplots(figsize=(7.2, 6.0))
pcm = ax.pcolormesh(ee, qe, grid, cmap="magma", vmin=0, vmax=1, shading="flat")
cb = plt.colorbar(pcm, ax=ax)
cb.set_label(r"peak cross-correlation $\max_{\Delta t} C_{\lambda r_2}(\Delta t)$", fontsize=11)
for i, qb in enumerate(QB):
    for jj, eb in enumerate(ECC):
        v = grid[i, jj]
        if not np.isfinite(v):
            continue
        ax.text(eb, qb, f"{v:.2f}", ha="center", va="center", fontsize=8,
                color="white" if v < 0.6 else "black")
        if v >= 0.7:  # outline clean cells
            ax.add_patch(Rectangle((ee[jj], qe[i]), ee[jj + 1] - ee[jj],
                                   qe[i + 1] - qe[i], fill=False, edgecolor="cyan", lw=1.6))
ax.set_xticks(ECC); ax.set_xticklabels([f"{e:.1f}" for e in ECC])
ax.set_yticks(QB); ax.set_yticklabels([f"{q:.1f}" for q in QB])
ax.set_xlim(ee[0], ee[-1]); ax.set_ylim(qe[0], qe[-1])
ax.set_xlabel(r"$e_b$", fontsize=12); ax.set_ylabel(r"$q_b$", fontsize=12)
fig.savefig(os.path.join(ROOT, "appendix_crosscorr_peakC.pdf"), bbox_inches="tight")
plt.close(fig)
print("wrote appendix_crosscorr_examples.pdf, appendix_crosscorr_peakC.pdf")
