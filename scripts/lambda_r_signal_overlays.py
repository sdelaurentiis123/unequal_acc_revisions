#!/usr/bin/env python3 -u
"""
For three representative simulations — one clean (large |peak C|),
one zero-lag clean (C(0) large and negative), one messy (low |C|) —
plot the actual λ(t), r_1(t), r_2(t) time series side-by-side with
their measured C(τ). Lets us see physically what the sign and lag of
the cross-correlation really represent.

Output: numerics_audit/lambda_r_overlays.pdf
"""
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import zscore

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT = V3 / "numerics_audit"
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'
T_CUT = 3000.0
DT_TAU = 10.0
MAX_LAG = 100


def load_sim(eb, qb):
    with open(f'{DATA}/data_eb_{eb}_qb_{qb}', 'rb') as f:
        d = pickle.load(f)
    keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2']
    n = min(len(d[k]) for k in keys)
    arr = {k: np.asarray(d[k])[:n] for k in keys}
    t = arr['time']
    keep = t >= T_CUT
    t = t[keep]
    m1 = arr['mdot1'][keep]
    m2 = arr['mdot2'][keep]
    lam = m2 / np.where(m1 != 0, m1, np.nan)
    r1 = arr['rmin1'][keep]
    r2 = arr['rmin2'][keep]
    # Fill NaN with median
    for v in (lam,):
        m = np.isfinite(v)
        v[~m] = np.nanmedian(v[m]) if m.any() else 0.0
    return t, lam, r1, r2


def lag_corr(x, y, max_lag):
    n = len(x)
    lags = np.arange(-max_lag, max_lag + 1)
    out = np.zeros_like(lags, dtype=float)
    for i, k in enumerate(lags):
        if k < 0:
            a, b = x[-k:], y[:n + k]
        elif k > 0:
            a, b = x[:n - k], y[k:]
        else:
            a, b = x, y
        if a.std() > 0 and b.std() > 0:
            out[i] = np.corrcoef(a, b)[0, 1]
    return lags, out


# Three cases:
#   1. Clean cell with C_peak large & POSITIVE for both λ↔r_1 and λ↔r_2 — (0.6, 1.0)
#   2. Clean cell with C_peak large & NEGATIVE for λ↔r_2 — (0.6, 0.8) (peak_C = -0.94)
#   3. Zero-lag-strong clean cell — (0.1, 0.5) (peak_C = -0.76 @ τ=0)
#   4. Messy cell — (0.3, 0.6) (low |peak C|)
CASES = [
    (0.6, 1.0, "Clean, positive both: peak C ≈ +0.95 for both pairs"),
    (0.6, 0.8, "Clean, sign-split: λ↔r_1 +0.89 @ τ=−130, λ↔r_2 −0.94 @ τ=−140"),
    (0.1, 0.5, "Zero-lag locked: λ↔r_1 −0.76 at τ=0"),
    (0.3, 0.6, "Messy: low |C| — pure precession-phase confusion"),
]

fig, axes = plt.subplots(len(CASES), 3, figsize=(17, 4*len(CASES)),
                        gridspec_kw={'width_ratios': [1.5, 1.5, 1]})

for row, (eb, qb, title) in enumerate(CASES):
    t, lam, r1, r2 = load_sim(eb, qb)
    # Z-score for fair overlay
    lam_z = zscore(lam)
    r1_z = zscore(r1)
    r2_z = zscore(r2)

    # Get C(τ) for both pairs
    lags, c1 = lag_corr(lam_z, r1_z, MAX_LAG)
    _, c2 = lag_corr(lam_z, r2_z, MAX_LAG)
    i1 = np.argmax(np.abs(c1)); peak_c1, tau1, c0_1 = c1[i1], lags[i1] * DT_TAU, c1[len(c1)//2]
    i2 = np.argmax(np.abs(c2)); peak_c2, tau2, c0_2 = c2[i2], lags[i2] * DT_TAU, c2[len(c2)//2]

    # Find a stretch where we can see clear oscillations — first 1500 τ_b after cut
    show_n = min(150, len(t))   # 150 snapshots * 10 = 1500 τ_b
    t_show = t[:show_n]

    # Panel 1: λ(t) and r_1(t) overlay (z-scored)
    ax = axes[row, 0]
    ax.plot(t_show, lam_z[:show_n], 'b-', lw=1.0, label=r'$\lambda(t)$ (z)')
    ax.plot(t_show, r1_z[:show_n], 'r-', lw=1.0, label=r'$r_1(t)$ (z)')
    if row == 0:
        ax.legend(fontsize=9, loc='upper right')
    ax.axhline(0, color='gray', lw=0.4)
    ax.set_xlabel(r'$t\ [\tau_b]$', fontsize=10)
    ax.set_ylabel('z-scored signal', fontsize=10)
    ax.set_title(rf'($e_b,q_b$)=({eb},{qb}) — $\lambda$ & $r_1$ overlay '
                 rf'(peak C={peak_c1:+.2f}, $\tau_{{\rm peak}}$={tau1:+.0f}, C(0)={c0_1:+.2f})',
                 fontsize=10)
    ax.grid(alpha=0.3)

    # Panel 2: λ(t) and r_2(t) overlay (z-scored)
    ax = axes[row, 1]
    ax.plot(t_show, lam_z[:show_n], 'b-', lw=1.0, label=r'$\lambda(t)$ (z)')
    ax.plot(t_show, r2_z[:show_n], color='green', lw=1.0, label=r'$r_2(t)$ (z)')
    if row == 0:
        ax.legend(fontsize=9, loc='upper right')
    ax.axhline(0, color='gray', lw=0.4)
    ax.set_xlabel(r'$t\ [\tau_b]$', fontsize=10)
    ax.set_title(rf'$\lambda$ & $r_2$ overlay '
                 rf'(peak C={peak_c2:+.2f}, $\tau_{{\rm peak}}$={tau2:+.0f}, C(0)={c0_2:+.2f})',
                 fontsize=10)
    ax.grid(alpha=0.3)

    # Panel 3: C(τ) for both pairs
    ax = axes[row, 2]
    ax.plot(lags * DT_TAU, c1, 'r-', lw=1.5, label=r'$C(\lambda, r_1)$')
    ax.plot(lags * DT_TAU, c2, color='green', lw=1.5, label=r'$C(\lambda, r_2)$')
    ax.axhline(0, color='gray', lw=0.4)
    ax.axvline(0, color='gray', lw=0.4)
    ax.axvline(tau1, color='red', lw=0.6, ls=':', alpha=0.6)
    ax.axvline(tau2, color='green', lw=0.6, ls=':', alpha=0.6)
    if row == 0:
        ax.legend(fontsize=9, loc='upper right')
    ax.set_xlabel(r'lag $\tau\ [\tau_b]$', fontsize=10)
    ax.set_ylabel(r'$C(\tau)$', fontsize=10)
    ax.set_title(title, fontsize=10)
    ax.set_ylim(-1.05, 1.05)
    ax.grid(alpha=0.3)

plt.tight_layout()
out_path = OUT / "lambda_r_overlays.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out_path}")
