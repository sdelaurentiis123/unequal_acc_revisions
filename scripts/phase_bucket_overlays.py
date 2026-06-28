#!/usr/bin/env python3 -u
"""
Phase-bucket overlays — version 2: STANDARDIZED phase anchor.

Picks representative clean cells (|C_peak(λ, r_2)| ≥ 0.7) for each
phase bucket using the STANDARDIZED trough-to-peak phase φ_r2 from
phase_anchor_summary.csv (the same definition the tau_peak_panel uses).

For each bucket, plots:
  - λ(t), r_2(t) overlay (z-scored)
  - C(λ, r_2)(τ) with τ_peak marked

Bucket centers in units of π: [-1, -0.75, -0.5, -0.25, 0, +0.25, +0.5, +0.75, +1]
(wrapping: -π ≡ +π)

Buckets that have no clean cells nearby are still attempted, with a
fall-back to the closest available cell.

Output:
  numerics_audit/phase_bucket_overlays.pdf
"""
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import zscore
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT = V3 / "numerics_audit"
SWEEP = V3 / "cross_corr" / "sweep_summary.csv"
PHASE = V3 / "cross_corr" / "phase_anchor_summary.csv"
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'
T_CUT = 3000.0
DT_TAU = 10.0
MAX_LAG = 20

BUCKETS = [-1.0, -0.75, -0.5, -0.25, 0.0, +0.25, +0.5, +0.75, +1.0]


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


def load_sim(eb, qb):
    with open(f'{DATA}/data_eb_{eb}_qb_{qb}', 'rb') as f:
        d = pickle.load(f)
    keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2']
    n = min(len(d[k]) for k in keys)
    arr = {k: np.asarray(d[k])[:n] for k in keys}
    keep = arr['time'] >= T_CUT
    m1 = arr['mdot1'][keep]; m2 = arr['mdot2'][keep]
    lam = m2 / np.where(m1 != 0, m1, np.nan)
    fin = np.isfinite(lam)
    lam[~fin] = np.nanmedian(lam[fin]) if fin.any() else 0.0
    return arr['time'][keep], lam, arr['rmin1'][keep], arr['rmin2'][keep]


def wrap_pm_pi_over_pi(phi_deg):
    """Wrap degrees to (-180, +180] then divide by 180 → (-1, +1] in units of π."""
    wrapped = ((phi_deg + 180) % 360) - 180
    return wrapped / 180.0


# Load and merge
sweep = pd.read_csv(SWEEP)
phase = pd.read_csv(PHASE)
# T_r2 sanity bound — fall back to T_lam if r_2 FFT was the whole-window artifact
T_BOUND = 1500
phase['T_use'] = np.where(
    phase.T_r2.between(1, T_BOUND, inclusive='both'),
    phase.T_r2,
    phase.T_lam,
)
sweep_lr2 = sweep[sweep.pair == 'lambda-rmin2'][['eb', 'qb', 'peak_C', 'peak_lag_tau_b']]
merged = sweep_lr2.merge(phase[['eb', 'qb', 'phi_r2', 'T_use']], on=['eb', 'qb'])
merged.rename(columns={'T_use': 'T_r2'}, inplace=True)
merged = merged[merged.phi_r2.notna() & merged.T_r2.notna()].copy()
merged['phi_over_pi_signed'] = wrap_pm_pi_over_pi(merged.phi_r2)
merged['abs_pc'] = merged.peak_C.abs()

print(f"Loaded {len(merged)} cells with valid phase + cross-corr data.")
print()


def pick_representative(target):
    candidates = merged[merged.abs_pc >= 0.7].copy()
    if len(candidates) == 0:
        candidates = merged.copy()
    # cyclic distance on the unit circle
    d_raw = candidates.phi_over_pi_signed - target
    d_wrap = np.minimum(np.abs(d_raw), 2 - np.abs(d_raw))
    candidates = candidates.assign(dist=d_wrap)
    return candidates.sort_values('dist').iloc[0]


chosen = []
seen = set()
for target in BUCKETS:
    pick = pick_representative(target)
    if (pick.eb, pick.qb) in seen:
        # try next closest unseen cell from clean set
        cands = merged[merged.abs_pc >= 0.7].copy()
        cands['dist'] = np.minimum(
            np.abs(cands.phi_over_pi_signed - target),
            2 - np.abs(cands.phi_over_pi_signed - target))
        cands = cands.sort_values('dist')
        for _, c in cands.iterrows():
            if (c.eb, c.qb) not in seen:
                pick = c
                break
    seen.add((pick.eb, pick.qb))
    chosen.append((target, pick))

print(f"{'bucket':>8s}  {'(eb,qb)':>10s}  {'φ_anchor/π':>11s}  "
      f"{'τ_peak':>8s}  {'C_peak':>7s}  {'T_r2':>6s}")
for target, p in chosen:
    print(f"{target:+8.2f}  ({p.eb:.1f},{p.qb:.1f})  "
          f"{p.phi_over_pi_signed:+11.2f}  {p.peak_lag_tau_b:+8.0f}  "
          f"{p.peak_C:+7.2f}  {p.T_r2:6.0f}")
print()


# Plot
nrows = len(BUCKETS)
fig, axes = plt.subplots(nrows, 2, figsize=(15, 2.6 * nrows),
                         gridspec_kw={'width_ratios': [2, 1]})

for row, (target, pick) in enumerate(chosen):
    eb, qb = pick.eb, pick.qb
    t, lam, r1, r2 = load_sim(eb, qb)
    lam_z = zscore(lam); r2_z = zscore(r2)

    show_T = min(3 * pick.T_r2, t[-1] - t[0])
    mask = t <= (t[0] + show_T)
    t_show = t[mask]

    # Lightly smooth for peak detection (matches phase_anchor_analysis.py)
    lam_s = gaussian_filter1d(lam, sigma=1.0)
    r2_s  = gaussian_filter1d(r2, sigma=1.0)
    lam_zs = zscore(lam_s)
    r2_zs  = zscore(r2_s)
    lam_peaks_idx, _  = find_peaks(lam_zs,  prominence=0.5, distance=5)
    r2_troughs_idx, _ = find_peaks(-r2_zs, prominence=0.5, distance=5)
    # Restrict to the show window
    lam_peaks_in = lam_peaks_idx[(t[lam_peaks_idx] >= t_show[0]) &
                                  (t[lam_peaks_idx] <= t_show[-1])]
    r2_troughs_in = r2_troughs_idx[(t[r2_troughs_idx] >= t_show[0]) &
                                    (t[r2_troughs_idx] <= t_show[-1])]

    ax = axes[row, 0]
    ax.plot(t_show, lam_z[mask], 'b-', lw=1.1, label=r'$\lambda(t)$ (z)')
    ax.plot(t_show, r2_z[mask], 'g-', lw=1.1, label=r'$r_2(t)$ (z)')
    # Mark detected events
    for p in lam_peaks_in:
        ax.axvline(t[p], color='blue', alpha=0.15, lw=0.4)
        ax.plot(t[p], lam_z[p], 'bv', markersize=7, zorder=5)
    for p in r2_troughs_in:
        ax.axvline(t[p], color='green', alpha=0.15, lw=0.4)
        ax.plot(t[p], r2_z[p], 'g^', markersize=7, zorder=5)
    ax.axhline(0, color='gray', lw=0.4)
    ax.set_xlabel(r'$t\ [\tau_b]$', fontsize=10)
    ax.set_ylabel('z-score', fontsize=10)
    title = (
        rf'bucket $\phi/\pi={target:+.2f}$:  '
        rf'$(e_b, q_b)=({eb}, {qb})$,  '
        rf'$\phi={pick.phi_over_pi_signed:+.2f}\pi$  (standardized),  '
        rf'$\tau_{{\rm peak}}={int(pick.peak_lag_tau_b):+d}\,\tau_b$,  '
        rf'$T={pick.T_r2:.0f}\,\tau_b$,  '
        rf'$C_{{\rm peak}}={pick.peak_C:+.2f}$'
    )
    ax.set_title(title, fontsize=9)
    if row == 0:
        ax.legend(loc='upper right', fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[row, 1]
    lags, c = lag_corr(lam_z, r2_z, MAX_LAG)
    ax.plot(lags * DT_TAU, c, 'k-', lw=1.5)
    ax.axhline(0, color='gray', lw=0.4)
    ax.axvline(0, color='gray', lw=0.4)
    ax.axvline(pick.peak_lag_tau_b, color='red', ls='--', alpha=0.7,
               label=rf'$\tau_{{\rm peak}}={int(pick.peak_lag_tau_b):+d}\,\tau_b$')
    ax.set_xlabel(r'lag $\tau\ [\tau_b]$', fontsize=10)
    ax.set_ylabel(r'$C(\lambda, r_2)$', fontsize=10)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlim(-MAX_LAG * DT_TAU, MAX_LAG * DT_TAU)
    if row == 0:
        ax.legend(loc='lower right', fontsize=9)
    ax.grid(alpha=0.3)

fig.suptitle(
    r'Phase-bucket overlays.  Bucket label = target $\phi/\pi$ (standardized anchor).'
    '\n'
    r'$\phi>0$: $r_2$ trough leads $\lambda$ peak (cavity-distance picture).  '
    r'$\phi<0$: $r_2$ trough follows $\lambda$ peak (eating-then-retreat).',
    fontsize=10.5, y=1.005)
plt.tight_layout()
out_path = OUT / "phase_bucket_overlays.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=140)
plt.close(fig)
print(f"Saved {out_path}")
