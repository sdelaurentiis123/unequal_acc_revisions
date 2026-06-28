#!/usr/bin/env python3 -u
"""
Phase-consistency check: are r_1 and r_2 actually anti-phase?

If yes (anti-phase as expected from BHs on opposite sides of the binary):
  C(r_1, r_2)(τ=0) should be near −1
  τ_peak(λ, r_1) and τ_peak(λ, r_2) should differ by T_prec/2

If no (same-phase or complex):
  C(r_1, r_2) at τ=0 is positive
  τ_peak(λ, r_1) ≈ τ_peak(λ, r_2): r_1 and r_2 track the same cavity feature

Procedure:
  1. For every (e_b, q_b), compute τ_peak and peak_C for (λ,r_1), (λ,r_2),
     and (r_1,r_2) using the ±200 τ_b search.
  2. Categorize each cell by the relationship.
  3. Plot per-pair τ_peak scatter and a flag map of "both negative" cells.

Output:
  cross_corr/r1_r2_phase_summary.csv
  numerics_audit/r1_r2_phase_check.pdf
"""
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import zscore
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT_FIG = V3 / "numerics_audit"
OUT_CSV = V3 / "cross_corr"
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'
T_CUT = 3000.0
DT_TAU = 10.0
MAX_LAG = 20    # ±200 τ_b

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


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


def peak(lags, c):
    i = int(np.nanargmax(np.abs(c)))
    return float(c[i]), float(lags[i]) * DT_TAU, float(c[len(c)//2])


def load_sim(eb, qb):
    with open(f'{DATA}/data_eb_{eb}_qb_{qb}', 'rb') as f:
        d = pickle.load(f)
    keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2']
    n = min(len(d[k]) for k in keys)
    arr = {k: np.asarray(d[k])[:n] for k in keys}
    t = arr['time']
    keep = t >= T_CUT
    m1 = arr['mdot1'][keep]
    m2 = arr['mdot2'][keep]
    lam = m2 / np.where(m1 != 0, m1, np.nan)
    fin = np.isfinite(lam)
    lam[~fin] = np.nanmedian(lam[fin])
    return lam, arr['rmin1'][keep], arr['rmin2'][keep]


rows = []
for qb in QB:
    for eb in ECC:
        try:
            lam, r1, r2 = load_sim(eb, qb)
        except FileNotFoundError:
            continue
        lam_z = zscore(lam); r1_z = zscore(r1); r2_z = zscore(r2)
        lags, c_lr1 = lag_corr(lam_z, r1_z, MAX_LAG)
        _,    c_lr2 = lag_corr(lam_z, r2_z, MAX_LAG)
        _,    c_r12 = lag_corr(r1_z, r2_z, MAX_LAG)
        pc_lr1, tau_lr1, c0_lr1 = peak(lags, c_lr1)
        pc_lr2, tau_lr2, c0_lr2 = peak(lags, c_lr2)
        pc_r12, tau_r12, c0_r12 = peak(lags, c_r12)
        rows.append(dict(
            eb=eb, qb=qb,
            tau_lr1=tau_lr1, pc_lr1=pc_lr1, c0_lr1=c0_lr1,
            tau_lr2=tau_lr2, pc_lr2=pc_lr2, c0_lr2=c0_lr2,
            tau_r12=tau_r12, pc_r12=pc_r12, c0_r12=c0_r12,
        ))

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV / "r1_r2_phase_summary.csv", index=False)

# --- summarize ---
clean = (df.pc_lr1.abs() >= 0.7) & (df.pc_lr2.abs() >= 0.7)
print(f"Total cells: {len(df)}; both r_1 and r_2 clean (|C| >= 0.7 for both): "
      f"{int(clean.sum())}")
print()

print("=" * 70)
print("Are r_1 and r_2 actually anti-phase?")
print("=" * 70)
print(f"  C(r_1, r_2) at zero lag — distribution:")
print(f"    median signed C(0): {df.c0_r12.median():+.2f}")
print(f"    cells with C(0) < -0.5: {(df.c0_r12 < -0.5).sum()}/{len(df)}   "
      f"(strong anti-phase)")
print(f"    cells with C(0) > +0.5: {(df.c0_r12 > +0.5).sum()}/{len(df)}   "
      f"(strong in-phase)")
print(f"    cells with |C(0)| < 0.3: {(df.c0_r12.abs() < 0.3).sum()}/{len(df)} "
      f"(weakly related)")
print()

print("=" * 70)
print("In cells where BOTH (λ, r_i) are clean, do their τ_peaks agree or differ?")
print("=" * 70)
sub = df[clean].copy()
sub['tau_diff'] = sub.tau_lr1 - sub.tau_lr2
sub['sign_lr1'] = np.sign(sub.tau_lr1).astype(int)
sub['sign_lr2'] = np.sign(sub.tau_lr2).astype(int)
print(sub[['eb', 'qb', 'tau_lr1', 'pc_lr1', 'tau_lr2', 'pc_lr2',
           'tau_r12', 'c0_r12', 'tau_diff']].to_string(index=False, float_format='%.0f'))
print()

# How many clean-both cells have BOTH τ_peaks negative?
both_neg = (sub.tau_lr1 < 0) & (sub.tau_lr2 < 0)
both_pos = (sub.tau_lr1 > 0) & (sub.tau_lr2 > 0)
opposite = (sub.tau_lr1 * sub.tau_lr2 < 0)
print(f"  both τ_peak negative (r_1 AND r_2 lead λ):  {int(both_neg.sum())}")
print(f"  both τ_peak positive (λ leads both r_1 AND r_2): {int(both_pos.sum())}")
print(f"  opposite-sign τ_peaks (mirror-image, anti-phase): "
      f"{int(opposite.sum())}")
print()

# --- visualize ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Panel 1: τ_peak(λ, r_1) vs τ_peak(λ, r_2) scatter; color by |C(r_1,r_2)|
ax = axes[0]
clean_all = df[clean]
sc = ax.scatter(clean_all.tau_lr1, clean_all.tau_lr2,
                c=clean_all.c0_r12, cmap='RdBu_r', vmin=-1, vmax=1,
                s=80, edgecolor='black', linewidth=0.5)
plt.colorbar(sc, ax=ax, label=r'$C(r_1, r_2)$ at $\tau=0$')
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
ax.plot([-200, 200], [-200, 200], 'k--', alpha=0.3, label='same lag')
ax.plot([-200, 200], [200, -200], 'k:', alpha=0.3, label='opposite lag (mirror)')
ax.set_xlim(-220, 220); ax.set_ylim(-220, 220)
ax.set_xlabel(r'$\tau_{\rm peak}(\lambda, r_1)\ [\tau_b]$', fontsize=11)
ax.set_ylabel(r'$\tau_{\rm peak}(\lambda, r_2)\ [\tau_b]$', fontsize=11)
ax.set_title(r'Clean cells: $\tau_{\rm peak}(\lambda, r_1)$ vs $\tau_{\rm peak}(\lambda, r_2)$',
             fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# Panel 2: heatmap of "category" — which sign combo
ax = axes[1]
cat = np.full((len(QB), len(ECC)), np.nan)
# 0 = not clean, 1 = both neg, 2 = both pos, 3 = opposite (mirror)
for i, qb in enumerate(QB):
    for j, eb in enumerate(ECC):
        r = df[(df.eb == eb) & (df.qb == qb)]
        if r.empty:
            continue
        r = r.iloc[0]
        if abs(r.pc_lr1) < 0.7 or abs(r.pc_lr2) < 0.7:
            cat[i, j] = 0
        elif r.tau_lr1 < 0 and r.tau_lr2 < 0:
            cat[i, j] = 1
        elif r.tau_lr1 > 0 and r.tau_lr2 > 0:
            cat[i, j] = 2
        elif r.tau_lr1 * r.tau_lr2 < 0:
            cat[i, j] = 3

def e_edges(values):
    edges = np.zeros(len(values) + 1)
    edges[0] = values[0] - (values[1] - values[0]) / 2
    edges[-1] = values[-1] + (values[-1] - values[-2]) / 2
    for i in range(1, len(values)):
        edges[i] = (values[i-1] + values[i]) / 2
    return edges

def q_edges(values):
    edges = np.zeros(len(values) + 1)
    edges[0] = values[0] - 0.05
    edges[-1] = values[-1] + 0.05
    for i in range(1, len(values)):
        edges[i] = (values[i-1] + values[i]) / 2
    return edges

e_e = e_edges(ECC); q_e = q_edges(QB)
from matplotlib.colors import ListedColormap
cmap_cat = ListedColormap(['lightgray', 'salmon', 'lightblue', 'lightgreen'])
ax.pcolormesh(e_e, q_e, cat, cmap=cmap_cat, vmin=-0.5, vmax=3.5, shading='flat')
# Annotate each clean cell with C(r_1, r_2) at zero lag
for i, qb in enumerate(QB):
    for j, eb in enumerate(ECC):
        r = df[(df.eb == eb) & (df.qb == qb)]
        if r.empty or np.isnan(cat[i, j]) or cat[i, j] == 0:
            continue
        ax.text(eb, qb, f"C(r₁,r₂)\n={r.iloc[0].c0_r12:+.2f}",
                ha='center', va='center', fontsize=6.5, weight='bold',
                color='black')
ax.set_xticks(ECC); ax.set_xticklabels([f'{e:.1f}' for e in ECC], fontsize=10)
ax.set_yticks(QB); ax.set_yticklabels([f'{q:.1f}' for q in QB], fontsize=10)
ax.set_xlim(e_e[0], e_e[-1]); ax.set_ylim(q_e[0], q_e[-1])
ax.set_xlabel(r'$e_b$', fontsize=11)
ax.set_ylabel(r'$q_b$', fontsize=11)
# Legend
from matplotlib.patches import Patch
legend = [
    Patch(facecolor='lightgray', label='not clean'),
    Patch(facecolor='salmon', label=r'both $\tau<0$ (both $r_i$ lead $\lambda$)'),
    Patch(facecolor='lightblue', label=r'both $\tau>0$ ($\lambda$ leads both)'),
    Patch(facecolor='lightgreen', label='opposite sign (mirror — anti-phase!)'),
]
ax.legend(handles=legend, loc='lower left', fontsize=8, framealpha=0.9)
ax.set_title(r'Per-cell category of $(\tau_{\lambda r_1}, \tau_{\lambda r_2})$ signs',
             fontsize=10)

# Panel 3: histogram of C(r_1, r_2) at zero lag
ax = axes[2]
ax.hist(df.c0_r12, bins=20, color='gray', edgecolor='black', alpha=0.7,
        label=f'all {len(df)} cells')
ax.hist(df[clean].c0_r12, bins=20, color='orange', alpha=0.6,
        edgecolor='black',
        label=f'clean (both $r_i$): {clean.sum()} cells')
ax.axvline(-1, color='blue', ls='--', alpha=0.6,
           label='perfect anti-phase')
ax.axvline(0, color='gray', lw=0.5)
ax.axvline(+1, color='red', ls='--', alpha=0.6, label='perfect in-phase')
ax.set_xlabel(r'$C(r_1, r_2)$ at $\tau = 0$', fontsize=11)
ax.set_ylabel('count')
ax.set_title(r'Are $r_1$ and $r_2$ anti-phase? (would expect $C(0) \approx -1$)',
             fontsize=10)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

fig.suptitle(r'$r_1$–$r_2$ phase relationship check across the suite', fontsize=12,
             y=1.02)
plt.tight_layout()
out = OUT_FIG / "r1_r2_phase_check.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out}")
